import json
from swarm.types import Result


def account_lookup(context_variables: dict) -> str:
    """Look up the current customer's account details using their ID from context."""
    customer_id = context_variables.get("customer_id", "unknown")
    # Stub: in production this queries a CRM / database
    data = {
        "customer_id": customer_id,
        "name": "Jane Doe",
        "plan": "Pro",
        "balance_due": 0.00,
        "open_tickets": 1,
        "member_since": "2022-03",
    }
    return json.dumps(data)


def set_customer_id(context_variables: dict, customer_id: str) -> Result:
    """Record the customer's ID so all downstream agents can access it.

    This is called during triage to identify the customer before routing.
    Returns a Result that updates context_variables for all subsequent agents.
    """
    return Result(
        value=f"Customer ID {customer_id!r} noted. Proceeding with lookup.",
        context_variables={"customer_id": customer_id},
    )
