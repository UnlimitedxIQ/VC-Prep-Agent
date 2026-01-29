# FinalPass_agent

## Purpose
Review the PowerPoint deck produced by `POWERPOINT_VC_AGENT`, suggest improvements, and pass the revised deck back to the original agent for re‑generation.

## Workflow
1. **Input** – Accepts a `.pptx` file from `POWERPOINT_VC_AGENT`.
2. **Analysis** – Uses a PowerPoint parsing library to extract slide content.
3. **Feedback** – Generates a list of suggested changes (e.g., slide layout, font size, missing citations, over‑crowding).
4. **Revision** – If requested, forwards the suggestions to `POWERPOINT_VC_AGENT` which updates the deck and re‑exports.
5. **Output** – Provides the final revised `.pptx` to the Telegram bot for delivery.

## Dependencies
- python‑pptx (or similar) for reading/writing slides.
- Natural language processing library for summarizing suggestions.

## Next Steps
- Create `review.py` to analyze the deck.
- Implement a simple rule‑based system for formatting checks.
- Write unit tests.

## Output
A revised `.pptx` file with all suggested improvements applied.
