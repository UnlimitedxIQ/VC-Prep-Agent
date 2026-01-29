# GPTOSS VC Thesis Agent System

An intelligent multi-agent system for generating comprehensive venture capital industry theses on-demand.

## 🚀 What It Does

This system uses AI agents to research any industry sector and produce:
- **Complete VC Thesis** (markdown document)
- **PowerPoint Presentation** (professional deck)
- **Quality Review Analysis** (improvement recommendations)

All delivered automatically via Telegram bot in 3-5 minutes.

## 📁 Project Structure

```
GPTOSS_AGENTFILES/
├── Agents/               # All agent implementations
│   ├── Slide1_Agent/     # Emerging trends research
│   ├── Slide2_Agent/     # Ecosystem mapping
│   ├── Slide3_Agent/     # Macro thesis development
│   ├── Slide4_Agent/     # Investment filter definition
│   ├── Slide5_Agent/     # Company identification
│   ├── Outline_AGENT_VC/ # Thesis compilation
│   ├── POWERPOINT_VC_AGENT/ # Deck generation
│   ├── FinalPass_agent/  # Quality review
│   └── TelegramVCBot/    # Telegram orchestrator
├── Outputs/              # Generated theses and decks
├── Secrets/              # API keys and templates
│   ├── .env              # Environment variables
│   └── VC_DECK_TEMPLATE.pptx (optional)
├── SubAgents/            # Future sub-agents
└── TODOs/                # Task specifications

```

## ⚡ Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- LangChain and OpenAI libraries
- python-pptx for PowerPoint generation
- python-telegram-bot for Telegram interface

### 2. Configure API Keys

Edit `Secrets/.env`:

```bash
# Required
OPENAI_API_KEY=your_openai_api_key_here
LANGCHAIN_API_KEY=your_langchain_api_key_here

# Optional - for Telegram bot
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
```

**Where to get keys:**
- OpenAI: https://platform.openai.com/api-keys
- LangChain: https://smith.langchain.com/settings
- Telegram: Message @BotFather on Telegram

### 3. Run the System

#### Option A: Telegram Bot (Recommended)

```bash
cd Agents/TelegramVCBot
python bot.py
```

Then in Telegram, send:
```
/vc B2B Fintech US
```

#### Option B: Command Line (Individual Agents)

```bash
# Research phase
cd Agents/Slide1_Agent && python agent.py "B2B Fintech" "US"
cd ../Slide2_Agent && python agent.py "B2B Fintech" "US"
cd ../Slide3_Agent && python agent.py "B2B Fintech" "US"
cd ../Slide4_Agent && python agent.py "B2B Fintech" "US"
cd ../Slide5_Agent && python agent.py "B2B Fintech" "US"

# Compilation phase
cd ../Outline_AGENT_VC && python agent.py "B2B Fintech" "US"

# Presentation phase
cd ../POWERPOINT_VC_AGENT && python agent.py "B2B Fintech"

# Review phase
cd ../FinalPass_agent && python agent.py "B2B Fintech"
```

## 🎯 System Components

### Research Agents (Phase 1)
Generate structured research for each slide of the thesis:

1. **Slide1_Agent**: Emerging market trends, CAGR projections, inflection points
2. **Slide2_Agent**: 3-tier ecosystem stack (Core/Layer/Edge)
3. **Slide3_Agent**: Macro thesis with contrarian viewpoint
4. **Slide4_Agent**: Investment criteria and filters
5. **Slide5_Agent**: Candidate company identification

### Compilation Agent (Phase 2)
6. **Outline_AGENT_VC**: Aggregates all research into cohesive thesis document

### Presentation Agent (Phase 3)
7. **POWERPOINT_VC_AGENT**: Converts markdown thesis to PowerPoint deck

### Review Agent (Phase 4)
8. **FinalPass_agent**: Analyzes quality and suggests improvements

### Orchestrator (All Phases)
9. **TelegramVCBot**: Manages entire pipeline via Telegram commands

## 📊 Output Examples

After running the system for "B2B Fintech", you'll get:

```
Outputs/
├── slide1_b2b_fintech_20260126_143022.md
├── slide2_b2b_fintech_20260126_143045.md
├── slide3_b2b_fintech_20260126_143108.md
├── slide4_b2b_fintech_20260126_143131.md
├── slide5_b2b_fintech_20260126_143154.md
├── vc_thesis_b2b_fintech_20260126_143220.md
├── vc_thesis_b2b_fintech_20260126_143245.pptx
├── vc_thesis_b2b_fintech_20260126_143310_reviewed.pptx
└── review_analysis_b2b_fintech_20260126_143310.md
```

## 🔧 Configuration

### PowerPoint Template

For branded decks, add your template:
```
Secrets/VC_DECK_TEMPLATE.pptx
```

The system will use this template if present, otherwise creates a blank deck.

### Environment Variables

All configuration in `Secrets/.env`:

```bash
# Required API Keys
OPENAI_API_KEY=sk-proj-...
LANGCHAIN_API_KEY=lsv2_pt_...

# Optional Telegram
TELEGRAM_BOT_TOKEN=123456:ABC-DEF...

# LangChain Configuration
LANGCHAIN_TRACING_V2=true
LANGCHAIN_PROJECT=vc-thesis-agents
```

## 💰 Cost Estimates

Using GPT-4, approximate cost per thesis:
- Research agents (5x): $0.50
- Compilation: $0.20
- Review: $0.15
- **Total: ~$0.85 per complete thesis**

## ⏱️ Performance

- Single research agent: 30-60 seconds
- Complete pipeline: 3-5 minutes
- Research phase can be parallelized

## 🛠️ Troubleshooting

### "OpenAI API key not provided"
→ Check `Secrets/.env` file has `OPENAI_API_KEY` set

### "No research found for Slide X"
→ Run research agents (Slide 1-5) before Outline_AGENT_VC

### Telegram bot not responding
→ Verify `TELEGRAM_BOT_TOKEN` in `.env` and bot is running

### PowerPoint looks generic
→ Add custom template at `Secrets/VC_DECK_TEMPLATE.pptx`

## 📚 Documentation

- **System Overview**: `Agents/README.md`
- **Individual Agents**: Each agent folder has its own README
- **Task Specifications**: See `TODOs/` folder

## 🔐 Security

- Never commit `Secrets/.env` to version control
- API keys are loaded from environment only
- Keep `.env` file permissions restricted

## 🚧 Future Enhancements

Potential additions:
- Parallel execution of research agents
- Web interface alongside Telegram
- Custom output formats (Word, PDF)
- Integration with CRM/deal flow tools
- Historical thesis comparison
- Automated competitor analysis

## 📞 Support

For issues:
1. Check agent-specific README files
2. Review console logs
3. Verify API keys and internet connection
4. Check `Outputs/` for partial results

## 📄 License

Internal use only. Proprietary.

---

**Generated by**: GPTOSS Agent System
**Version**: 1.0
**Date**: January 26, 2026
