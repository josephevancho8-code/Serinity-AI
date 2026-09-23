import pytest
from serinity.core.policy import PolicyEngine


def test_default_baseline_permissions():
    policy = PolicyEngine()
    assert policy.is_allowed("conversation") is True
    assert policy.is_allowed("local_research") is True
    assert policy.is_allowed("code_generation") is True
    assert policy.is_allowed("sandbox_execution") is True


def test_default_disabled_permissions():
    policy = PolicyEngine()
    assert policy.is_allowed("background_learning") is False
    assert policy.is_allowed("phone_observation") is False


def test_immutable_hard_deny():
    policy = PolicyEngine()

    assert policy.is_allowed("delete_data") is False
    assert policy.is_allowed("purchases") is False
    assert policy.is_allowed("system_modification") is False

    policy.update_permissions({
        "delete_data": True,
        "purchases": True,
        "system_modification": True,
    })

    assert policy.is_allowed("delete_data") is False
    assert policy.is_allowed("purchases") is False
    assert policy.is_allowed("system_modification") is False


def test_dynamic_permission_toggling():
    policy = PolicyEngine()
    assert policy.is_allowed("background_learning") is False

    policy.update_permissions({"background_learning": True})
    assert policy.is_allowed("background_learning") is True

    policy.update_permissions({"background_learning": False})
    assert policy.is_allowed("background_learning") is False
