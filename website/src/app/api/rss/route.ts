import { getPublishedArticles } from '@/lib/supabase';
import { getArticleTitle, getArticleCategory, parseSeoMeta, getSiteUrl } from '@/lib/utils';
import { contentToPlainText } from '@/lib/content';
import { SITE } from '@/lib/site';

export const revalidate = 300;

export async function GET() {
  const articles = await getPublishedArticles(50);
  const siteUrl = getSiteUrl();
  const buildDate = new Date().toUTCString();

  const items = articles
    .map((article) => {
      const seo = parseSeoMeta(article);
      const title = getArticleTitle(article);
      const category = getArticleCategory(article);
      const description = seo.meta_description || '';
      const content = article.content ? contentToPlainText(article.content).slice(0, 500) : description;
      const pubDate = article.published_at
        ? new Date(article.published_at).toUTCString()
        : buildDate;

      return `    <item>
      <title><![CDATA[${title}]]></title>
      <link>${siteUrl}/news/${article.slug}</link>
      <guid isPermaLink="true">${siteUrl}/news/${article.slug}</guid>
      <description><![CDATA[${description}]]></description>
      <content:encoded><![CDATA[${content}]]></content:encoded>
      <pubDate>${pubDate}</pubDate>
      <category><![CDATA[${category}]]></category>
    </item>`;
    })
    .join('\n');

  const xml = `<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:content="http://purl.org/rss/1.0/modules/content/">
  <channel>
    <title>${SITE.name}</title>
    <link>${siteUrl}</link>
    <description>${SITE.tagline}</description>
    <language>en-us</language>
    <lastBuildDate>${buildDate}</lastBuildDate>
    <generator>${SITE.name}</generator>
${items}
  </channel>
</rss>`;

  return new Response(xml, {
    headers: {
      'Content-Type': 'application/rss+xml; charset=utf-8',
      'Cache-Control': 'public, s-maxage=300, stale-while-revalidate=600',
    },
  });
}
