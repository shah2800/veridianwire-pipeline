import Link from 'next/link';
import { SiteLayout } from '@/components/layout/SiteLayout';
import { Globe, Shield, PenLine, Newspaper } from 'lucide-react';
import { SITE } from '@/lib/site';

export const metadata = {
  title: 'About Us',
  description: `Learn about ${SITE.name} and our editorial standards`,
};

export default function AboutPage() {
  return (
    <SiteLayout>
      <div className="border-b border-slate-200 bg-slate-50">
        <div className="mx-auto max-w-4xl px-4 py-12 sm:px-6 lg:px-8">
          <h1 className="font-serif text-4xl font-bold text-slate-900">About {SITE.name}</h1>
          <p className="mt-4 text-xl text-slate-600">{SITE.tagline}</p>
        </div>
      </div>

      <div className="mx-auto max-w-4xl px-4 py-12 sm:px-6 lg:px-8">
        <section className="mb-12">
          <h2 className="mb-4 font-serif text-2xl font-bold text-slate-900">Our Mission</h2>
          <p className="leading-relaxed text-slate-700">
            {SITE.name} brings together breaking coverage from respected wire services and global
            newsrooms. We focus on clarity, speed, and context — so readers can stay informed on
            technology, business, politics, and world events without wading through noise.
          </p>
        </section>

        <section className="mb-12">
          <h2 className="mb-6 font-serif text-2xl font-bold text-slate-900">How We Work</h2>
          <div className="grid gap-6 sm:grid-cols-2">
            <div className="rounded-xl border border-slate-200 p-6">
              <Globe className="mb-3 h-8 w-8 text-news-red" />
              <h3 className="mb-2 font-bold text-slate-900">1. Source</h3>
              <p className="text-sm text-slate-600">
                Our desk monitors leading outlets — BBC, Reuters, AP, TechCrunch, and other trusted
                feeds — for stories that matter.
              </p>
            </div>
            <div className="rounded-xl border border-slate-200 p-6">
              <Shield className="mb-3 h-8 w-8 text-news-red" />
              <h3 className="mb-2 font-bold text-slate-900">2. Verify</h3>
              <p className="text-sm text-slate-600">
                Each story is checked for duplication, source credibility, and consistency with
                wire reports before it reaches our pages.
              </p>
            </div>
            <div className="rounded-xl border border-slate-200 p-6">
              <PenLine className="mb-3 h-8 w-8 text-news-red" />
              <h3 className="mb-2 font-bold text-slate-900">3. Edit</h3>
              <p className="text-sm text-slate-600">
                Copy is tightened for readability while preserving the facts reported by the
                original outlet.
              </p>
            </div>
            <div className="rounded-xl border border-slate-200 p-6">
              <Newspaper className="mb-3 h-8 w-8 text-news-red" />
              <h3 className="mb-2 font-bold text-slate-900">4. Publish</h3>
              <p className="text-sm text-slate-600">
                Stories go live with clear source links, categories, and structured data for search
                and sharing.
              </p>
            </div>
          </div>
        </section>

        <section
          id="editorial-standards"
          className="mb-12 rounded-xl border border-slate-200 bg-slate-50 p-8"
        >
          <h2 className="mb-4 font-serif text-2xl font-bold text-slate-900">Editorial Standards</h2>
          <p className="mb-4 leading-relaxed text-slate-700">
            We aggregate and edit reporting from licensed and publicly available news sources. Every
            article includes attribution to the original publisher where possible. For breaking or
            consequential news, we encourage readers to consult the source link for full context.
          </p>
          <p className="leading-relaxed text-slate-700">
            {SITE.name} does not publish opinion as news. Corrections can be requested at any time.
          </p>
        </section>

        <section>
          <h2 className="mb-4 font-serif text-2xl font-bold text-slate-900">Contact</h2>
          <p className="text-slate-700">
            Questions, tips, or corrections? Reach us at{' '}
            <a href={`mailto:${SITE.email.editor}`} className="text-news-red hover:underline">
              {SITE.email.editor}
            </a>
          </p>
          <div className="mt-6 flex gap-4">
            <Link href="/privacy" className="text-sm font-medium text-news-red hover:underline">
              Privacy Policy
            </Link>
            <Link href="/terms" className="text-sm font-medium text-news-red hover:underline">
              Terms of Service
            </Link>
          </div>
        </section>
      </div>
    </SiteLayout>
  );
}
