PROMPT = """
You are an expert cancer genomic pathologist.

Variant: {gene} {alteration}
Tumor type: {tumor_type}

Real evidence retrieved:
OncoKB → {oncokb_summary}
CIViC → {civic_summary}
Clinical Trials → {clinical_trials_summary}

Return ONLY valid JSON (no markdown, no extra text):

{{
  "gene": "{gene}",
  "variant": "{alteration}",
  "classification": "Oncogenic | Likely Oncogenic | VUS | Benign",
  "highest_level_of_evidence": "Level 1 | Level 2 | Level 3A | Level 4 | R1/R2 | No evidence",
  "recommended_therapies": [],
  "clinical_trials": [],
  "summary": "One-sentence plain-English explanation"
}}
"""