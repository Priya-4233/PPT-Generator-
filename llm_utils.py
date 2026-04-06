import os
import json
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

load_dotenv(dotenv_path=".env")

api_key = os.getenv("HF_API_KEY")

if not api_key:
    raise ValueError("❌ HF_API_KEY missing in .env")

client = InferenceClient(token=api_key)


def safe_parse(text, fallback):
    try:
        text = text.strip().replace("```", "")
        return json.loads(text)
    except:
        return fallback


def generate_titles(topic: str):

    prompt = f"""
Create 5 slide titles for a beginner PPT on:
{topic}

Return ONLY JSON list:
["title1","title2","title3","title4","title5"]
"""

    res = client.chat.completions.create(
        model="meta-llama/Meta-Llama-3-8B-Instruct",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=300
    )

    return safe_parse(res.choices[0].message.content, [
        "Introduction",
        "What is AI",
        "How AI Works",
        "Applications",
        "Future of AI"
    ])


def generate_bullets(topic: str, title: str):

    prompt = f"""
Create 4-5 bullet points.

Topic: {topic}
Slide: {title}

Rules:
- beginner friendly
- context specific
- return ONLY JSON list

["point1","point2","point3"]
"""

    res = client.chat.completions.create(
        model="meta-llama/Meta-Llama-3-8B-Instruct",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=300
    )

    return safe_parse(res.choices[0].message.content, [
        f"{title} overview",
        "Key concept explanation",
        "Real-world example",
        "Important takeaway"
    ])