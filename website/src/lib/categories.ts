import type { Category } from '@/types/article';

export const CATEGORIES: Category[] = [
  {
    slug: 'technology',
    label: 'Technology',
    description: 'AI, startups, gadgets, and digital innovation',
  },
  {
    slug: 'business',
    label: 'Business',
    description: 'Markets, finance, and corporate news',
  },
  {
    slug: 'politics',
    label: 'Politics',
    description: 'Policy, elections, and government',
  },
  {
    slug: 'science',
    label: 'Science',
    description: 'Research, space, and discoveries',
  },
  {
    slug: 'world',
    label: 'World',
    description: 'Global events and international affairs',
  },
  {
    slug: 'sports',
    label: 'Sports',
    description: 'Leagues, athletes, and game-day coverage',
  },
  {
    slug: 'health',
    label: 'Health',
    description: 'Medicine, wellness, and public health',
  },
];

export function getCategoryLabel(slug: string): string {
  const found = CATEGORIES.find((c) => c.slug === slug.toLowerCase());
  return found?.label || slug.charAt(0).toUpperCase() + slug.slice(1);
}
