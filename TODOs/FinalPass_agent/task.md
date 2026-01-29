# Task: FinalPass_agent

**Goal:** Inspect the PPTX from `POWERPOINT_VC_AGENT`, provide feedback, and produce a revised deck.

**Steps:**
1. Load PPTX.
2. Run checks (slide count, bullet point limit, citation presence, font consistency).
3. Output a markdown summary of suggested changes.
4. If changes required, generate a new PPTX and write to `Outputs/revised_{timestamp}.pptx`.
5. Return the revised file path for the Telegram bot.

**Next Steps:**
- Implement `review.py`.
- Write tests for checks.
- Integrate with the Telegram bot.
