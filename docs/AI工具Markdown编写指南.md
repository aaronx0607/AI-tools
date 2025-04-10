# AI工具目录 - Markdown编写指南

## 简介

本指南将帮助您为AI工具目录创建标准化的Markdown文件。这些文件将被用于生成网站上的工具详情页面，并支持多语言显示、分类浏览和标签搜索功能。

## 文件位置

所有工具的Markdown文件应放置在以下目录结构中：

```
src/content/tools/
├── en/         # 英文版工具描述
├── es/         # 西班牙语版工具描述
├── fr/         # 法语版工具描述
└── zh/         # 中文版工具描述
```

每个语言目录下的文件名应使用工具的英文ID，例如：`chatgpt.md`、`midjourney.md`等。

## Markdown文件结构

每个Markdown文件由两部分组成：
1. **前置元数据（Frontmatter）**：包含在`---`之间的YAML格式数据
2. **内容**：Markdown格式的详细描述

### 前置元数据示例

```yaml
---
id: chatgpt
name: ChatGPT
description: OpenAI开发的强大AI对话和文本生成工具
category: text-generation
rating: 4.9
reviews: 320
website: https://chat.openai.com
icon: 🤖
tags: [AI对话, 文本生成, OpenAI, GPT, 聊天机器人]
pricing:
  free: true
  plus: $20/月
  team: $30/用户/月
  enterprise: 定制价格
features:
  - 自然语言对话
  - 多语言支持
  - 内容创作
  - 代码辅助
  - 知识问答
publishedAt: 2022-06-21
updatedAt: 2025-04-09
---
```

### 必填字段

| 字段 | 描述 | 示例 |
|------|------|------|
| `id` | 工具的唯一标识符（英文，小写，使用连字符） | `chatgpt`, `midjourney` |
| `name` | 工具的显示名称 | `ChatGPT`, `Midjourney` |
| `description` | 简短描述（100-150字符） | `OpenAI开发的强大AI对话和文本生成工具` |
| `category` | 工具所属分类（必须是预定义分类之一） | `text-generation` |
| `rating` | 评分（1.0-5.0） | `4.9` |
| `reviews` | 评论数量 | `320` |
| `website` | 官方网站URL | `https://chat.openai.com` |
| `icon` | 工具图标（可使用emoji、Unicode字符或图片URL） | `🤖` 或 `https://example.com/icon.png` |
| `tags` | 标签数组（用于搜索和分类） | `[AI对话, 文本生成, OpenAI]` |
| `pricing` | 价格计划（键值对） | 见示例 |
| `features` | 主要功能列表 | 见示例 |
| `publishedAt` | 该工具上市日期（格式：YYYY-MM-DD） | `2022-06-21` |
| `updatedAt` | 页面更新日期（格式：YYYY-MM-DD） | `2025-04-09` |


## 支持的分类

目前支持以下分类：

- `text-generation` - 文本生成
- `image-generation` - 图像生成
- `code-generation` - 代码生成
- `audio-generation` - 音频生成
- `video-generation` - 视频生成
- `chatbots` - 聊天机器人
- `data-analysis` - 数据分析
- `automation` - 自动化

## 内容部分

内容部分应使用Markdown格式，包含以下建议的结构（此外你应该添加更多内容，以符合SEO要求）：

```markdown
# 工具名称

详细介绍，包括工具的背景、开发者、主要用途等。

## 主要功能

### 功能1
功能1的详细说明

### 功能2
功能2的详细说明

## 使用场景

1. **场景1**
   - 子场景A
   - 子场景B

2. **场景2**
   - 子场景C
   - 子场景D

## 版本与价格

### 免费版
- 功能限制
- 使用限制

### 付费版
- 额外功能
- 价格详情
```

## 完整示例

```markdown
---
id: chatgpt
name: ChatGPT
description: OpenAI开发的强大AI对话和文本生成工具
category: text-generation
rating: 4.9
reviews: 320
website: https://chat.openai.com
icon: 🤖
tags: [AI对话, 文本生成, OpenAI, GPT, 聊天机器人]
pricing:
  free: true
  plus: $20/月
  team: $30/用户/月
  enterprise: 定制价格
features:
  - 自然语言对话
  - 多语言支持
  - 内容创作
  - 代码辅助
  - 知识问答
publishedAt: 2022-06-21
updatedAt: 2025-04-09
---

# ChatGPT

ChatGPT是由OpenAI开发的先进大型语言模型，能够理解和生成类人的文本内容，为用户提供自然流畅的对话体验。

## 主要功能

### 自然语言对话
ChatGPT能够理解上下文，进行连贯的多轮对话，模拟人类交流方式，提供流畅的对话体验。

### 多语言支持
支持包括中文、英文、日文、西班牙语等在内的多种语言，能够进行跨语言的内容创作和翻译。

### 内容创作
可以帮助用户撰写各类文本内容，包括文章、报告、电子邮件、脚本、诗歌等，并根据用户需求调整风格和语调。

### 代码辅助
能够生成、解释和调试多种编程语言的代码，帮助开发者提高编程效率。

### 知识问答
基于训练数据回答用户关于各领域的问题，提供信息和解释，但知识截止日期有限制。

## 使用场景

1. **内容创作**
   - 博客文章和社交媒体内容
   - 营销文案和广告语
   - 学术论文和报告
   - 创意写作和故事创作

2. **教育辅助**
   - 学习辅导和解答问题
   - 生成教学材料
   - 语言学习和练习

3. **商业应用**
   - 客户服务自动化
   - 市场研究和分析
   - 商业报告和提案
   - 产品描述和说明书

4. **个人助理**
   - 日程安排和提醒
   - 信息查询和总结
   - 创意灵感和建议

## 版本与价格

### 免费版
- 基本对话功能
- 有使用限制
- 使用较旧的模型

### Plus ($20/月)
- 优先访问新功能
- 更快的响应速度
- 使用最新的GPT-4模型
- 更高的使用限制

### Team ($30/用户/月)
- 团队协作功能
- 共享工作空间
- 高级数据分析
- 专业支持

### Enterprise (定制价格)
- 定制化解决方案
- 高级安全和隐私保护
- 专属客户支持
- API集成选项
```

## 多语言支持

为了支持多语言，您需要为每种支持的语言创建对应的Markdown文件。确保：

1. 文件名保持一致（例如，所有语言版本的ChatGPT都使用`chatgpt.md`）
2. 前置元数据中的`id`字段保持一致
3. 翻译`name`、`description`、`tags`和内容部分
4. 价格可以根据地区进行调整

## 标签最佳实践

1. 使用3-7个相关标签
2. 标签应简洁明了
3. 包含工具名称、类别和主要功能相关的标签
4. 使用当地语言的标签（例如，中文版使用中文标签）
5. 避免过于宽泛的标签（如"AI"、"工具"）

## 图片和媒体

目前不支持在Markdown中直接嵌入图片。如需添加图片功能，请联系开发团队。

## 提交流程

1. 创建或编辑相应语言目录下的Markdown文件
2. 确保文件名和ID一致
3. 验证前置元数据格式
4. 提交更改

## 常见问题

**Q: 如何添加新的分类？**
A: 目前分类是预定义的。如需添加新分类，请联系开发团队。

**Q: 可以使用HTML标签吗？**
A: 是的，但建议尽量使用Markdown语法以保持一致性。

**Q: 如何更新已有工具的信息？**
A: 直接编辑对应的Markdown文件，保持ID不变。

---

如有任何问题或建议，请联系项目维护团队。
