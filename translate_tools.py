#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI工具Markdown文件多语言翻译脚本

该脚本将src/content/tools/en目录下的Markdown文件翻译成多种语言，
并将翻译后的文件保存到对应的语言目录中。
"""

import os
import yaml
import re
import json
import requests
from pathlib import Path
import time
import argparse
import concurrent.futures

# OpenRouter API配置
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"

# 支持的语言配置
LANGUAGES = {
    "es": "西班牙语",
    "fr": "法语",
    "zh": "简体中文"
}

# 默认设置
DEFAULT_SOURCE_DIR = "src/content/tools/en"
DEFAULT_MODEL = "openai/gpt-4o-mini"  # 也可以使用 "openai/gpt-3.5-turbo" 等

def ensure_directory_exists(directory):
    """确保目录存在，如不存在则创建"""
    os.makedirs(directory, exist_ok=True)

def read_markdown_file(file_path):
    """读取Markdown文件，分离前置元数据和内容"""
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # 使用正则表达式分离前置元数据和Markdown内容
    pattern = r'^---\n(.*?)\n---\n(.*)'
    match = re.match(pattern, content, re.DOTALL)
    
    if match:
        frontmatter_str = match.group(1)
        markdown_content = match.group(2)
        
        # 解析YAML前置元数据
        frontmatter = yaml.safe_load(frontmatter_str)
        
        return frontmatter, markdown_content
    
    return None, content

def translate_text(text, target_language, api_key, model):
    """使用OpenRouter API翻译文本"""
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": model,
        "messages": [
            {
                "role": "system",
                "content": f"你是一位专业的AI和技术词汇翻译专家。请将用户提供的文本翻译成{target_language}，保持原文的格式、标点符号和技术术语的准确性。请勿改变Markdown格式符号。对于代码块、链接等特殊内容要保持其格式不变。技术术语应使用该语言中通用的表达方式。遇到产品名称，不应该翻译。"
            },
            {
                "role": "user",
                "content": text
            }
        ]
    }
    
    try:
        response = requests.post(OPENROUTER_API_URL, headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()
        translated_text = result["choices"][0]["message"]["content"]
        return translated_text
    except Exception as e:
        print(f"翻译时出错: {e}")
        if 'response' in locals() and hasattr(response, 'text'):
            print(f"API响应: {response.text}")
        return None

def translate_frontmatter(frontmatter, target_language_code, api_key, model):
    """翻译前置元数据中的特定字段"""
    target_language = LANGUAGES[target_language_code]
    
    # 需要翻译的字段
    fields_to_translate = ['name', 'description']
    
    translated_frontmatter = frontmatter.copy()
    
    for field in fields_to_translate:
        if field in frontmatter:
            translated_text = translate_text(frontmatter[field], target_language, api_key, model)
            if translated_text:
                translated_frontmatter[field] = translated_text.strip()
    
    # 翻译标签
    if 'tags' in frontmatter and isinstance(frontmatter['tags'], list):
        translated_tags = []
        tags_text = ", ".join(frontmatter['tags'])
        translated_tags_text = translate_text(tags_text, target_language, api_key, model)
        
        if translated_tags_text:
            translated_tags = [tag.strip() for tag in translated_tags_text.split(",")]
            translated_frontmatter['tags'] = translated_tags
    
    # 翻译价格信息中的文字部分
    if 'pricing' in frontmatter and isinstance(frontmatter['pricing'], dict):
        translated_pricing = {}
        for key, value in frontmatter['pricing'].items():
            if isinstance(value, str) and not value.startswith('$') and not value.isdigit():
                translated_value = translate_text(value, target_language, api_key, model)
                if translated_value:
                    translated_pricing[key] = translated_value.strip()
                else:
                    translated_pricing[key] = value
            else:
                translated_pricing[key] = value
        
        translated_frontmatter['pricing'] = translated_pricing
    
    # 翻译功能列表
    if 'features' in frontmatter and isinstance(frontmatter['features'], list):
        translated_features = []
        for feature in frontmatter['features']:
            translated_feature = translate_text(feature, target_language, api_key, model)
            if translated_feature:
                translated_features.append(translated_feature.strip())
            else:
                translated_features.append(feature)
        
        translated_frontmatter['features'] = translated_features
    
    return translated_frontmatter

def translate_and_save_file(source_file, target_language_code, api_key, model, force_retranslate=False, verbose=False):
    """翻译文件并保存到目标目录"""
    if verbose:
        print(f"开始处理文件: {source_file} 到 {target_language_code}")
    
    target_language = LANGUAGES[target_language_code]
    target_dir = source_file.replace("/en/", f"/{target_language_code}/")
    target_dir_path = os.path.dirname(target_dir)
    
    # 检查目标文件是否已存在
    if os.path.exists(target_dir) and not force_retranslate:
        print(f"跳过已存在的文件: {target_dir}")
        return True, "skipped"
    
    # 确保目标目录存在
    ensure_directory_exists(target_dir_path)
    
    # 读取源文件
    frontmatter, markdown_content = read_markdown_file(source_file)
    
    if frontmatter is None:
        print(f"无法解析文件: {source_file}")
        return False, "parse_error"
    
    # 翻译前置元数据
    if verbose:
        print(f"翻译前置元数据...")
    translated_frontmatter = translate_frontmatter(frontmatter, target_language_code, api_key, model)
    
    # 翻译Markdown内容
    if verbose:
        print(f"翻译Markdown内容...")
    translated_content = translate_text(markdown_content, target_language, api_key, model)
    
    if not translated_content:
        print(f"翻译内容失败: {source_file}")
        return False, "translation_error"
    
    # 将翻译后的内容写入目标文件
    with open(target_dir, 'w', encoding='utf-8') as file:
        file.write("---\n")
        file.write(yaml.dump(translated_frontmatter, allow_unicode=True))
        file.write("---\n")
        file.write(translated_content)
    
    print(f"已完成文件翻译: {target_dir}")
    return True, "translated"

def translate_files_parallel(source_files, languages, api_key, model, force_retranslate=False, max_workers=3, verbose=False):
    """并行翻译多个文件到多种语言"""
    tasks = []
    
    for source_file in source_files:
        for lang_code in languages:
            tasks.append((source_file, lang_code))
    
    success_count = 0
    failure_count = 0
    skipped_count = 0
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_task = {
            executor.submit(translate_and_save_file, src, lang, api_key, model, force_retranslate, verbose): (src, lang)
            for src, lang in tasks
        }
        
        for future in concurrent.futures.as_completed(future_to_task):
            src, lang = future_to_task[future]
            try:
                success, status = future.result()
                if success:
                    if status == "skipped":
                        skipped_count += 1
                    else:
                        success_count += 1
                else:
                    failure_count += 1
            except Exception as e:
                print(f"翻译文件 {src} 到 {lang} 时出错: {e}")
                failure_count += 1
            
            # 添加延迟以避免API速率限制
            time.sleep(1)
    
    return success_count, failure_count, skipped_count

def translate_single_file(file_path, languages, api_key, model, force_retranslate=False, verbose=False):
    """翻译单个文件到多种语言"""
    success_count = 0
    failure_count = 0
    skipped_count = 0
    
    for lang_code in languages:
        if verbose:
            print(f"翻译 {file_path} 到 {LANGUAGES[lang_code]}...")
        
        success, status = translate_and_save_file(file_path, lang_code, api_key, model, force_retranslate, verbose)
        if success:
            if status == "skipped":
                skipped_count += 1
            else:
                success_count += 1
        else:
            failure_count += 1
        
        # 添加延迟以避免API速率限制
        time.sleep(2)
    
    return success_count, failure_count, skipped_count

def parse_arguments():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(description='将AI工具的Markdown文件从英文翻译到多种语言')
    
    parser.add_argument('--api-key', required=True, help='OpenRouter API密钥')
    parser.add_argument('--source-dir', default=DEFAULT_SOURCE_DIR, help=f'源目录 (默认: {DEFAULT_SOURCE_DIR})')
    parser.add_argument('--model', default=DEFAULT_MODEL, help=f'翻译使用的语言模型 (默认: {DEFAULT_MODEL})')
    parser.add_argument('--languages', default='es,fr,zh', help='目标语言代码，用逗号分隔 (默认: es,fr,zh)')
    parser.add_argument('--file', help='要翻译的单个文件路径 (可选，如不指定则翻译整个目录)')
    parser.add_argument('--max-workers', type=int, default=3, help='并行翻译的最大工作线程数 (默认: 3)')
    parser.add_argument('--verbose', action='store_true', help='显示详细输出')
    parser.add_argument('--force', action='store_true', help='强制重新翻译已存在的文件')
    
    return parser.parse_args()

def main():
    """主函数"""
    args = parse_arguments()
    
    api_key = args.api_key
    source_dir = args.source_dir
    model = args.model
    languages = [lang.strip() for lang in args.languages.split(',')]
    verbose = args.verbose
    force_retranslate = args.force
    
    # 验证语言代码
    for lang in languages:
        if lang not in LANGUAGES:
            print(f"错误: 不支持的语言代码 '{lang}'。支持的语言代码: {', '.join(LANGUAGES.keys())}")
            return
    
    # 翻译单个文件或整个目录
    if args.file:
        if not os.path.isfile(args.file):
            print(f"错误: 文件不存在 '{args.file}'")
            return
        
        print(f"开始翻译文件 {args.file} 到 {', '.join(languages)}...")
        success_count, failure_count, skipped_count = translate_single_file(
            args.file, languages, api_key, model, force_retranslate, verbose
        )
    else:
        # 获取源目录下的所有Markdown文件
        if not os.path.isdir(source_dir):
            print(f"错误: 目录不存在 '{source_dir}'")
            return
        
        source_files = []
        for root, _, files in os.walk(source_dir):
            for file in files:
                if file.endswith('.md'):
                    source_files.append(os.path.join(root, file))
        
        if not source_files:
            print(f"错误: 在 '{source_dir}' 中没有找到Markdown文件")
            return
        
        print(f"找到 {len(source_files)} 个Markdown文件")
        print(f"开始翻译到 {', '.join(languages)}...")
        
        if force_retranslate:
            print("注意: 启用强制重新翻译模式，将覆盖所有已存在的翻译文件")
        
        success_count, failure_count, skipped_count = translate_files_parallel(
            source_files, languages, api_key, model, force_retranslate, args.max_workers, verbose
        )
    
    print(f"\n翻译完成: {success_count} 个成功, {skipped_count} 个跳过, {failure_count} 个失败")

if __name__ == "__main__":
    main() 