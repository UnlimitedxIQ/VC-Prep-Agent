# Slide2_Agent: Taxonomy and Ecosystem Map

## Purpose
Compile taxonomy and ecosystem map with 3-tier stack (Core, Layer, Edge), quantitative claims, and value-capture hypothesis.

## Output Format
The agent produces markdown with:

1. **The Core**: Foundational infrastructure, system of record, or primitive
2. **The Layer**: Orchestration, tooling, analytics (with quantitative claim if available)
3. **The Edge**: Distribution surfaces, workflow owners, vertical platforms
4. **Value Capture Hypothesis**: Where value accrues or moats form

## Usage

### Command Line
```bash
python agent.py "<sector>" "<region>"
```

Example:
```bash
python agent.py "B2B Fintech" "US"
```

### Programmatic
```python
from agent import Slide2Agent

agent = Slide2Agent()
output_path = agent.run("B2B Fintech", "US")
```

## Environment Variables
- `OPENAI_API_KEY`: Your OpenAI API key
- `LANGCHAIN_API_KEY`: Your LangChain API key

## Output
Results are saved to `../../Outputs/slide2_{sector}_{timestamp}.md`
