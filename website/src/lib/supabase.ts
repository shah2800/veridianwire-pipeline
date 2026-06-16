import { createClient } from '@supabase/supabase-js';
import fs from 'fs';
import path from 'path';
import type { PublishedArticle } from '@/types/article';

const supabaseUrl =
  process.env.SUPABASE_URL || process.env.NEXT_PUBLIC_SUPABASE_URL || '';
const supabaseKey =
  process.env.SUPABASE_SERVICE_KEY ||
  process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY ||
  '';

if (!supabaseUrl || !supabaseKey) {
  console.warn('Supabase environment variables not configured');
}

export const supabase = createClient(supabaseUrl, supabaseKey);

function getFallbackArticles(): PublishedArticle[] {
  try {
    const file = path.join(process.cwd(), 'public', 'fallback-articles.json');
    if (!fs.existsSync(file)) return [];
    const raw = fs.readFileSync(file, 'utf-8');
    return JSON.parse(raw) as PublishedArticle[];
  } catch {
    return [];
  }
}

export async function getPublishedArticles(limit = 50): Promise<PublishedArticle[]> {
  try {
    const { data, error } = await supabase
      .from('published_articles')
      .select('*')
      .order('published_at', { ascending: false })
      .limit(limit);

    if (!error && data && data.length > 0) {
      return data as PublishedArticle[];
    }
  } catch (err) {
    console.error('Error fetching articles:', err);
  }

  return getFallbackArticles().slice(0, limit);
}

export async function getArticleBySlug(slug: string): Promise<PublishedArticle | null> {
  try {
    const { data, error } = await supabase
      .from('published_articles')
      .select('*')
      .eq('slug', slug)
      .single();

    if (!error && data) {
      return data as PublishedArticle;
    }
  } catch (err) {
    console.error('Error fetching article:', err);
  }

  return getFallbackArticles().find((a) => a.slug === slug) ?? null;
}

export async function getArticlesByCategory(category: string, limit = 20): Promise<PublishedArticle[]> {
  try {
    const { data, error } = await supabase
      .from('published_articles')
      .select('*')
      .contains('seo_meta', { category })
      .order('published_at', { ascending: false })
      .limit(limit);

    if (!error && data && data.length > 0) {
      return data as PublishedArticle[];
    }
  } catch (err) {
    console.error('Error fetching articles by category:', err);
  }

  return getFallbackArticles()
    .filter((a) => {
      const seo = (a.seo_meta as Record<string, string>) || {};
      return (seo.category || 'news').toLowerCase() === category.toLowerCase();
    })
    .slice(0, limit);
}

export async function searchArticles(query: string, limit = 30): Promise<PublishedArticle[]> {
  const all = await getPublishedArticles(500);
  const q = query.toLowerCase().trim();
  if (!q) return all.slice(0, limit);

  return all
    .filter((article) => {
      const seo = (article.seo_meta as Record<string, string>) || {};
      const title = (seo.meta_title || article.slug).toLowerCase();
      const desc = (seo.meta_description || '').toLowerCase();
      const content = (article.content || '').toLowerCase();
      const category = (seo.category || '').toLowerCase();
      return (
        title.includes(q) ||
        desc.includes(q) ||
        content.includes(q) ||
        category.includes(q) ||
        article.slug.includes(q)
      );
    })
    .slice(0, limit);
}

export async function getRelatedArticles(
  slug: string,
  category: string,
  limit = 4
): Promise<PublishedArticle[]> {
  const articles = await getArticlesByCategory(category, limit + 5);
  return articles.filter((a) => a.slug !== slug).slice(0, limit);
}

export async function getPipelineStats(): Promise<{
  totalArticles: number;
  recentLogs: Array<{ stage: string; status: string; message: string; logged_at: string }>;
}> {
  const [articlesRes, logsRes] = await Promise.all([
    supabase.from('published_articles').select('id', { count: 'exact', head: true }),
    supabase
      .from('pipeline_logs')
      .select('stage, status, message, logged_at')
      .order('logged_at', { ascending: false })
      .limit(20),
  ]);

  return {
    totalArticles: articlesRes.count ?? getFallbackArticles().length,
    recentLogs: logsRes.data || [],
  };
}

export async function subscribeNewsletter(email: string): Promise<{ success: boolean; error?: string }> {
  const { error } = await supabase
    .from('newsletter_subscribers')
    .insert({ email, subscribed_at: new Date().toISOString() });

  if (error) {
    if (error.code === '23505') {
      return { success: true };
    }
    return { success: false, error: error.message };
  }

  return { success: true };
}
