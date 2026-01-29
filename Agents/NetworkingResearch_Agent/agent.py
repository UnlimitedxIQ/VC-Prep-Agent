"""
NetworkingResearch_Agent: Networking Strategy Research

Gathers data for target profiles, outreach methods, and ethical norms
for sourcing and evaluating VC deals in a given sector and stage.

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

    def web_search(self, query: str, max_results: int = 8) -> List[Dict]:
        """Perform web search and return results."""
        try:
            return list(self.ddgs.text(query, max_results=max_results))
        except Exception as e:
            print(f"DuckDuckGo Search error: {e}")
            return []

    def news_search(self, query: str, max_results: int = 5) -> List[Dict]:
        """Perform news search for recent articles."""
        try:
            return list(self.ddgs.news(query, max_results=max_results))
        except Exception as e:
            print(f"DuckDuckGo News Search error: {e}")
            return []


class NetworkingResearchAgent:
    """Agent for researching networking strategy inputs."""

    def __init__(self, api_key: str = None):
        """Initialize the Networking Research Agent with GPT-4o-mini."""
        self.openai_api_key = api_key or os.getenv("OPENAI_API_KEY")

        if not self.openai_api_key:
            raise ValueError("OpenAI API key not provided")

        self.llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0.6,
            openai_api_key=self.openai_api_key
        )

        self.search = DuckDuckGoSearch()

        self.base_path = Path(__file__).parent.parent.parent
        self.outputs_path = self.base_path / "Outputs"
        self.outputs_path.mkdir(exist_ok=True)

    def search_networking_data(self, sector: str, region: str) -> Dict[str, List[Dict]]:
        """Search for networking strategy inputs using DuckDuckGo."""
        print(f"  Searching web for networking strategy inputs ({sector}, {region})...")

        searches = {
            "target_profiles": [
                f"{sector} startup founder profile seed stage {region}",
                f"{sector} accelerator list {region} seed stage",
                f"{sector} angel investors {region} early stage"
            ],
            "outreach_methods": [
                f"{sector} demo day conference startup events {region} 2024 2025",
                "venture capital sourcing LinkedIn outreach best practices",
                "warm introduction investor outreach best practices"
            ],
            "ethics_reputation": [
                "venture capital ethics sourcing deals best practices",
                "conflict of interest policy venture capital investing",
                "investor reputation best practices startup ecosystem"
            ]
        }

        results = {}
        for category, queries in searches.items():
            category_results = {"web": [], "news": []}
            print(f"    -> Searching: {category}")
            for query in queries:
                category_results["web"].extend(self.search.web_search(query, max_results=4))
                category_results["news"].extend(self.search.news_search(query, max_results=2))
            results[category] = category_results

        return results

    def format_search_results(self, results: Dict[str, List[Dict]]) -> str:
        """Format search results for LLM context."""
        formatted = []

        for category, data in results.items():
            formatted.append(f"\n### {category.replace('_', ' ').title()} Research:\n")

            for item in data.get("web", [])[:8]:
                title = item.get("title", "")
                body = item.get("body", "")
                url = item.get("href", "")
                formatted.append(f"- **{title}**: {body}\n  Source: {url}\n")

            for item in data.get("news", [])[:5]:
                title = item.get("title", "")
                body = item.get("body", "")
                url = item.get("url", "")
                formatted.append(f"- [NEWS] **{title}**: {body}\n  Source: {url}\n")

        return "\n".join(formatted)

    def research_strategy(self, sector: str, region: str = "US") -> Dict[str, Any]:
        """Research networking strategy using web search + LLM."""
        search_results = self.search_networking_data(sector, region)
        search_context = self.format_search_results(search_results)

        system_prompt = """You are a venture capital platform strategist.
Use ONLY the provided sources to draft a networking strategy research brief.

Rules:
- Cite sources with URLs for every claim
- Do not invent statistics or names
- If data is missing, state it explicitly
- Keep bullets concise and actionable"""

        user_prompt = f"""Based on the research below for {sector} in {region}, create a networking strategy brief with 3 sections.

{search_context}

---

Provide markdown output with these sections:

1. **Target Profiles (Founders, Accelerators, Angels)**
   - 4-6 bullets describing who to target and why
   - Include specific accelerator/angel examples if found
   - Cite sources

2. **Outreach Methods (Events, LinkedIn, Warm Introductions)**
   - 4-6 bullets on practical sourcing methods
   - Include event types or programs if found
   - Cite sources

3. **Ethical Norms & Reputational Best Practices**
   - 4-6 bullets on ethics, conflicts, confidentiality, and transparency
   - Cite sources

Return ONLY the formatted markdown with citations in-line (e.g., "(Source: URL)")."""

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
        """Format research data as markdown."""
        return f"""# Networking Strategy Research

**Sector**: {research_data['sector']}
**Region**: {research_data['region']}
**Generated**: {research_data['timestamp']}
**Model**: GPT-4o-mini with DuckDuckGo Search

---

{research_data['content']}

---

*Research conducted by NetworkingResearch_Agent with real-time web search*
"""

    def save_research(self, research_data: Dict[str, Any], filename: str = None) -> Path:
        """Save research results to file."""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            sector_slug = research_data['sector'].lower().replace(" ", "_")
            filename = f"networking_research_{sector_slug}_{timestamp}.md"

        output_path = self.outputs_path / filename
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(self.format_as_markdown(research_data))

        print(f"  Research saved to: {output_path}")
        return output_path

    def run(self, sector: str, region: str = "US") -> Path:
        """Run the complete research workflow."""
        print(f"\n{'='*60}")
        print("NetworkingResearch_Agent: Networking Strategy Research")
        print(f"Sector: {sector} | Region: {region}")
        print("Model: GPT-4o-mini | Search: DuckDuckGo")
        print(f"{'='*60}\n")

        research_data = self.research_strategy(sector, region)
        output_path = self.save_research(research_data)

        print(f"\n{'='*60}")
        print("NetworkingResearch_Agent completed!")
        print(f"{'='*60}\n")

        return output_path


def main():
    """CLI entry point for NetworkingResearch_Agent."""
    if len(sys.argv) < 2:
        print("Usage: python agent.py <sector> [region]")
        print("Example: python agent.py 'B2B Fintech' 'US'")
        sys.exit(1)

    sector = sys.argv[1]
    region = sys.argv[2] if len(sys.argv) > 2 else "US"

    try:
        agent = NetworkingResearchAgent()
        agent.run(sector, region)
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
