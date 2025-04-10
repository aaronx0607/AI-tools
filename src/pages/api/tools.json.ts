import type { APIRoute } from 'astro';
import { defaultLang, languages } from '../../i18n/ui';

export const GET: APIRoute = async ({ request }) => {
  try {
    // 从 URL 参数中获取语言
    const url = new URL(request.url);
    let lang = url.searchParams.get('lang') || defaultLang;

    // 调试信息
    console.log('API Request URL:', request.url);
    console.log('Detected language:', lang);

    // 验证语言是否有效
    if (!Object.keys(languages).includes(lang)) {
      console.log('Invalid language, falling back to default:', defaultLang);
      lang = defaultLang;
    }

    // 从相应语言的目录获取工具
    const toolFiles = import.meta.glob('../../content/tools/*/*.md', { eager: true });

    // 根据语言过滤工具
    const allPaths = Object.keys(toolFiles);
    console.log('All tool paths:', allPaths);

    const filteredTools = Object.entries(toolFiles).filter(([path]) => {
      // 检查路径是否包含指定语言的目录
      const matches = path.includes(`/tools/${lang}/`);
      console.log(`Path: ${path}, Language: ${lang}, Matches: ${matches}`);
      return matches;
    });

    console.log(`Found ${filteredTools.length} tools for language: ${lang}`);

    // 提取工具数据
    const tools = filteredTools.map(([_, tool]: [string, any]) => ({
      id: tool.frontmatter.id,
      name: tool.frontmatter.name,
      description: tool.frontmatter.description,
      category: tool.frontmatter.category,
      rating: tool.frontmatter.rating,
      reviews: tool.frontmatter.reviews,
      tags: tool.frontmatter.tags || []
    }));

    return new Response(JSON.stringify(tools), {
      status: 200,
      headers: {
        'Content-Type': 'application/json'
      }
    });
  } catch (error) {
    console.error('Error fetching tools:', error);
    return new Response(JSON.stringify({ error: 'Failed to fetch tools' }), {
      status: 500,
      headers: {
        'Content-Type': 'application/json'
      }
    });
  }
}
