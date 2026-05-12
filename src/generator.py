import os
import re

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"

if not OPENROUTER_API_KEY:
    raise ValueError("OPENROUTER_API_KEY is not set in environment variables.")

client = OpenAI(
    api_key=OPENROUTER_API_KEY,
    base_url=OPENROUTER_BASE_URL,
    timeout=90,
)


def clean_yaml_response(content: str) -> str:
    content = content.strip()

    if content.startswith("```"):
        content = re.sub(r"^```(?:yaml|yml)?\s*", "", content, flags=re.IGNORECASE)
        content = re.sub(r"\s*```$", "", content)

    openapi_index = content.find("openapi:")
    if openapi_index != -1:
        content = content[openapi_index:]

    return content.strip()


def generate_openapi(prompt: str, model: str) -> str:
    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        temperature=0,
        max_tokens=4000,
    )

    content = response.choices[0].message.content

    if not content:
        raise ValueError(f"Model {model} returned an empty response.")

    return clean_yaml_response(content)