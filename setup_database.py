#!/usr/bin/env python3
"""Initialize Supabase database schema."""
import os
from dotenv import load_dotenv

load_dotenv()

def setup_database():
    """Create all required tables in Supabase."""
    from supabase import create_client

    url = os.getenv('SUPABASE_URL')
    key = os.getenv('SUPABASE_SERVICE_KEY')

    if not url or not key:
        print("ERROR: SUPABASE_URL and SUPABASE_SERVICE_KEY required in .env")
        return False

    client = create_client(url, key)

    print("Creating database tables...")

    # Table 1: raw_news (fetched articles)
    print("1. Creating raw_news table...")
    try:
        client.table('raw_news').select('id').limit(1).execute()
        print("   ✅ raw_news table exists")
    except:
        try:
            client.rpc('create_raw_news_table').execute()
        except:
            # Use direct SQL via supabase_admin
            sql = """
            CREATE TABLE IF NOT EXISTS raw_news (
                id BIGSERIAL PRIMARY KEY,
                source VARCHAR(255),
                url TEXT UNIQUE,
                title TEXT,
                content TEXT,
                published_at TIMESTAMP,
                author VARCHAR(255),
                fetched_at TIMESTAMP DEFAULT NOW(),
                created_at TIMESTAMP DEFAULT NOW()
            );
            CREATE INDEX IF NOT EXISTS idx_raw_news_source ON raw_news(source);
            CREATE INDEX IF NOT EXISTS idx_raw_news_published ON raw_news(published_at);
            """
            try:
                # Execute SQL directly via Supabase
                result = client.postgrest.execute(sql)
                print("   ✅ raw_news table created")
            except Exception as e:
                print(f"   ⚠️  raw_news: {e}")

    # Table 2: filtered_news (deduplicated articles)
    print("2. Creating filtered_news table...")
    try:
        client.table('filtered_news').select('id').limit(1).execute()
        print("   ✅ filtered_news table exists")
    except:
        sql = """
        CREATE TABLE IF NOT EXISTS filtered_news (
            id BIGSERIAL PRIMARY KEY,
            raw_news_id BIGINT REFERENCES raw_news(id),
            title TEXT,
            content TEXT,
            score FLOAT,
            dedup_hash VARCHAR(255) UNIQUE,
            is_duplicate BOOLEAN DEFAULT FALSE,
            filtered_at TIMESTAMP DEFAULT NOW(),
            created_at TIMESTAMP DEFAULT NOW()
        );
        CREATE INDEX IF NOT EXISTS idx_filtered_dedup ON filtered_news(dedup_hash);
        CREATE INDEX IF NOT EXISTS idx_filtered_score ON filtered_news(score);
        """
        try:
            result = client.postgrest.execute(sql)
            print("   ✅ filtered_news table created")
        except Exception as e:
            print(f"   ⚠️  filtered_news: {e}")

    # Table 3: published_articles (final articles)
    print("3. Creating published_articles table...")
    try:
        client.table('published_articles').select('id').limit(1).execute()
        print("   ✅ published_articles table exists")
    except:
        sql = """
        CREATE TABLE IF NOT EXISTS published_articles (
            id BIGSERIAL PRIMARY KEY,
            filtered_news_id BIGINT REFERENCES filtered_news(id),
            slug VARCHAR(500) UNIQUE,
            url TEXT,
            content TEXT,
            seo_meta JSONB,
            status VARCHAR(50) DEFAULT 'published',
            view_count INTEGER DEFAULT 0,
            published_at TIMESTAMP DEFAULT NOW(),
            created_at TIMESTAMP DEFAULT NOW()
        );
        CREATE INDEX IF NOT EXISTS idx_published_slug ON published_articles(slug);
        CREATE INDEX IF NOT EXISTS idx_published_status ON published_articles(status);
        """
        try:
            result = client.postgrest.execute(sql)
            print("   ✅ published_articles table created")
        except Exception as e:
            print(f"   ⚠️  published_articles: {e}")

    # Table 4: pipeline_logs (logging)
    print("4. Creating pipeline_logs table...")
    try:
        client.table('pipeline_logs').select('id').limit(1).execute()
        print("   ✅ pipeline_logs table exists")
    except:
        sql = """
        CREATE TABLE IF NOT EXISTS pipeline_logs (
            id BIGSERIAL PRIMARY KEY,
            stage VARCHAR(50),
            status VARCHAR(50),
            message TEXT,
            details JSONB,
            error TEXT,
            created_at TIMESTAMP DEFAULT NOW()
        );
        CREATE INDEX IF NOT EXISTS idx_logs_stage ON pipeline_logs(stage);
        CREATE INDEX IF NOT EXISTS idx_logs_created ON pipeline_logs(created_at);
        """
        try:
            result = client.postgrest.execute(sql)
            print("   ✅ pipeline_logs table created")
        except Exception as e:
            print(f"   ⚠️  pipeline_logs: {e}")

    print("\n✅ Database setup complete!")
    print("\nNow run: python start_daemon.py")
    return True

if __name__ == '__main__':
    try:
        setup_database()
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
