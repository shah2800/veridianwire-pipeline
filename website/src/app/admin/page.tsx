import { redirect } from 'next/navigation';
import Link from 'next/link';
import { Activity, Database, FileText, AlertCircle, CheckCircle } from 'lucide-react';
import { createClient } from '@/lib/supabase-server';
import { getPipelineStats, getPublishedArticles } from '@/lib/supabase';
import { SiteLayout } from '@/components/layout/SiteLayout';
import { getArticleTitle, formatDateTime } from '@/lib/utils';

export const metadata = { title: 'Admin Panel' };

export default async function AdminPage() {
  const supabase = createClient();
  const { data: { user } } = await supabase.auth.getUser();

  if (!user) redirect('/login');

  const { data: profile } = await supabase
    .from('profiles')
    .select('role')
    .eq('id', user.id)
    .single();

  if (profile?.role !== 'admin') redirect('/dashboard');

  const [stats, recentArticles] = await Promise.all([
    getPipelineStats(),
    getPublishedArticles(10),
  ]);

  const successLogs = stats.recentLogs.filter((l) => l.status === 'success').length;
  const errorLogs = stats.recentLogs.filter((l) => l.status === 'error').length;

  return (
    <SiteLayout>
      <div className="mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8">
        <div className="mb-8">
          <h1 className="font-serif text-3xl font-bold text-slate-900">Admin Panel</h1>
          <p className="mt-1 text-slate-600">Pipeline monitoring and content overview</p>
        </div>

        {/* Stats */}
        <div className="mb-10 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
          <div className="rounded-xl border border-slate-200 bg-white p-6">
            <div className="flex items-center gap-3">
              <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-emerald-50">
                <FileText className="h-5 w-5 text-emerald-600" />
              </div>
              <div>
                <p className="text-2xl font-bold text-slate-900">{stats.totalArticles}</p>
                <p className="text-sm text-slate-500">Published Articles</p>
              </div>
            </div>
          </div>
          <div className="rounded-xl border border-slate-200 bg-white p-6">
            <div className="flex items-center gap-3">
              <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-sky-50">
                <Activity className="h-5 w-5 text-sky-600" />
              </div>
              <div>
                <p className="text-2xl font-bold text-slate-900">{stats.recentLogs.length}</p>
                <p className="text-sm text-slate-500">Recent Pipeline Events</p>
              </div>
            </div>
          </div>
          <div className="rounded-xl border border-slate-200 bg-white p-6">
            <div className="flex items-center gap-3">
              <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-emerald-50">
                <CheckCircle className="h-5 w-5 text-emerald-600" />
              </div>
              <div>
                <p className="text-2xl font-bold text-slate-900">{successLogs}</p>
                <p className="text-sm text-slate-500">Successful Events</p>
              </div>
            </div>
          </div>
          <div className="rounded-xl border border-slate-200 bg-white p-6">
            <div className="flex items-center gap-3">
              <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-red-50">
                <AlertCircle className="h-5 w-5 text-red-600" />
              </div>
              <div>
                <p className="text-2xl font-bold text-slate-900">{errorLogs}</p>
                <p className="text-sm text-slate-500">Error Events</p>
              </div>
            </div>
          </div>
        </div>

        <div className="grid gap-8 lg:grid-cols-2">
          {/* Pipeline logs */}
          <section className="rounded-xl border border-slate-200 bg-white">
            <div className="flex items-center gap-2 border-b border-slate-200 px-6 py-4">
              <Database className="h-5 w-5 text-slate-600" />
              <h2 className="font-semibold text-slate-900">Pipeline Logs</h2>
            </div>
            <div className="max-h-96 overflow-y-auto">
              {stats.recentLogs.length === 0 ? (
                <p className="p-6 text-sm text-slate-500">No pipeline logs yet.</p>
              ) : (
                <table className="w-full text-sm">
                  <thead className="sticky top-0 bg-slate-50">
                    <tr>
                      <th className="px-4 py-2 text-left font-medium text-slate-600">Stage</th>
                      <th className="px-4 py-2 text-left font-medium text-slate-600">Status</th>
                      <th className="px-4 py-2 text-left font-medium text-slate-600">Time</th>
                    </tr>
                  </thead>
                  <tbody>
                    {stats.recentLogs.map((log, i) => (
                      <tr key={i} className="border-t border-slate-100">
                        <td className="px-4 py-2 capitalize">{log.stage}</td>
                        <td className="px-4 py-2">
                          <span
                            className={
                              log.status === 'success'
                                ? 'text-emerald-600'
                                : log.status === 'error'
                                  ? 'text-red-600'
                                  : 'text-slate-600'
                            }
                          >
                            {log.status}
                          </span>
                        </td>
                        <td className="px-4 py-2 text-slate-500">
                          {formatDateTime(log.logged_at)}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              )}
            </div>
          </section>

          {/* Recent articles */}
          <section className="rounded-xl border border-slate-200 bg-white">
            <div className="flex items-center gap-2 border-b border-slate-200 px-6 py-4">
              <FileText className="h-5 w-5 text-slate-600" />
              <h2 className="font-semibold text-slate-900">Recent Publications</h2>
            </div>
            <div className="divide-y divide-slate-100">
              {recentArticles.length === 0 ? (
                <p className="p-6 text-sm text-slate-500">No articles published yet.</p>
              ) : (
                recentArticles.map((article) => (
                  <Link
                    key={article.slug}
                    href={`/news/${article.slug}`}
                    className="block px-6 py-3 hover:bg-slate-50"
                  >
                    <p className="line-clamp-1 font-medium text-slate-900">
                      {getArticleTitle(article)}
                    </p>
                    <p className="text-xs text-slate-500">
                      {formatDateTime(article.published_at)}
                    </p>
                  </Link>
                ))
              )}
            </div>
          </section>
        </div>
      </div>
    </SiteLayout>
  );
}
