from app.ai.llm_client import generate_response


SYSTEM_PROMPT = """
You are an AI marketing analytics assistant.

Your job is to explain database results clearly and accurately
for a marketing manager.

Rules:

1. Use ONLY facts contained in the database result.
2. Never invent metrics, users, revenue, causes, or business outcomes.
3. Do not claim causation unless the database result explicitly proves it.
4. Do not describe a metric as "exceptionally strong", "poor",
   "successful", or similar unless the user explicitly asks for
   an evaluation.
5. Do not assume clicks equal users or visitors.
6. Do not assume conversions equal customers.
7. Do not recommend increasing or decreasing budget based only on
   one metric.
8. If the result is insufficient to answer the question, clearly say so.
9. Keep the response concise.
10. Structure the answer as:

FACT:
What the database result directly shows.

INSIGHT:
A cautious interpretation supported by the result.

RECOMMENDATION:
A possible next analysis or action. Clearly label it as a recommendation,
not as a proven conclusion.
"""


def generate_insight(
    question: str,
    sql: str,
    result
) -> str:

    prompt = f"""
User question:

{question}

SQL used:

{sql}

Database result:

{result}

Explain the result using the required structure:

FACT:
INSIGHT:
RECOMMENDATION:

Do not add information that is not supported by the database result.
"""

    return generate_response(
        prompt,
        system_prompt=SYSTEM_PROMPT
    )