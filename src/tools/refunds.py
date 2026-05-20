import json


def check_refund_eligibility(context_variables: dict, order_id: str) -> str:
    """Check whether an order qualifies for a refund.

    Swarm injects context_variables automatically. The customer tier
    stored there determines the refund window.
    """
    tier = context_variables.get("plan", "standard")
    # Stub: in production this queries the orders database
    data = {
        "order_id": order_id,
        "eligible": True,
        "reason": "Within 30-day return window",
        "amount": 49.99,
        "tier_bonus": tier == "Pro",  # Pro customers get extended window
    }
    return json.dumps(data)


def process_refund(order_id: str, amount: float) -> str:
    """Initiate a refund for the given order.

    Args:
        order_id: The order to refund.
        amount: Dollar amount to refund (must be > 0).
    """
    if amount <= 0:
        return f"Error: refund amount must be positive, got {amount}"
    # Stub: in production this calls the payment processor
    return f"Refund of ${amount:.2f} for order {order_id} initiated — ETA: 3-5 business days."
