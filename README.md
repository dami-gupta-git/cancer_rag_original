# CancerRAG

**LLM-powered cancer variant annotation with real-time clinical evidence**

CancerRAG combines the power of Large Language Models with clinical databases (OncoKB and CIViC) to provide rapid, evidence-based interpretation of cancer genetic variants. Designed for clinicians, researchers, and bioinformaticians who need quick, contextual analysis of cancer mutations.

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Features

- **Real-time Evidence Retrieval**: Fetches variant data from OncoKB and CIViC databases in parallel
- **LLM-Powered Analysis**: Uses GPT-4, Claude, Grok, or local models for intelligent interpretation
- **Structured Output**: Returns JSON with classification, evidence levels, and therapy recommendations
- **CLI Interface**: Simple command-line tool for rapid queries
- **Flexible LLM Support**: Works with OpenAI, Anthropic, Grok, or local LLMs via LiteLLM

## Quick Start

### Installation

```bash
pip install cancerrag
```

### Setup

Create a `.env` file in your project directory with your API key:

```bash
# For OpenAI (default)
OPENAI_API_KEY=sk-...

# For other providers, see Configuration section
```

### Usage

```bash
# Basic usage with default tumor type
cancerrag ALK EML4-ALK 

# Specify tumor type
cancerrag ALK EML4-ALK -t "Non-Small Cell Lung Cancer"
```

### Example Output

```json
{
  "gene": "ALK",
  "variant": "EML4-ALK",
  "classification": "Unknown - not in curated databases",
  "highest_level_of_evidence": "None",
  "recommended_therapies": [],
  "summary": "The EML4-ALK fusion gene is a well-known driver mutation in non-small cell lung cancer (NSCLC), typically resulting from a chromosomal rearrangement between the EML4 gene and the ALK gene. This fusion is associated with sensitivity to ALK inhibitors such as crizotinib. However, the specific variant 'EML4-ALK' was not found in the CIViC or COSMIC databases, which raises uncertainty regarding its clinical significance and therapeutic implications. It is important to note that this analysis is based on inference and not validated clinical annotation. The absence of this variant in established databases suggests that it may not be well-characterized or recognized in the current literature, and further research would be necessary to determine its role in NSCLC.",
  "limitations": [
    "Variant not found in CIViC or COSMIC",
    "Analysis is LLM inference only"
  ],
  "_metadata": {
    "confidence": "inferred",
    "found_in_civic": false,
    "found_in_cosmic": false,
    "civic_evidence_count": 0,
    "cosmic_mutation_count": 0,
    "caveats": [
      "Variant not found in CIViC or COSMIC databases",
      "Analysis is LLM inference only - not validated clinical annotation"
    ]
  }
}

```

## Installation from Source

For development or customization:

```bash
# Clone the repository
git clone https://github.com/yourusername/CancerRAG.git
cd CancerRAG

# Install in editable mode
pip install -e .
```

## Configuration

### Using Different LLM Providers

CancerRAG supports multiple LLM providers. Edit [cancerrag/annotator.py](cancerrag/annotator.py) to configure your preferred model:

**OpenAI (default)**
```python
client = AsyncOpenAI()  # Uses OPENAI_API_KEY from .env
model = "gpt-4o-mini"
```

**Anthropic Claude**
```python
client = AsyncOpenAI(
    base_url="https://api.anthropic.com/v1",
    api_key=os.getenv("ANTHROPIC_API_KEY")
)
model = "claude-3-5-sonnet-20241022"
```

**xAI Grok**
```python
client = AsyncOpenAI(
    base_url="https://api.x.ai/v1",
    api_key=os.getenv("XAI_API_KEY")
)
model = "grok-beta"
```

**Local LLM (Ollama)**
```python
client = AsyncOpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"
)
model = "llama3.1:405b"
```

## Project Structure

```
CancerRAG/
├── cancerrag/
│   ├── __init__.py       # Package metadata
│   ├── cli.py            # Command-line interface (Typer)
│   ├── annotator.py      # Core annotation logic
│   ├── databases.py      # OncoKB & CIViC API clients
│   └── prompts.py        # LLM prompt templates
├── examples/
│   ├── egfr.json         # Example EGFR output
│   └── braf.json         # Example BRAF output
├── pyproject.toml        # Project configuration
└── README.md
```

## How It Works

1. **Input**: User provides gene symbol, variant, and optionally tumor type
2. **Data Retrieval**: Async HTTP requests fetch evidence from OncoKB and CIViC
3. **Summarization**: Evidence is condensed for efficient LLM processing
4. **LLM Analysis**: Prompt instructs LLM to act as a genomic pathologist
5. **Structured Output**: LLM returns JSON with classification and recommendations

## API Reference

### Command Line

```bash
cancerrag [GENE] [ALTERATION] [OPTIONS]

Arguments:
  GENE         Gene symbol (e.g., EGFR, BRAF, TP53)
  ALTERATION   Protein change (e.g., L858R, V600E)

Options:
  --tumor, -t  Tumor type (default: "Cancer")
  --help       Show help message
```

### Programmatic Usage

```python
import asyncio
from cancerrag.annotator import annotate

async def main():
    result = await annotate(
        gene="EGFR",
        alteration="L858R",
        tumor_type="Lung Adenocarcinoma"
    )
    print(result)

asyncio.run(main())
```

## Output Schema

```typescript
{
  "gene": string,                    // Gene symbol
  "variant": string,                 // Variant alteration
  "classification": string,          // Oncogenic | Likely Oncogenic | VUS | Benign
  "highest_level_of_evidence": string, // Level 1-4 or N/A
  "recommended_therapies": string[], // List of therapy names
  "summary": string                  // Plain-English explanation
}
```

## Data Sources

- **OncoKB**: Precision oncology knowledge base from Memorial Sloan Kettering
- **CIViC**: Clinical Interpretation of Variants in Cancer (community-curated)

## Development

### Running Tests

```bash
pytest
```

### Code Formatting

```bash
black cancerrag/
```

## Limitations

- **Not for Clinical Use**: This tool is for research and educational purposes only
- **LLM Hallucinations**: Always verify critical findings against primary sources
- **API Rate Limits**: OncoKB and CIViC have usage limits
- **Evidence Currency**: Database evidence may not reflect the latest research

## Roadmap

- [ ] Add ClinVar and COSMIC database integration
- [ ] Implement batch processing for VCF files
- [ ] Add evidence citation tracking
- [ ] Support multi-model comparison
- [ ] Generate PDF reports for tumor boards
- [ ] Add germline vs somatic variant handling

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License - see LICENSE file for details

## Citation

If you use CancerRAG in your research, please cite:

```bibtex
@software{cancerrag2025,
  author = {Gupta, Dami},
  title = {CancerRAG: LLM-powered cancer variant annotation},
  year = {2025},
  url = {https://github.com/dami-gupta-git/cancer_rag}
}
```

## Acknowledgments

- OncoKB API for precision oncology data
- CIViC for community-curated variant interpretations
- OpenAI, Anthropic, and xAI for LLM access

## Contact

For questions or support, please open an issue on GitHub or contact dami.gupta@gmail.com

---

**Disclaimer**: This tool is for research purposes only and should not be used as a substitute for professional medical advice, diagnosis, or treatment.
