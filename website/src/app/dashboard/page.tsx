import Link from 'next/link';
import { redirect } from 'next/navigation';
import { Newspaper, Bookmark, Settings, Shield } from 'lucide-react';
import { createClient } from '@/lib/supabase-server';
import { getPublishedArticles } from '@/lib/supabase';
import { SiteLayout } from '@/components/layout/SiteLayout';
import { ArticleCard } from '@/components/articles/ArticleCard';
import { getArticleTitle } from '@/lib/utils';

export const metadata = {
  title: 'Dashboard',
};

export default async function DashboardPage() {
  const supabase = createClient();
  const { data: { user } } = await supabase.auth.getUser();

  if (!user) redirect('/login');

  const { data: profile } = await supabase
    .from('profiles')
    .select('*')
    .eq('id', user.id)
    .single();

  const articles = await getPublishedArticles(6);
  const displayName = profile?.full_name || user.user_metadata?.full_name || user.email?.split('@')[0];

  return (
    <SiteLayout>
      <div className="mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8">
        <div className="mb-8">
          <h1 className="font-serif text-3xl font-bold text-slate-900">
            Welcome back, {displayName}
          </h1>
          <p className="mt-1 text-slate-600">Your personalized news dashboard</p>
        </div>

        {/* Quick actions */}
        <div className="mb-10 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
          <Link
            href="/"
            className="flex items-center gap-4 rounded-xl border border-slate-200 bg-white p-5 transition-shadow hover:shadow-md"
          >
            <div className="flex h-12 w-12 items-center justify-center rounded-lg bg-red-50">
              <Newspaper className="h-6 w-6 text-news-red" />
            </div>
            <div>
              <p className="font-semibold text-slate-900">Latest News</p>
              <p className="text-sm text-slate-500">Browse all articles</p>
            </div>
          </Link>
          <Link
            href="/search"
            className="flex items-center gap-4 rounded-xl border border-slate-200 bg-white p-5 transition-shadow hover:shadow-md"
          >
            <div className="flex h-12 w-12 items-center justify-center rounded-lg bg-sky-50">
              <Bookmark className="h-6 w-6 text-sky-600" />
            </div>
            <div>
              <p className="font-semibold text-slate-900">Search</p>
              <p className="text-sm text-slate-500">Find specific topics</p>
            </div>
          </Link>
          <Link
            href="/settings"
            className="flex items-center gap-4 rounded-xl border border-slate-200 bg-white p-5 transition-shadow hover:shadow-md"
          >
            <div className="flex h-12 w-12 items-center justify-center rounded-lg bg-slate-100">
              <Settings className="h-6 w-6 text-slate-600" />
            </div>
            <div>
              <p className="font-semibold text-slate-900">Settings</p>
              <p className="text-sm text-slate-500">Manage your account</p>
            </div>
          </Link>
          {profile?.role === 'admin' && (
            <Link
              href="/admin"
              className="flex items-center gap-4 rounded-xl border border-slate-200 bg-white p-5 transition-shadow hover:shadow-md"
            >
              <div className="flex h-12 w-12 items-center justify-center rounded-lg bg-amber-50">
                <Shield className="h-6 w-6 text-amber-600" />
              </div>
              <div>
                <p className="font-semibold text-slate-900">Admin Panel</p>
                <p className="text-sm text-slate-500">Pipeline monitoring</p>
              </div>
            </Link>
          )}
        </div>

        {/* Recent articles */}
        <section>
          <h2 className="mb-6 font-serif text-2xl font-bold text-slate-900">Recent Articles</h2>
          {articles.length === 0 ? (
            <p className="text-slate-600">No articles published yet. The pipeline will populate this soon.</p>
          ) : (
            <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
              {articles.map((article) => (
                <ArticleCard key={article.slug} article={article} />
              ))}
            </div>
          )}
        </section>
      </div>
    </SiteLayout>
  );
}
