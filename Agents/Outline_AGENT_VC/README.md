# Outline_AGENT_VC: Thesis Compiler

## Purpose
Pulls industry research from Slide 1-5 agents, populates outline with data, and generates a complete VC thesis markdown document.

## Workflow
1. Loads research from all 5 slide agents (most recent files for the sector)
2. Uses LLM to compile research into cohesive narrative
3. Formats as professional thesis document
4. Saves complete thesis to Outputs folder

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
from agent import OutlineAgent

agent = OutlineAgent()
output_path = agent.run("B2B Fintech", "US")
```

## Prerequisites
Before running Outline_AGENT_VC, ensure you have research from all 5 slide agents:
- Slide1_Agent: Emerging trends
- Slide2_Agent: Taxonomy/ecosystem
- Slide3_Agent: Macro thesis
- Slide4_Agent: Company filters
- Slide5_Agent: Candidate companies

## Output
Complete VC thesis saved to `../../Outputs/vc_thesis_{sector}_{timestamp}.md`

The thesis includes:
- Executive summary
- All 5 slides' research organized
- Smooth narrative flow
- Professional formatting
- Methodology section
