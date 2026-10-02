import streamlit as st
from groq import Groq


# Current Groq production model
MODEL_NAME = "openai/gpt-oss-120b"


def get_groq_client():
    """Create and return the Groq client."""

    api_key = st.secrets.get("GROQ_API_KEY", "")

    if not api_key:
        raise ValueError(
            "GROQ_API_KEY is not configured in .streamlit/secrets.toml"
        )

    return Groq(api_key=api_key)


def generate_response(
    user_prompt: str,
    system_prompt: str = "You are a helpful marketing analytics assistant.",
) -> str:
    """Send a prompt to the Groq LLM and return its response."""

    client = get_groq_client()

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": user_prompt,
            },
        ],
        temperature=0.2,
        max_completion_tokens=1000,
    )

    return response.choices[0].message.content