import sys
import io

from langsmith import traceable, uuid7
from langchain_openai import ChatOpenAI

from dotenv import load_dotenv
load_dotenv()

# Ensure UTF-8 encoding for stdin, stdout, and stderr
sys.stdin = io.TextIOWrapper(sys.stdin.buffer, encoding="utf-8", errors="strict")
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="strict")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="strict")


# 1) LLM CONFIGURATION
router_llM = ChatOpenAI(model="gpt-4o-mini", temperature=0)
agent_llM = ChatOpenAI(model="gpt-4o-mini", temperature=0)


# 2) AGENTS
@traceable(run_type="llm")
def hr_agent(query: str) -> str:
    """Handles HR-related queries."""
    response = agent_llM.invoke(
        f"[HR Agent] Answer the following HR-related query clearly and formally:\n{query}",
        config={"run_id": uuid7()}
    )
    return response.content


@traceable(run_type="llm")
def tech_agent(query: str) -> str:
    """Handles technical queries."""
    response = agent_llM.invoke(
        f"[Tech Agent] Answer the following technical query:\n{query}",
        config={"run_id": uuid7()}
    )
    return response.content


# 3) MULTI-AGENT ROUTER
@traceable(run_type="chain")
def route_query(query: str) -> str:
    """Classifies the query into HR or TECH."""
    result = router_llM.invoke(
        f"Classify this query into 'HR' or 'TECH'. Respond with only one word:\n{query}",
        config={"run_id": uuid7()}
    )

    category = result.content.strip().lower()

    if "hr" in category:
        return "hr"
    return "tech"


# 4) ORCHESTRATOR
@traceable(run_type="chain")
def orchestrator(query: str) -> dict:
    """Routes the query to the correct agent and returns the response."""
    route = route_query(query)

    if route == "hr":
        answer = hr_agent(query)
    else:
        answer = tech_agent(query)

    return {
        "route": route,
        "answer": answer,
    }


# 5) INTERACTIVE CLI
def main():
    print("\nLangSmith Multi-Agent Demo (type 'exit' to quit)\n")

    while True:
        query = input("Enter your query: ")

        if query.lower().strip() == "exit":
            break

        result = orchestrator(query)

        print("\n------------------------------------")
        print("ROUTE:", result["route"])
        print("ANSWER:", result["answer"])
        print("------------------------------------\n")


if __name__ == "__main__":
    main()
