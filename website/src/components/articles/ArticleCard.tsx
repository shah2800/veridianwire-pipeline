'use client';

import Link from 'next/link';
import { Clock } from 'lucide-react';
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

interface ArticleCardProps {
  article: PublishedArticle;
  variant?: 'default' | 'compact' | 'horizontal';
  priority?: boolean;
}

export function ArticleCard({ article, variant = 'default', priority }: ArticleCardProps) {
  const seo = parseSeoMeta(article);
  const title = getArticleTitle(article);
  const category = getArticleCategory(article);
  const readingTime = getReadingTime(article.content);

  if (variant === 'horizontal') {
    return (
      <article className="group flex gap-4 border-b border-slate-200 py-4 last:border-0">
        <Link href={`/news/${article.slug}`} className="relative h-20 w-28 flex-shrink-0 overflow-hidden rounded-md">
          <ArticleImage article={article} alt={title} priority={priority} sizes="112px" className="transition-transform duration-300 group-hover:scale-105" />
        </Link>
        <div className="min-w-0 flex-1">
          <Link
            href={`/category/${category}`}
            className={cn('mb-1 inline-block rounded px-2 py-0.5 text-xs font-semibold uppercase tracking-wide', getCategoryColor(category))}
          >
            {getCategoryLabel(category)}
          </Link>
          <h3 className="mb-1 line-clamp-2 font-serif text-base font-bold leading-snug text-slate-900 group-hover:text-news-red">
            <Link href={`/news/${article.slug}`}>{title}</Link>
          </h3>
          <div className="flex items-center gap-2 text-xs text-slate-500">
            <Clock className="h-3 w-3" />
            <span>{formatDate(article.published_at, 'relative')}</span>
            <span>·</span>
            <span>{readingTime} min read</span>
          </div>
        </div>
      </article>
    );
  }

  if (variant === 'compact') {
    return (
      <article className="group">
        <Link href={`/news/${article.slug}`} className="block">
          <h3 className="mb-1 line-clamp-2 font-serif text-sm font-bold leading-snug text-slate-900 group-hover:text-news-red">
            {title}
          </h3>
          <time className="text-xs text-slate-500">{formatDate(article.published_at, 'short')}</time>
        </Link>
      </article>
    );
  }

  return (
    <article className="group overflow-hidden rounded-lg border border-slate-200 bg-white shadow-sm transition-shadow hover:shadow-md">
      <Link href={`/news/${article.slug}`} className="relative block aspect-[16/10] overflow-hidden">
        <ArticleImage
          article={article}
          alt={title}
          priority={priority}
          sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw"
          className="transition-transform duration-500 group-hover:scale-105"
        />
        <span
          className={cn(
            'absolute left-3 top-3 rounded px-2.5 py-1 text-xs font-bold uppercase tracking-wide',
            getCategoryColor(category)
          )}
        >
          {getCategoryLabel(category)}
        </span>
      </Link>
      <div className="p-5">
        <h3 className="mb-2 line-clamp-2 font-serif text-lg font-bold leading-snug text-slate-900 group-hover:text-news-red">
          <Link href={`/news/${article.slug}`}>{title}</Link>
        </h3>
        {seo.meta_description && (
          <p className="mb-3 line-clamp-2 text-sm text-slate-600">{seo.meta_description}</p>
        )}
        <div className="flex items-center gap-2 text-xs text-slate-500">
          <Clock className="h-3.5 w-3.5" />
          <time>{formatDate(article.published_at, 'relative')}</time>
          <span>·</span>
          <span>{readingTime} min read</span>
        </div>
      </div>
    </article>
  );
}
