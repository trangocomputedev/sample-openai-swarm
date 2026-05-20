"""Verify agent topology without making LLM calls."""
from src.agents import triage_agent, billing_agent, tech_agent, refund_agent


def _fn_names(agent) -> list[str]:
    return [f.__name__ for f in agent.functions]


def test_triage_agent_name():
    assert triage_agent.name == "TriageAgent"


def test_triage_has_transfer_functions():
    names = _fn_names(triage_agent)
    assert "_transfer_to_billing" in names
    assert "_transfer_to_tech" in names
    assert "_transfer_to_refunds" in names


def test_triage_can_set_customer_id():
    assert "set_customer_id" in _fn_names(triage_agent)


def test_billing_agent_has_account_lookup():
    assert "account_lookup" in _fn_names(billing_agent)


def test_billing_agent_can_create_ticket():
    assert "create_ticket" in _fn_names(billing_agent)


def test_billing_can_transfer_back():
    assert "_transfer_to_triage" in _fn_names(billing_agent)


def test_tech_agent_can_create_ticket():
    assert "create_ticket" in _fn_names(tech_agent)


def test_refund_agent_has_eligibility_check():
    assert "check_refund_eligibility" in _fn_names(refund_agent)


def test_refund_agent_can_process_refund():
    assert "process_refund" in _fn_names(refund_agent)


def test_transfer_to_billing_returns_billing_agent():
    from src.agents import _transfer_to_billing
    assert _transfer_to_billing() is billing_agent


def test_transfer_to_triage_returns_triage_agent():
    from src.agents import _transfer_to_triage
    assert _transfer_to_triage() is triage_agent
