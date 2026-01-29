# FinalPass_agent: PowerPoint Reviewer

## Purpose
Reviews PowerPoint deck produced by POWERPOINT_VC_AGENT, suggests improvements, and generates a revised version.

## Workflow
1. Loads PowerPoint presentation from Outputs folder
2. Extracts content from all slides
3. Uses GPT-4 to analyze presentation quality
4. Identifies issues with layout, content, typography, narrative flow
5. Applies improvements (currently adds analysis as speaker notes)
6. Saves reviewed version with "_reviewed" suffix
7. Generates analysis report as markdown

## Usage

### Command Line
```bash
python agent.py "<sector>" [pptx_file]
```

Examples:
```bash
# Review most recent presentation for sector
python agent.py "B2B Fintech"

# Review specific presentation
python agent.py "B2B Fintech" "../Outputs/vc_thesis_b2b_fintech_20260126.pptx"
```

### Programmatic
```python
from agent import FinalPassAgent

agent = FinalPassAgent()
reviewed_path, report_path = agent.run("B2B Fintech")
```

## Review Criteria
The agent analyzes:
1. **Slide Layout**: Crowding, information hierarchy, visual elements
2. **Content Quality**: Citations, claim specificity, formatting consistency
3. **Typography**: Font sizes, readability
4. **Narrative Flow**: Logical progression between slides
5. **Professional Polish**: Consistency, formatting standards

## Output
- Reviewed presentation: `vc_thesis_{sector}_{timestamp}_reviewed.pptx`
- Analysis report: `review_analysis_{sector}_{timestamp}.md`

## Environment Variables
- `OPENAI_API_KEY`: Your OpenAI API key
- `LANGCHAIN_API_KEY`: Your LangChain API key
