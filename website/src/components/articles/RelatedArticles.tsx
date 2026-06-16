import Link from 'next/link';
import { ArticleCard } from '@/components/articles/ArticleCard';
import type { PublishedArticle } from '@/types/article';

interface RelatedArticlesProps {
  articles: PublishedArticle[];
}

export function RelatedArticles({ articles }: RelatedArticlesProps) {
  if (!articles.length) return null;

  return (
    <section className="mt-12 border-t border-slate-200 pt-10">
      <h2 className="mb-6 font-serif text-2xl font-bold text-slate-900">Related Stories</h2>
      <div className="grid gap-6 sm:grid-cols-2">
        {articles.map((article) => (
          <ArticleCard key={article.slug} article={article} variant="horizontal" />
        ))}
      </div>
      <div className="mt-6 text-center">
        <Link
          href="/"
          className="text-sm font-semibold text-news-red hover:underline"
        >
          View all news →
        </Link>
      </div>
    </section>
  );
}
