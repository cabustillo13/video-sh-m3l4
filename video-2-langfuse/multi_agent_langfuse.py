import sys
import io

import os
from langfuse import Langfuse
from langchain_openai import ChatOpenAI
from langsmith import uuid7

from dotenv import load_dotenv
load_dotenv()

# Ensure UTF-8 encoding for stdin, stdout, and stderr
sys.stdin = io.TextIOWrapper(sys.stdin.buffer, encoding="utf-8", errors="strict")
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="strict")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="strict")


# 1) SETUP LANGFUSE
langfuse = Langfuse(
    public_key=os.getenv("LANGFUSE_PUBLIC_KEY"),
    secret_key=os.getenv("LANGFUSE_SECRET_KEY")
)


# 2) LLM CONFIGURATION
router_llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
agent_llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)


# 3) AGENTS
def hr_agent(query: str) -> str:
    """Handles HR-related queries."""
    response = agent_llm.invoke(
        f"[HR Agent] Answer the following HR-related query clearly and formally:\n{query}",
        config={"run_id": uuid7()},
    )
    return response.content


def tech_agent(query: str) -> str:
    """Handles technical queries."""
    response = agent_llm.invoke(
        f"[Tech Agent] Answer the following technical query:\n{query}",
        config={"run_id": uuid7()},
    )
    return response.content


# 4) MULTI-AGENT ROUTER
def route_query(query: str) -> str:
    """Classifies the query into HR or TECH."""
    result = router_llm.invoke(
        f"Classify this query into 'HR' or 'TECH'. Respond with only one word:\n{query}",
        config={"run_id": uuid7()},
    )
    category = result.content.strip().lower()
    return "hr" if "hr" in category else "tech"


# 5) ORCHESTRATOR WITH LANGFUSE TRACING
def orchestrator(query: str) -> dict:
    """Routes the query to the correct agent and traces using Langfuse spans."""
    with langfuse.start_as_current_span(name="multi-agent-root", input={"query": query}) as root_span: # pylint: disable=not-context-manager
        # Assign trace-level metadata
        root_span.update_trace(input={"query": query})

        # Step 1: Routing
        route = route_query(query)
        span1 = langfuse.start_span(name="route_query", input={"query": query})
        span1.update(output={"route": route})
        span1.end()

        # Step 2: Call the correct agent
        if route == "hr":
            answer = hr_agent(query)
            span2 = langfuse.start_span(name="hr_agent", input={"query": query})
        else:
            answer = tech_agent(query)
            span2 = langfuse.start_span(name="tech_agent", input={"query": query})

        span2.update(output={"answer": answer})
        span2.end()

        # Set output trace
        root_span.update_trace(output={"route": route, "answer": answer})
        return {
            "route": route,
            "answer": answer,
        }


# 6) INTERACTIVE CLI
def main():
    print("\nLangfuse Multi-Agent Demo (type 'exit' to quit)\n")

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
