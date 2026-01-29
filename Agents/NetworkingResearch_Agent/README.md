# NetworkingResearch_Agent: Networking Strategy Research

## Purpose
Research target profiles, outreach methods, and ethical norms for sourcing and evaluating VC deals in a specific sector and stage.

## Output Format
The agent produces markdown with three research sections:
1. **Target Profiles (Founders, Accelerators, Angels)**
2. **Outreach Methods (Events, LinkedIn, Warm Introductions)**
3. **Ethical Norms & Reputational Best Practices**

Each section includes 4-6 bullets with citations.

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
from agent import NetworkingResearchAgent

agent = NetworkingResearchAgent()
output_path = agent.run("B2B Fintech", "US")
```

## Environment Variables
- `OPENAI_API_KEY`: Your OpenAI API key
- `LANGCHAIN_API_KEY`: Your LangChain API key

## Dependencies
See `requirements.txt`

## Output
Results are saved to `../../Outputs/networking_research_{sector}_{timestamp}.md`
