# POWERPOINT_NETWORKING_AGENT: Networking Strategy Deck Generator

## Purpose
Convert the networking strategy outline into a PowerPoint deck using the same visual format as the VC thesis deck.

## Output Format
Creates a PowerPoint deck with:
- Title slide
- 3 content slides (exactly 3 bullets each)
- Closing slide

## Usage

### Command Line
```bash
python agent.py "<sector>" [strategy_file]
```

Example:
```bash
python agent.py "B2B Fintech"
```

### Programmatic
```python
from agent import PowerPointNetworkingAgent

agent = PowerPointNetworkingAgent()
output_path = agent.run("B2B Fintech")
```

## Environment Variables
- `OPENAI_API_KEY`: Your OpenAI API key

## Dependencies
See `requirements.txt`

## Output
Results are saved to `../../Outputs/networking_strategy_{sector}_{timestamp}.pptx`
