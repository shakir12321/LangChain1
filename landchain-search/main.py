import argparse
import json
import os

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langchain_tavily import TavilyMap, TavilySearch
from langsmith import traceable
from pydantic import BaseModel, Field


class AgentAnswer(BaseModel):
    """Structured final answer after tools (if any) were used."""

    summary: str = Field(description="One short paragraph answering the user.")
    key_points: list[str] = Field(
        default_factory=list,
        description="Short bullet-style facts or site sections, max ~8 items.",
    )
    sources: list[str] = Field(
        default_factory=list,
        description="URLs or page titles cited from tool results, if available.",
    )
    caveats: str | None = Field(
        default=None,
        description="If data was missing, blocked, or uncertain, say so briefly.",
    )


@traceable(name="agent_search_invoke", run_type="chain")
def run_agent(agent, query: str):
    return agent.invoke({"messages": [{"role": "user", "content": query}]})


def main() -> None:
    load_dotenv()

    parser = argparse.ArgumentParser(
        description="Run a web agent that chooses the right tool per query."
    )
    parser.add_argument(
        "--query",
        required=True,
        help="Question for the agent (search or website-structure).",
    )
    parser.add_argument(
        "--model",
        default="gpt-4o-mini",
        help="OpenAI model name (default: gpt-4o-mini).",
    )
    parser.add_argument(
        "--langsmith-project",
        default="landchain-search",
        help="LangSmith project name (default: landchain-search).",
    )
    args = parser.parse_args()

    # Normalize common API key env variants and enable tracing.
    langsmith_api_key = (
        os.getenv("LANGSMITH_API_KEY")
        or os.getenv("Langsmith_API_KEY")
        or os.getenv("LANGCHAIN_API_KEY")
    )
    if langsmith_api_key:
        os.environ["LANGSMITH_API_KEY"] = langsmith_api_key
        os.environ.setdefault("LANGSMITH_TRACING", "true")
        os.environ.setdefault("LANGCHAIN_TRACING_V2", "true")
        os.environ.setdefault("LANGSMITH_PROJECT", args.langsmith_project)

    llm = ChatOpenAI(model=args.model, temperature=0)
    tools = [
        TavilySearch(max_results=5),
        TavilyMap(max_depth=2, max_breadth=20, limit=25),
    ]
    agent = create_agent(
        model=llm,
        tools=tools,
        system_prompt=(
            "You are a concise research assistant with two tools. "
            "Use tavily_search for factual/current-event web lookup questions. "
            "Use tavily_map for website structure, navigation, and content-layout questions. "
            "Choose the best tool based on user intent. "
            "Then respond only as the structured schema requires."
        ),
        response_format=AgentAnswer,
    )
    result = run_agent(agent, args.query)
    structured: AgentAnswer = result["structured_response"]
    print(json.dumps(structured.model_dump(), indent=2, ensure_ascii=False))
    

if __name__ == "__main__":
    main()
