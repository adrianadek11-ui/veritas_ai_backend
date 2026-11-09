import pytest
from core.tax_swarm import tax_swarm
from core.crypto_social_channels import crypto_manager
from core.darknet_sandbox_swarm import darknet_sandbox_swarm

def test_tax_swarm_audit():
    result = tax_swarm.audit_transactions({"test": "data"})
    assert result["tax_swarm_status"] == "AUDIT_COMPLETED"
    assert result["compliance_score"] > 99.0

def test_crypto_rumor_evaluation():
    result = crypto_manager.evaluate_crypto_rumor("Test pump rumor")
    assert result["fake_news_probability"] > 80.0
    assert "CRYPTO_WATCHDOG" in result["channel_target"]

def test_darknet_sandbox_isolation():
    result = darknet_sandbox_swarm.execute_passive_deep_sweep()
    assert result["sandbox_swarm_status"] == "AIR_GAPPED_SANDBOX_ACTIVE"
    assert result["sanitized_intelligence_feed"]["law_enforcement_dispatch_ready"] is True
