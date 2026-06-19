import Link from 'next/link';
import { ChevronLeft, ChevronRight, Newspaper } from 'lucide-react';
import { getPublishedArticlesPage } from '@/lib/supabase';
import { SiteLayout } from '@/components/layout/SiteLayout';
import { ArticleCard } from '@/components/articles/ArticleCard';
import { EmptyState } from '@/components/ui/EmptyState';
import { SITE } from '@/lib/site';

export const revalidate = 300;

export const metadata = {
  title: 'All News',
  description: `Browse every story published on ${SITE.name} — technology, business, politics, world, science, health, and sports.`,
  alternates: { canonical: '/news' },
  robots: { index: true, follow: true },
};

const PAGE_SIZE = 24;

type Props = { searchParams: { page?: string } };

export default async function AllNewsPage({ searchParams }: Props) {
  const page = Math.max(1, parseInt(searchParams.page || '1', 10) || 1);
  const { articles, total } = await getPublishedArticlesPage(page, PAGE_SIZE);
  const totalPages = Math.max(1, Math.ceil(total / PAGE_SIZE));

  return (
    <SiteLayout>
      <div className="border-b border-slate-200 bg-slate-50">
        <div className="mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8">
          <h1 className="flex items-center gap-2 font-serif text-3xl font-bold text-slate-900">
            <Newspaper className="h-7 w-7 text-news-red" />
            All News
          </h1>
          <p className="mt-2 text-sm text-slate-500">
            {total} stories · page {page} of {totalPages}
          </p>
        </div>
      </div>

      <div className="mx-auto max-w-7xl px-4 py-10 sm:px-6 lg:px-8">
        {articles.length === 0 ? (
          <EmptyState
            title="No articles yet"
            description="New stories publish throughout the day. Check back soon."
            actionLabel="Back to Home"
            actionHref="/"
          />
        ) : (
          <>
            <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
              {articles.map((article, i) => (
                <ArticleCard key={article.slug} article={article} priority={i < 3} />
              ))}
            </div>

            {/* Pagination */}
            <nav
              className="mt-12 flex items-center justify-between border-t border-slate-200 pt-6"
              aria-label="Pagination"
            >
              {page > 1 ? (
                <Link
                  href={`/news?page=${page - 1}`}
                  className="inline-flex items-center gap-1 rounded-md border border-slate-300 px-4 py-2 text-sm font-medium text-slate-700 hover:bg-slate-100"
                >
                  <ChevronLeft className="h-4 w-4" />
                  Previous
                </Link>
              ) : (
                <span className="inline-flex items-center gap-1 rounded-md border border-slate-200 px-4 py-2 text-sm font-medium text-slate-300">
                  <ChevronLeft className="h-4 w-4" />
                  Previous
                </span>
              )}

              <span className="text-sm text-slate-500">
                Page {page} of {totalPages}
              </span>

              {page < totalPages ? (
                <Link
                  href={`/news?page=${page + 1}`}
                  className="inline-flex items-center gap-1 rounded-md border border-slate-300 px-4 py-2 text-sm font-medium text-slate-700 hover:bg-slate-100"
                >
                  Next
                  <ChevronRight className="h-4 w-4" />
                </Link>
              ) : (
                <span className="inline-flex items-center gap-1 rounded-md border border-slate-200 px-4 py-2 text-sm font-medium text-slate-300">
                  Next
                  <ChevronRight className="h-4 w-4" />
                </span>
              )}
            </nav>
          </>
        )}
      </div>
    </SiteLayout>
  );
}
