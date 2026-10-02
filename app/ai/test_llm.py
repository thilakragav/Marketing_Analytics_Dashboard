from llm_client import generate_response


response = generate_response(
    "Explain ROAS in simple terms for a marketing manager."
)

print("\nAI RESPONSE:\n")
print(response)