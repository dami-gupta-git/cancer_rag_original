import httpx
from typing import Any, Dict

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

async def get_civic(gene: str, alteration: str) -> Dict[str, Any]:
    """Fetch variant data from CIViC database using GraphQL API."""
    url = "https://civicdb.org/api/graphql"

    # GraphQL query to search for variant
    query = """
    query ($featureName: String!, $variantName: String!) {
      browseVariants(featureName: $featureName, variantName: $variantName, first: 5) {
        edges {
          node {
            id
            name
            variantTypes {
              name
            }
            evidenceItemCount
            diseases {
              name
            }
            therapies {
              name
            }
          }
        }
      }
    }
    """

    variables = {
        "featureName": gene,
        "variantName": alteration
    }

    async with httpx.AsyncClient(timeout=15.0) as client:
        r = await client.post(url, json={"query": query, "variables": variables})
        if r.status_code != 200:
            return {}

        data = r.json()
        edges = data.get("data", {}).get("browseVariants", {}).get("edges", [])

        if not edges:
            return {}

        # Find exact match (case-insensitive)
        variant_data = None
        for edge in edges:
            node = edge.get("node", {})
            if node.get("name", "").upper() == alteration.upper():
                variant_data = node
                break

        # If no exact match, use first result
        if not variant_data:
            variant_data = edges[0]["node"]

        # Extract relevant information
        result = {
            "variant_name": variant_data.get("name", ""),
            "variant_types": [vt.get("name") for vt in variant_data.get("variantTypes", [])],
            "evidence_count": variant_data.get("evidenceItemCount", 0),
            "diseases": [d.get("name") for d in variant_data.get("diseases", [])],
            "therapies": [t.get("name") for t in variant_data.get("therapies", [])]
        }

        return result