"""
All Swarm agents defined in one module.

Swarm handoffs are Python functions that return an Agent. Because agents
reference each other through closures, keeping them in one file eliminates
circular import issues and makes the routing topology easy to read at a glance.

Topology:
    TriageAgent ──billing──▶ BillingAgent ──▶ (back to triage)
                ──technical▶ TechAgent    ──▶ (back to triage)
                ──refund───▶ RefundAgent  ──▶ (back to triage)
"""
from swarm import Agent
from src.tools.account import account_lookup, set_customer_id
from src.tools.tickets import create_ticket
from src.tools.refunds import check_refund_eligibility, process_refund


# ---------------------------------------------------------------------------
# Forward declarations — filled in below once all agents are defined
# ---------------------------------------------------------------------------

def _transfer_to_triage():
    """Escalate back to triage for re-classification."""
    return triage_agent


def _transfer_to_billing():
    """Transfer to the billing specialist for invoice and payment questions."""
    return billing_agent


def _transfer_to_tech():
    """Transfer to technical support for product and configuration questions."""
    return tech_agent


def _transfer_to_refunds():
    """Transfer to the refunds specialist for return and refund requests."""
    return refund_agent


# ---------------------------------------------------------------------------
# Billing Agent
# ---------------------------------------------------------------------------
billing_agent = Agent(
    name="BillingAgent",
    model="gpt-4o-mini",
    instructions=(
        "You are a billing specialist. "
        "Use account_lookup to retrieve the customer's account details. "
        "Answer questions about invoices, charges, and subscription plans clearly. "
        "If the customer needs technical help instead, transfer back to triage. "
        "If an issue cannot be resolved immediately, use create_ticket to escalate."
    ),
    functions=[account_lookup, create_ticket, _transfer_to_triage],
)

# ---------------------------------------------------------------------------
# Tech Support Agent
# ---------------------------------------------------------------------------
tech_agent = Agent(
    name="TechAgent",
    model="gpt-4o-mini",
    instructions=(
        "You are a technical support specialist. "
        "Help customers with product setup, configuration, bugs, and how-to questions. "
        "Provide step-by-step instructions. If you cannot resolve the issue, "
        "use create_ticket to open a high-priority ticket and transfer back to triage."
    ),
    functions=[create_ticket, _transfer_to_triage],
)

# ---------------------------------------------------------------------------
# Refunds Agent
# ---------------------------------------------------------------------------
refund_agent = Agent(
    name="RefundAgent",
    model="gpt-4o-mini",
    instructions=(
        "You are a refunds specialist. "
        "First use check_refund_eligibility to verify the order qualifies. "
        "If eligible, use process_refund to initiate the refund and confirm with the customer. "
        "If not eligible, explain the policy clearly and offer alternatives. "
        "Transfer back to triage if the customer has a different concern."
    ),
    functions=[check_refund_eligibility, process_refund, _transfer_to_triage],
)

# ---------------------------------------------------------------------------
# Triage Agent  — entry point for all conversations
# ---------------------------------------------------------------------------
triage_agent = Agent(
    name="TriageAgent",
    model="gpt-4o-mini",
    instructions=(
        "You are the first point of contact for customer support. "
        "Greet the customer and ask for their customer ID if not already known. "
        "Use set_customer_id to record it — this makes it available to all other agents. "
        "Then classify the customer's request and transfer to the right specialist:\n"
        "  - Billing questions (invoices, charges, plans) → transfer_to_billing\n"
        "  - Technical issues (bugs, setup, how-to) → transfer_to_tech\n"
        "  - Refund or return requests → transfer_to_refunds\n"
        "Do not attempt to resolve issues yourself — always hand off to a specialist."
    ),
    functions=[set_customer_id, _transfer_to_billing, _transfer_to_tech, _transfer_to_refunds],
)
