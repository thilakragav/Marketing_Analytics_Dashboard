-- ============================================================
-- MARKETING PERFORMANCE DASHBOARD
-- PostgreSQL Table Definitions
-- ============================================================

-- ============================================================
-- 1. DAILY PAID MEDIA PERFORMANCE
-- ============================================================

DROP TABLE IF EXISTS paid_media_daily;

CREATE TABLE paid_media_daily (
    date DATE,
    campaign_id VARCHAR(50),
    platform VARCHAR(50),
    account_id VARCHAR(100),
    campaign_name VARCHAR(255),
    objective VARCHAR(100),

    spend NUMERIC(18,2),
    impressions BIGINT,
    reach BIGINT,
    clicks BIGINT,
    leads BIGINT,
    conversions BIGINT,
    conversion_value NUMERIC(18,2),

    currency VARCHAR(10),
    source_refresh_timestamp TIMESTAMP,

    ctr NUMERIC(12,2),
    cpc NUMERIC(18,2),
    cpm NUMERIC(18,2),
    conversion_rate NUMERIC(12,2),
    cpa NUMERIC(18,2),
    cpl NUMERIC(18,2),
    roas NUMERIC(18,4),
    roi NUMERIC(18,2),

    owner VARCHAR(100),
    budget_type VARCHAR(50),
    daily_budget NUMERIC(18,2),
    total_budget NUMERIC(18,2),
    approved_budget NUMERIC(18,2),

    target_conversions BIGINT,
    "target_CPA" NUMERIC(18,2),
    target_revenue NUMERIC(18,2),
    "target_ROAS" NUMERIC(18,4),

    start_date DATE,
    end_date DATE,

    budget_utilization NUMERIC(12,2),
    days_elapsed INTEGER,
    expected_spend_to_date NUMERIC(18,2),
    pacing_variance NUMERIC(18,2),
    forecast_spend NUMERIC(18,2),

    budget_status VARCHAR(50),
    roi_status VARCHAR(50)
);


-- ============================================================
-- 2. CAMPAIGN PERFORMANCE SUMMARY
-- ============================================================

DROP TABLE IF EXISTS campaign_performance;

CREATE TABLE campaign_performance (
    campaign_id VARCHAR(50),
    platform VARCHAR(50),
    account_id VARCHAR(100),
    campaign_name VARCHAR(255),
    objective VARCHAR(100),

    spend NUMERIC(18,2),
    impressions BIGINT,
    reach BIGINT,
    clicks BIGINT,
    leads BIGINT,
    conversions BIGINT,
    revenue NUMERIC(18,2),

    approved_budget NUMERIC(18,2),
    target_conversions BIGINT,
    target_cpa NUMERIC(18,2),
    target_revenue NUMERIC(18,2),
    target_roas NUMERIC(18,4),

    ctr NUMERIC(12,2),
    cpc NUMERIC(18,2),
    cpm NUMERIC(18,2),
    conversion_rate NUMERIC(12,2),
    cpa NUMERIC(18,2),
    cpl NUMERIC(18,2),
    roas NUMERIC(18,4),
    roi NUMERIC(18,2),

    budget_utilization NUMERIC(12,2)
);


-- ============================================================
-- INDEXES
-- ============================================================

CREATE INDEX idx_paid_media_date
ON paid_media_daily(date);

CREATE INDEX idx_paid_media_campaign
ON paid_media_daily(campaign_id);

CREATE INDEX idx_paid_media_platform
ON paid_media_daily(platform);

CREATE INDEX idx_campaign_performance_campaign
ON campaign_performance(campaign_id);

CREATE INDEX idx_campaign_performance_platform
ON campaign_performance(platform);