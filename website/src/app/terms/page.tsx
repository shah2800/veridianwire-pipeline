import { SiteLayout } from '@/components/layout/SiteLayout';
import { SITE } from '@/lib/site';

export const metadata = {
  title: 'Terms of Service',
  description: `Terms of service for ${SITE.name}`,
};

export default function TermsPage() {
  return (
    <SiteLayout>
      <div className="mx-auto max-w-3xl px-4 py-12 sm:px-6 lg:px-8">
        <h1 className="mb-8 font-serif text-4xl font-bold text-slate-900">Terms of Service</h1>
        <p className="mb-6 text-sm text-slate-500">Last updated: June 15, 2026</p>

        <div className="space-y-6">
          <section>
            <h2 className="text-xl font-bold text-slate-900">Acceptance of Terms</h2>
            <p className="text-slate-700">
              By accessing {SITE.name}, you agree to these terms. If you disagree, please do not
              use our service.
            </p>
          </section>
          <section>
            <h2 className="text-xl font-bold text-slate-900">Content Disclaimer</h2>
            <p className="text-slate-700">
              Articles are compiled and edited from third-party news sources. We make no warranties
              about accuracy, completeness, or timeliness. Content is provided for informational
              purposes only and does not constitute professional advice.
            </p>
          </section>
          <section>
            <h2 className="text-xl font-bold text-slate-900">Intellectual Property</h2>
            <p className="text-slate-700">
              Original reporting remains the property of respective source publishers. Our edited
              summaries constitute derivative editorial content. You may share article links freely;
              republication of full content requires attribution.
            </p>
          </section>
          <section>
            <h2 className="text-xl font-bold text-slate-900">User Accounts</h2>
            <p className="text-slate-700">
              You are responsible for maintaining account security. We reserve the right to
              suspend accounts that violate these terms or engage in abusive behavior.
            </p>
          </section>
          <section>
            <h2 className="text-xl font-bold text-slate-900">Limitation of Liability</h2>
            <p className="text-slate-700">
              {SITE.name} shall not be liable for any damages arising from use of our service or
              reliance on published content.
            </p>
          </section>
          <section>
            <h2 className="text-xl font-bold text-slate-900">Contact</h2>
            <p className="text-slate-700">
              Questions about these terms:{' '}
              <a href={`mailto:${SITE.email.legal}`} className="text-news-red hover:underline">
                {SITE.email.legal}
              </a>
            </p>
          </section>
        </div>
      </div>
    </SiteLayout>
  );
}
