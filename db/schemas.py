"""SQL migration files for Supabase."""

MIGRATIONS = {
    "001_raw_news": """
    CREATE TABLE IF NOT EXISTS raw_news (
        id BIGSERIAL PRIMARY KEY,
        source VARCHAR(255) NOT NULL,
        url TEXT UNIQUE NOT NULL,
        title TEXT NOT NULL,
        content TEXT,
        published_at TIMESTAMPTZ,
        author VARCHAR(255),
        raw_json JSONB,
        fetched_at TIMESTAMPTZ DEFAULT NOW(),
        created_at TIMESTAMPTZ DEFAULT NOW()
    );
    CREATE INDEX idx_raw_news_source ON raw_news(source);
    CREATE INDEX idx_raw_news_url ON raw_news(url);
    """,
    
    "002_filtered_news": """
    CREATE TABLE IF NOT EXISTS filtered_news (
        id BIGSERIAL PRIMARY KEY,
        raw_news_id BIGINT REFERENCES raw_news(id) ON DELETE CASCADE,
        title TEXT NOT NULL,
        content TEXT,
        score FLOAT DEFAULT 0.5,
        dedup_hash VARCHAR(255) UNIQUE,
        embedding FLOAT8[],
        category VARCHAR(100),
        processed_at TIMESTAMPTZ DEFAULT NOW(),
        created_at TIMESTAMPTZ DEFAULT NOW()
    );
    CREATE INDEX idx_filtered_news_raw_news_id ON filtered_news(raw_news_id);
    CREATE INDEX idx_filtered_news_dedup ON filtered_news(dedup_hash);
    """,
    
    "003_published_articles": """
    CREATE TABLE IF NOT EXISTS published_articles (
        id BIGSERIAL PRIMARY KEY,
        filtered_news_id BIGINT REFERENCES filtered_news(id) ON DELETE CASCADE,
        url TEXT UNIQUE NOT NULL,
        slug VARCHAR(500) UNIQUE NOT NULL,
        content TEXT,
        seo_meta JSONB,
        tags TEXT[],
        published_at TIMESTAMPTZ DEFAULT NOW(),
        created_at TIMESTAMPTZ DEFAULT NOW()
    );
    CREATE INDEX idx_published_articles_slug ON published_articles(slug);
    CREATE INDEX idx_published_articles_published_at ON published_articles(published_at);
    """,
    
    "004_pipeline_logs": """
    CREATE TABLE IF NOT EXISTS pipeline_logs (
        id BIGSERIAL PRIMARY KEY,
        stage VARCHAR(100) NOT NULL,
        status VARCHAR(50) NOT NULL,
        message TEXT,
        error TEXT,
        details JSONB,
        timestamp TIMESTAMPTZ DEFAULT NOW()
    );
    CREATE INDEX idx_pipeline_logs_stage ON pipeline_logs(stage);
    CREATE INDEX idx_pipeline_logs_timestamp ON pipeline_logs(timestamp);
    """,
}

def apply_migrations(db):
    """Apply all migrations to database."""
    for migration_name, sql in MIGRATIONS.items():
        print(f"Applying {migration_name}...")
        db.execute(sql)
