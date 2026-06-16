-- Autonomous News Business - Complete Database Schema
-- Run this in Supabase SQL Editor

-- Table 1: raw_news (all fetched articles)
CREATE TABLE IF NOT EXISTS raw_news (
    id BIGSERIAL PRIMARY KEY,
    source VARCHAR(255),
    url TEXT UNIQUE,
    title TEXT,
    content TEXT,
    published_at TIMESTAMP,
    author VARCHAR(255),
    raw_json JSONB DEFAULT '{}',
    fetched_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_raw_news_source ON raw_news(source);
CREATE INDEX IF NOT EXISTS idx_raw_news_url ON raw_news(url);
CREATE INDEX IF NOT EXISTS idx_raw_news_published ON raw_news(published_at);

-- Table 2: filtered_news (deduplicated articles)
CREATE TABLE IF NOT EXISTS filtered_news (
    id BIGSERIAL PRIMARY KEY,
    raw_news_id BIGINT REFERENCES raw_news(id) ON DELETE CASCADE,
    title TEXT,
    content TEXT,
    score FLOAT,
    dedup_hash VARCHAR(255) UNIQUE,
    processed_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_filtered_dedup ON filtered_news(dedup_hash);
CREATE INDEX IF NOT EXISTS idx_filtered_score ON filtered_news(score);
CREATE INDEX IF NOT EXISTS idx_filtered_raw_news ON filtered_news(raw_news_id);

-- Table 3: published_articles (final published articles)
CREATE TABLE IF NOT EXISTS published_articles (
    id BIGSERIAL PRIMARY KEY,
    filtered_news_id BIGINT REFERENCES filtered_news(id) ON DELETE CASCADE,
    url TEXT,
    slug VARCHAR(500) UNIQUE,
    content TEXT,
    seo_meta JSONB DEFAULT '{}',
    published_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_published_slug ON published_articles(slug);
CREATE INDEX IF NOT EXISTS idx_published_filtered ON published_articles(filtered_news_id);
CREATE INDEX IF NOT EXISTS idx_published_published ON published_articles(published_at);

-- Table 4: pipeline_logs (all pipeline events)
CREATE TABLE IF NOT EXISTS pipeline_logs (
    id BIGSERIAL PRIMARY KEY,
    stage VARCHAR(50),
    status VARCHAR(50),
    message TEXT,
    error TEXT,
    details JSONB DEFAULT '{}',
    logged_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_logs_stage ON pipeline_logs(stage);
CREATE INDEX IF NOT EXISTS idx_logs_status ON pipeline_logs(status);
CREATE INDEX IF NOT EXISTS idx_logs_logged ON pipeline_logs(logged_at);
