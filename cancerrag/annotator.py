
import asyncio
import json
import os
from openai import AsyncOpenAI
from cancerrag.databases import get_oncokb, get_civic, get_clinical_trials
from cancerrag.prompts import PROMPT

from dotenv import load_dotenv
load_dotenv()
client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))  

async def annotate(gene: str, alteration: str, tumor_type: str = "Cancer") -> dict:
    oncokb, civic, clinical_trials = await asyncio.gather(
        get_oncokb(gene, alteration, tumor_type),
        get_civic(gene, alteration),
        get_clinical_trials(gene, alteration, tumor_type)
    )

    # Summarize for prompt size
    oncokb_summary = oncokb.get("level", "No OncoKB data") if oncokb else "Not found"

    # Format CIViC evidence data
    if civic and civic.get("evidence_count", 0) > 0:
        civic_parts = [f"Evidence items: {civic.get('evidence_count')}"]

        if civic.get("diseases"):
            diseases = ", ".join(civic.get("diseases", [])[:5])
            civic_parts.append(f"Associated diseases: {diseases}")

        if civic.get("therapies"):
            therapies = ", ".join(civic.get("therapies", [])[:5])
            civic_parts.append(f"Associated therapies: {therapies}")

        if civic.get("variant_types"):
            types = ", ".join(civic.get("variant_types", []))
            civic_parts.append(f"Variant types: {types}")

        civic_summary = "\n".join(civic_parts)
    else:
        civic_summary = "No CIViC data"

    # Format Clinical Trials data
    if clinical_trials and clinical_trials.get("trial_count", 0) > 0:
        trials = clinical_trials.get("trials", [])
        trial_parts = [f"Active trials found: {clinical_trials.get('trial_count')}"]

        for trial in trials[:3]:  # Show top 3 trials
            trial_parts.append(f"- {trial.get('nct_id')}: {trial.get('title')} (Phase {trial.get('phase')})")

        clinical_trials_summary = "\n".join(trial_parts)
    else:
        clinical_trials_summary = "No active clinical trials found"

    response = await client.chat.completions.create(
        model="gpt-4o-mini",  # change to grok-beta / claude-3-5-sonnet / llama3.1:405b etc.
        messages=[{
            "role": "user",
            "content": PROMPT.format(
                gene=gene,
                alteration=alteration,
                tumor_type=tumor_type,
                oncokb_summary=oncokb_summary,
                civic_summary=civic_summary,
                clinical_trials_summary=clinical_trials_summary
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