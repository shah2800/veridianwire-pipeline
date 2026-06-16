import { NextRequest } from 'next/server';
import { SITE } from '@/lib/site';

const THEMES: Record<string, { bg: string; accent: string; label: string }> = {
  technology: { bg: '#0f172a', accent: '#38bdf8', label: 'Technology' },
  business: { bg: '#1c1917', accent: '#fbbf24', label: 'Business' },
  politics: { bg: '#1e1b4b', accent: '#f87171', label: 'Politics' },
  science: { bg: '#022c22', accent: '#34d399', label: 'Science' },
  world: { bg: '#172554', accent: '#60a5fa', label: 'World' },
  health: { bg: '#042f2e', accent: '#2dd4bf', label: 'Health' },
  news: { bg: '#1e293b', accent: '#C41E3A', label: 'News' },
};

export async function GET(request: NextRequest) {
  const category = request.nextUrl.searchParams.get('category')?.toLowerCase() || 'news';
  const theme = THEMES[category] || THEMES.news;

  const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="630" viewBox="0 0 1200 630">
  <defs>
    <linearGradient id="g" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:${theme.bg}"/>
      <stop offset="100%" style="stop-color:${theme.accent};stop-opacity:0.35"/>
    </linearGradient>
  </defs>
  <rect width="1200" height="630" fill="url(#g)"/>
  <rect x="60" y="60" width="80" height="80" rx="8" fill="${theme.accent}" opacity="0.9"/>
  <text x="100" y="115" font-family="Georgia,serif" font-size="36" font-weight="bold" fill="white" text-anchor="middle">${SITE.initials}</text>
  <text x="160" y="110" font-family="Georgia,serif" font-size="42" font-weight="bold" fill="white">${SITE.name}</text>
  <text x="60" y="520" font-family="system-ui,sans-serif" font-size="28" fill="white" opacity="0.85">${theme.label}</text>
  <line x1="60" y1="540" x2="300" y2="540" stroke="${theme.accent}" stroke-width="4"/>
</svg>`;

  return new Response(svg, {
    headers: {
      'Content-Type': 'image/svg+xml',
      'Cache-Control': 'public, max-age=86400, immutable',
    },
  });
}
