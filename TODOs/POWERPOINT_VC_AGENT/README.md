# POWERPOINT_VC_AGENT

## Purpose
Generate a professional PowerPoint (pptx) presentation from the VC thesis outline produced by the Telegram bot.

## Workflow
1. **Input** – Receives the markdown thesis file (one per slide) from the `TelegramVCBot`.
2. **Slide Builder** – Parses the outline into slide objects.
3. **Layout Engine** – Uses a template (e.g., “VC Pitch Deck” PowerPoint template) and populates each slide with titles, bullet points, charts, and citations.
4. **Export** – Saves the presentation as `vc_thesis_{timestamp}.pptx` in the output folder.
5. **Logging** – Records any formatting warnings (e.g., too many bullet points, missing citations).

## Dependencies
- python‑pptx or an equivalent library for PowerPoint manipulation.
- A predefined .pptx template stored in `Secrets/VC_DECK_TEMPLATE.pptx`.

## Next Steps
- Create `build.py` to orchestrate the process.
- Write a simple parser to convert markdown sections into slide content.
- Implement a unit test suite.
- Prepare the final script to be called by the Telegram bot.

## Output
A single `.pptx` file ready for download or distribution.
