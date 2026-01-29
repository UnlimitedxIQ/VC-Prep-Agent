# Task: POWERPOINT_VC_AGENT

**Goal:** Turn the VC thesis markdown into a polished PowerPoint deck.

**Steps:**
1. Read the thesis file from `Outputs/`.
2. Parse each slide’s markdown.
3. Load the template PPTX from `Secrets/VC_DECK_TEMPLATE.pptx`.
4. Populate slides with titles, bullet points, citations.
5. Save the deck as `vc_thesis_{timestamp}.pptx`.
6. Return the file path for the next agent.

**Next Steps:**
- Implement `build.py`.
- Write tests.
- Integrate with the Telegram bot.
