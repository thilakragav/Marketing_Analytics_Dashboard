from db_client import run_query


query = """
SELECT
    COUNT(*) AS total_rows
FROM gsc_daily_queries;
"""


result = run_query(query)

print("\nDATABASE TEST RESULT:\n")
print(result)