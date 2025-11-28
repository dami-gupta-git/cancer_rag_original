import httpx
from typing import Any, Dict, List

async def get_oncokb(gene: str, alteration: str, tumor_type: str = "") -> Dict[str, Any]:
    url = "https://www.oncokb.org/api/v1/annotate/mutations/byProteinChange"
    params = {
        "hugoSymbol": gene,
        "alteration": alteration,
        "tumorType": tumor_type or "Cancer"
    }
    async with httpx.AsyncClient(timeout=10.0) as client:
        r = await client.get(url, params=params)
        return r.json() if r.status_code == 200 else {}

async def get_civic(gene: str, alteration: str) -> List[Dict[str, Any]]:
    url = f"https://civicdb.org/api/variants?gene={gene}&variant={alteration}"
    async with httpx.AsyncClient(timeout=10.0) as client:
        r = await client.get(url)
        data = r.json() if r.status_code == 200 else {}
        return data.get("records", [])[:3]