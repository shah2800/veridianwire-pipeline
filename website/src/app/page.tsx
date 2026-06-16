import Link from 'next/link';
import { getPublishedArticles } from '@/lib/supabase';
import { SiteLayout } from '@/components/layout/SiteLayout';
import { FeaturedArticle } from '@/components/articles/FeaturedArticle';
import { ArticleCard } from '@/components/articles/ArticleCard';
import { EmptyState } from '@/components/ui/EmptyState';
import { NewsletterForm } from '@/components/layout/NewsletterForm';
import { CATEGORIES } from '@/lib/categories';
import { getArticleCategory } from '@/lib/utils';
import { SITE, getSiteUrl } from '@/lib/site';
import { TrendingUp, Zap } from 'lucide-react';

export const revalidate = 300;

export default async function HomePage() {
  const articles = await getPublishedArticles(50);
  const featured = articles[0];
  const latest = articles.slice(1, 7);
  const trending = articles.slice(7, 13);

  const categoryCounts = CATEGORIES.map((cat) => ({
    ...cat,
    count: articles.filter((a) => getArticleCategory(a) === cat.slug).length,
  })).filter((c) => c.count > 0);

  return (
    <SiteLayout>
      <div className="mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8">
        {articles.length === 0 ? (
          <EmptyState
            title="No published articles yet"
            description="New stories publish throughout the day. Check back soon for the latest coverage."
            actionLabel="About Us"
            actionHref="/about"
          />
        ) : (
          <>
            {/* Featured */}
            {featured && (
              <section className="mb-10">
                <FeaturedArticle article={featured} />
              </section>
            )}

            <div className="grid gap-10 lg:grid-cols-3">
              {/* Main grid */}
              <div className="lg:col-span-2">
                <div className="mb-6 flex items-center justify-between">
                  <h2 className="flex items-center gap-2 font-serif text-2xl font-bold text-slate-900">
                    <Zap className="h-5 w-5 text-news-red" />
                    Latest News
                  </h2>
                  <Link
                    href="/search"
                    className="text-sm font-semibold text-news-red hover:underline"
                  >
                    View all →
                  </Link>
                </div>
                <div className="grid gap-6 sm:grid-cols-2">
                  {latest.map((article, i) => (
                    <ArticleCard key={article.slug} article={article} priority={i < 2} />
                  ))}
                </div>
              </div>

              {/* Sidebar */}
              <aside className="space-y-8">
                <div>
                  <h2 className="mb-4 flex items-center gap-2 font-serif text-xl font-bold text-slate-900">
                    <TrendingUp className="h-5 w-5 text-news-red" />
                    Trending
                  </h2>
                  <div className="rounded-lg border border-slate-200 bg-white p-4">
                    {trending.length > 0 ? (
                      trending.map((article) => (
                        <ArticleCard key={article.slug} article={article} variant="horizontal" />
                      ))
                    ) : (
                      latest.slice(0, 4).map((article) => (
                        <ArticleCard key={article.slug} article={article} variant="horizontal" />
                      ))
                    )}
                  </div>
                </div>

                {categoryCounts.length > 0 && (
                  <div>
                    <h2 className="mb-4 font-serif text-xl font-bold text-slate-900">Topics</h2>
                    <div className="flex flex-wrap gap-2">
                      {categoryCounts.map((cat) => (
                        <Link
                          key={cat.slug}
                          href={`/category/${cat.slug}`}
                          className="rounded-full border border-slate-200 bg-white px-4 py-1.5 text-sm font-medium text-slate-700 transition-colors hover:border-news-red hover:text-news-red"
                        >
                          {cat.label}
                          <span className="ml-1.5 text-slate-400">({cat.count})</span>
                        </Link>
                      ))}
                    </div>
                  </div>
                )}

                <NewsletterForm />
              </aside>
            </div>
          </>
        )}
      </div>
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{
          __html: JSON.stringify({
            '@context': 'https://schema.org',
            '@type': 'WebSite',
            name: SITE.name,
            url: getSiteUrl(),
            description: SITE.description,
            potentialAction: {
              '@type': 'SearchAction',
              target: `${getSiteUrl()}/search?q={search_term_string}`,
              'query-input': 'required name=search_term_string',
            },
          }),
        }}
      />
    </SiteLayout>
  );
}
