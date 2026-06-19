import { getPublishedArticles } from '@/lib/supabase';
import { CATEGORIES } from '@/lib/categories';
import { getSiteUrl } from '@/lib/site';

export const revalidate = 300;

export async function GET() {
  const articles = await getPublishedArticles(500);
  const base = getSiteUrl();

  const staticPages = [
    { loc: base, changefreq: 'hourly', priority: '1.0' },
    { loc: `${base}/news`, changefreq: 'hourly', priority: '0.9' },
    { loc: `${base}/about`, changefreq: 'monthly', priority: '0.5' },
    { loc: `${base}/search`, changefreq: 'weekly', priority: '0.6' },
    ...CATEGORIES.map((cat) => ({
      loc: `${base}/category/${cat.slug}`,
      changefreq: 'hourly',
      priority: '0.7',
    })),
  ];

  const urls = [
    ...staticPages.map(
      (p) => `  <url>
    <loc>${p.loc}</loc>
    <changefreq>${p.changefreq}</changefreq>
    <priority>${p.priority}</priority>
  </url>`
    ),
    ...articles.map((a) => {
      const lastmod = a.published_at
        ? new Date(a.published_at).toISOString()
        : new Date().toISOString();
      return `  <url>
    <loc>${base}/news/${a.slug}</loc>
    <lastmod>${lastmod}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.8</priority>
  </url>`;
    }),
  ];

  const xml = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
${urls.join('\n')}
</urlset>`;

  return new Response(xml, {
    headers: {
      'Content-Type': 'application/xml',
      'Cache-Control': 'public, s-maxage=300, stale-while-revalidate=600',
    },
  });
}
