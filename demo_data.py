"""Demo Data Seeder for ResolveIQ.

Provides 10 realistic historical customer support cases representing EXPERIENCE MEMORY
rather than basic FAQ documents.

Covers:
1. Payment deducted but order cancelled
2. Duplicate payment
3. Refund pending
4. Wrong product delivered
5. Delayed delivery
6. Account locked
7. Subscription cancellation
8. Failed payment
9. Previous troubleshooting failed
10. Customer requested email-only communication
"""

from typing import Any, Dict, List, Optional
import memory_service

DEMO_SUPPORT_CASES: List[Dict[str, Any]] = [
    {
        "document_id": "demo_case_c101",
        "customer_id": "C101",
        "category": "Payment & Order",
        "issue": "Payment deducted from credit card ($129.00), but website showed order failed/cancelled.",
        "actions_attempted": [
            "Customer refreshed page multiple times",
            "Checked banking mobile app to confirm deduction",
            "Attempted to re-order but hesitated due to double-charge risk",
        ],
        "resolution": "Traced Stripe checkout session ID; found order creation webhook timed out while charge captured. Manually initiated gateway refund of $129.00 and regenerated shopping cart with priority shipping waiver and 10% apology voucher.",
        "outcome": "Refund processed in 3 business days; customer re-ordered with discount voucher successfully.",
        "customer_preferences": "Prefers email-only communication; requested no automated telemarketing calls.",
        "escalation_required": False,
        "additional_notes": "Tier-1 billing specialist handled directly using payment gateway portal.",
        "tags": ["demo", "billing", "order_cancelled", "refund"],
    },
    {
        "document_id": "demo_case_c102",
        "customer_id": "C102",
        "category": "Duplicate Charge",
        "issue": "Duplicate payment: charged twice ($89.50 x 2) for a single checkout transaction.",
        "actions_attempted": [
            "Customer submitted bank screenshot displaying two concurrent pending charges",
            "Waited 24 hours to see if one charge would auto-drop",
        ],
        "resolution": "Audited payment gateway authorization logs; identified duplicate idempotency key sent during network reconnect. Voided the second pending transaction immediately before settlement capture.",
        "outcome": "Second authorization voided within 2 hours; zero overdraft fees incurred; customer received release confirmation.",
        "customer_preferences": "Wants immediate email receipt with transaction reference ID for accountant.",
        "escalation_required": True,
        "additional_notes": "Escalated to Finance Ops for manual ledger reconciliation and idempotency audit.",
        "tags": ["demo", "billing", "duplicate_charge", "void"],
    },
    {
        "document_id": "demo_case_c103",
        "customer_id": "C103",
        "category": "Refund Pending",
        "issue": "Refund pending: approved refund of $340.00 has not arrived after 12 business days (promised 5-7 days).",
        "actions_attempted": [
            "Customer contacted card issuer who claimed merchant had not released funds",
            "Submitted bank statement showing no incoming credit",
        ],
        "resolution": "Retrieved formal Acquirer Reference Number (ARN: 745123987123987) from payment processor. Generated formal bank tracer document containing ARN and processor timestamp for customer's bank.",
        "outcome": "Customer presented ARN to bank manager; bank located held batch and posted funds within 24 hours.",
        "customer_preferences": "Prefers SMS alert with tracking code, followed by comprehensive email.",
        "escalation_required": True,
        "additional_notes": "Payments Operations Tier-2 generated the formal ARN tracer certificate.",
        "tags": ["demo", "refund", "arn_tracer", "banking"],
    },
    {
        "document_id": "demo_case_c104",
        "customer_id": "C104",
        "category": "Fulfillment",
        "issue": "Wrong product delivered: ordered ErgoPro Mechanical Keyboard (Blue Switches), received Membrane Keyboard (Model M-10).",
        "actions_attempted": [
            "Customer unboxed unit and verified barcode mismatch against packing slip",
            "Uploaded photos of box and SKU label to helpdesk portal",
        ],
        "resolution": "Authorized immediate cross-ship replacement of ErgoPro Keyboard with expedited 2-day transit without waiting for wrong item return. Provided prepaid return label with courier pickup at doorstep.",
        "outcome": "Correct keyboard delivered in 48 hours; incorrect unit picked up by courier with zero customer friction.",
        "customer_preferences": "Works night shift; strictly DO NOT call between 8:00 AM and 4:00 PM; use in-app notifications.",
        "escalation_required": False,
        "additional_notes": "Handled under frontline Expedited Mismatch Replacement policy.",
        "tags": ["demo", "shipping", "wrong_item", "cross_ship"],
    },
    {
        "document_id": "demo_case_c105",
        "customer_id": "C105",
        "category": "Logistics",
        "issue": "Delayed delivery: high-priority parcel stuck at regional distribution hub for 6 days with no status updates.",
        "actions_attempted": [
            "Customer refreshed carrier tracking link daily",
            "Filed automated lost package inquiry with carrier with no response",
        ],
        "resolution": "Contacted dedicated regional logistics freight manager; located package held in sorting backlog; re-routed shipment onto high-priority Saturday morning express dispatch.",
        "outcome": "Package delivered Saturday morning at 10:15 AM before customer's business trip.",
        "customer_preferences": "Prefers WhatsApp direct messaging for time-critical tracking alerts.",
        "escalation_required": True,
        "additional_notes": "Logistics team lead escalated directly to carrier hub dispatch supervisor.",
        "tags": ["demo", "logistics", "delayed_shipment", "rerouted"],
    },
    {
        "document_id": "demo_case_c106",
        "customer_id": "C106",
        "category": "Account Access & Security",
        "issue": "Account locked: customer locked out after 5 unsuccessful login attempts; SMS 2FA codes never arrive.",
        "actions_attempted": [
            "Customer initiated password reset 4 times",
            "Switched between WiFi and mobile cellular network",
            "Carrier spam filter was silently dropping short-code SMS verification",
        ],
        "resolution": "Conducted secure out-of-band video identity verification; temporarily bypassed SMS 2FA lock; enrolled customer in Authenticator App (TOTP / Google Authenticator) and established backup recovery codes.",
        "outcome": "Customer regained full workspace access within 20 minutes with enhanced security.",
        "customer_preferences": "Hates SMS 2FA due to travel roaming; prefers hardware security key or TOTP app.",
        "escalation_required": True,
        "additional_notes": "Security & Trust engineer authorized identity override and TOTP reset.",
        "tags": ["demo", "security", "account_locked", "2fa_override"],
    },
    {
        "document_id": "demo_case_c107",
        "customer_id": "C107",
        "category": "Subscription",
        "issue": "Subscription cancellation: customer intended to cancel before annual auto-renew ($360/yr) but timezone difference triggered renewal charge 6 hours early.",
        "actions_attempted": [
            "Attempted to downgrade subscription in workspace billing tab after charge went through",
            "Submitted ticket immediately requesting cancellation and reversal",
        ],
        "resolution": "Approved immediate cancellation of Enterprise Annual renewal; executed full refund of $360.00; converted account to legacy grandfathered Free Tier to ensure zero loss of customer projects and history.",
        "outcome": "Refund credited in 48 hours; workspace downgraded cleanly with full data preserved.",
        "customer_preferences": "Strictly email communication; requested formal refund receipt for corporate accounting audit.",
        "escalation_required": False,
        "additional_notes": "Tier-1 billing representative processed within courtesy refund policy window.",
        "tags": ["demo", "subscription", "cancellation", "courtesy_refund"],
    },
    {
        "document_id": "demo_case_c108",
        "customer_id": "C108",
        "category": "Payment Failure",
        "issue": "Failed recurring payment: subscription renewal failing with generic 'Card Declined: Do Not Honor' error.",
        "actions_attempted": [
            "Customer re-entered credit card details twice",
            "Tried a second corporate debit card which also failed",
            "Customer received account suspension warning banner",
        ],
        "resolution": "Diagnosed bank merchant classification block: issuing bank was blocking overseas software charges. Guided customer to call card fraud desk to authorize merchant ID; extended billing grace period by 7 days to prevent service outage.",
        "outcome": "Customer unblocked international merchant with bank; invoice re-charge succeeded on first retry.",
        "customer_preferences": "Email receipts with European VAT ID and company tax number displayed.",
        "escalation_required": False,
        "additional_notes": "Resolved by frontline support with grace period extension.",
        "tags": ["demo", "billing", "declined_card", "grace_period"],
    },
    {
        "document_id": "demo_case_c109",
        "customer_id": "C109",
        "category": "Technical Troubleshooting",
        "issue": "Previous troubleshooting failed: Desktop client crashes on launch following v2.4 upgrade; official knowledge base fix failed.",
        "actions_attempted": [
            "Customer followed standard KB guide: uninstalled and reinstalled app 3 times",
            "Cleared browser and local temporary cache",
            "Updated GPU display drivers and restarted Windows - crash persisted",
        ],
        "resolution": "Examined client crash dump logs; identified stale database lock file in '%APPDATA%/ResolveIQ/locks/db.lock' causing SQLite assertion error. Provided command to delete lock directory and launched with '--safe-mode'.",
        "outcome": "Desktop app launched instantly; corrupt lock cleared permanently; customer saved from full OS reinstall.",
        "customer_preferences": "Technical communicator; prefers exact terminal commands and log file paths via email.",
        "escalation_required": True,
        "additional_notes": "Tier-2 technical support engineer diagnosed crash dump assertion.",
        "tags": ["demo", "technical", "app_crash", "sqlite_lock"],
    },
    {
        "document_id": "demo_case_c110",
        "customer_id": "C110",
        "category": "Accessibility & Preferences",
        "issue": "Customer requested strict email-only communication and billing address correction for EU cross-border tax exemption.",
        "actions_attempted": [
            "Customer attempted to edit billing address in web form, but postal regex rejected UK/EU alphanumeric postcodes",
            "Received unsolicited outbound phone call from support agent despite being deaf / hard of hearing",
        ],
        "resolution": "Manually corrected alphanumeric postal code in customer profile; validated VIES VAT registration number for zero-rated cross-border invoice; permanently marked profile with high-visibility flag: 'STRICTLY EMAIL-ONLY: HARD OF HEARING CUSTOMER - NEVER CALL'.",
        "outcome": "Valid zero-rated VAT invoice issued; communication preferences permanently enforced across team.",
        "customer_preferences": "STRICTLY EMAIL-ONLY. Under no circumstances should voice calls or phone SMS be attempted due to hearing impairment.",
        "escalation_required": True,
        "additional_notes": "Escalated to Database Admin to override UI postcode regex and tag account profile.",
        "tags": ["demo", "accessibility", "email_only", "tax_vat"],
    },
]


def seed_demo_memories(
    bank_id: Optional[str] = None,
    service: Optional[Any] = None,
) -> Dict[str, Any]:
    """Store all 10 experience-oriented demo cases into Hindsight Cloud.

    Uses fixed document_ids and update_mode='replace' to avoid duplicate memories
    when clicked multiple times.
    """
    mem_service = service or memory_service._default_service
    target_bank = bank_id or mem_service.bank_id

    stored_cases = []
    errors = []

    for case in DEMO_SUPPORT_CASES:
        try:
            res = mem_service.retain_resolution(
                customer_id=case["customer_id"],
                issue=case["issue"],
                resolution=case["resolution"],
                outcome=case["outcome"],
                actions_attempted=case["actions_attempted"],
                customer_preferences=case["customer_preferences"],
                escalation_required=case["escalation_required"],
                additional_notes=f"Category: {case['category']} | {case['additional_notes']}",
                bank_id=target_bank,
                tags=case["tags"],
                document_id=case["document_id"],
                update_mode="replace",
            )
            stored_cases.append({
                "customer_id": case["customer_id"],
                "issue": case["issue"],
                "document_id": case["document_id"],
                "status": "stored",
            })
        except Exception as e:
            errors.append({
                "customer_id": case["customer_id"],
                "error": str(e),
            })

    return {
        "success": len(errors) == 0,
        "total_cases": len(DEMO_SUPPORT_CASES),
        "stored_count": len(stored_cases),
        "error_count": len(errors),
        "stored_cases": stored_cases,
        "errors": errors,
        "bank_id": target_bank,
    }
