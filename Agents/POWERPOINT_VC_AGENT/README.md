# POWERPOINT_VC_AGENT: PowerPoint Generator

## Purpose
Turns VC thesis markdown into a polished PowerPoint deck using a template.

## Workflow
1. Loads thesis markdown from Outputs folder
2. Parses markdown into sections (title, executive summary, 5 slides)
3. Loads PowerPoint template from Secrets/VC_DECK_TEMPLATE.pptx (if available)
4. Populates slides with parsed content
5. Saves as timestamped .pptx file

## Usage

### Command Line
```bash
python agent.py "<sector>" [thesis_file]
```

Examples:
```bash
# Use most recent thesis for sector
python agent.py "B2B Fintech"

# Use specific thesis file
python agent.py "B2B Fintech" "../Outputs/vc_thesis_b2b_fintech_20260126.md"
```

### Programmatic
```python
from agent import PowerPointAgent

agent = PowerPointAgent()
output_path = agent.run("B2B Fintech")
```

## Template
Place a PowerPoint template at `../../Secrets/VC_DECK_TEMPLATE.pptx` to use custom formatting.

If no template is found, a blank presentation is created.

## Output
PowerPoint file saved to `../../Outputs/vc_thesis_{sector}_{timestamp}.pptx`

## Features
- Automatically parses markdown sections
- Converts markdown bullets to PowerPoint bullets
- Removes markdown formatting (bold, italic, code)
- Creates title slide and content slides
- Preserves citations
