# Outline_NETWORKING_AGENT: Networking Strategy Compiler

## Purpose
Compile networking research into a 3-slide outline with exactly 3 bullets per slide.

## Output Format
The agent produces markdown with three sections:
1. **Target Profiles**
2. **Outreach Methods**
3. **Ethical Norms & Reputation**

Each section has exactly 3 bullets.

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
from agent import OutlineNetworkingAgent

agent = OutlineNetworkingAgent()
output_path = agent.run("B2B Fintech", "US")
```

## Environment Variables
- `OPENAI_API_KEY`: Your OpenAI API key
- `LANGCHAIN_API_KEY`: Your LangChain API key

## Dependencies
See `requirements.txt`

## Output
Results are saved to `../../Outputs/networking_strategy_{sector}_{timestamp}.md`
