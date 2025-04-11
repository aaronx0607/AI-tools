import { marked } from 'marked';

/**
 * 自定义Markdown渲染器，支持工具卡片语法
 * @param {string} markdown - 原始Markdown内容
 * @param {string} lang - 当前语言
 * @returns {string} 处理后的HTML
 */
export function parseMarkdown(markdown, lang) {
  // 创建自定义渲染器
  const renderer = new marked.Renderer();

  // 保存原始的段落渲染方法
  const originalParagraph = renderer.paragraph.bind(renderer);

  // 重写段落渲染方法，处理工具卡片语法
  renderer.paragraph = (text) => {
    // 检查是否包含工具卡片语法 {{tool:工具ID}}
    const toolMatch = text.match(/^\s*{{tool:([a-z0-9-]+)}}\s*$/);

    if (toolMatch) {
      const toolId = toolMatch[1];
      // 返回工具卡片组件的占位符，稍后会被替换
      return `<!--TOOL_CARD_PLACEHOLDER:${toolId}-->`;
    }

    // 如果不是工具卡片语法，使用原始渲染方法
    return originalParagraph(text);
  };

  // 使用自定义渲染器解析Markdown
  const html = marked.parse(markdown, { renderer });

  return html;
}

/**
 * 替换HTML中的工具卡片占位符为特殊的HTML标记
 * @param {string} html - 包含占位符的HTML
 * @returns {string} 替换后的HTML
 */
export function replaceToolCardPlaceholders(html) {
  // 查找所有工具卡片占位符
  const placeholderRegex = /<!--TOOL_CARD_PLACEHOLDER:([a-z0-9-]+)-->/g;

  // 替换占位符为特殊的HTML标记
  const replacedHtml = html.replace(placeholderRegex, (match, toolId) => {
    return `<div class="tool-card-placeholder" data-tool-id="${toolId}"></div>`;
  });

  return replacedHtml;
}
