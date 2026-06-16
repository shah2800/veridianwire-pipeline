import { clsx, type ClassValue } from 'clsx';
import { twMerge } from 'tailwind-merge';
import type { PublishedArticle, SeoMeta } from '@/types/article';

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export function getSiteUrl(): string {
  return process.env.NEXT_PUBLIC_SITE_URL || 'http://localhost:3000';
}

export function parseSeoMeta(article: PublishedArticle): SeoMeta {
  const raw = article.seo_meta;
  if (!raw || typeof raw !== 'object') return {};
  return raw as SeoMeta;
}

export function getArticleTitle(article: PublishedArticle): string {
  const seo = parseSeoMeta(article);
  if (seo.meta_title) return seo.meta_title;
  return article.slug.replace(/-/g, ' ').replace(/\b\w/g, (c) => c.toUpperCase());
}

export function getArticleCategory(article: PublishedArticle): string {
  const seo = parseSeoMeta(article);
  return seo.category || 'news';
}

export function formatDate(dateStr?: string, style: 'short' | 'long' | 'relative' = 'long'): string {
  if (!dateStr) return 'Recently';
  const date = new Date(dateStr);
  if (Number.isNaN(date.getTime())) return 'Recently';

  if (style === 'relative') {
    const diff = Date.now() - date.getTime();
    const hours = Math.floor(diff / (1000 * 60 * 60));
    if (hours < 1) return 'Just now';
    if (hours < 24) return `${hours}h ago`;
    const days = Math.floor(hours / 24);
    if (days < 7) return `${days}d ago`;
  }

  if (style === 'short') {
    return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
  }

  return date.toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  });
}

export function formatDateTime(dateStr?: string): string {
  if (!dateStr) return 'Unknown';
  const date = new Date(dateStr);
  if (Number.isNaN(date.getTime())) return 'Unknown';
  return date.toLocaleString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: 'numeric',
    minute: '2-digit',
  });
}

export function getReadingTime(content?: string): number {
  if (!content) return 1;
  const text = content.replace(/<[^>]*>/g, ' ');
  const words = text.split(/\s+/).filter(Boolean).length;
  return Math.max(1, Math.ceil(words / 200));
}

export function getCategoryColor(category: string): string {
  const colors: Record<string, string> = {
    technology: 'bg-sky-100 text-sky-800',
    business: 'bg-amber-100 text-amber-900',
    politics: 'bg-rose-100 text-rose-800',
    science: 'bg-emerald-100 text-emerald-800',
    world: 'bg-blue-100 text-blue-800',
    health: 'bg-teal-100 text-teal-800',
    sports: 'bg-orange-100 text-orange-900',
    news: 'bg-slate-100 text-slate-800',
  };
  return colors[category.toLowerCase()] || colors.news;
}

export function slugify(text: string): string {
  return text
    .toLowerCase()
    .replace(/[^\w\s-]/g, '')
    .replace(/\s+/g, '-')
    .replace(/-+/g, '-')
    .trim();
}
