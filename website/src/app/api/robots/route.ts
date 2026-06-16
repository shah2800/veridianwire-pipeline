import { SITE, getSiteUrl } from '@/lib/site';

export async function GET() {
  const base = getSiteUrl()
  const body = `User-agent: *
Allow: /
Disallow: /admin
Disallow: /dashboard
Disallow: /settings
Disallow: /login
Disallow: /signup

Sitemap: ${base}/api/sitemap
`
  return new Response(body, {
    headers: { 'Content-Type': 'text/plain' },
  })
}
