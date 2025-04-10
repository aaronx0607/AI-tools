# AI工具多语言翻译脚本使用指南

## 简介

`translate_tools.py` 是一个用于将AI工具的Markdown文件从英文翻译到多种语言的Python脚本。该脚本利用OpenRouter API提供的AI模型进行高质量翻译，可以自动处理Markdown文件的前置元数据和内容部分，并将翻译后的文件按照相同的目录结构保存到对应的语言目录中。

本脚本具有以下特点：

- 支持同时翻译到多种语言（西班牙语、法语、简体中文等）
- 智能处理前置元数据（Frontmatter）中的各种字段
- 保持Markdown格式和特殊内容（如代码块、链接）的完整性
- 支持单文件翻译或批量翻译整个目录
- 可并行处理多个翻译任务，提高效率
- 自动跳过已翻译的文件，避免重复工作和不必要的API调用

## 安装依赖

运行脚本前，需要安装以下Python依赖包：

```bash
pip install pyyaml requests
```

## 基本用法

### 命令行参数

脚本支持以下命令行参数：

| 参数 | 描述 | 默认值 |
|------|------|--------|
| `--api-key` | OpenRouter API密钥（必需） | 无 |
| `--source-dir` | 英文Markdown文件源目录 | src/content/tools/en |
| `--model` | 使用的AI模型 | openai/gpt-4o-mini |
| `--languages` | 目标语言代码（逗号分隔） | es,fr,zh |
| `--file` | 单个文件路径（可选） | 无 |
| `--max-workers` | 并行工作线程数 | 3 |
| `--verbose` | 显示详细输出 | False |
| `--force` | 强制重新翻译已存在的文件 | False |

### 翻译整个目录

```bash
python3 translate_tools.py --api-key YOUR_OPENROUTER_API_KEY
```

这将翻译 `src/content/tools/en` 目录下的所有Markdown文件到西班牙语(es)、法语(fr)和简体中文(zh)。**注意：已存在的翻译文件将被跳过**。

### 翻译单个文件

```bash
python translate_tools.py --api-key YOUR_OPENROUTER_API_KEY --file src/content/tools/en/chatgpt.md
```

这将只翻译指定的文件 `chatgpt.md` 到默认的三种语言。

### 指定目标语言

```bash
python3 translate_tools.py --api-key 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 --languages zh,es
```

这将只翻译到简体中文和西班牙语。

### 使用不同的AI模型

```bash
python translate_tools.py --api-key YOUR_OPENROUTER_API_KEY --model openai/gpt-3.5-turbo
```

这将使用OpenAI的GPT-3.5 Turbo模型来进行翻译。

### 强制重新翻译已存在的文件

```bash
python translate_tools.py --api-key YOUR_OPENROUTER_API_KEY --force
```

这将重新翻译所有文件，包括已经存在翻译的文件。当您需要更新或改进现有翻译时，这个选项很有用。

### 显示详细输出

```bash
python translate_tools.py --api-key YOUR_OPENROUTER_API_KEY --verbose
```

这将显示翻译过程中的详细信息。

## 翻译内容说明

脚本会翻译Markdown文件中的以下内容：

### 前置元数据（Frontmatter）

- `name`：工具名称
- `description`：工具描述
- `tags`：标签数组
- `pricing`：价格信息中的文本部分（而不是价格数字）
- `features`：功能列表

示例：
```yaml
---
id: chatgpt        # 不翻译
name: ChatGPT      # 翻译
description: OpenAI的强大AI助手  # 翻译
category: chatbots  # 不翻译
tags: [AI assistant, chatbot]  # 翻译为 [AI助手, 聊天机器人]
pricing:
  free: Free tier  # 翻译
  plus: $20/month  # 不翻译价格数字
features:
  - Text generation  # 翻译
  - Code assistance  # 翻译
---
```

### Markdown正文内容

脚本会翻译Markdown正文的全部内容，同时保持以下元素不变：

- Markdown格式标记（#, -, *, 等）
- 链接URL部分（但会翻译链接文本）
- 代码块内容
- 图片路径

## 支持的语言

当前脚本支持以下语言：

| 语言代码 | 语言名称 |
|----------|----------|
| es | 西班牙语 |
| fr | 法语 |
| zh | 简体中文 |

## 添加新的目标语言

如需添加新的目标语言，请修改脚本开头的 `LANGUAGES` 字典：

```python
LANGUAGES = {
    "es": "西班牙语",
    "fr": "法语",
    "zh": "简体中文",
    "de": "德语",   # 添加新语言
    "ja": "日语"    # 添加新语言
}
```

## 跳过已翻译文件的机制

为了避免重复翻译和不必要的API调用，脚本会自动检查目标文件是否已存在：

1. 如果目标文件已存在（例如 `src/content/tools/zh/chatgpt.md`），脚本会默认跳过该文件
2. 跳过的文件会在控制台输出中显示为"跳过已存在的文件"
3. 如果需要强制重新翻译已存在的文件，请使用 `--force` 参数

这种机制的优点：
- 节省API调用费用
- 减少翻译时间
- 保护已经人工优化过的翻译内容
- 支持增量翻译（只翻译新添加的文件）

## 常见问题

### API密钥获取

1. 注册[OpenRouter](https://openrouter.ai/)账户
2. 在控制面板中创建API密钥
3. 将该密钥作为 `--api-key` 参数传递给脚本

### API调用失败

如果遇到API调用失败，可能的原因包括：

- API密钥无效或已过期
- 达到API调用速率限制
- 选择的模型不可用

出现此类问题时，脚本会显示详细的错误信息。

### 翻译质量问题

翻译质量主要取决于选择的AI模型。一般而言：

- `openai/gpt-4o-mini`：性价比高，适合大多数翻译任务
- `anthropic/claude-3-haiku`：适合大多数翻译任务，速度较快
- `anthropic/claude-3-sonnet`：质量更高，但速度较慢
- `anthropic/claude-3-opus`：最高质量，但速度更慢且成本更高
- `openai/gpt-4`：高质量翻译，特别适合技术内容

### 费用控制

使用该脚本会产生API调用费用。可以通过以下方法控制费用：

- 选择更经济的模型（如 `openai/gpt-3.5-turbo`）
- 一次只翻译少量文件
- 限制目标语言数量
- 利用跳过已翻译文件的功能，避免重复翻译

## 示例输出

运行脚本后，将在对应的语言目录中生成翻译后的文件。例如，如果原始文件路径为：

```
src/content/tools/en/chatgpt.md
```

翻译后将在以下路径生成文件：

```
src/content/tools/es/chatgpt.md  # 西班牙语
src/content/tools/fr/chatgpt.md  # 法语
src/content/tools/zh/chatgpt.md  # 简体中文
```

输出的统计信息将包括：
- 成功翻译的文件数量
- 跳过的文件数量
- 翻译失败的文件数量

## 扩展和定制

该脚本可以根据需要进行扩展和定制：

- 修改翻译的字段：编辑 `translate_frontmatter` 函数
- 添加新的语言：扩展 `LANGUAGES` 字典
- 调整翻译提示：修改 `translate_text` 函数中的提示模板
- 支持新的文件格式：调整 `read_markdown_file` 函数
- 修改跳过文件的逻辑：编辑 `translate_and_save_file` 函数

## 注意事项

- 翻译大量文件可能需要较长时间
- API调用会产生费用，请注意控制使用量
- 翻译结果仍然需要人工审核以确保准确性和专业性
- 已存在的文件会被跳过，除非使用 `--force` 参数

## 技术支持

如有任何问题或需要技术支持，请联系项目维护团队。 