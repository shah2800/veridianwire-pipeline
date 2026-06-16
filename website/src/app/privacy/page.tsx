import { SiteLayout } from '@/components/layout/SiteLayout';
import { SITE } from '@/lib/site';

export const metadata = {
  title: 'Privacy Policy',
  description: `Privacy policy for ${SITE.name}`,
};

export default function PrivacyPage() {
  return (
    <SiteLayout>
      <div className="mx-auto max-w-3xl px-4 py-12 sm:px-6 lg:px-8">
        <h1 className="mb-8 font-serif text-4xl font-bold text-slate-900">Privacy Policy</h1>
        <p className="mb-6 text-sm text-slate-500">Last updated: June 15, 2026</p>

        <div className="prose prose-slate max-w-none space-y-6">
          <section>
            <h2 className="text-xl font-bold text-slate-900">Information We Collect</h2>
            <p className="text-slate-700">
              When you create an account, we collect your email address and name. If you subscribe
              to our newsletter, we store your email. We use cookies for authentication sessions.
              We do not sell personal data to third parties.
            </p>
          </section>
          <section>
            <h2 className="text-xl font-bold text-slate-900">How We Use Data</h2>
            <p className="text-slate-700">
              Account data is used to provide personalized features and manage your subscription.
              Newsletter emails are used solely to deliver news updates. Analytics may be collected
              in aggregate to improve our service.
            </p>
          </section>
          <section>
            <h2 className="text-xl font-bold text-slate-900">Data Storage</h2>
            <p className="text-slate-700">
              Data is stored securely via Supabase (PostgreSQL) with row-level security policies.
              Passwords are hashed and never stored in plain text.
            </p>
          </section>
          <section>
            <h2 className="text-xl font-bold text-slate-900">Your Rights</h2>
            <p className="text-slate-700">
              You may update or delete your account at any time via Settings. You may unsubscribe
              from newsletters via the link in any email. Contact us at{' '}
              <a href={`mailto:${SITE.email.privacy}`} className="text-news-red hover:underline">
                {SITE.email.privacy}
              </a>{' '}
              for data requests.
            </p>
          </section>
          <section>
            <h2 className="text-xl font-bold text-slate-900">Editorial Content</h2>
            <p className="text-slate-700">
              News articles are sourced from public and licensed outlets. We do not use your
              personal data to produce editorial content.
            </p>
          </section>
        </div>
      </div>
    </SiteLayout>
  );
}
