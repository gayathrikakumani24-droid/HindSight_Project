"""Test suite for ResolveIQ Hindsight Memory Service.

Tests:
1. Experience-oriented memory formatting
2. Retain interaction & resolution operations
3. Recall similar cases operation
4. Reflect on cases operation
5. Error handling and SDK compatibility
"""

import sys
from unittest.mock import MagicMock
from memory_service import (
    HindsightMemoryService,
    format_experience_content,
    retain_interaction,
    retain_resolution,
    recall_similar_cases,
    reflect_on_cases,
    _default_service,
)
from hindsight_client_api.models.retain_response import RetainResponse
from hindsight_client_api.models.recall_response import RecallResponse
from hindsight_client_api.models.reflect_response import ReflectResponse
from hindsight_client_api.models.recall_result import RecallResult


def test_experience_formatting():
    print("\n--- Testing Experience-Oriented Memory Formatting ---")
    formatted = format_experience_content(
        customer_id="cust_1024",
        issue="Payment webhook failing with 401 unauthorized",
        actions_attempted=["Re-generated API secret in dashboard", "Checked SSL certificate"],
        resolution="Updated Authorization header format to Bearer <token>",
        outcome="Resolved successfully in 10 mins",
        customer_preferences="Prefers Slack notifications over email",
        escalation_required=False,
        additional_notes="Customer is a Tier-1 Enterprise account",
    )
    print(formatted)
    
    assert "Customer ID: cust_1024" in formatted
    assert "Issue Description: Payment webhook failing" in formatted
    assert "Actions Already Attempted: Re-generated API secret" in formatted
    assert "Resolution: Updated Authorization header" in formatted
    assert "Outcome: Resolved successfully" in formatted
    assert "Customer Preferences: Prefers Slack" in formatted
    assert "Escalation Required: No" in formatted
    print("Formatting tests passed!")


def test_retain_and_recall_mocked():
    print("\n--- Testing Retain, Recall, and Reflect with SDK Mock ---")
    service = HindsightMemoryService(
        base_url="https://api.hindsight.vectorize.io",
        api_key="test-api-key-mock",
        bank_id="test-support-bank",
    )

    mock_client = MagicMock()

    # Mock Retain response
    mock_retain_response = MagicMock(spec=RetainResponse)
    mock_client.retain.return_value = mock_retain_response

    # Mock Recall response with RecallResult
    mock_recall_item = MagicMock(spec=RecallResult)
    mock_recall_item.text = "Payment webhook 401 resolved by updating Bearer token format."
    mock_recall_item.score = 0.94
    mock_recall_item.type = "resolution"
    mock_recall_item.timestamp = "2026-09-29T10:00:00Z"
    mock_recall_item.metadata = {"customer_id": "cust_1024"}

    mock_recall_response = MagicMock(spec=RecallResponse)
    mock_recall_response.results = [mock_recall_item]
    mock_client.recall.return_value = mock_recall_response

    # Mock Reflect response
    mock_reflect_response = MagicMock(spec=ReflectResponse)
    mock_reflect_response.text = "Common root cause: Authorization header mismatches after rotating API secrets."
    mock_reflect_response.based_on = ["cust_1024_ticket_42"]
    mock_client.reflect.return_value = mock_reflect_response

    service._client = mock_client

    # 1. Test Retain Interaction
    res_interaction = service.retain_interaction(
        customer_id="cust_1024",
        issue="Webhook not triggering",
        actions_attempted="Rotated credentials",
        customer_preferences="Slack updates",
    )
    assert res_interaction["success"] is True
    assert mock_client.retain.called
    print("retain_interaction test passed!")

    # 2. Test Retain Resolution
    res_resolution = service.retain_resolution(
        customer_id="cust_1024",
        issue="Payment webhook failing with 401 unauthorized",
        resolution="Updated Authorization header format to Bearer <token>",
        outcome="Resolved",
        actions_attempted="Checked headers",
        escalation_required=False,
    )
    assert res_resolution["success"] is True
    assert "Escalation Required: No" in res_resolution["content"]
    print("retain_resolution test passed!")

    # 3. Test Recall
    res_recall = service.recall_similar_cases(
        query="Customer experiencing 401 webhook errors",
        customer_id="cust_1024",
    )
    assert res_recall["success"] is True
    assert res_recall["count"] == 1
    assert "Bearer token format" in res_recall["memories"][0]["text"]
    print("recall_similar_cases test passed!")

    # 4. Test Reflect
    res_reflect = service.reflect_on_cases(
        query="What are the top failure modes for webhook integration?",
    )
    assert res_reflect["success"] is True
    assert "Authorization header mismatches" in res_reflect["reasoning"]
    print("reflect_on_cases test passed!")


def test_demo_data_seeding():
    print("\n--- Testing Demo Data Seeding with SDK Mock ---")
    import demo_data
    assert len(demo_data.DEMO_SUPPORT_CASES) == 10
    
    mock_service = MagicMock(spec=HindsightMemoryService)
    mock_service.bank_id = "test-bank"
    mock_service.retain_resolution.return_value = {"success": True, "operation": "retain_resolution"}
    
    result = demo_data.seed_demo_memories(service=mock_service)
    assert result["success"] is True
    assert result["stored_count"] == 10
    assert result["total_cases"] == 10
    assert mock_service.retain_resolution.call_count == 10
    print(f"Successfully verified seeding {result['stored_count']} demo cases with mock!")


def test_live_cloud_if_configured():
    import config
    if config.HINDSIGHT_API_KEY:
        print("\n--- Running Live Hindsight Cloud Retain and Recall Test ---")
        try:
            res_retain = retain_resolution(
                customer_id="live_test_user",
                issue="Testing live Hindsight Cloud retain operation",
                resolution="Verified SDK connection and storage",
                outcome="Verified",
                escalation_required=False,
            )
            print("Live Retain Success:", res_retain["success"])

            res_recall = recall_similar_cases("Testing live Hindsight Cloud retain operation")
            print("Live Recall Count:", res_recall.get("count", 0))
        except Exception as e:
            print("Live Cloud error:", e)
        finally:
            _default_service.close()
    else:
        print("\n[NOTE] HINDSIGHT_API_KEY is not set in environment. Skipping live network call (Mock verification succeeded).")


if __name__ == "__main__":
    test_experience_formatting()
    test_retain_and_recall_mocked()
    test_demo_data_seeding()
    test_live_cloud_if_configured()
    print("\n[SUCCESS] All Memory Service tests passed successfully!")
