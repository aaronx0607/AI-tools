import type { APIRoute } from 'astro';

export const GET: APIRoute = async ({ request }) => {
  try {
    // 从URL获取语言参数
    const url = new URL(request.url);
    const lang = url.searchParams.get('lang') || 'en';

    // 根据语言获取对应的工具文件
    const toolFiles = import.meta.glob('@content/tools/*/*.md', { eager: true });

    // 筛选当前语言的工具文件
    const langToolFiles = Object.entries(toolFiles)
      .filter(([path]) => path.includes(`/tools/${lang}/`))
      .map(([_, content]) => content);

    // 如果当前语言没有工具文件，则使用英文版本
    const filesToUse = langToolFiles.length > 0 ? langToolFiles : Object.entries(toolFiles)
      .filter(([path]) => path.includes('/tools/en/'))
      .map(([_, content]) => content);

    // 提取工具数据
    const tools = filesToUse.map((tool: any) => ({
      id: tool.frontmatter.id,
      name: tool.frontmatter.name,
      description: tool.frontmatter.description,
      category: tool.frontmatter.category,
      rating: tool.frontmatter.rating,
      reviews: tool.frontmatter.reviews,
      website: tool.frontmatter.website,
      icon: tool.frontmatter.icon
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
