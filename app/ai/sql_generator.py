from app.ai.llm_client import generate_response
from app.ai.context import get_page_context
import pandas as pd


SYSTEM_PROMPT = """
You are an expert marketing analytics SQL analyst.

Convert the user's question into ONE PostgreSQL SELECT query.

STRICT RULES:
1. Use only tables and columns provided in the page context.
2. Generate PostgreSQL-compatible SQL.
3. SELECT queries only.
4. Never generate INSERT, UPDATE, DELETE, DROP, ALTER, TRUNCATE,
   CREATE, GRANT, REVOKE, or other write operations.
5. Never invent tables or columns.
6. Do not use markdown code fences.
7. Return ONLY the SQL query.
8. Do not explain the query.
"""


def generate_sql(user_question: str, page_name: str, active_filters: dict = None) -> str:

    page_context = get_page_context(page_name)

    # Prevent oversized LLM requests.
    # Keep the page schema/context concise.
    MAX_CONTEXT_CHARS = 12000

    if len(page_context) > MAX_CONTEXT_CHARS:
        page_context = page_context[:MAX_CONTEXT_CHARS]

    filter_section = ""
    if active_filters:
        filter_lines = []
        if active_filters.get("start_date") and active_filters.get("end_date"):
            s_d = pd.to_datetime(active_filters["start_date"]).strftime("%Y-%m-%d")
            e_d = pd.to_datetime(active_filters["end_date"]).strftime("%Y-%m-%d")
            filter_lines.append(f"- Date Range: {s_d} to {e_d}")
        if active_filters.get("selected_channels"):
            filter_lines.append(f"- Marketing Channels / Platforms: {', '.join(active_filters['selected_channels'])}")
        if active_filters.get("selected_campaigns"):
            filter_lines.append(f"- Selected Campaigns: {', '.join(active_filters['selected_campaigns'])}")
        if active_filters.get("selected_objectives"):
            filter_lines.append(f"- Selected Objectives: {', '.join(active_filters['selected_objectives'])}")

        if filter_lines:
            filter_section = f"""
ACTIVE DASHBOARD FILTERS TO RESPECT:
{chr(10).join(filter_lines)}

CRITICAL FILTER APPLICATION RULES:
- ONLY apply a filter to a table if that table actually contains the required column.
- DO NOT invent WHERE date BETWEEN ... on tables like campaign_performance or vw_budget_performance that lack a date column!
- If the question asks for date-filtered performance, query paid_media_daily, ga4_daily_channel, or gsc_daily_queries which contain a date column.
- If filtering by platform, use WHERE platform IN (...) when supported.
"""

    prompt = f"""
PAGE:
{page_name}

AVAILABLE DATABASE CONTEXT:
{page_context}
{filter_section}
USER QUESTION:
{user_question}

Generate ONE PostgreSQL SELECT query that answers the question considering the active filters appropriately.

Return ONLY SQL.
"""

    sql = generate_response(
        prompt,
        system_prompt=SYSTEM_PROMPT
    )

    return sql.strip()