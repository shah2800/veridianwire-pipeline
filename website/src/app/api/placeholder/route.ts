import { NextRequest } from 'next/server';
import { SITE } from '@/lib/site';

const THEMES: Record<string, { from: string; to: string; accent: string; label: string }> = {
  technology: { from: '#0b1220', to: '#0e7490', accent: '#38bdf8', label: 'Technology' },
  business: { from: '#1c1917', to: '#a16207', accent: '#fbbf24', label: 'Business' },
  politics: { from: '#1e1b4b', to: '#9f1239', accent: '#fb7185', label: 'Politics' },
  science: { from: '#022c22', to: '#047857', accent: '#34d399', label: 'Science' },
  world: { from: '#172554', to: '#1d4ed8', accent: '#60a5fa', label: 'World' },
  health: { from: '#042f2e', to: '#0d9488', accent: '#2dd4bf', label: 'Health' },
  sports: { from: '#1a2e05', to: '#4d7c0f', accent: '#a3e635', label: 'Sports' },
  entertainment: { from: '#2e1065', to: '#7e22ce', accent: '#c084fc', label: 'Entertainment' },
  news: { from: '#0f172a', to: '#7f1d2e', accent: '#C41E3A', label: 'News' },
};

export async function GET(request: NextRequest) {
  const category = request.nextUrl.searchParams.get('category')?.toLowerCase() || 'news';
  const theme = THEMES[category] || THEMES.news;

  const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="630" viewBox="0 0 1200 630">
  <defs>
    <linearGradient id="g" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="${theme.from}"/>
      <stop offset="100%" stop-color="${theme.to}"/>
    </linearGradient>
    <radialGradient id="glow" cx="78%" cy="22%" r="60%">
      <stop offset="0%" stop-color="${theme.accent}" stop-opacity="0.45"/>
      <stop offset="100%" stop-color="${theme.accent}" stop-opacity="0"/>
    </radialGradient>
  </defs>
  <rect width="1200" height="630" fill="url(#g)"/>
  <rect width="1200" height="630" fill="url(#glow)"/>
  <g opacity="0.10" stroke="#ffffff" stroke-width="2" fill="none">
    <circle cx="980" cy="150" r="120"/>
    <circle cx="980" cy="150" r="200"/>
    <circle cx="980" cy="150" r="290"/>
  </g>
  <g opacity="0.07" fill="#ffffff">
    <rect x="120" y="250" width="520" height="22" rx="11"/>
    <rect x="120" y="300" width="430" height="22" rx="11"/>
    <rect x="120" y="350" width="480" height="22" rx="11"/>
  </g>
  <rect x="80" y="80" width="84" height="84" rx="14" fill="${SITE.initials ? '#C41E3A' : theme.accent}"/>
  <text x="122" y="138" font-family="Georgia,serif" font-size="40" font-weight="bold" fill="#ffffff" text-anchor="middle">${SITE.initials}</text>
  <text x="184" y="135" font-family="Georgia,serif" font-size="46" font-weight="bold" fill="#ffffff">${SITE.name}</text>
  <rect x="82" y="500" width="60" height="8" rx="4" fill="${theme.accent}"/>
  <text x="82" y="556" font-family="system-ui,Segoe UI,sans-serif" font-size="40" font-weight="700" fill="#ffffff" opacity="0.95">${theme.label}</text>
</svg>`;

  return new Response(svg, {
    headers: {
      'Content-Type': 'image/svg+xml',
      'Cache-Control': 'public, max-age=86400, immutable',
    },
  });
}
