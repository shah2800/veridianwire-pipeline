import type { PublishedArticle, SeoMeta } from '@/types/article';
import { parseSeoMeta, getArticleCategory } from '@/lib/utils';
import { extractImageFromHtml } from '@/lib/content';

export interface ArticleMedia {
  imageUrl: string;
  videoUrl?: string;
  isPlaceholder: boolean;
}

const PLACEHOLDER_COLORS: Record<string, { bg: string; accent: string }> = {
  technology: { bg: '#0f172a', accent: '#38bdf8' },
  business: { bg: '#1c1917', accent: '#fbbf24' },
  politics: { bg: '#1e1b4b', accent: '#f87171' },
  science: { bg: '#022c22', accent: '#34d399' },
  world: { bg: '#172554', accent: '#60a5fa' },
  health: { bg: '#042f2e', accent: '#2dd4bf' },
  news: { bg: '#1e293b', accent: '#C41E3A' },
};

export function getPlaceholderPath(category: string): string {
  return `/api/placeholder?category=${encodeURIComponent(category.toLowerCase())}`;
}

export function resolveArticleMedia(article: PublishedArticle): ArticleMedia {
  const seo = parseSeoMeta(article) as SeoMeta & { video_url?: string };
  const category = getArticleCategory(article);

  let imageUrl = seo.image_url;
  if (!imageUrl && article.content) {
    imageUrl = extractImageFromHtml(article.content);
  }

  const videoUrl = seo.video_url;

  if (imageUrl) {
    return { imageUrl, videoUrl, isPlaceholder: false };
  }

  return {
    imageUrl: getPlaceholderPath(category),
    videoUrl,
    isPlaceholder: true,
  };
}

export function getYouTubeEmbedUrl(url: string): string | null {
  try {
    const u = new URL(url);
    if (u.hostname.includes('youtu.be')) {
      return `https://www.youtube.com/embed/${u.pathname.slice(1)}`;
    }
    if (u.hostname.includes('youtube.com')) {
      const id = u.searchParams.get('v');
      if (id) return `https://www.youtube.com/embed/${id}`;
    }
    if (u.hostname.includes('vimeo.com')) {
      const id = u.pathname.split('/').filter(Boolean).pop();
      if (id) return `https://player.vimeo.com/video/${id}`;
    }
  } catch {
    return null;
  }
  return null;
}

export { PLACEHOLDER_COLORS };
