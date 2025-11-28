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
    """Fetch variant data from CIViC database."""
    # Step 1: Get gene info (includes list of variants)
    gene_url = f"https://civicdb.org/api/genes/{gene}?identifier_type=entrez_symbol"
    
    async with httpx.AsyncClient(timeout=10.0) as client:
        r = await client.get(gene_url)
        if r.status_code != 200:
            return []
        
        gene_data = r.json()
        variants = gene_data.get("variants", [])
        
        # Step 2: Find matching variant(s) by name
        matching = []
        for v in variants:
            # Case-insensitive match
            if v.get("name", "").upper() == alteration.upper():
                # Step 3: Get full variant details
                variant_id = v.get("id")
                if variant_id:
                    detail_url = f"https://civicdb.org/api/variants/{variant_id}"
                    detail_r = await client.get(detail_url)
                    if detail_r.status_code == 200:
                        matching.append(detail_r.json())
        
        return matching[:3]