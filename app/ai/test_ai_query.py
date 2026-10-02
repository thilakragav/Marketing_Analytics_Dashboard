from app.ai.ai_query import ask_database


# ============================================================
# CMO EXECUTIVE SUMMARY AI TEST QUESTIONS
# ============================================================

questions = [
    "What is the total marketing spend?",
    "What is the overall ROAS?",
    "Which channel generated the most revenue?",
    "Which channel generated the most conversions?",
    "Which channel has the highest ROAS?",
    "Which campaign generated the highest revenue?",
    "Which campaigns are below their target ROAS?",
    "Which campaign has the lowest CPA?",
    "Show the daily spend trend for Google Ads.",
]


# ============================================================
# RUN TESTS
# ============================================================

for question in questions:

    print("\n" + "=" * 80)

    print("QUESTION:")
    print(question)

    try:

        result = ask_database(
            question=question,
            page_name="CMO Executive Summary"
        )

        print("\n" + "-" * 80)
        print("GENERATED SQL:")
        print("-" * 80)

        print(result["sql"])

        print("\n" + "-" * 80)
        print("DATABASE RESULT:")
        print("-" * 80)

        if result["data"].empty:
            print("No rows returned.")
        else:
            print(result["data"].to_string(index=False))

        print("\n" + "-" * 80)
        print("AI INSIGHT:")
        print("-" * 80)

        print(result["insight"])

    except Exception as e:

        print("\n" + "-" * 80)
        print("ERROR:")
        print("-" * 80)

        print(str(e))


# ============================================================
# COMPLETION MESSAGE
# ============================================================

print("\n" + "=" * 80)
print("CMO EXECUTIVE SUMMARY AI TESTING COMPLETED")
print("=" * 80)