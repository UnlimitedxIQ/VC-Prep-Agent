# TelegramVCBot: VC Thesis Orchestrator

## Purpose
Telegram chatbot that orchestrates all research agents (Slide 1-5, Outline, PowerPoint, FinalPass) to produce a complete VC industry thesis on-demand.

## Features
- Listen for `/vc <sector> [region]` commands
- Orchestrate all 8 agents in sequence
- Send progress updates via Telegram
- Deliver final thesis markdown, PowerPoint, and review analysis
- Error handling and logging
- Status checks

## Commands
- `/start` - Welcome message and instructions
- `/help` - Show help text
- `/status` - Check bot and agent status
- `/vc <sector> [region]` - Generate complete VC thesis

## Usage

### Setup
1. Create a Telegram bot via @BotFather
2. Add bot token to `.env` file:
   ```
   TELEGRAM_BOT_TOKEN=your_token_here
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Run Bot
```bash
python bot.py
```

The bot will start polling for messages. Send `/start` to begin.

### Example Usage
In Telegram:
```
/vc B2B Fintech US
```

The bot will:
1. Run all 5 research agents (Slide 1-5)
2. Compile thesis with Outline_AGENT_VC
3. Generate PowerPoint with POWERPOINT_VC_AGENT
4. Review with FinalPass_agent
5. Send you all files (thesis.md, deck.pptx, analysis.md)

Takes approximately 3-5 minutes.

## Architecture

### Pipeline Phases
1. **Phase 1**: Research (parallel execution of Slide 1-5 agents)
2. **Phase 2**: Compilation (Outline_AGENT_VC)
3. **Phase 3**: PowerPoint generation
4. **Phase 4**: Quality review and polish

### Error Handling
- Each phase has try/catch with logging
- Partial success: delivers available outputs even if later phases fail
- User receives error messages via Telegram

## Environment Variables
Required in `.env`:
- `TELEGRAM_BOT_TOKEN`: Bot token from @BotFather
- `OPENAI_API_KEY`: OpenAI API key
- `LANGCHAIN_API_KEY`: LangChain API key

## Deployment
For production deployment:
1. Use a process manager (systemd, PM2, supervisor)
2. Set up logging to file
3. Configure webhook instead of polling for better performance
4. Add user authentication/authorization
5. Implement rate limiting

## Logs
The bot logs all activities to console. In production, redirect to file:
```bash
python bot.py >> bot.log 2>&1
```
