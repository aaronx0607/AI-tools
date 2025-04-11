# AI工具多语言翻译脚本使用指南

## 简介

这个Python脚本用于将英文Markdown文件翻译成其他语言。它使用OpenRouter API进行翻译,支持并发处理,并且能够保持Markdown格式和代码块的完整性。

## 功能特点

- 支持多语言翻译(默认支持中文、法语和西班牙语)
- 保持Markdown格式和Front Matter完整性
- 不翻译代码块内的代码
- 支持大文件的分块翻译
- 并发处理多个文件
- 详细的日志记录
- 进度条显示
- 可配置的翻译参数

## 安装依赖

```bash
pip install requests tqdm pyyaml
```

## 配置API密钥

在脚本中已经直接设置了OpenRouter API密钥。使用前请确认`translate_blog.py`文件中的密钥是否正确:

```python
# 直接设置 OpenRouter API 密钥
OPENROUTER_API_KEY = "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"
```

## 使用方法

### 基本用法

```bash
python translate_blog.py
```

这将使用默认配置:
- 源目录: `src/content/blog/en`
- 目标目录前缀: `src/content/blog`
- 目标语言: `fr`, `es`, `zh`
- OpenRouter模型: `openai/gpt-4o-mini`

### 自定义配置

```bash
python translate_blog.py \
  --source path/to/source \
  --target-prefix path/to/target \
  --languages fr es zh \
  --model openai/gpt-4o \
  --threads 3 \
  --chunk-size 4000 \
  --force
```

### 命令行参数

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--source` | 源文件目录 | src/content/blog/en |
| `--target-prefix` | 目标文件目录前缀 | src/content/blog |
| `--languages` | 目标语言列表 | fr es zh |
| `--model` | OpenRouter模型 | openai/gpt-4o-mini |
| `--threads` | 并发线程数 | 3 |
| `--chunk-size` | 分块大小(令牌数) | 4000 |
| `--force` | 强制重新翻译 | False |
| `--max-files` | 最大翻译文件数 | None |

## 注意事项

1. 翻译过程会自动跳过已存在的目标文件,除非使用`--force`参数
2. 大文件会自动分块处理,每块默认4000个令牌
3. 翻译日志保存在`translation.log`文件中
4. 代码块内的代码不会被翻译
5. Front Matter会被保留并翻译
6. 所有Markdown格式会被保持

## 支持的模型

脚本使用OpenRouter API，可以使用各种模型进行翻译，例如：

- `openai/gpt-4o-mini` - 默认，性价比高
- `openai/gpt-4o` - 更高质量但成本更高
- `anthropic/claude-3-haiku` - 适合大多数翻译任务
- `anthropic/claude-3-sonnet` - 质量更高
- `anthropic/claude-3-opus` - 最高质量，但成本更高

## 示例

### 翻译单个语言

```bash
python translate_blog.py --languages zh
```

### 强制重新翻译

```bash
python translate_blog.py --force
```

### 使用不同的模型

```bash
python translate_blog.py --model anthropic/claude-3-haiku
```

### 限制并发数

```bash
python translate_blog.py --threads 2
```

## 故障排除

### 常见问题

1. API密钥不正确
   ```
   错误: 401 Client Error: Unauthorized
   ```
   解决: 在脚本中修改`OPENROUTER_API_KEY`变量为正确的API密钥

2. 目标文件已存在
   ```
   跳过 [文件路径] (已存在)
   ```
   解决: 使用 `--force` 参数强制重新翻译

3. API速率限制
   ```
   错误: 429 Client Error: Too Many Requests
   ```
   解决: 减少并发线程数或增加延迟时间

### 日志查看

翻译过程的详细日志保存在`translation.log`文件中,包含:
- 翻译开始和完成时间
- 成功和失败的文件列表
- 错误信息和堆栈跟踪

## 贡献

欢迎提交问题报告和改进建议! 