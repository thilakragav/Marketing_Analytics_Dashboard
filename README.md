# Marketing Performance Dashboard

An end-to-end marketing analytics dashboard built with **Python, PostgreSQL, SQL, Pandas, Plotly, and Streamlit**.

The project combines data from multiple marketing channels into a centralized analytics platform for monitoring campaign performance, budget utilization, conversions, revenue, ROI, and SEO performance.

---

## 🚀 Project Overview

The Marketing Performance Dashboard provides a unified view of marketing performance across:

- Google Ads
- Meta Ads
- LinkedIn Ads
- GA4 Analytics
- Google Search Console / SEO
- Campaign Performance
- Budget and ROI
- Executive Marketing KPIs

The application uses PostgreSQL as the central analytical database and Streamlit as the dashboard interface.

---

## 🏗️ Architecture

```text
Marketing Data Sources
        │
        ├── Google Ads
        ├── Meta Ads
        ├── LinkedIn Ads
        ├── GA4
        └── Google Search Console
        │
        ▼
   Raw Data / CSV
        │
        ▼
 Data Ingestion Scripts
        │
        ▼
    PostgreSQL
        │
        ▼
 Data Transformation
        │
        ▼
 Analytics Tables / Views
        │
        ▼
 Streamlit Dashboard
        │
        ├── Executive Summary
        ├── Budget & ROI
        ├── Channel Performance
        ├── Google Ads
        ├── LinkedIn Ads
        ├── Meta Ads
        ├── GA4 Analytics
        └── SEO Performance