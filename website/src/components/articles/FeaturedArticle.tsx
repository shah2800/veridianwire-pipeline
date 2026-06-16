import Link from 'next/link';
import { Clock, ShieldCheck } from 'lucide-react';
import type { PublishedArticle } from '@/types/article';
import {
  getArticleTitle,
  getArticleCategory,
  formatDate,
  getReadingTime,
  getCategoryColor,
  parseSeoMeta,
  cn,
} from '@/lib/utils';
import { getCategoryLabel } from '@/lib/categories';
import { ArticleImage } from '@/components/articles/ArticleImage';

interface FeaturedArticleProps {
  article: PublishedArticle;
}

export function FeaturedArticle({ article }: FeaturedArticleProps) {
  const seo = parseSeoMeta(article);
  const title = getArticleTitle(article);
  const category = getArticleCategory(article);
  const readingTime = getReadingTime(article.content);
  const factScore = seo.fact_check_score ?? article.fact_check_score;

  return (
    <article className="group relative overflow-hidden rounded-xl bg-slate-900">
      <Link href={`/news/${article.slug}`} className="relative block aspect-[3/4] min-h-[460px] sm:aspect-[21/9] sm:min-h-[400px]">
        <ArticleImage
          article={article}
          alt={title}
          priority
          sizes="100vw"
          className="opacity-60 transition-transform duration-700 group-hover:scale-105 group-hover:opacity-50"
        />
        <div className="absolute inset-0 bg-gradient-to-t from-slate-900 via-slate-900/60 to-transparent" />
        <div className="absolute bottom-0 left-0 right-0 p-4 sm:p-10">
          <div className="mb-2 flex flex-wrap items-center gap-2 sm:mb-3 sm:gap-3">
            <span className="rounded bg-news-red px-3 py-1 text-xs font-bold uppercase tracking-widest text-white">
              Breaking
            </span>
            <Link
              href={`/category/${category}`}
              className={cn('rounded px-2.5 py-1 text-xs font-semibold uppercase', getCategoryColor(category))}
            >
              {getCategoryLabel(category)}
            </Link>
            {factScore !== undefined && factScore > 0 && (
              <span className="flex items-center gap-1 text-xs text-emerald-300">
                <ShieldCheck className="h-3.5 w-3.5" />
                {(factScore * 100).toFixed(0)}% verified
              </span>
            )}
          </div>
          <h2 className="mb-2 max-w-4xl font-serif text-xl font-bold leading-tight text-white sm:mb-3 sm:text-4xl lg:text-5xl">
            {title}
          </h2>
          {seo.meta_description && (
            <p className="mb-3 hidden max-w-2xl line-clamp-2 text-base text-slate-300 sm:mb-4 sm:block sm:text-lg">
              {seo.meta_description}
            </p>
          )}
          <div className="flex items-center gap-3 text-sm text-slate-400">
            <Clock className="h-4 w-4" />
            <time>{formatDate(article.published_at)}</time>
            <span>·</span>
            <span>{readingTime} min read</span>
          </div>
        </div>
      </Link>
    </article>
  );
}
