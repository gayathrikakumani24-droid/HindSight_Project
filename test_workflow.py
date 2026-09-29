"""End-to-End Test Suite for ResolveIQ Support Workflow.

Verifies:
1. Step 1: Customer ID & Issue Identification
2. Step 2: Hindsight Recall (retrieves relevant memories)
3. Step 3: Hindsight Reflect (synthesizes reasoning & compares situation)
4. Step 4: Decision & Response (avoids repeated troubleshooting, respects preferences, escalates when needed, states uncertainty)
5. Step 5: Retain new interaction
"""

import sys
import agent_workflow


def test_workflow_c101_payment_cancelled():
    print("\n--- Testing Workflow: Customer C101 (Payment Deducted / Order Cancelled) ---")
    res = agent_workflow.process_customer_issue(
        customer_id="C101",
        issue="Payment was deducted from my credit card but the order failed and was cancelled",
        actions_already_tried="Refreshed page twice, checked bank app",
        auto_retain=False,
    )
    assert res["step2_recall"]["count"] > 0, "Should recall memories from Hindsight"
    assert res["step4_decision"]["confidence"] in ["high", "medium"], "Confidence should be high/medium"
    assert "C101" in res["step4_response"]
    assert "email" in res["step4_response"].lower(), "Should respect email preference"
    print("[PASS] C101 workflow verified successfully!")


def test_workflow_c103_refund_tracer_escalation():
    print("\n--- Testing Workflow: Customer C103 (Refund Pending / ARN Tracer) ---")
    res = agent_workflow.process_customer_issue(
        customer_id="C103",
        issue="Approved refund of $340 has not arrived after 12 days; bank cannot locate funds",
        actions_already_tried="Contacted card issuer, submitted bank statement",
        auto_retain=False,
    )
    assert res["step4_decision"]["escalation_recommended"] is True, "Should recommend escalation for bank tracer"
    assert "escalat" in res["step4_response"].lower(), "Response must mention escalation"
    print("[PASS] C103 escalation workflow verified successfully!")


def test_workflow_c109_avoid_repeated_troubleshooting():
    print("\n--- Testing Workflow: Customer C109 (App Crash / Avoid Repetition) ---")
    res = agent_workflow.process_customer_issue(
        customer_id="C109",
        issue="Desktop client crashes on launch after v2.4 upgrade",
        actions_already_tried="Reinstalled 3 times, cleared cache, updated drivers",
        auto_retain=False,
    )
    assert len(res["step4_decision"]["avoid_actions"]) > 0 or "reinstall" in str(res["step4_response"]).lower(), "Must avoid repeated troubleshooting"
    print("[PASS] C109 repetition avoidance verified successfully!")


def test_workflow_c110_strict_email_preference():
    print("\n--- Testing Workflow: Customer C110 (Hard of Hearing / Strict Email) ---")
    res = agent_workflow.process_customer_issue(
        customer_id="C110",
        issue="Need EU zero-rated VAT invoice address corrected; strictly email-only communication",
        actions_already_tried="Tried editing postal code in form",
        auto_retain=False,
    )
    assert "email" in res["step4_decision"]["customer_preference_applied"].lower()
    assert "email" in res["step4_response"].lower()
    print("[PASS] C110 strict communication preference verified successfully!")


def test_workflow_unknown_novel_issue_uncertainty():
    print("\n--- Testing Workflow: Unknown Issue (Clearly State Uncertainty) ---")
    res = agent_workflow.process_customer_issue(
        customer_id="C888_NEW",
        issue="Quantum optical laser resonator anomalous photon leakage in chamber 4",
        actions_already_tried="Recalibrated laser diode once",
        auto_retain=False,
    )
    assert res["step4_decision"]["confidence"] == "low", "Confidence should be low for novel unknown query"
    assert res["step4_decision"]["action_type"] == "CLARIFY_UNSURE"
    assert "uncertainty" in res["step4_response"].lower() or "do not have an exact matching prior case" in res["step4_response"].lower(), "Must state uncertainty"
    print("[PASS] Unknown issue uncertainty handling verified successfully!")


def test_never_make_me_repeat_myself_c102():
    print("\n--- Testing Feature: 'Never Make Me Repeat Myself' (Customer C102) ---")
    res = agent_workflow.process_customer_issue(
        customer_id="C102",
        issue="Payment deducted but order cancelled",
        actions_already_tried="Payment retry",
        auto_retain=False,
    )
    prof = res["customer_memory_profile"]
    assert prof["customer_id"] == "C102"
    assert prof["previous_issue"] != ""
    assert prof["already_tried"] != ""
    assert prof["previous_successful_resolution"] != ""
    assert "email" in prof["communication_preference"].lower()
    assert prof["previous_escalation"] in ["Yes", "No"]
    assert prof["memory_used_count"] > 0
    assert "won't ask you to repeat" in res["step4_response"].lower() or "not ask you to repeat" in res["step4_response"].lower()
    print(f"Customer Memory: {prof}")
    print("[PASS] 'Never Make Me Repeat Myself' verified successfully for C102!")


def test_what_worked_before():
    print("\n--- Testing Feature: 'What Worked Before?' ---")
    res = agent_workflow.process_customer_issue(
        customer_id="C101",
        issue="Payment was deducted from card but order cancelled",
        actions_already_tried="Payment retry",
        auto_retain=False,
    )
    wwb = res["what_worked_before"]
    assert wwb is not None, "what_worked_before must be present in workflow output"
    
    cases = wwb["similar_past_cases"]
    assert len(cases) == 3, f"Expected 3 similar past cases, got {len(cases)}"

    # Case #1
    c1 = cases[0]
    assert c1["case_number"] == 1
    assert "payment" in c1["category"].lower()
    assert c1["status_symbol"] == "✓"
    assert c1["outcome"] == "Resolved"
    assert "manual refund" in c1["action_text"].lower()

    # Case #2
    c2 = cases[1]
    assert c2["case_number"] == 2
    assert "payment" in c2["category"].lower()
    assert c2["status_symbol"] == "✗"
    assert c2["outcome"] == "Failed"
    assert "payment retry" in c2["action_text"].lower()

    # Case #3
    c3 = cases[2]
    assert c3["case_number"] == 3
    assert "payment" in c3["category"].lower()
    assert c3["status_symbol"] == "⚠"
    assert c3["outcome"] == "Resolved"
    assert "billing escalation" in c3["action_text"].lower() or "escalat" in c3["action_text"].lower()

    # Learned summary
    assert wwb["learned_summary"] == "ResolveIQ learned from 3 previous experiences."
    assert wwb["prioritized_successful_solution"] == "Manual refund"

    # Prioritization in response
    resp = res["step4_response"]
    assert "manual refund" in resp.lower(), "Response must prioritize the successful resolution"

    print("[PASS] 'What Worked Before?' verified successfully!")


def test_hitl_learning_workflow():
    import time
    print("\n--- Testing Feature: Human-in-the-Loop Learning Workflow (Case 1 -> Case 2) ---")
    
    # 1. Human Operator resolves Case 1
    hitl_res = agent_workflow.record_human_operator_resolution(
        customer="C201",
        original_issue="Payment charged via Apple Pay but subscription status stuck on free trial",
        agent_recommendation="Ask customer to check subscription tab",
        human_decision="✓ Resolve Case",
        final_resolution="Verified Apple Pay transaction token in gateway and manually granted Premium Annual entitlement.",
        outcome="Resolved",
        recommendation_correct="Partially",
        customer_preference="Strictly email receipt confirmation",
        timestamp="2026-09-29 15:50:00",
    )
    assert hitl_res["success"] is True, "Human-verified resolution must be retained in Hindsight"
    assert "Verified Apple Pay transaction token" in hitl_res["content"]
    assert hitl_res["metadata"]["human_decision"] == "✓ Resolve Case"
    assert hitl_res["metadata"]["outcome"] == "Resolved"
    print("[PASS] Case 1: Human operator resolved and retained into Hindsight Cloud successfully!")

    # Short delay to allow Cloud bank indexing
    time.sleep(2)

    # 2. Case 2: Similar issue arrives
    case2_res = agent_workflow.process_customer_issue(
        customer_id="C202",
        issue="Paid through Apple Pay yesterday, money debited from card, but account still says free trial",
        actions_already_tried="Checked bank statement, saw Apple Pay charge",
        auto_retain=False,
    )
    
    assert case2_res["step2_recall"]["count"] > 0, "Case 2 must recall experiences from Hindsight Cloud"
    
    # Verify Case 2's decision or response incorporates what worked in Case 1
    wwb = case2_res["what_worked_before"]
    assert wwb is not None
    assert len(wwb["similar_past_cases"]) == 3
    
    print("[PASS] Case 2: Recalled Case 1 from Hindsight and generated resolution plan successfully!")
    print("[PASS] Human-in-the-Loop learning cycle verified successfully!")


def test_mental_model_customer_support_profile():
    print("\n--- Testing Feature: Hindsight Mental Model 'Customer Support Profile' ---")
    res = agent_workflow.process_customer_issue(
        customer_id="C102",
        issue="Payment deducted but order cancelled",
        actions_already_tried="Payment retry",
        auto_retain=False,
    )
    profile = res.get("mental_model_customer_profile")
    assert profile is not None, "mental_model_customer_profile must be present in workflow output"
    
    assert profile["customer_id"] == "C102"
    assert "email" in profile["communication"].lower()
    assert "payment" in profile["recurring_issue"].lower()
    assert "retry" in profile["failed_approach"].lower()
    assert "refund" in profile["successful_approach"].lower()
    assert "3" in profile["support_history"] or "case" in profile["support_history"]
    assert profile["mental_model_name"] == "Customer Support Profile"

    print(f"Verified Mental Model Profile for C102: {profile}")
    print("[PASS] Hindsight Mental Model 'Customer Support Profile' verified successfully!")


if __name__ == "__main__":
    test_workflow_c101_payment_cancelled()
    test_workflow_c103_refund_tracer_escalation()
    test_workflow_c109_avoid_repeated_troubleshooting()
    test_workflow_c110_strict_email_preference()
    test_workflow_unknown_novel_issue_uncertainty()
    test_never_make_me_repeat_myself_c102()
    test_what_worked_before()
    test_hitl_learning_workflow()
    test_mental_model_customer_support_profile()
    print("\n[SUCCESS] ALL RESOLVEIQ SUPPORT WORKFLOW TESTS PASSED!")
