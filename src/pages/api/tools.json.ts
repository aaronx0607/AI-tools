import type { APIRoute } from 'astro';

export const GET: APIRoute = async () => {
  try {
    // 从 content/tools/en 目录获取所有工具
    const toolFiles = await import.meta.glob('@content/tools/en/*.md', { eager: true });

    // 提取工具数据
    const tools = Object.values(toolFiles).map((tool: any) => ({
      id: tool.frontmatter.id,
      name: tool.frontmatter.name,
      description: tool.frontmatter.description,
      category: tool.frontmatter.category,
      rating: tool.frontmatter.rating,
      reviews: tool.frontmatter.reviews
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
