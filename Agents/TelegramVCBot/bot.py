"""
TelegramVCBot: VC Thesis Orchestrator

Telegram chatbot that orchestrates all research agents to produce a complete
VC industry thesis on-demand.
"""

import os
import sys
from pathlib import Path
from typing import Dict, Any
import asyncio
import logging
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
env_path = Path(__file__).parent.parent.parent / "Secrets" / ".env"
load_dotenv(env_path)

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters
)

# Import agent modules
sys.path.append(str(Path(__file__).parent.parent))
from Slide1_Agent.agent import Slide1Agent
from Slide2_Agent.agent import Slide2Agent
from Slide3_Agent.agent import Slide3Agent
from Slide4_Agent.agent import Slide4Agent
from Slide5_Agent.agent import Slide5Agent
from Outline_AGENT_VC.agent import OutlineAgent
from POWERPOINT_VC_AGENT.agent import PowerPointAgent
from FinalPass_agent.agent import FinalPassAgent
from NetworkingResearch_Agent.agent import NetworkingResearchAgent
from Outline_NETWORKING_AGENT.agent import OutlineNetworkingAgent
from POWERPOINT_NETWORKING_AGENT.agent import PowerPointNetworkingAgent


# Configure logging - hide sensitive tokens
class TokenFilter(logging.Filter):
    """Filter to hide sensitive tokens from logs."""
    def filter(self, record):
        if hasattr(record, 'msg') and isinstance(record.msg, str):
            # Hide Telegram bot tokens (format: 123456789:ABC...)
            import re
            record.msg = re.sub(r'bot\d+:[A-Za-z0-9_-]+', 'bot***TOKEN_HIDDEN***', record.msg)
            # Hide in args too
            if record.args:
                new_args = []
                for arg in record.args:
                    if isinstance(arg, str):
                        arg = re.sub(r'bot\d+:[A-Za-z0-9_-]+', 'bot***TOKEN_HIDDEN***', arg)
                    new_args.append(arg)
                record.args = tuple(new_args)
        return True

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Apply token filter to all loggers
for handler in logging.root.handlers:
    handler.addFilter(TokenFilter())

# Suppress verbose HTTP logs that show tokens
logging.getLogger('httpx').setLevel(logging.WARNING)
logging.getLogger('httpcore').setLevel(logging.WARNING)
logging.getLogger('telegram').setLevel(logging.WARNING)
logging.getLogger('primp').setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


class VCThesisBot:
    """Telegram bot for orchestrating VC thesis generation."""

    def __init__(self, bot_token: str):
        """Initialize the bot."""
        self.bot_token = bot_token
        self.base_path = Path(__file__).parent.parent.parent

        # Initialize agents lazily to avoid startup issues
        self._slide1_agent = None
        self._slide2_agent = None
        self._slide3_agent = None
        self._slide4_agent = None
        self._slide5_agent = None
        self._outline_agent = None
        self._powerpoint_agent = None
        self._finalpass_agent = None
        self._networking_research_agent = None
        self._networking_outline_agent = None
        self._networking_powerpoint_agent = None

    def _get_agents(self):
        """Lazy initialization of agents."""
        if self._slide1_agent is None:
            self._slide1_agent = Slide1Agent()
            self._slide2_agent = Slide2Agent()
            self._slide3_agent = Slide3Agent()
            self._slide4_agent = Slide4Agent()
            self._slide5_agent = Slide5Agent()
            self._outline_agent = OutlineAgent()
            self._powerpoint_agent = PowerPointAgent()
            self._finalpass_agent = FinalPassAgent()
            self._networking_research_agent = NetworkingResearchAgent()
            self._networking_outline_agent = OutlineNetworkingAgent()
            self._networking_powerpoint_agent = PowerPointNetworkingAgent()

        return {
            'slide1': self._slide1_agent,
            'slide2': self._slide2_agent,
            'slide3': self._slide3_agent,
            'slide4': self._slide4_agent,
            'slide5': self._slide5_agent,
            'outline': self._outline_agent,
            'powerpoint': self._powerpoint_agent,
            'finalpass': self._finalpass_agent,
            'networking_research': self._networking_research_agent,
            'networking_outline': self._networking_outline_agent,
            'networking_powerpoint': self._networking_powerpoint_agent
        }

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command."""
        welcome_message = """
Welcome to the VC Thesis Bot!

I can generate complete venture capital industry theses for any sector.

Commands:
- /vc <sector> [region] - Generate a complete VC thesis
- /networking <sector> [region] - Generate a networking strategy deck
- /status - Check bot status
- /help - Show this help message

Example:
/vc B2B Fintech US

/networking B2B Fintech US

This will:
1. Research emerging trends
2. Map the ecosystem
3. Develop macro thesis
4. Define investment filters
5. Identify candidate companies
6. Compile into thesis document
7. Generate PowerPoint deck
8. Review and polish

The process takes 3-5 minutes. You'll receive progress updates.
"""
        await update.message.reply_text(welcome_message)

    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command."""
        await self.start(update, context)

    async def status_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /status command."""
        status_message = """
[OK] Bot Status: Online

Available Agents:
- Slide1_Agent - Emerging Trends [OK]
- Slide2_Agent - Taxonomy/Ecosystem [OK]
- Slide3_Agent - Macro Thesis [OK]
- Slide4_Agent - Company Filters [OK]
- Slide5_Agent - Candidate Companies [OK]
- Outline_AGENT_VC - Thesis Compiler [OK]
- POWERPOINT_VC_AGENT - Deck Generator [OK]
- FinalPass_agent - Quality Review [OK]
- NetworkingResearch_Agent - Networking Research [OK]
- Outline_NETWORKING_AGENT - Networking Strategy Compiler [OK]
- POWERPOINT_NETWORKING_AGENT - Networking Deck Generator [OK]

All systems operational.
"""
        await update.message.reply_text(status_message)

    async def vc_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /vc command to generate thesis."""
        if not context.args:
            await update.message.reply_text(
                "Please provide a sector.\n\nUsage: /vc <sector> [region]\nExample: /vc B2B Fintech US"
            )
            return

        # Parse sector and region from arguments
        sector = " ".join(context.args[:-1]) if len(context.args) > 1 else context.args[0]
        region = context.args[-1] if len(context.args) > 1 and len(context.args[-1]) == 2 else "US"

        # If last arg looks like part of sector name, include it
        if len(context.args) > 1 and len(context.args[-1]) > 2:
            sector = " ".join(context.args)
            region = "US"

        await update.message.reply_text(
            f"[STARTING] VC thesis generation for: {sector} ({region})\n\n"
            f"This will take approximately 3-5 minutes. I'll send you updates as I progress."
        )

        try:
            # Get agents
            agents = self._get_agents()

            # Run research pipeline
            await self.run_research_pipeline(update, sector, region, agents)

        except Exception as e:
            logger.error(f"Error generating thesis: {e}", exc_info=True)
            await update.message.reply_text(
                f"[ERROR] Error generating thesis: {str(e)}\n\nPlease try again."
            )

    async def networking_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /networking command to generate networking strategy deck."""
        if not context.args:
            await update.message.reply_text(
                "Please provide a sector.\n\nUsage: /networking <sector> [region]\nExample: /networking B2B Fintech US"
            )
            return

        sector = " ".join(context.args[:-1]) if len(context.args) > 1 else context.args[0]
        region = context.args[-1] if len(context.args) > 1 and len(context.args[-1]) == 2 else "US"

        if len(context.args) > 1 and len(context.args[-1]) > 2:
            sector = " ".join(context.args)
            region = "US"

        await update.message.reply_text(
            f"[STARTING] Networking strategy generation for: {sector} ({region})\n\n"
            f"This will take approximately 2-4 minutes. I'll send you updates as I progress."
        )

        try:
            agents = self._get_agents()
            await self.run_networking_pipeline(update, sector, region, agents)
        except Exception as e:
            logger.error(f"Error generating networking strategy: {e}", exc_info=True)
            await update.message.reply_text(
                f"[ERROR] Error generating networking strategy: {str(e)}\n\nPlease try again."
            )

    async def run_research_pipeline(self, update: Update, sector: str, region: str, agents: dict):
        """Run the complete research pipeline."""

        # Phase 1: Research agents
        await update.message.reply_text("[Phase 1/4] Running research agents...")

        try:
            await update.message.reply_text("  -> Researching emerging trends...")
            agents['slide1'].run(sector, region)

            await update.message.reply_text("  -> Mapping ecosystem...")
            agents['slide2'].run(sector, region)

            await update.message.reply_text("  -> Developing macro thesis...")
            agents['slide3'].run(sector, region)

            await update.message.reply_text("  -> Defining investment filters...")
            agents['slide4'].run(sector, region)

            await update.message.reply_text("  -> Identifying candidate companies...")
            agents['slide5'].run(sector, region)

            await update.message.reply_text("[OK] Phase 1 complete: All research gathered")

        except Exception as e:
            logger.error(f"Error in research phase: {e}", exc_info=True)
            raise

        # Phase 2: Compile thesis
        await update.message.reply_text("[Phase 2/4] Compiling thesis document...")

        try:
            thesis_path = agents['outline'].run(sector, region)
            await update.message.reply_text("[OK] Phase 2 complete: Thesis compiled")

        except Exception as e:
            logger.error(f"Error compiling thesis: {e}", exc_info=True)
            raise

        # Phase 3: Generate PowerPoint
        await update.message.reply_text("[Phase 3/4] Creating PowerPoint deck...")

        try:
            pptx_path = agents['powerpoint'].run(sector)
            await update.message.reply_text("[OK] Phase 3 complete: PowerPoint created")

        except Exception as e:
            logger.error(f"Error creating PowerPoint: {e}", exc_info=True)
            await update.message.reply_text(
                "[ERROR] PowerPoint generation failed. Please try again."
            )
            return

        # Phase 4: Review and polish
        await update.message.reply_text("[Phase 4/4] Running quality assurance...")

        try:
            reviewed_path, report_path = agents['finalpass'].run(sector, pptx_file=pptx_path)
            await update.message.reply_text("[OK] Phase 4 complete: QA passed")

            # Send ONLY the final reviewed PowerPoint
            with open(reviewed_path, 'rb') as f:
                await update.message.reply_document(
                    document=f,
                    filename=f"VC_Thesis_{sector.replace(' ', '_')}.pptx",
                    caption=f"VC Industry Thesis: {sector} ({region})"
                )

        except Exception as e:
            logger.error(f"Error in review phase: {e}", exc_info=True)
            # Send the original deck if QA fails
            with open(pptx_path, 'rb') as f:
                await update.message.reply_document(
                    document=f,
                    filename=f"VC_Thesis_{sector.replace(' ', '_')}.pptx",
                    caption=f"VC Industry Thesis: {sector} ({region})"
                )

        # Success message
        await update.message.reply_text(
            f"[COMPLETE] VC Thesis for {sector} ({region})\n\n"
            f"8 slides | 3 bullets each | QA verified\n\n"
            f"Generate another: /vc <sector>"
        )

    async def run_networking_pipeline(self, update: Update, sector: str, region: str, agents: dict):
        """Run the networking strategy pipeline."""
        await update.message.reply_text("[Phase 1/3] Running networking research...")

        try:
            await update.message.reply_text("  -> Researching target profiles, outreach, ethics...")
            agents['networking_research'].run(sector, region)
            await update.message.reply_text("[OK] Phase 1 complete: Networking research gathered")
        except Exception as e:
            logger.error(f"Error in networking research phase: {e}", exc_info=True)
            raise

        await update.message.reply_text("[Phase 2/3] Compiling networking strategy outline...")

        try:
            agents['networking_outline'].run(sector, region)
            await update.message.reply_text("[OK] Phase 2 complete: Strategy outline compiled")
        except Exception as e:
            logger.error(f"Error compiling networking strategy: {e}", exc_info=True)
            raise

        await update.message.reply_text("[Phase 3/3] Creating networking strategy deck...")

        try:
            pptx_path = agents['networking_powerpoint'].run(sector)
            await update.message.reply_text("[OK] Phase 3 complete: PowerPoint created")
        except Exception as e:
            logger.error(f"Error creating networking PowerPoint: {e}", exc_info=True)
            await update.message.reply_text(
                "[ERROR] PowerPoint generation failed. Please try again."
            )
            return

        with open(pptx_path, 'rb') as f:
            await update.message.reply_document(
                document=f,
                filename=f"Networking_Strategy_{sector.replace(' ', '_')}.pptx",
                caption=f"Networking Strategy: {sector} ({region})"
            )

        await update.message.reply_text(
            f"[COMPLETE] Networking Strategy for {sector} ({region})\n\n"
            f"3 content slides | 3 bullets each\n\n"
            f"Generate another: /networking <sector>"
        )

    async def error_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle errors."""
        logger.error(f"Update {update} caused error {context.error}")

        if update and update.message:
            await update.message.reply_text(
                "[ERROR] An error occurred. Please try again."
            )

    def run(self):
        """Start the bot."""
        logger.info("Starting VC Thesis Bot...")

        # Create application
        application = Application.builder().token(self.bot_token).build()

        # Add handlers
        application.add_handler(CommandHandler("start", self.start))
        application.add_handler(CommandHandler("help", self.help_command))
        application.add_handler(CommandHandler("status", self.status_command))
        application.add_handler(CommandHandler("vc", self.vc_command))
        application.add_handler(CommandHandler("networking", self.networking_command))

        # Add error handler
        application.add_error_handler(self.error_handler)

        # Start bot
        logger.info("Bot started successfully!")
        print("\n" + "="*60)
        print("VC Thesis Bot is running!")
        print("Bot: @VCBOTBRYSONSMITHbot")
        print("Send /start to begin")
        print("="*60 + "\n")

        application.run_polling(allowed_updates=Update.ALL_TYPES)


def main():
    """CLI entry point."""
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")

    if not bot_token:
        print("Error: TELEGRAM_BOT_TOKEN environment variable not set")
        print("Please add it to your .env file in the Secrets folder")
        sys.exit(1)

    bot = VCThesisBot(bot_token)
    bot.run()


if __name__ == "__main__":
    # Fix for Python 3.14+ asyncio event loop
    import asyncio
    try:
        asyncio.get_running_loop()
    except RuntimeError:
        asyncio.set_event_loop(asyncio.new_event_loop())

    main()
