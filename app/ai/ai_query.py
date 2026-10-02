from app.ai.db_client import run_query
from app.ai.sql_generator import generate_sql
from app.ai.sql_validator import validate_sql
from app.ai.insight_generator import generate_insight
from app.ai.question_router import route_question


def ask_database(question: str, page_name: str, active_filters: dict = None):
    """
    Process a natural-language marketing question through:

    Question
        ↓
    Question Router
        ↓
    Page Context + Active Filters
        ↓
    SQL Generator
        ↓
    SQL Validator
        ↓
    PostgreSQL
        ↓
    AI Insight
    """

    # ============================================================
    # 1. ROUTE QUESTION
    # ============================================================

    routed_page = route_question(
        question=question,
        current_page=page_name,
    )

    # ============================================================
    # 2. GENERATE PAGE-AWARE SQL WITH ACTIVE FILTERS
    # ============================================================

    sql = generate_sql(
        user_question=question,
        page_name=routed_page,
        active_filters=active_filters,
    )


    # ============================================================
    # 3. VALIDATE SQL
    # ============================================================

    is_valid, result = validate_sql(sql)

    if not is_valid:
        raise ValueError(
            f"Unsafe SQL generated: {result}"
        )

    safe_sql = result

    # ============================================================
    # 4. EXECUTE SQL
    # ============================================================

    data = run_query(safe_sql)

    # ============================================================
    # 5. GENERATE AI INSIGHT
    # ============================================================

    insight = generate_insight(
        question=question,
        sql=safe_sql,
        result=data.to_string(index=False),
    )

    # ============================================================
    # 6. RETURN RESULT
    # ============================================================

    return {
        "question": question,
        "page_name": routed_page,
        "sql": safe_sql,
        "data": data,
        "insight": insight,
        "active_filters": active_filters,
    }