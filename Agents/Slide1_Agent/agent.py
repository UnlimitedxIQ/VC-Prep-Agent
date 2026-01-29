"""
Slide1_Agent: Emerging Trends of Interest

Gathers data for emerging trends including market shifts, metrics, CAGR,
business-model multipliers, and regulatory/technical inflection points.

Uses DuckDuckGo for real-time web research and GPT-4o-mini for synthesis.
"""

import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List
from dotenv import load_dotenv

from ddgs import DDGS
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

# Load environment variables
env_path = Path(__file__).parent.parent.parent / "Secrets" / ".env"
load_dotenv(env_path)


class DuckDuckGoSearch:
    """DuckDuckGo Search client for web research."""

    def __init__(self):
        self.ddgs = DDGS()

    def web_search(self, query: str, max_results: int = 10) -> List[Dict]:
        """Perform web search and return results."""
        try:
            results = list(self.ddgs.text(query, max_results=max_results))
            return results
        except Exception as e:
            print(f"DuckDuckGo Search error: {e}")
            return []

    def news_search(self, query: str, max_results: int = 10) -> List[Dict]:
        """Perform news search for recent articles."""
        try:
            results = list(self.ddgs.news(query, max_results=max_results))
            return results
        except Exception as e:
            print(f"DuckDuckGo News Search error: {e}")
            return []


class Slide1Agent:
    """Agent for researching emerging trends in a given industry/sector."""

    def __init__(self, api_key: str = None):
        """Initialize the Slide1 Agent with GPT-4o-mini."""
        self.openai_api_key = api_key or os.getenv("OPENAI_API_KEY")

        if not self.openai_api_key:
            raise ValueError("OpenAI API key not provided")

        # Use GPT-4o-mini for cost efficiency
        self.llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0.7,
            openai_api_key=self.openai_api_key
        )

        # Initialize search client
        self.search = DuckDuckGoSearch()

        # Set up paths
        self.base_path = Path(__file__).parent.parent.parent
        self.outputs_path = self.base_path / "Outputs"
        self.outputs_path.mkdir(exist_ok=True)

    def search_market_data(self, sector: str, region: str) -> Dict[str, List[Dict]]:
        """Search for market data using DuckDuckGo."""
        print(f"  Searching web for {sector} market data...")

        searches = {
            "market_size": f"{sector} market size CAGR forecast {region} 2024 2025",
            "trends": f"{sector} emerging trends technology {region} 2024",
            "regulations": f"{sector} regulatory changes policy {region} 2024",
            "business_model": f"{sector} revenue model ARPU growth"
        }

        results = {}
        for category, query in searches.items():
            print(f"    -> Searching: {category}")
            web_results = self.search.web_search(query, max_results=5)
            news_results = self.search.news_search(query, max_results=3)
            results[category] = {
                "web": web_results,
                "news": news_results
            }

        return results

    def format_search_results(self, results: Dict[str, List[Dict]]) -> str:
        """Format search results for LLM context."""
        formatted = []

        for category, data in results.items():
            formatted.append(f"\n### {category.replace('_', ' ').title()} Research:\n")

            # Web results
            for item in data.get("web", [])[:3]:
                title = item.get("title", "")
                body = item.get("body", "")
                url = item.get("href", "")
                formatted.append(f"- **{title}**: {body}\n  Source: {url}\n")

            # News results
            for item in data.get("news", [])[:2]:
                title = item.get("title", "")
                body = item.get("body", "")
                url = item.get("url", "")
                formatted.append(f"- [NEWS] **{title}**: {body}\n  Source: {url}\n")

        return "\n".join(formatted)

    def research_trends(self, sector: str, region: str = "US") -> Dict[str, Any]:
        """Research emerging trends using web search + LLM."""
        # Step 1: Search the web for real data
        search_results = self.search_market_data(sector, region)
        search_context = self.format_search_results(search_results)

        # Step 2: Use LLM to synthesize findings
        system_prompt = """You are a venture capital analyst researching emerging trends.
Your task is to synthesize the search results into specific, data-driven insights.

IMPORTANT: Only use data from the provided search results. Include specific:
- Dollar amounts and percentages with sources
- Years and dates
- CAGR projections
- Citations with URLs

Do NOT make up statistics. If data isn't available, note it clearly."""

        user_prompt = f"""Based on the following research about {sector} in {region}, create a Slide 1 analysis:

{search_context}

---

Synthesize exactly 3 insights with REAL data from the sources above:

1. **The $X Shift**: A major market-level metric showing market size, volume, or CAGR.
   - Include specific dollar amount or percentage
   - Include the year/date
   - CITE THE SOURCE URL

2. **The Business Model Multiplier**: How this trend increases ARPU, retention, or margins.
   - Include specific multiplier numbers if found
   - CITE THE SOURCE URL

3. **Regulatory / Platform / Technical Inflection**: The enabling change.
   - Be specific about the regulation, technology, or platform
   - CITE THE SOURCE URL

Format as markdown with proper citations."""

        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_prompt)
        ]

        print("  Synthesizing research with GPT-4o-mini...")
        response = self.llm.invoke(messages)

        return {
            "sector": sector,
            "region": region,
            "content": response.content,
            "timestamp": datetime.now().isoformat()
        }

    def format_as_markdown(self, research_data: Dict[str, Any]) -> str:
        """Format research data as markdown for slide content."""
        return f"""# Slide 1: Emerging Trends of Interest

**Sector**: {research_data['sector']}
**Region**: {research_data['region']}
**Generated**: {research_data['timestamp']}
**Model**: GPT-4o-mini with DuckDuckGo Search

---

{research_data['content']}

---

*Research conducted by Slide1_Agent with real-time web search*
"""

    def save_research(self, research_data: Dict[str, Any], filename: str = None) -> Path:
        """Save research results to file."""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            sector_slug = research_data['sector'].lower().replace(" ", "_")
            filename = f"slide1_{sector_slug}_{timestamp}.md"

        output_path = self.outputs_path / filename
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(self.format_as_markdown(research_data))

        print(f"  Research saved to: {output_path}")
        return output_path

    def run(self, sector: str, region: str = "US") -> Path:
        """Run the complete research workflow."""
        print(f"\n{'='*60}")
        print(f"Slide1_Agent: Emerging Trends Research")
        print(f"Sector: {sector} | Region: {region}")
        print(f"Model: GPT-4o-mini | Search: DuckDuckGo")
        print(f"{'='*60}\n")

        research_data = self.research_trends(sector, region)
        output_path = self.save_research(research_data)

        print(f"\n{'='*60}")
        print(f"Slide1_Agent completed!")
        print(f"{'='*60}\n")

        return output_path


def main():
    """CLI entry point for Slide1_Agent."""
    if len(sys.argv) < 2:
        print("Usage: python agent.py <sector> [region]")
        print("Example: python agent.py 'B2B Fintech' 'US'")
        sys.exit(1)

    sector = sys.argv[1]
    region = sys.argv[2] if len(sys.argv) > 2 else "US"

    try:
        agent = Slide1Agent()
        agent.run(sector, region)
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
