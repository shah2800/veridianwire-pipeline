/** Public-facing site brand — single source of truth for name, copy, and contact. */
export const SITE = {
  name: 'Veridian Wire',
  namePrimary: 'Veridian',
  nameAccent: 'Wire',
  initials: 'VW',
  tagline: 'Breaking stories from trusted sources worldwide',
  banner: 'Fresh coverage, updated throughout the day',
  description:
    'Timely news and analysis on technology, business, politics, and world events from established wire services and global outlets.',
  aboutLink: 'About our editorial standards',
  keywords: ['news', 'breaking news', 'world news', 'technology', 'business', 'politics'],
  email: {
    editor: 'editor@veridianwire.com',
    legal: 'legal@veridianwire.com',
    privacy: 'privacy@veridianwire.com',
  },
} as const;

export function getSiteUrl(): string {
  return process.env.NEXT_PUBLIC_SITE_URL || 'http://localhost:3000';
}
