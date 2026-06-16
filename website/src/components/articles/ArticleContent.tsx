import { sanitizeArticleContent } from '@/lib/content';

interface ArticleContentProps {
  content: string;
}

export function ArticleContent({ content }: ArticleContentProps) {
  const sanitized = sanitizeArticleContent(content);

  return (
    <div
      className="article-content prose prose-lg prose-slate max-w-none prose-headings:font-serif prose-headings:text-slate-900 prose-a:text-news-red prose-a:no-underline hover:prose-a:underline prose-img:rounded-lg"
      dangerouslySetInnerHTML={{ __html: sanitized }}
    />
  );
}
