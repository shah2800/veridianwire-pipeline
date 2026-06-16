-- Website extensions: user profiles, newsletter, article views
-- Run in Supabase SQL Editor after DATABASE_SCHEMA.sql

-- User profiles (linked to Supabase Auth)
CREATE TABLE IF NOT EXISTS profiles (
    id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
    email TEXT NOT NULL,
    full_name TEXT,
    avatar_url TEXT,
    role TEXT DEFAULT 'user' CHECK (role IN ('user', 'admin')),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

ALTER TABLE profiles ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view own profile"
    ON profiles FOR SELECT
    USING (auth.uid() = id);

CREATE POLICY "Users can update own profile"
    ON profiles FOR UPDATE
    USING (auth.uid() = id);

CREATE POLICY "Users can insert own profile"
    ON profiles FOR INSERT
    WITH CHECK (auth.uid() = id);

-- Auto-create profile on signup
CREATE OR REPLACE FUNCTION public.handle_new_user()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO public.profiles (id, email, full_name, role)
    VALUES (
        NEW.id,
        NEW.email,
        NEW.raw_user_meta_data->>'full_name',
        'user'
    );
    RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

DROP TRIGGER IF EXISTS on_auth_user_created ON auth.users;
CREATE TRIGGER on_auth_user_created
    AFTER INSERT ON auth.users
    FOR EACH ROW EXECUTE FUNCTION public.handle_new_user();

-- Newsletter subscribers
CREATE TABLE IF NOT EXISTS newsletter_subscribers (
    id BIGSERIAL PRIMARY KEY,
    email TEXT UNIQUE NOT NULL,
    subscribed_at TIMESTAMPTZ DEFAULT NOW(),
    active BOOLEAN DEFAULT TRUE
);

ALTER TABLE newsletter_subscribers ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Anyone can subscribe"
    ON newsletter_subscribers FOR INSERT
    WITH CHECK (true);

-- Published articles: allow public read
ALTER TABLE published_articles ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "Public read published articles" ON published_articles;
CREATE POLICY "Public read published articles"
    ON published_articles FOR SELECT
    USING (true);

-- Pipeline logs: admin read only (via service key)
ALTER TABLE pipeline_logs ENABLE ROW LEVEL SECURITY;

-- Article views counter
ALTER TABLE published_articles ADD COLUMN IF NOT EXISTS views_count INTEGER DEFAULT 0;
ALTER TABLE published_articles ADD COLUMN IF NOT EXISTS updated_at TIMESTAMPTZ DEFAULT NOW();
ALTER TABLE published_articles ADD COLUMN IF NOT EXISTS fact_check_score FLOAT;

CREATE OR REPLACE FUNCTION increment_views(slug_param TEXT)
RETURNS VOID AS $$
BEGIN
    UPDATE published_articles
    SET views_count = COALESCE(views_count, 0) + 1
    WHERE slug = slug_param;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Grant anon access to increment views
GRANT EXECUTE ON FUNCTION increment_views(TEXT) TO anon, authenticated;

-- To make a user admin, run:
-- UPDATE profiles SET role = 'admin' WHERE email = 'your@email.com';
