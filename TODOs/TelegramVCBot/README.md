# Telegram VC Thesis Bot

## Overview
This project is a Telegram bot that serves as an orchestrator for generating data‑driven VC industry theses. It accepts a user‑defined niche or sector via a Telegram command, then sequentially triggers the research agents (Slide 1‑5) to gather market data, build a taxonomy, formulate a macro thesis, define company filters, and identify candidate companies.

## How it works
1. **Telegram Integration** – Listens to messages from a specified Telegram bot token.
2. **Command Parsing** – Expects a command like `/vc <industry>` or `/vc <sector> [<region>]`.
3. **Orchestration** – For each slide, it spawns the corresponding research agent (`Slide1_Agent` … `Slide5_Agent`).
4. **Aggregation** – Once all agents finish, it compiles their example outputs into a single markdown document, ready to be turned into a slide deck.
5. **Feedback Loop** – If any agent fails, it informs the user and can retry.

## Next Steps
- Implement the Telegram bot handler (`bot.py`).
- Hook into the existing research agent directories.
- Add unit tests for command parsing.
- Deploy to a container or server with the bot token stored in `Secrets/telegram_token.env`.

## Usage
```text
/start vc fintech B2B
```
The bot will then build a VC thesis for the B2B fintech sector.
