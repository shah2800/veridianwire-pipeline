import Link from 'next/link';
import { notFound } from 'next/navigation';
import { Clock, ShieldCheck, ExternalLink, ChevronLeft } from 'lucide-react';
import {
  getArticleBySlug,
  getPublishedArticles,
  getRelatedArticles,
} from '@/lib/supabase';
import { SiteLayout } from '@/components/layout/SiteLayout';
import { ArticleContent } from '@/components/articles/ArticleContent';
import { ArticleImage } from '@/components/articles/ArticleImage';
import { ArticleVideoFromMeta } from '@/components/articles/ArticleVideo';
import { ShareButtons } from '@/components/articles/ShareButtons';
import { RelatedArticles } from '@/components/articles/RelatedArticles';
import { NewsletterForm } from '@/components/layout/NewsletterForm';
import {
  getArticleTitle,
  getArticleCategory,
  formatDate,
  formatDateTime,
  getReadingTime,
  getCategoryColor,
  parseSeoMeta,
  getSiteUrl,
} from '@/lib/utils';
import { resolveArticleMedia } from '@/lib/media';
import { contentToPlainText } from '@/lib/content';
import { getCategoryLabel } from '@/lib/categories';
import { SITE } from '@/lib/site';
import { cn } from '@/lib/utils';

export const revalidate = 300;

type Props = { params: { slug: string } };

export async function generateStaticParams() {
  try {
    const articles = await getPublishedArticles(100);
    return articles.map((article) => ({ slug: article.slug }));
  } catch {
    return [];
  }
}

export async function generateMetadata({ params }: Props) {
  const article = await getArticleBySlug(params.slug);
  if (!article) return {};

  const seo = parseSeoMeta(article);
  const title = getArticleTitle(article);
  const siteUrl = getSiteUrl();
  const imageUrl = resolveArticleMedia(article).imageUrl;

  return {
    title,
    description: seo.meta_description,
    keywords: seo.keywords,
    alternates: {
      canonical: `/news/${article.slug}`,
    },
    openGraph: {
      title,
      description: seo.meta_description,
      url: `${siteUrl}/news/${article.slug}`,
      type: 'article',
      publishedTime: article.published_at,
      images: [{ url: imageUrl, width: 1200, height: 630 }],
    },
    twitter: {
      card: 'summary_large_image',
      title,
      description: seo.meta_description,
      images: [imageUrl],
    },
  };
}

export default async function ArticlePage({ params }: Props) {
  const article = await getArticleBySlug(params.slug);
  if (!article) notFound();

  const seo = parseSeoMeta(article);
  const title = getArticleTitle(article);
  const category = getArticleCategory(article);
  const imageUrl = resolveArticleMedia(article).imageUrl;
  const readingTime = getReadingTime(article.content);
  const factScore = seo.fact_check_score ?? article.fact_check_score;
  const related = await getRelatedArticles(article.slug, category, 4);
  const siteUrl = getSiteUrl();
  const bodyText = contentToPlainText(article.content || '');
  const showSubtitle =
    seo.meta_description &&
    !bodyText.toLowerCase().startsWith(seo.meta_description.trim().toLowerCase().slice(0, 40));

  return (
    <SiteLayout>
      <article>
        {/* Hero image */}
        <div className="relative h-64 sm:h-80 lg:h-96">
          <ArticleImage
            article={article}
            alt={title}
            priority
            sizes="100vw"
          />
          <div className="absolute inset-0 bg-gradient-to-t from-slate-900/80 to-transparent" />
        </div>

        <div className="mx-auto max-w-4xl px-4 py-8 sm:px-6 lg:px-8">
          <Link
            href="/"
            className="mb-6 inline-flex items-center gap-1 text-sm font-medium text-news-red hover:underline"
          >
            <ChevronLeft className="h-4 w-4" />
            Back to Home
          </Link>

          {/* Meta */}
          <div className="mb-4 flex flex-wrap items-center gap-3">
            <Link
              href={`/category/${category}`}
              className={cn(
                'rounded px-3 py-1 text-xs font-bold uppercase tracking-wide',
                getCategoryColor(category)
              )}
            >
              {getCategoryLabel(category)}
            </Link>
            <time className="text-sm text-slate-500">{formatDate(article.published_at)}</time>
            <span className="flex items-center gap-1 text-sm text-slate-500">
              <Clock className="h-3.5 w-3.5" />
              {readingTime} min read
            </span>
            {factScore !== undefined && factScore > 0 && (
              <span className="flex items-center gap-1 rounded-full bg-emerald-50 px-2.5 py-0.5 text-xs font-medium text-emerald-700">
                <ShieldCheck className="h-3.5 w-3.5" />
                {(factScore * 100).toFixed(0)}% fact-checked
              </span>
            )}
          </div>

          {/* Title */}
          <h1 className="mb-4 font-serif text-3xl font-bold leading-tight text-slate-900 sm:text-4xl lg:text-5xl">
            {title}
          </h1>

          {showSubtitle && (
            <p className="mb-6 text-xl leading-relaxed text-slate-600">{seo.meta_description}</p>
          )}

          <ShareButtons slug={article.slug} title={title} />

          <ArticleVideoFromMeta seoMeta={seo} title={title} />

          {/* Content */}
          <div className="my-10 border-t border-slate-200 pt-10">
            {article.content ? (
              <ArticleContent content={article.content} />
            ) : (
              <p className="text-slate-600">No content available for this article.</p>
            )}
          </div>

          {/* Source attribution */}
          {(seo.source_name || seo.source_url) && (
            <div className="mb-8 rounded-lg border border-slate-200 bg-slate-50 p-4">
              <p className="text-sm text-slate-600">
                Originally reported by{' '}
                {seo.source_url ? (
                  <a
                    href={seo.source_url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="inline-flex items-center gap-1 font-medium text-news-red hover:underline"
                  >
                    {seo.source_name || 'source'}
                    <ExternalLink className="h-3.5 w-3.5" />
                  </a>
                ) : (
                  <span className="font-medium">{seo.source_name}</span>
                )}
              </p>
            </div>
          )}

          {/* Article info */}
          <div className="mb-8 grid grid-cols-2 gap-4 rounded-lg border border-slate-200 bg-slate-50 p-6 text-sm sm:grid-cols-4">
            <div>
              <dt className="font-semibold text-slate-500">Category</dt>
              <dd className="mt-1 capitalize text-slate-900">{getCategoryLabel(category)}</dd>
            </div>
            <div>
              <dt className="font-semibold text-slate-500">Published</dt>
              <dd className="mt-1 text-slate-900">{formatDateTime(article.published_at)}</dd>
            </div>
            <div>
              <dt className="font-semibold text-slate-500">Fact-Check</dt>
              <dd className="mt-1 text-slate-900">
                {factScore ? `${(factScore * 100).toFixed(0)}%` : 'N/A'}
              </dd>
            </div>
            <div>
              <dt className="font-semibold text-slate-500">Views</dt>
              <dd className="mt-1 text-slate-900">{article.views_count ?? 0}</dd>
            </div>
          </div>

          {/* Keywords */}
          {seo.keywords && (
            <div className="mb-10">
              <h3 className="mb-3 text-sm font-bold uppercase tracking-wider text-slate-500">
                Tags
              </h3>
              <div className="flex flex-wrap gap-2">
                {seo.keywords.split(',').map((keyword) => (
                  <Link
                    key={keyword.trim()}
                    href={`/search?q=${encodeURIComponent(keyword.trim())}`}
                    className="rounded-full bg-slate-100 px-3 py-1 text-sm text-slate-700 hover:bg-slate-200"
                  >
                    #{keyword.trim()}
                  </Link>
                ))}
              </div>
            </div>
          )}

          <RelatedArticles articles={related} />

          <div className="mt-10">
            <NewsletterForm />
          </div>
        </div>
      </article>

      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{
          __html: JSON.stringify({
            '@context': 'https://schema.org',
            '@type': 'NewsArticle',
            headline: title,
            description: seo.meta_description,
            image: imageUrl,
            datePublished: article.published_at,
            dateModified: article.updated_at || article.published_at,
            author: { '@type': 'Organization', name: SITE.name },
            publisher: {
              '@type': 'Organization',
              name: SITE.name,
              logo: { '@type': 'ImageObject', url: `${siteUrl}/logo.png` },
            },
            mainEntityOfPage: { '@type': 'WebPage', '@id': `${siteUrl}/news/${article.slug}` },
          }),
        }}
      />
    </SiteLayout>
  );
}
