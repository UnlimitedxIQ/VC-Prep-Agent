# Task: Telegram VC Thesis Bot

**Goal:** Build a Telegram chatbot that, upon receiving a user‑defined niche or sector, orchestrates the existing research agents (Slide 1‑5) to gather data and produce a complete VC industry thesis.

**Key Features:**
- Listen for `/vc <sector> [region]` commands.
- For each slide, trigger the corresponding agent.
- Aggregate results into a markdown thesis.
- Return the final document via Telegram.
- Log progress and errors.

**Next Steps:**
1. Create `bot.py` with Telegram bot logic.
2. Integrate with the research agent folders.
3. Write tests for command parsing.
4. Prepare a deployment script.
