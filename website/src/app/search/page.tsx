import Link from 'next/link';
import { Suspense } from 'react';
import { Search } from 'lucide-react';
import { searchArticles } from '@/lib/supabase';
import { SiteLayout } from '@/components/layout/SiteLayout';
import { ArticleCard } from '@/components/articles/ArticleCard';
import { SearchBar } from '@/components/search/SearchBar';
import { EmptyState } from '@/components/ui/EmptyState';

import { SITE } from '@/lib/site';

export const metadata = {
  title: 'Search',
  description: `Search ${SITE.name} for breaking news, politics, business, technology, and world coverage.`,
  robots: { index: true, follow: true },
};

type Props = { searchParams: { q?: string } };

async function SearchResults({ query }: { query: string }) {
  const articles = await searchArticles(query, 30);

  if (!query.trim()) {
    return (
      <EmptyState
        title="Search the news"
        description="Enter a keyword, topic, or headline to find articles across all categories."
        icon={<Search className="h-8 w-8" />}
      />
    );
  }

  if (articles.length === 0) {
    return (
      <EmptyState
        title={`No results for "${query}"`}
        description="Try different keywords or browse categories from the homepage."
        actionLabel="Browse All News"
        actionHref="/"
      />
    );
  }

  return (
    <>
      <p className="mb-6 text-sm text-slate-500">
        {articles.length} result{articles.length !== 1 ? 's' : ''} for &ldquo;{query}&rdquo;
      </p>
      <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
        {articles.map((article) => (
          <ArticleCard key={article.slug} article={article} />
        ))}
      </div>
    </>
  );
}

export default function SearchPage({ searchParams }: Props) {
  const query = searchParams.q || '';

  return (
    <SiteLayout>
      <div className="border-b border-slate-200 bg-slate-50">
        <div className="mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8">
          <h1 className="font-serif text-3xl font-bold text-slate-900">Search</h1>
          <div className="mt-4 max-w-xl">
            <SearchBar defaultValue={query} />
          </div>
        </div>
      </div>
      <div className="mx-auto max-w-7xl px-4 py-10 sm:px-6 lg:px-8">
        <Suspense
          fallback={
            <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
              {Array.from({ length: 6 }).map((_, i) => (
                <div key={i} className="h-64 animate-pulse rounded-lg bg-slate-100" />
              ))}
            </div>
          }
        >
          <SearchResults query={query} />
        </Suspense>
      </div>
    </SiteLayout>
  );
}
