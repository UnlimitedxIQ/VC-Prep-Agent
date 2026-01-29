"""
Slide3_Agent: Macro-Market Thesis

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

env_path = Path(__file__).parent.parent.parent / "Secrets" / ".env"
load_dotenv(env_path)


class DuckDuckGoSearch:
    def __init__(self):
        self.ddgs = DDGS()

    def web_search(self, query: str, max_results: int = 10) -> List[Dict]:
        try:
            return list(self.ddgs.text(query, max_results=max_results))
        except Exception as e:
            print(f"Search error: {e}")
            return []


class Slide3Agent:
    def __init__(self, api_key: str = None):
        self.openai_api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.openai_api_key:
            raise ValueError("OpenAI API key not provided")

        self.llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7, openai_api_key=self.openai_api_key)
        self.search = DuckDuckGoSearch()
        self.base_path = Path(__file__).parent.parent.parent
        self.outputs_path = self.base_path / "Outputs"
        self.outputs_path.mkdir(exist_ok=True)

    def search_thesis_data(self, sector: str, region: str) -> Dict[str, List[Dict]]:
        print(f"  Searching web for {sector} thesis insights...")
        searches = {
            "investment_thesis": f"{sector} venture capital investment thesis trends",
            "market_segments": f"{sector} market segments opportunities growth {region}",
            "contrarian_views": f"{sector} challenges disruption contrarian view",
            "thought_leadership": f"{sector} future predictions analysis expert opinion"
        }
        results = {}
        for category, query in searches.items():
            print(f"    -> Searching: {category}")
            results[category] = self.search.web_search(query, max_results=5)
        return results

    def format_search_results(self, results: Dict[str, List[Dict]]) -> str:
        formatted = []
        for category, items in results.items():
            formatted.append(f"\n### {category.replace('_', ' ').title()} Research:\n")
            for item in items[:4]:
                title = item.get("title", "")
                body = item.get("body", "")
                url = item.get("href", "")
                formatted.append(f"- **{title}**: {body}\n  Source: {url}\n")
        return "\n".join(formatted)

    def research_thesis(self, sector: str, region: str = "US") -> Dict[str, Any]:
        search_results = self.search_thesis_data(sector, region)
        search_context = self.format_search_results(search_results)

        system_prompt = """You are a venture capital thought leader crafting investment theses.
Create a sharp, contrarian point of view using ONLY data from the search results.
Include citations with URLs for all claims."""

        user_prompt = f"""Based on the following research about {sector} in {region}, create a Slide 3 analysis:

{search_context}

---

Provide exactly 3 components:

1. **Focus**: The specific sub-segment you're targeting based on the research.
   - Be specific about the market opportunity
   - CITE THE SOURCE URL

2. **The Opinion**: A sharp take with contrast that shows differentiated view.
   - Format: "X is commoditizing, alpha is in Y"
   - Must be supported by research findings
   - CITE THE SOURCE URL

3. **Thought Leadership Hook**: A memorable 2-5 word phrase + one defining sentence.
   - Examples: "Silent Finance", "Zero-touch ops"

Format as markdown with proper citations."""

        messages = [SystemMessage(content=system_prompt), HumanMessage(content=user_prompt)]
        print("  Synthesizing research with GPT-4o-mini...")
        response = self.llm.invoke(messages)
        return {"sector": sector, "region": region, "content": response.content, "timestamp": datetime.now().isoformat()}

    def save_research(self, research_data: Dict[str, Any]) -> Path:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        sector_slug = research_data['sector'].lower().replace(" ", "_")
        filename = f"slide3_{sector_slug}_{timestamp}.md"
        output_path = self.outputs_path / filename

        markdown = f"""# Slide 3: Macro-Market Thesis

**Sector**: {research_data['sector']}
**Region**: {research_data['region']}
**Generated**: {research_data['timestamp']}
**Model**: GPT-4o-mini with DuckDuckGo Search

---

{research_data['content']}

---

*Research conducted by Slide3_Agent with real-time web search*
"""
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(markdown)
        print(f"  Research saved to: {output_path}")
        return output_path

    def run(self, sector: str, region: str = "US") -> Path:
        print(f"\n{'='*60}")
        print(f"Slide3_Agent: Macro-Market Thesis Research")
        print(f"Sector: {sector} | Region: {region}")
        print(f"{'='*60}\n")
        research_data = self.research_thesis(sector, region)
        return self.save_research(research_data)


def main():
    if len(sys.argv) < 2:
        print("Usage: python agent.py <sector> [region]")
        sys.exit(1)
    sector = sys.argv[1]
    region = sys.argv[2] if len(sys.argv) > 2 else "US"
    try:
        Slide3Agent().run(sector, region)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
