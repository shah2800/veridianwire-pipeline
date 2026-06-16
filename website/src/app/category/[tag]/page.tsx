import Link from 'next/link';
import { notFound } from 'next/navigation';
import { getPublishedArticles } from '@/lib/supabase';
import { SiteLayout } from '@/components/layout/SiteLayout';
import { ArticleCard } from '@/components/articles/ArticleCard';
import { EmptyState } from '@/components/ui/EmptyState';
import { getArticleCategory } from '@/lib/utils';
import { getCategoryLabel, CATEGORIES } from '@/lib/categories';
import { SITE } from '@/lib/site';
import { ChevronLeft } from 'lucide-react';

export const revalidate = 300;

type Props = { params: { tag: string } };

export async function generateStaticParams() {
  return CATEGORIES.map((cat) => ({ tag: cat.slug }));
}

export async function generateMetadata({ params }: Props) {
  const tag = decodeURIComponent(params.tag).toLowerCase();
  const label = getCategoryLabel(tag);
  return {
    title: `${label} News`,
    description: `Latest ${label.toLowerCase()} news and analysis from ${SITE.name}`,
  };
}

export default async function CategoryPage({ params }: Props) {
  const tag = decodeURIComponent(params.tag).toLowerCase();
  const validCategory = CATEGORIES.find((c) => c.slug === tag);

  if (!validCategory && tag !== 'news') {
    notFound();
  }

  const all = await getPublishedArticles(100);
  const articles = all.filter((a) => getArticleCategory(a).toLowerCase() === tag);
  const label = getCategoryLabel(tag);

  return (
    <SiteLayout>
      <div className="border-b border-slate-200 bg-slate-50">
        <div className="mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8">
          <Link
            href="/"
            className="mb-4 inline-flex items-center gap-1 text-sm font-medium text-news-red hover:underline"
          >
            <ChevronLeft className="h-4 w-4" />
            Home
          </Link>
          <h1 className="font-serif text-3xl font-bold text-slate-900 sm:text-4xl">
            {label} News
          </h1>
          {validCategory && (
            <p className="mt-2 text-lg text-slate-600">{validCategory.description}</p>
          )}
          <p className="mt-2 text-sm text-slate-500">
            {articles.length} article{articles.length !== 1 ? 's' : ''}
          </p>
        </div>
      </div>

      <div className="mx-auto max-w-7xl px-4 py-10 sm:px-6 lg:px-8">
        {articles.length === 0 ? (
          <EmptyState
            title={`No ${label.toLowerCase()} articles yet`}
            description="Stories in this section are updated as new coverage is published."
            actionLabel="Browse All News"
            actionHref="/"
          />
        ) : (
          <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
            {articles.map((article, i) => (
              <ArticleCard key={article.slug} article={article} priority={i < 3} />
            ))}
          </div>
        )}
      </div>
    </SiteLayout>
  );
}
