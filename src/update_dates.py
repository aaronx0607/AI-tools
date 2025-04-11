#!/usr/bin/env python3
import os
import re
import sys
from pathlib import Path

def extract_dates_from_file(file_path):
    """从英文文件中提取 publishedAt 和 updatedAt 信息"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    published_match = re.search(r'publishedAt:\s*([\d-]+)', content)
    updated_match = re.search(r'updatedAt:\s*([\d-]+)', content)
    
    published_date = published_match.group(1) if published_match else None
    updated_date = updated_match.group(1) if updated_match else None
    
    return published_date, updated_date

def add_dates_to_file(file_path, published_date, updated_date):
    """将日期信息添加到文件中（在 tags 字段之后）"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 检查文件是否已包含 publishedAt 和 updatedAt
    if 'publishedAt:' in content or 'updatedAt:' in content:
        print(f"跳过已包含日期的文件: {file_path}")
        return False
    
    # 查找 frontmatter 部分（在两个 --- 之间的内容）
    frontmatter_match = re.search(r'---(.*?)---', content, re.DOTALL)
    if not frontmatter_match:
        print(f"无法找到文件的 frontmatter 部分: {file_path}")
        return False
    
    frontmatter = frontmatter_match.group(1)
    
    # 查找 tags 字段
    tags_match = re.search(r'(tags:.*?)(\n[a-zA-Z]+:|$)', frontmatter, re.DOTALL)
    
    if tags_match:
        # 找到 tags 字段，在其后添加日期信息
        new_frontmatter = frontmatter.replace(
            tags_match.group(0),
            f"{tags_match.group(1)}\npublishedAt: {published_date}\nupdatedAt: {updated_date}{tags_match.group(2)}"
        )
    else:
        # 找不到 tags 字段，尝试在 frontmatter 末尾添加
        new_frontmatter = f"{frontmatter.rstrip()}\npublishedAt: {published_date}\nupdatedAt: {updated_date}\n"
    
    # 更新文件内容
    updated_content = content.replace(frontmatter, new_frontmatter)
    
    # 写回文件
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(updated_content)
    
    return True

def process_files(base_dir):
    """处理所有文件，从英文添加日期到其他语言"""
    base_dir = Path(base_dir)
    en_dir = base_dir / 'en'
    target_dirs = [base_dir / lang for lang in ['es', 'fr', 'zh']]
    
    # 获取英文目录下所有工具文件
    en_files = list(en_dir.glob('*.md'))
    print(f"找到 {len(en_files)} 个英文工具文件")
    
    success_count = 0
    skipped_count = 0
    error_count = 0
    
    for en_file in en_files:
        tool_name = en_file.name
        published_date, updated_date = extract_dates_from_file(en_file)
        
        if not published_date or not updated_date:
            print(f"警告: 无法从 {tool_name} 提取日期信息")
            error_count += 1
            continue
        
        print(f"处理工具: {tool_name}")
        print(f"  日期信息: publishedAt={published_date}, updatedAt={updated_date}")
        
        # 更新每个语言目录中的同名文件
        for target_dir in target_dirs:
            target_file = target_dir / tool_name
            if not target_file.exists():
                print(f"  跳过: 在 {target_dir.name} 目录中未找到 {tool_name}")
                skipped_count += 1
                continue
                
            result = add_dates_to_file(target_file, published_date, updated_date)
            if result:
                print(f"  成功: 已更新 {target_dir.name}/{tool_name}")
                success_count += 1
            else:
                skipped_count += 1
    
    print("\n摘要:")
    print(f"总共处理: {len(en_files)} 个工具")
    print(f"成功更新: {success_count} 个文件")
    print(f"跳过文件: {skipped_count} 个文件")
    print(f"错误文件: {error_count} 个文件")

def repair_files(base_dir):
    """修复已添加但格式不正确的日期字段"""
    base_dir = Path(base_dir)
    target_dirs = [base_dir / lang for lang in ['es', 'fr', 'zh']]
    
    fixed_count = 0
    skipped_count = 0
    
    # 正则表达式匹配格式错误的日期字段（没有换行的情况）
    wrong_format_pattern = r'(updatedAt:\s*[\d-]+)([^\n])'
    
    for target_dir in target_dirs:
        md_files = list(target_dir.glob('*.md'))
        for file_path in md_files:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 检查是否有格式错误的日期字段
            match = re.search(wrong_format_pattern, content)
            if match:
                print(f"修复文件格式: {file_path}")
                # 修复格式，在日期后添加换行
                fixed_content = re.sub(
                    wrong_format_pattern, 
                    r'\1\n\2', 
                    content
                )
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(fixed_content)
                
                fixed_count += 1
            else:
                skipped_count += 1
    
    print(f"\n修复摘要:")
    print(f"已修复文件: {fixed_count} 个")
    print(f"正常文件: {skipped_count} 个")

if __name__ == "__main__":
    content_dir = "src/content/tools"
    if len(sys.argv) > 1:
        content_dir = sys.argv[1]
    
    print(f"开始处理文件，基础目录: {content_dir}")
    
    # 首先修复已有但格式不正确的文件
    repair_files(content_dir)
    
    # 然后添加缺失的日期信息
    process_files(content_dir)
    
    print("处理完成!") 