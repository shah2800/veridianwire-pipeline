import Link from 'next/link';
import { Rss } from 'lucide-react';
import { CATEGORIES } from '@/lib/categories';
import { NewsletterForm } from '@/components/layout/NewsletterForm';
import { SITE } from '@/lib/site';

export function Footer() {
  const year = new Date().getFullYear();

  return (
    <footer className="mt-auto border-t border-slate-200 bg-slate-900 text-slate-300">
      <div className="mx-auto max-w-7xl px-4 py-12 sm:px-6 lg:px-8">
        <div className="grid gap-10 md:grid-cols-2 lg:grid-cols-4">
          <div>
            <div className="mb-4 flex items-center gap-2">
              <div className="flex h-9 w-9 items-center justify-center rounded-md bg-news-red">
                <span className="font-serif text-lg font-bold text-white">{SITE.initials}</span>
              </div>
              <span className="font-serif text-lg font-bold text-white">{SITE.name}</span>
            </div>
            <p className="mb-4 text-sm leading-relaxed text-slate-400">{SITE.description}</p>
            <Link
              href="/api/rss"
              className="inline-flex items-center gap-2 text-sm text-slate-400 hover:text-white"
            >
              <Rss className="h-4 w-4" />
              RSS Feed
            </Link>
          </div>

          <div>
            <h3 className="mb-4 text-sm font-bold uppercase tracking-wider text-white">
              Categories
            </h3>
            <ul className="space-y-2">
              {CATEGORIES.map((cat) => (
                <li key={cat.slug}>
                  <Link
                    href={`/category/${cat.slug}`}
                    className="text-sm text-slate-400 transition-colors hover:text-white"
                  >
                    {cat.label}
                  </Link>
                </li>
              ))}
            </ul>
          </div>

          <div>
            <h3 className="mb-4 text-sm font-bold uppercase tracking-wider text-white">
              Company
            </h3>
            <ul className="space-y-2">
              <li>
                <Link href="/about" className="text-sm text-slate-400 hover:text-white">
                  About Us
                </Link>
              </li>
              <li>
                <Link href="/privacy" className="text-sm text-slate-400 hover:text-white">
                  Privacy Policy
                </Link>
              </li>
              <li>
                <Link href="/terms" className="text-sm text-slate-400 hover:text-white">
                  Terms of Service
                </Link>
              </li>
              <li>
                <Link href="/search" className="text-sm text-slate-400 hover:text-white">
                  Search
                </Link>
              </li>
            </ul>
          </div>

          <div>
            <NewsletterForm />
          </div>
        </div>

        <div className="mt-10 flex flex-col items-center justify-between gap-4 border-t border-slate-800 pt-8 sm:flex-row">
          <p className="text-sm text-slate-500">
            © {year} {SITE.name}. All rights reserved.
          </p>
          <p className="text-xs text-slate-600">
            Stories are edited for clarity and sourced from established outlets.{' '}
            <Link href="/about#editorial-standards" className="underline hover:text-slate-400">
              Editorial standards
            </Link>
          </p>
        </div>
      </div>
    </footer>
  );
}
