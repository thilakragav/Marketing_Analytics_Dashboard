from sql_validator import validate_sql


test_queries = [
    # Safe
    "SELECT COUNT(*) FROM gsc_daily_queries;",

    # Safe
    "SELECT SUM(clicks) FROM gsc_daily_queries;",

    # Unsafe
    "DELETE FROM gsc_daily_queries;",

    # Unsafe
    "DROP TABLE gsc_daily_queries;",

    # Unsafe
    "UPDATE gsc_daily_queries SET clicks = 0;",

    # Unsafe
    "SELECT COUNT(*) FROM gsc_daily_queries; DELETE FROM gsc_daily_queries;",
]


for query in test_queries:

    print("\n" + "=" * 70)
    print("SQL:")
    print(query)

    is_valid, result = validate_sql(query)

    print("\nVALID:", is_valid)
    print("RESULT:", result)