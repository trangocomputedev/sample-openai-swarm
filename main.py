"""
Interactive customer support session using OpenAI Swarm.
Usage: python main.py
       python main.py --demo       # run a non-interactive scripted demo
"""
import sys
from dotenv import load_dotenv
load_dotenv()

from swarm import Swarm
from swarm.repl import run_demo_loop
from src.agents import triage_agent


def demo() -> None:
    """Run a scripted demo without interactive input."""
    client = Swarm()
    messages = [{"role": "user", "content": "Hi, I need help with a refund. My customer ID is C-1042."}]
    context = {}

    print("=== OpenAI Swarm — Customer Support Demo ===\n")

    while True:
        response = client.run(
            agent=triage_agent,
            messages=messages,
            context_variables=context,
            stream=False,
        )
        context.update(response.context_variables)
        for msg in response.messages:
            if msg["role"] == "assistant" and msg.get("content"):
                print(f"[{response.agent.name}]: {msg['content']}\n")
        messages.extend(response.messages)

        if not response.messages or response.messages[-1].get("role") == "assistant":
            break


if __name__ == "__main__":
    if "--demo" in sys.argv:
        demo()
    else:
        # Full interactive REPL
        run_demo_loop(triage_agent, stream=True)
