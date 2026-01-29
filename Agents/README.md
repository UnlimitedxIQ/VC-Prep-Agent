# GPTOSS VC Thesis Agents

A multi-agent system for generating complete venture capital industry theses on-demand.

## System Overview

This system uses 11 specialized agents to research, compile, and present VC industry theses and networking strategies:

### Research Agents (Slide 1-5)
1. **Slide1_Agent** - Emerging Trends of Interest
   - Market shifts, CAGR projections
   - Business model multipliers
   - Regulatory/technical inflection points

2. **Slide2_Agent** - Taxonomy and Ecosystem Map
   - 3-tier stack (Core, Layer, Edge)
   - Value capture hypothesis
   - Quantitative claims

3. **Slide3_Agent** - Macro-Market Thesis
   - Focus sub-segment
   - Contrarian opinion
   - Thought-leadership hook

4. **Slide4_Agent** - Company Profile Filters
   - Traction and growth metrics
   - Stickiness indicators
   - Stage and unit economics

5. **Slide5_Agent** - Candidate Companies
   - Core/Layer/Edge company mapping
   - Justifications and descriptors
   - Investment targets

### Networking Strategy Agents
9. **NetworkingResearch_Agent** - Networking Research
   - Target profiles (founders, accelerators, angels)
   - Outreach methods (events, LinkedIn, warm introductions)
   - Ethical norms and reputational best practices

10. **Outline_NETWORKING_AGENT** - Networking Strategy Compiler
    - Aggregates networking research
    - Produces 3-slide outline with 3 bullets each

11. **POWERPOINT_NETWORKING_AGENT** - Networking Strategy Deck Generator
    - Converts networking outline to PowerPoint
    - Uses same formatting as VC thesis deck

### Orchestration Agents
6. **Outline_AGENT_VC** - Thesis Compiler
   - Aggregates research from Slides 1-5
   - Creates cohesive markdown thesis
   - Professional formatting

7. **POWERPOINT_VC_AGENT** - Deck Generator
   - Converts thesis to PowerPoint
   - Uses template if available
   - Formats slides professionally

8. **FinalPass_agent** - Quality Reviewer
   - Analyzes presentation quality
   - Identifies improvement areas
   - Generates review report

### User Interface
12. **TelegramVCBot** - Telegram Orchestrator
   - Telegram bot interface
   - Orchestrates all agents
   - Delivers results to users

## Quick Start

### 1. Setup Environment

Install dependencies for all agents:

```bash
# Navigate to each agent folder and install
cd Slide1_Agent && pip install -r requirements.txt
cd ../Slide2_Agent && pip install -r requirements.txt
# ... repeat for all agents
```

Or create a master requirements file:
```bash
pip install langchain langchain-openai openai python-pptx python-telegram-bot python-dotenv
```

### 2. Configure API Keys

Edit `../Secrets/.env`:

```bash
OPENAI_API_KEY=your_openai_key
LANGCHAIN_API_KEY=your_langchain_key
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
```

### 3. Run Individual Agents

Each agent can be run standalone:

```bash
# Research agents
cd Slide1_Agent && python agent.py "B2B Fintech" "US"
cd ../Slide2_Agent && python agent.py "B2B Fintech" "US"
# ... etc

# Compilation
cd ../Outline_AGENT_VC && python agent.py "B2B Fintech" "US"

# PowerPoint generation
cd ../POWERPOINT_VC_AGENT && python agent.py "B2B Fintech"

# Review
cd ../FinalPass_agent && python agent.py "B2B Fintech"

# Networking strategy
cd ../NetworkingResearch_Agent && python agent.py "B2B Fintech" "US"
cd ../Outline_NETWORKING_AGENT && python agent.py "B2B Fintech" "US"
cd ../POWERPOINT_NETWORKING_AGENT && python agent.py "B2B Fintech"
```

### 4. Run Telegram Bot

For full orchestration:

```bash
cd TelegramVCBot
python bot.py
```

Then in Telegram:
```
/vc B2B Fintech US
```

For networking strategy:
```
/networking B2B Fintech US
```

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    TelegramVCBot                        │
│                  (User Interface)                       │
└────────────────────┬────────────────────────────────────┘
                     │
                     ├──► Phase 1: Research (Parallel)
                     │    ├─► Slide1_Agent
                     │    ├─► Slide2_Agent
                     │    ├─► Slide3_Agent
                     │    ├─► Slide4_Agent
                     │    └─► Slide5_Agent
                     │
                     ├──► Phase 2: Compilation
                     │    └─► Outline_AGENT_VC
                     │
                     ├──► Phase 3: Presentation
                     │    └─► POWERPOINT_VC_AGENT
                     │
                     └──► Phase 4: Review
                          └─► FinalPass_agent
```

Networking strategy flow:
```
┌─────────────────────────────────────────────────────────┐
│                    TelegramVCBot                        │
│                  (User Interface)                       │
└────────────────────┬────────────────────────────────────┘
                     │
                     ├──► Phase 1: Research
                     │    └─► NetworkingResearch_Agent
                     │
                     ├──► Phase 2: Compilation
                     │    └─► Outline_NETWORKING_AGENT
                     │
                     └──► Phase 3: Presentation
                          └─► POWERPOINT_NETWORKING_AGENT
```

## Output Files

All outputs saved to `../Outputs/`:

- `slide1_<sector>_<timestamp>.md` - Emerging trends research
- `slide2_<sector>_<timestamp>.md` - Ecosystem map
- `slide3_<sector>_<timestamp>.md` - Macro thesis
- `slide4_<sector>_<timestamp>.md` - Investment filters
- `slide5_<sector>_<timestamp>.md` - Candidate companies
- `vc_thesis_<sector>_<timestamp>.md` - Complete thesis
- `vc_thesis_<sector>_<timestamp>.pptx` - PowerPoint deck
- `vc_thesis_<sector>_<timestamp>_reviewed.pptx` - Reviewed deck
- `review_analysis_<sector>_<timestamp>.md` - Quality analysis
- `networking_research_<sector>_<timestamp>.md` - Networking research
- `networking_strategy_<sector>_<timestamp>.md` - Networking strategy outline
- `networking_strategy_<sector>_<timestamp>.pptx` - Networking strategy deck

## Development

### Adding New Agents

1. Create agent folder in `Agents/`
2. Implement `agent.py` with standard interface
3. Add `requirements.txt` and `README.md`
4. Integrate into `TelegramVCBot/bot.py` if needed

### Agent Interface Standard

Each agent should have:
- `__init__()` - Initialize with API keys
- `run(sector, region)` - Main execution method
- Returns Path to output file
- Saves results to `../Outputs/`

### Testing

Test individual agents before integration:
```bash
cd <AgentFolder>
python agent.py "Test Sector" "US"
```

Check `../Outputs/` for results.

## Troubleshooting

### Common Issues

1. **"OpenAI API key not provided"**
   - Check `.env` file in `Secrets/` folder
   - Ensure `OPENAI_API_KEY` is set
   - Load env vars: `python-dotenv` should handle this

2. **"No research found for Slide X"**
   - Run research agents (Slide 1-5) before Outline_AGENT_VC
   - Check `Outputs/` folder for slide markdown files

3. **Telegram bot not responding**
   - Verify `TELEGRAM_BOT_TOKEN` in `.env`
   - Check bot is running (`python bot.py`)
   - Verify internet connection

4. **PowerPoint template not found**
   - Place template at `../Secrets/VC_DECK_TEMPLATE.pptx`
   - Or let agent create blank presentation

## Performance

- Single agent: ~30-60 seconds
- Complete pipeline: ~3-5 minutes
- Research phase can be parallelized for faster execution

## API Costs

Approximate costs per thesis (GPT-4):
- Research agents (5x): ~$0.50
- Compilation: ~$0.20
- Review: ~$0.15
- **Total: ~$0.85 per thesis**

## License

Internal use only. See project LICENSE for details.

## Support

For issues or questions:
1. Check agent README files
2. Review logs in console output
3. Check `Outputs/` folder for partial results
4. Verify API keys and environment setup
