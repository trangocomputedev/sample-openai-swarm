import json
import pytest


# --- account_lookup ---

def test_account_lookup_uses_context_customer_id():
    from src.tools.account import account_lookup
    result = account_lookup(context_variables={"customer_id": "C-9999"})
    data = json.loads(result)
    assert data["customer_id"] == "C-9999"


def test_account_lookup_fallback_unknown():
    from src.tools.account import account_lookup
    result = account_lookup(context_variables={})
    data = json.loads(result)
    assert data["customer_id"] == "unknown"


def test_account_lookup_returns_expected_fields():
    from src.tools.account import account_lookup
    data = json.loads(account_lookup(context_variables={"customer_id": "C-1"}))
    for field in ("name", "plan", "balance_due", "open_tickets"):
        assert field in data


# --- set_customer_id ---

def test_set_customer_id_updates_context():
    from src.tools.account import set_customer_id
    result = set_customer_id(context_variables={}, customer_id="C-42")
    assert result.context_variables["customer_id"] == "C-42"


def test_set_customer_id_returns_confirmation():
    from src.tools.account import set_customer_id
    result = set_customer_id(context_variables={}, customer_id="C-42")
    assert "C-42" in result.value


# --- create_ticket ---

def test_create_ticket_returns_ticket_id():
    from src.tools.tickets import create_ticket
    result = create_ticket(subject="Cannot login", description="Error 403")
    assert "TKT-" in result


def test_create_ticket_includes_priority():
    from src.tools.tickets import create_ticket
    result = create_ticket(subject="Test", description="Desc", priority="high")
    assert "high" in result


def test_create_ticket_ids_are_unique():
    from src.tools.tickets import create_ticket
    a = create_ticket(subject="A", description="a")
    b = create_ticket(subject="B", description="b")
    assert a != b


# --- refunds ---

def test_check_refund_eligibility_eligible():
    from src.tools.refunds import check_refund_eligibility
    result = json.loads(check_refund_eligibility(context_variables={}, order_id="ORD-001"))
    assert result["eligible"] is True
    assert result["order_id"] == "ORD-001"


def test_process_refund_returns_confirmation():
    from src.tools.refunds import process_refund
    result = process_refund(order_id="ORD-001", amount=49.99)
    assert "49.99" in result
    assert "ORD-001" in result


def test_process_refund_rejects_zero_amount():
    from src.tools.refunds import process_refund
    result = process_refund(order_id="ORD-001", amount=0)
    assert "Error" in result
