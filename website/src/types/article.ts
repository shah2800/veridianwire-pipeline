export interface SeoMeta {
  meta_title?: string;
  meta_description?: string;
  keywords?: string;
  category?: string;
  fact_check_score?: number;
  image_url?: string;
  video_url?: string;
  source_name?: string;
  source_url?: string;
}

export interface PublishedArticle {
  id?: number;
  filtered_news_id?: number;
  url?: string;
  slug: string;
  content?: string;
  seo_meta?: SeoMeta | Record<string, string | number>;
  published_at?: string;
  created_at?: string;
  updated_at?: string;
  fact_check_score?: number;
  views_count?: number;
}

export interface UserProfile {
  id: string;
  email: string;
  full_name: string | null;
  avatar_url: string | null;
  role: 'user' | 'admin';
  created_at: string;
  updated_at: string;
}

export type CategorySlug =
  | 'technology'
  | 'business'
  | 'politics'
  | 'science'
  | 'world'
  | 'health'
  | 'sports'
  | 'news';

export interface Category {
  slug: CategorySlug;
  label: string;
  description: string;
}
