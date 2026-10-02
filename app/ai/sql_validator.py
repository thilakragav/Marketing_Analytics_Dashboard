import re


FORBIDDEN_KEYWORDS = [
    "INSERT",
    "UPDATE",
    "DELETE",
    "DROP",
    "ALTER",
    "TRUNCATE",
    "CREATE",
    "GRANT",
    "REVOKE",
]


def validate_sql(sql: str) -> tuple[bool, str]:
    """
    Validate AI-generated SQL before execution.

    Returns:
        (True, cleaned_sql) if safe
        (False, reason) if unsafe
    """

    if not sql or not sql.strip():
        return False, "SQL query is empty."

    # Remove markdown code fences if the LLM accidentally adds them
    cleaned_sql = sql.strip()

    cleaned_sql = re.sub(
        r"^```(?:sql)?\s*",
        "",
        cleaned_sql,
        flags=re.IGNORECASE,
    )

    cleaned_sql = re.sub(
        r"\s*```$",
        "",
        cleaned_sql,
        flags=re.IGNORECASE,
    )

    cleaned_sql = cleaned_sql.strip()

    # Only SELECT queries are allowed
    if not re.match(r"^SELECT\b", cleaned_sql, re.IGNORECASE):
        return False, "Only SELECT queries are allowed."

    # Block multiple statements
    statements = [
        statement.strip()
        for statement in cleaned_sql.split(";")
        if statement.strip()
    ]

    if len(statements) > 1:
        return False, "Multiple SQL statements are not allowed."

    # Check forbidden SQL commands
    for keyword in FORBIDDEN_KEYWORDS:

        pattern = rf"\b{keyword}\b"

        if re.search(pattern, cleaned_sql, re.IGNORECASE):
            return False, f"Forbidden SQL keyword detected: {keyword}"

    return True, cleaned_sql