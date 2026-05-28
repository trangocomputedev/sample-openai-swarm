# Sample OpenAI Swarm

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)

A multi-agent customer support triage system built with [OpenAI Swarm](https://github.com/openai/swarm). Demonstrates Swarm's core patterns: agent handoffs via function returns, context variable propagation, and the `Result` type for updating shared state.

## Architecture

```
User
 │
 ▼
[TriageAgent]  ── set_customer_id ──▶ context_variables{"customer_id"}
      │
      ├──(billing)────▶ [BillingAgent]   uses: account_lookup, create_ticket
      │                      │
      ├──(technical)──▶ [TechAgent]      uses: create_ticket
      │                      │
      └──(refund)─────▶ [RefundAgent]    uses: check_refund_eligibility, process_refund
                             │
                    all agents ──▶ _transfer_to_triage (re-routing)
```

## Features Demonstrated

| Swarm Feature | Location |
|---|---|
| `Agent(name, model, instructions, functions)` | `src/agents.py` |
| Handoff via function returning `Agent` | `src/agents.py` — `_transfer_to_*` |
| `context_variables` injected into tools | `src/tools/account.py`, `refunds.py` |
| `Result(value, context_variables)` for state update | `src/tools/account.py` — `set_customer_id` |
| `Swarm()` client | `main.py` |
| `client.run(agent, messages, context_variables)` | `main.py` |
| `run_demo_loop` interactive REPL | `main.py` |
| Multi-turn conversation with agent switching | `main.py` |

## Quickstart

```bash
# 1. Install
pip install -r requirements.txt

# 2. Configure
cp .env.example .env
# Set OPENAI_API_KEY

# 3a. Interactive REPL
python main.py

# 3b. Scripted demo (no input required)
python main.py --demo
```

## How Handoffs Work

In Swarm, a handoff is just a Python function that returns another `Agent` object:

```python
def _transfer_to_billing():
    """Transfer to the billing specialist."""
    return billing_agent
```

The LLM calls this function when it decides to hand off. Swarm then continues the conversation using the returned agent. Because it's plain Python, the routing logic is easy to test directly — no mocking required.

## How Context Variables Work

`context_variables` is a dict passed to `client.run()` and threaded through the whole conversation. Any function that declares `context_variables` as its first parameter receives it automatically:

```python
def account_lookup(context_variables: dict) -> str:
    customer_id = context_variables.get("customer_id")
    ...
```

To update context, return a `Result`:

```python
from swarm.types import Result

def set_customer_id(context_variables: dict, customer_id: str) -> Result:
    return Result(
        value="Customer ID noted.",
        context_variables={"customer_id": customer_id},
    )
```

## Tests

```bash
pytest tests/ -v
```

All tests are synchronous — tools are plain functions and handoffs are verified by calling them directly.

## Project Structure

```
src/
├── agents.py          # All agents + handoff topology — the file the visualizer parses
└── tools/
    ├── account.py     # account_lookup, set_customer_id (with Result)
    ├── tickets.py     # create_ticket
    └── refunds.py     # check_refund_eligibility, process_refund
tests/
main.py                # Interactive REPL + scripted demo
```

---

Built by [Trango Compute](https://trango-compute.com)
