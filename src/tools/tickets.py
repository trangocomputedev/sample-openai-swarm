import uuid


def create_ticket(subject: str, description: str, priority: str = "medium") -> str:
    """Create a support ticket and return the assigned ticket ID.

    Args:
        subject: Short summary of the issue (< 80 chars).
        description: Full description of the problem.
        priority: One of 'low', 'medium', 'high'. Defaults to 'medium'.
    """
    ticket_id = f"TKT-{uuid.uuid4().hex[:8].upper()}"
    # Stub: in production this writes to Zendesk / Jira
    return f"Ticket {ticket_id} created — priority: {priority} | Subject: {subject}"
