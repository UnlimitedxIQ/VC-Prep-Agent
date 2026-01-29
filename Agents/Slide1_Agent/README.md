# Slide1_Agent: Emerging Trends of Interest

## Purpose
Gather data for emerging trends including market shifts, metrics, CAGR, business-model multipliers, and regulatory/technical inflection points.

## Output Format
The agent produces markdown with exactly 3 insights:

1. **The $X Shift**: Major market-level metric with date and source
2. **The Business Model Multiplier**: How the trend increases ARPU/retention/margins/distribution
3. **Regulatory / Platform / Technical Inflection**: The enabling change (law, standard, API, hardware, cost curve)

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
from agent import Slide1Agent

agent = Slide1Agent()
output_path = agent.run("B2B Fintech", "US")
```

## Environment Variables
- `OPENAI_API_KEY`: Your OpenAI API key
- `LANGCHAIN_API_KEY`: Your LangChain API key

## Dependencies
See `requirements.txt`

## Output
Results are saved to `../../Outputs/slide1_{sector}_{timestamp}.md`
