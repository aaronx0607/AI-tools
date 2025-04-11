#!/usr/bin/env python3

import os
import sys
import time
import argparse
import requests
import json
from tqdm import tqdm
import concurrent.futures
import logging
import yaml

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('translation.log')
    ]
)

logger = logging.getLogger(__name__)

# 直接设置 OpenRouter API 密钥
# 已设置为您提供的API密钥
OPENROUTER_API_KEY = "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"

# OpenRouter API 端点
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"

def setup_args():
    """设置命令行参数和环境变量"""
    parser = argparse.ArgumentParser(description='将英文内容翻译成其他语言')
    
    # 命令行参数,支持环境变量回退
    parser.add_argument('--source', type=str, 
                        default=os.environ.get('SOURCE', 'src/content/blog/en'), 
                        help='包含英文文件的源目录')
    
    parser.add_argument('--target-prefix', type=str, 
                        default=os.environ.get('TARGET_PREFIX', 'src/content/blog'), 
                        help='翻译文件的目标目录前缀')
    
    # 从环境变量解析语言
    default_languages = ['fr', 'es', 'zh']
    env_languages = os.environ.get('LANGUAGES')
    if env_languages:
        default_languages = env_languages.split()
    
    parser.add_argument('--languages', type=str, nargs='+', 
                        default=default_languages, 
                        help='目标语言(目录名)')
    
    parser.add_argument('--model', type=str, 
                        default=os.environ.get('MODEL', 'openai/gpt-4o-mini'), 
                        help='使用的OpenRouter模型')
    
    parser.add_argument('--max-files', type=int, 
                        default=None, 
                        help='要翻译的最大文件数(用于测试)')
    
    parser.add_argument('--threads', type=int, 
                        default=3, 
                        help='并发翻译线程数')
    
    parser.add_argument('--force', action='store_true', 
                        default=False, 
                        help='即使目标文件存在也强制翻译')
    
    parser.add_argument('--chunk-size', type=int, 
                        default=4000, 
                        help='长文档的每个块的最大令牌数')
    
    return parser.parse_args()

def get_files_to_translate(source_dir, target_dirs, force=False, max_files=None):
    """获取要翻译的文件列表及其目标路径"""
    translation_tasks = []
    
    # 获取源目录中的所有markdown文件
    source_files = [f for f in os.listdir(source_dir) if f.endswith('.md')]
    
    if max_files:
        source_files = source_files[:max_files]
    
    for source_file in source_files:
        source_path = os.path.join(source_dir, source_file)
        
        # 对每个目标语言
        for target_dir in target_dirs:
            target_path = os.path.join(target_dir, source_file)
            
            # 如果目标文件存在且不强制翻译则跳过
            if os.path.exists(target_path) and not force:
                logger.info(f"跳过 {target_path} (已存在)")
                continue
                
            translation_tasks.append((source_path, target_path, target_dir.split('/')[-1]))
    
    return translation_tasks

def split_content_into_chunks(content, chunk_size=4000):
    """将内容分割成块进行翻译
    
    此函数将内容分成块,确保:
    1. Front matter(在---标记之间)保持在一起
    2. Markdown标题不被分割
    3. 代码块不被分割
    4. 块大约为chunk_size个令牌
    
    返回块列表。
    """
    # 首先分离front matter
    front_matter = ""
    main_content = content
    
    if content.startswith('---'):
        # 查找front matter的结尾
        second_marker = content.find('---', 3)
        if second_marker != -1:
            front_matter = content[:second_marker + 3] + "\n"
            main_content = content[second_marker + 4:]
    
    # 按行分割主要内容
    lines = main_content.split('\n')
    
    chunks = []
    current_chunk = front_matter if front_matter else ""
    current_chunk_size = len(current_chunk.split())
    in_code_block = False
    code_block_content = ""
    
    for line in lines:
        # 检查是否进入或离开代码块
        if line.strip().startswith('```'):
            in_code_block = not in_code_block
            
            if in_code_block:
                # 开始代码块
                code_block_content = line + "\n"
            else:
                # 结束代码块,将整个块添加到当前块
                code_block_content += line + "\n"
                line_size = len(code_block_content.split())
                
                # 如果添加此代码块会超过块大小且当前块不为空,
                # 开始新块
                if current_chunk_size + line_size > chunk_size and current_chunk:
                    chunks.append(current_chunk)
                    current_chunk = code_block_content
                    current_chunk_size = line_size
                else:
                    current_chunk += code_block_content
                    current_chunk_size += line_size
                
                code_block_content = ""
            continue
        
        if in_code_block:
            # 如果在代码块中,只累积该行
            code_block_content += line + "\n"
            continue
        
        # 检查是否为标题
        is_heading = line.strip().startswith('#')
        
        # 估计此行的令牌大小(粗略近似)
        line_size = len(line.split())
        
        # 如果添加此行会超过块大小且不是标题或当前块为空,
        # 开始新块
        if current_chunk_size + line_size > chunk_size and current_chunk and not is_heading:
            chunks.append(current_chunk)
            current_chunk = line + "\n"
            current_chunk_size = line_size
        else:
            current_chunk += line + "\n"
            current_chunk_size += line_size
    
    # 如果最后一块不为空则添加
    if current_chunk:
        chunks.append(current_chunk)
    
    return chunks

def translate_chunk(chunk, language, model):
    """翻译单个内容块"""
    try:
        # 确定语言名称
        language_names = {
            'fr': 'French',
            'es': 'Spanish',
            'zh': 'Chinese'
        }
        
        language_name = language_names.get(language, language)
        
        # 创建保留markdown格式和front matter的系统消息
        system_message = f"""你是一位专业翻译。将以下markdown内容从英语翻译成{language_name}。
        重要规则:
        1. 保留所有markdown格式,包括标题、列表、代码块和链接
        2. 保留所有front matter(顶部---标记之间的内容)
        3. 不要翻译代码块内的代码(```标记之间的内容)
        4. 不要翻译URL或HTML标签
        5. 保持相同的段落结构
        6. 自然流畅地翻译成{language_name}
        7. 保持专业术语的准确性
        8. 保留原文中的变量名和函数名
        """
        
        # 准备请求数据
        payload = {
            "model": model,
            "messages": [
                {"role": "system", "content": system_message},
                {"role": "user", "content": chunk}
            ],
            "temperature": 0.1,  # 降低温度以获得更一致的翻译
        }
        
        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://bestfreeai.net",  # 替换为您的网站
            "X-Title": "BestFreeAI"  # 您的应用名称
        }
        
        # 发送请求到OpenRouter API
        response = requests.post(
            OPENROUTER_API_URL,
            headers=headers,
            json=payload
        )
        
        # 检查响应状态
        response.raise_for_status()
        
        # 解析响应
        response_data = response.json()
        
        # 提取翻译后的内容
        translated_chunk = response_data["choices"][0]["message"]["content"]
        
        return translated_chunk
    
    except Exception as e:
        logger.error(f"翻译块时出错: {str(e)}")
        if response and hasattr(response, 'text'):
            logger.error(f"API响应: {response.text}")
        raise

def translate_file(source_path, target_path, language, model, chunk_size=4000):
    """使用OpenRouter API翻译文件,通过分块处理长内容"""
    try:
        # 读取源文件
        with open(source_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 如果目标目录不存在则创建
        os.makedirs(os.path.dirname(target_path), exist_ok=True)
        
        # 检查内容是否足够短以进行单次API调用
        # 粗略估计:英文文本1个令牌~= 4个字符
        estimated_tokens = len(content) / 4
        
        if estimated_tokens <= chunk_size:
            # 内容足够短,一次性翻译
            translated_content = translate_chunk(content, language, model)
        else:
            # 内容太长,分块翻译
            logger.info(f"文件 {os.path.basename(source_path)} 较大 ({estimated_tokens:.0f} 估计令牌),正在分块")
            
            chunks = split_content_into_chunks(content, chunk_size)
            logger.info(f"分成了 {len(chunks)} 块")
            
            # 翻译每个块
            translated_chunks = []
            for i, chunk in enumerate(chunks):
                logger.info(f"正在翻译 {os.path.basename(source_path)} 的第 {i+1}/{len(chunks)} 块")
                translated_chunk = translate_chunk(chunk, language, model)
                translated_chunks.append(translated_chunk)
                
                # 小延迟以避免速率限制
                time.sleep(0.5)
            
            # 合并翻译后的块
            translated_content = ''.join(translated_chunks)
        
        # 将翻译后的内容写入目标文件
        with open(target_path, 'w', encoding='utf-8') as f:
            f.write(translated_content)
        
        return True, f"成功将 {os.path.basename(source_path)} 翻译成 {language}"
    
    except Exception as e:
        logger.error(f"将 {source_path} 翻译成 {language} 时出错: {str(e)}")
        return False, str(e)

def translate_files_with_progress(translation_tasks, model, num_threads, chunk_size):
    """使用线程池翻译文件并显示进度条"""
    results = {"success": 0, "failed": 0}
    
    with tqdm(total=len(translation_tasks), desc="正在翻译文件") as pbar:
        with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
            # 创建字典以跟踪futures
            future_to_task = {}
            
            # 提交所有任务
            for source_path, target_path, language in translation_tasks:
                future = executor.submit(
                    translate_file, source_path, target_path, language, model, chunk_size
                )
                future_to_task[future] = (source_path, target_path, language)
            
            # 处理完成的futures
            for future in concurrent.futures.as_completed(future_to_task):
                source_path, target_path, language = future_to_task[future]
                try:
                    success, message = future.result()
                    if success:
                        results["success"] += 1
                        logger.info(message)
                    else:
                        results["failed"] += 1
                        logger.error(f"无法将 {source_path} 翻译成 {language}: {message}")
                except Exception as e:
                    results["failed"] += 1
                    logger.error(f"翻译 {source_path} 到 {language} 时发生异常: {str(e)}")
                
                # 更新进度条
                pbar.update(1)
                pbar.set_postfix({
                    "成功": results["success"],
                    "失败": results["failed"]
                })
                
                # 小延迟以避免速率限制
                time.sleep(0.1)
    
    return results

def main():
    # 解析命令行参数
    args = setup_args()
    
    # 规范化路径
    source_dir = os.path.normpath(args.source)
    target_dirs = [os.path.join(args.target_prefix, lang) for lang in args.languages]
    
    # 获取要翻译的文件
    logger.info(f"正在扫描源目录: {source_dir}")
    translation_tasks = get_files_to_translate(
        source_dir, target_dirs, force=args.force, max_files=args.max_files
    )
    
    if not translation_tasks:
        logger.info("没有要翻译的文件。所有目标文件可能已存在。")
        logger.info("使用--force或设置FORCE=true以强制翻译已存在的文件。")
        return
    
    logger.info(f"找到 {len(translation_tasks)} 个要翻译的文件")
    logger.info(f"对长文档使用 {args.chunk_size} 个令牌的块大小")
    logger.info(f"使用模型: {args.model}")
    
    # 翻译文件
    results = translate_files_with_progress(
        translation_tasks, args.model, args.threads, args.chunk_size
    )
    
    # 打印摘要
    logger.info("\n翻译完成!")
    logger.info(f"成功翻译: {results['success']} 个文件")
    logger.info(f"翻译失败: {results['failed']} 个文件")
    
    if results['failed'] > 0:
        logger.info("查看日志文件以了解失败翻译的详细信息。")

if __name__ == "__main__":
    main() 