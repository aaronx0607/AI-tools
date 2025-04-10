import type { APIRoute } from 'astro';

export const GET: APIRoute = async ({ request, url }) => {
  try {
    // 获取请求的语言
    const lang = url.searchParams.get('lang') || 'en';

    // 支持的语言列表
    const supportedLangs = ['en', 'es', 'fr', 'zh'];

    // 验证语言是否支持
    const validLang = supportedLangs.includes(lang) ? lang : 'en';

    // 使用静态导入路径
    let toolFiles: Record<string, any> = {};

    // 根据语言选择相应的工具文件
    if (validLang === 'en') {
      toolFiles = await import.meta.glob('../../content/tools/en/*.md', { eager: true });
    } else if (validLang === 'es') {
      toolFiles = await import.meta.glob('../../content/tools/es/*.md', { eager: true });
    } else if (validLang === 'fr') {
      toolFiles = await import.meta.glob('../../content/tools/fr/*.md', { eager: true });
    } else if (validLang === 'zh') {
      toolFiles = await import.meta.glob('../../content/tools/zh/*.md', { eager: true });
    }

    // 如果指定语言的工具为空，回退到英文
    let finalToolFiles = toolFiles;
    if (Object.keys(toolFiles).length === 0 && validLang !== 'en') {
      console.log(`No tools found for language ${validLang}, falling back to English`);
      finalToolFiles = await import.meta.glob('../../content/tools/en/*.md', { eager: true });
    }

    // 提取工具数据
    const tools = Object.values(finalToolFiles).map((tool: any) => ({
      id: tool.frontmatter.id,
      name: tool.frontmatter.name,
      description: tool.frontmatter.description,
      category: tool.frontmatter.category,
      rating: tool.frontmatter.rating,
      reviews: tool.frontmatter.reviews,
      lang: validLang // 添加语言标记
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
