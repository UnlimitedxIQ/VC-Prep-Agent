"""
Slide4_Agent: Company Profile Filters

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


class Slide4Agent:
    def __init__(self, api_key: str = None):
        self.openai_api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.openai_api_key:
            raise ValueError("OpenAI API key not provided")

        self.llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7, openai_api_key=self.openai_api_key)
        self.search = DuckDuckGoSearch()
        self.base_path = Path(__file__).parent.parent.parent
        self.outputs_path = self.base_path / "Outputs"
        self.outputs_path.mkdir(exist_ok=True)

    def search_filter_data(self, sector: str, region: str) -> Dict[str, List[Dict]]:
        print(f"  Searching web for {sector} investment criteria...")
        searches = {
            "growth_metrics": f"{sector} SaaS growth metrics benchmarks ARR MRR",
            "retention": f"{sector} retention metrics NRR churn benchmarks",
            "unit_economics": f"{sector} LTV CAC payback period unit economics",
            "investment_criteria": f"{sector} venture capital investment criteria seed series A"
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

    def research_filters(self, sector: str, region: str = "US") -> Dict[str, Any]:
        search_results = self.search_filter_data(sector, region)
        search_context = self.format_search_results(search_results)

        system_prompt = """You are a venture capital investment analyst defining investment criteria.
Specify measurable filters using ONLY data from the search results.
Include citations with URLs for all benchmark numbers."""

        user_prompt = f"""Based on the following research about {sector} in {region}, create a Slide 4 analysis:

{search_context}

---

Provide exactly 3 categories of filters with REAL benchmarks from the research:

1. **Metrics**: Traction and growth thresholds.
   - Examples: "30% MoM growth", "$5M ARR", "NRR > 130%"
   - Use ACTUAL benchmarks found in research
   - CITE THE SOURCE URL

2. **Stickiness**: Integration depth, switching costs, workflow embeddedness.
   - What makes customers stick around?
   - CITE THE SOURCE URL

3. **Stage & Unit Economics**: Investment stage and unit economics benchmarks.
   - LTV/CAC ratio, payback period, gross margins
   - CITE THE SOURCE URL

Format as markdown with proper citations."""

        messages = [SystemMessage(content=system_prompt), HumanMessage(content=user_prompt)]
        print("  Synthesizing research with GPT-4o-mini...")
        response = self.llm.invoke(messages)
        return {"sector": sector, "region": region, "content": response.content, "timestamp": datetime.now().isoformat()}

    def save_research(self, research_data: Dict[str, Any]) -> Path:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        sector_slug = research_data['sector'].lower().replace(" ", "_")
        filename = f"slide4_{sector_slug}_{timestamp}.md"
        output_path = self.outputs_path / filename

        markdown = f"""# Slide 4: Company Profile Filters

**Sector**: {research_data['sector']}
**Region**: {research_data['region']}
**Generated**: {research_data['timestamp']}
**Model**: GPT-4o-mini with DuckDuckGo Search

---

{research_data['content']}

---

*Research conducted by Slide4_Agent with real-time web search*
"""
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(markdown)
        print(f"  Research saved to: {output_path}")
        return output_path

    def run(self, sector: str, region: str = "US") -> Path:
        print(f"\n{'='*60}")
        print(f"Slide4_Agent: Company Profile Filters Research")
        print(f"Sector: {sector} | Region: {region}")
        print(f"{'='*60}\n")
        research_data = self.research_filters(sector, region)
        return self.save_research(research_data)


def main():
    if len(sys.argv) < 2:
        print("Usage: python agent.py <sector> [region]")
        sys.exit(1)
    sector = sys.argv[1]
    region = sys.argv[2] if len(sys.argv) > 2 else "US"
    try:
        Slide4Agent().run(sector, region)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
