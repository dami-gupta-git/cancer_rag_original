
import asyncio
import json
import os
from openai import AsyncOpenAI
from .databases import get_oncokb, get_civic
from .prompts import PROMPT

from dotenv import load_dotenv
load_dotenv()
client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))  

async def annotate(gene: str, alteration: str, tumor_type: str = "Cancer") -> dict:
    oncokb, civic = await asyncio.gather(
        get_oncokb(gene, alteration, tumor_type),
        get_civic(gene, alteration)
    )

    # Summarize for prompt size
    oncokb_summary = oncokb.get("level", "No OncoKB data") if oncokb else "Not found"
    civic_summary = "; ".join([e.get("name", "") for e in civic]) if civic else "No CIViC data"

    response = await client.chat.completions.create(
        model="gpt-4o-mini",  # change to grok-beta / claude-3-5-sonnet / llama3.1:405b etc.
        messages=[{
            "role": "user",
            "content": PROMPT.format(
                gene=gene,
                alteration=alteration,
                tumor_type=tumor_type,
                oncokb_summary=oncokb_summary,
                civic_summary=civic_summary
            )
        }],
        temperature=0.1,
        max_tokens=500
    )

    raw = response.choices[0].message.content.strip()
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return {"error": "LLM returned invalid JSON", "raw_output": raw}