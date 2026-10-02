-- ============================================================
-- MARKETING PERFORMANCE DASHBOARD
-- ANALYTICS VIEWS
-- ============================================================


-- ============================================================
-- 1. OVERALL MARKETING KPI SUMMARY
-- ============================================================

CREATE OR REPLACE VIEW vw_marketing_kpi_summary AS

SELECT
    SUM(spend) AS total_spend,
    SUM(impressions) AS total_impressions,
    SUM(clicks) AS total_clicks,
    SUM(leads) AS total_leads,
    SUM(conversions) AS total_conversions,
    SUM(conversion_value) AS total_revenue,

    (
        SUM(clicks)::numeric
        / NULLIF(SUM(impressions)::numeric, 0)
        * 100
    )::numeric(18,2) AS ctr,

    (
        SUM(spend)::numeric
        / NULLIF(SUM(clicks)::numeric, 0)
    )::numeric(18,2) AS cpc,

    (
        SUM(spend)::numeric
        / NULLIF(SUM(impressions)::numeric, 0)
        * 1000
    )::numeric(18,2) AS cpm,

    (
        SUM(leads)::numeric
        / NULLIF(SUM(clicks)::numeric, 0)
        * 100
    )::numeric(18,2) AS lead_conversion_rate,

    (
        SUM(conversions)::numeric
        / NULLIF(SUM(clicks)::numeric, 0)
        * 100
    )::numeric(18,2) AS conversion_rate,

    (
        SUM(spend)::numeric
        / NULLIF(SUM(leads)::numeric, 0)
    )::numeric(18,2) AS cpl,

    (
        SUM(spend)::numeric
        / NULLIF(SUM(conversions)::numeric, 0)
    )::numeric(18,2) AS cpa,

    (
        SUM(conversion_value)::numeric
        / NULLIF(SUM(spend)::numeric, 0)
    )::numeric(18,2) AS roas,

    (
        (
            SUM(conversion_value)::numeric
            - SUM(spend)::numeric
        )
        / NULLIF(SUM(spend)::numeric, 0)
        * 100
    )::numeric(18,2) AS roi

FROM paid_media_daily;


-- ============================================================
-- 2. CHANNEL PERFORMANCE
-- ============================================================

CREATE OR REPLACE VIEW vw_channel_performance AS

SELECT
    platform,

    SUM(spend) AS spend,
    SUM(impressions) AS impressions,
    SUM(reach) AS reach,
    SUM(clicks) AS clicks,
    SUM(leads) AS leads,
    SUM(conversions) AS conversions,
    SUM(conversion_value) AS revenue,

    (
        SUM(clicks)::numeric
        / NULLIF(SUM(impressions)::numeric, 0)
        * 100
    )::numeric(18,2) AS ctr,

    (
        SUM(spend)::numeric
        / NULLIF(SUM(clicks)::numeric, 0)
    )::numeric(18,2) AS cpc,

    (
        SUM(spend)::numeric
        / NULLIF(SUM(impressions)::numeric, 0)
        * 1000
    )::numeric(18,2) AS cpm,

    (
        SUM(spend)::numeric
        / NULLIF(SUM(leads)::numeric, 0)
    )::numeric(18,2) AS cpl,

    (
        SUM(spend)::numeric
        / NULLIF(SUM(conversions)::numeric, 0)
    )::numeric(18,2) AS cpa,

    (
        SUM(conversion_value)::numeric
        / NULLIF(SUM(spend)::numeric, 0)
    )::numeric(18,2) AS roas,

    (
        (
            SUM(conversion_value)::numeric
            - SUM(spend)::numeric
        )
        / NULLIF(SUM(spend)::numeric, 0)
        * 100
    )::numeric(18,2) AS roi

FROM paid_media_daily

GROUP BY platform

ORDER BY spend DESC;


-- ============================================================
-- 3. DAILY PERFORMANCE TREND
-- ============================================================

CREATE OR REPLACE VIEW vw_daily_performance AS

SELECT
    date,

    SUM(spend) AS spend,
    SUM(impressions) AS impressions,
    SUM(clicks) AS clicks,
    SUM(leads) AS leads,
    SUM(conversions) AS conversions,
    SUM(conversion_value) AS revenue,

    (
        SUM(clicks)::numeric
        / NULLIF(SUM(impressions)::numeric, 0)
        * 100
    )::numeric(18,2) AS ctr,

    (
        SUM(conversion_value)::numeric
        / NULLIF(SUM(spend)::numeric, 0)
    )::numeric(18,2) AS roas

FROM paid_media_daily

GROUP BY date

ORDER BY date;


-- ============================================================
-- 4. CAMPAIGN PERFORMANCE
-- ============================================================

CREATE OR REPLACE VIEW vw_campaign_performance AS

SELECT
    campaign_id,
    platform,
    account_id,
    campaign_name,
    objective,
    spend,
    impressions,
    reach,
    clicks,
    leads,
    conversions,
    revenue,
    approved_budget,
    target_conversions,
    "target_CPA",
    target_revenue,
    "target_ROAS",
    ctr,
    cpc,
    cpm,
    conversion_rate,
    cpa,
    cpl,
    roas,
    roi,
    budget_utilization,

    CASE
        WHEN budget_utilization >= 100
            THEN 'Over Budget'
        WHEN budget_utilization >= 80
            THEN 'Near Budget'
        ELSE 'On Track'
    END AS budget_status,

    CASE
        WHEN roas >= "target_ROAS"
            THEN 'Target Met'
        ELSE 'Below Target'
    END AS roi_status

FROM campaign_performance;


-- ============================================================
-- 5. BUDGET PERFORMANCE
-- ============================================================

CREATE OR REPLACE VIEW vw_budget_performance AS

SELECT
    platform,

    SUM(approved_budget) AS approved_budget,

    SUM(spend) AS actual_spend,

    SUM(approved_budget) - SUM(spend)
        AS remaining_budget,

    (
        SUM(spend)::numeric
        / NULLIF(SUM(approved_budget)::numeric, 0)
        * 100
    )::numeric(18,2) AS budget_utilization,

    SUM(conversions) AS conversions,

    SUM(revenue) AS revenue,

    (
        SUM(revenue)::numeric
        / NULLIF(SUM(spend)::numeric, 0)
    )::numeric(18,2) AS roas,

    (
        (
            SUM(revenue)::numeric
            - SUM(spend)::numeric
        )
        / NULLIF(SUM(spend)::numeric, 0)
        * 100
    )::numeric(18,2) AS roi

FROM campaign_performance

GROUP BY platform

ORDER BY approved_budget DESC;