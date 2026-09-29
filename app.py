"""ResolveIQ - Memory-Powered Customer Support Agent.

Hackathon MVP powered by Streamlit and Hindsight Cloud.
"Support that learns from every resolution and never makes customers repeat themselves."
"""

import streamlit as st
import config
from hindsight_service import hindsight_service
import memory_service
import demo_data
import agent_workflow

# Page Configuration
st.set_page_config(
    page_title="ResolveIQ - Memory-Powered Support",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for polished hackathon MVP look
st.markdown(
    """
    <style>
    .main-title {
        font-size: 2.3rem;
        font-weight: 800;
        margin-bottom: 0.2rem;
        color: #1E293B;
    }
    .sub-title {
        font-size: 1.15rem;
        font-weight: 400;
        color: #475569;
        margin-bottom: 1.5rem;
    }
    .status-card {
        padding: 1rem;
        border-radius: 8px;
        background-color: #F8FAFC;
        border: 1px solid #E2E8F0;
        margin-bottom: 1rem;
    }
    .pipeline-step {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 8px;
        padding: 1.2rem;
        margin-bottom: 1.2rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    .memory-box {
        background-color: #F1F5F9;
        border-left: 4px solid #3B82F6;
        padding: 0.8rem 1rem;
        border-radius: 4px;
        margin-bottom: 0.8rem;
    }
    .response-box {
        background-color: #F0FDF4;
        border: 1px solid #BBF7D0;
        border-left: 5px solid #16A34A;
        padding: 1.2rem;
        border-radius: 6px;
        margin-top: 1rem;
    }
    .avoid-badge {
        background-color: #FEE2E2;
        color: #991B1B;
        padding: 0.2rem 0.6rem;
        border-radius: 4px;
        font-weight: 600;
        font-size: 0.85rem;
        display: inline-block;
        margin: 0.2rem 0.2rem 0.2rem 0;
    }
    .pref-badge {
        background-color: #E0E7FF;
        color: #3730A3;
        padding: 0.2rem 0.6rem;
        border-radius: 4px;
        font-weight: 600;
        font-size: 0.85rem;
        display: inline-block;
        margin: 0.2rem 0.2rem 0.2rem 0;
    }
    .escalate-badge {
        background-color: #FEF3C7;
        color: #92400E;
        padding: 0.2rem 0.6rem;
        border-radius: 4px;
        font-weight: 600;
        font-size: 0.85rem;
        display: inline-block;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Sidebar: Health & Configuration Status
with st.sidebar:
    st.markdown("### 🧠 ResolveIQ System Status")

    is_configured = hindsight_service.is_configured()
    env_status = config.get_environment_status()

    # Health Indicator
    if is_configured:
        st.success("🟢 Hindsight Cloud: Ready")
    else:
        st.warning("🟡 Hindsight Cloud: Missing API Key")

    st.markdown("---")
    st.markdown("#### ⚙️ Configuration")

    st.markdown(f"**Bank ID:** `{env_status['hindsight_bank_id']}`")
    st.markdown(f"**Base URL:** `{env_status['hindsight_base_url']}`")
    st.markdown(f"**API Key:** `{env_status['hindsight_api_key_masked']}`")

    # LLM Providers detection
    llm_detected = []
    if env_status["openai_configured"]:
        llm_detected.append("OpenAI")
    if env_status["groq_configured"]:
        llm_detected.append("Groq")
    if env_status["anthropic_configured"]:
        llm_detected.append("Anthropic")

    if llm_detected:
        st.markdown(f"**LLM Detected:** `{', '.join(llm_detected)}`")
    else:
        st.markdown("**LLM Detected:** `Hindsight Reflect (Native)`")

    st.markdown("---")

    # Demo Seeding Section in Sidebar
    st.markdown("#### 🌱 Demo Seeder")
    st.caption("Store 10 benchmark experience memories in Hindsight Cloud with duplicate prevention.")
    if st.button("🌱 Seed Demo Memories", type="primary", use_container_width=True, key="sidebar_seed_btn"):
        if not is_configured:
            st.error("Please configure HINDSIGHT_API_KEY in .env before seeding.")
        else:
            with st.spinner("Seeding 10 demo cases into Hindsight Cloud..."):
                result = demo_data.seed_demo_memories()
                st.session_state["seed_result"] = result
                if result["success"]:
                    st.success(f"Stored {result['stored_count']} of {result['total_cases']} cases!")
                else:
                    st.warning(f"Stored {result['stored_count']} cases with {result['error_count']} errors.")

    st.markdown("---")

    # Connection Health Test Button
    st.markdown("#### 🩺 Health Check")
    if st.button("Test Hindsight Connection", use_container_width=True):
        with st.spinner("Pinging Hindsight Cloud..."):
            success, message = hindsight_service.test_connection()
            if success:
                st.success(message)
            else:
                st.error(message)

    # Quick Setup Helper
    with st.expander("ℹ️ Setup Instructions"):
        st.markdown(
            """
            1. Copy `.env.example` to `.env`:
               ```bash
               cp .env.example .env
               ```
            2. Add your **Hindsight API Key** & **Bank ID**:
               ```env
               HINDSIGHT_API_KEY=your_key_here
               HINDSIGHT_BANK_ID=resolveiq-support-bank
               ```
            3. Restart the Streamlit app.
            """
        )

# Main App Header with Prominent Demo Mode Toggle
col_head1, col_head2 = st.columns([3, 1])
with col_head1:
    st.markdown('<div class="main-title">ResolveIQ 🧠</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="sub-title"><em>"Support that learns from every resolution and never makes customers repeat themselves."</em></div>',
        unsafe_allow_html=True,
    )
with col_head2:
    st.markdown("<div style='margin-top: 12px;'></div>", unsafe_allow_html=True)
    demo_mode_toggle = st.toggle("🎬 Demo Mode", value=st.session_state.get("demo_mode_active", False), key="demo_mode_toggle")
    st.session_state["demo_mode_active"] = demo_mode_toggle

# Status banner on top of main window
if not is_configured:
    st.info(
        "👋 **Hindsight Cloud credentials are not configured yet.** "
        "Set `HINDSIGHT_API_KEY` in `.env` to execute live Cloud operations.",
        icon="ℹ️",
    )
else:
    st.success(
        f"✅ Connected to Hindsight Memory Bank: **{config.HINDSIGHT_BANK_ID}**",
        icon="🚀",
    )

# Value Proposition Cards
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(
        """
        <div class="status-card">
            <h4>💡 1. RECALL EXPERIENCES</h4>
            <p>Retrieves past customer attempts, verified fixes, and communication preferences so customers never repeat themselves.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
with col2:
    st.markdown(
        """
        <div class="status-card">
            <h4>🔍 2. REFLECT & COMPARE</h4>
            <p>Synthesizes reasoning over retrieved cases and compares current symptoms rather than blindly copying past fixes.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
with col3:
    st.markdown(
        """
        <div class="status-card">
            <h4>🔄 3. RESOLVE & RETAIN</h4>
            <p>Delivers a personalized response respecting preferences and automatically retains the new resolution for continuous learning.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

# Main Application Tabs
tab_demo, tab_workflow, tab_recall, tab_reflect, tab_demo_cases, tab_diagnostics = st.tabs([
    "🎬 Demo Mode (Judge Story)",
    "⚡ 1. ResolveIQ Workflow (Support Agent)",
    "🔍 2. Recall Memory Explorer",
    "🧠 3. Hindsight Reflect Engine",
    "📚 4. Seeded Cases Library",
    "🛠️ 5. Diagnostics & Health",
])

# =============================================================================
# TAB 0: DEDICATED DEMO MODE - THE JUDGE STORY
# =============================================================================
with tab_demo:
    st.markdown("### 🎬 Demo Mode: The Judge Experience Walkthrough")
    st.caption("A guided 5-step demonstration showing how persistent Hindsight memory changes customer support outcomes.")

    # Visual storyline progression banner
    st.markdown(
        """
        <div style="background: linear-gradient(90deg, #1E3A8A, #2563EB, #059669); color: white; padding: 0.9rem 1.25rem; border-radius: 8px; font-weight: 700; font-size: 0.95rem; text-align: center; margin-bottom: 1.25rem; letter-spacing: 0.03em;">
            BEFORE MEMORY &nbsp;➔&nbsp; Human Resolution &nbsp;➔&nbsp; HINDSIGHT RETAIN &nbsp;➔&nbsp; HINDSIGHT RECALL &nbsp;➔&nbsp; Better Future Support
        </div>
        """,
        unsafe_allow_html=True,
    )

    demo_btn_col1, demo_btn_col2 = st.columns([3, 1])
    with demo_btn_col1:
        run_full_demo = st.button("🚀 Run Entire Judge Story (1-Click Walkthrough)", type="primary", use_container_width=True)
    with demo_btn_col2:
        reset_demo = st.button("🔄 Reset Demo State", use_container_width=True)

    if reset_demo:
        st.session_state["demo_step1_res"] = None
        st.session_state["demo_step2_res"] = None
        st.session_state["demo_step3_res"] = None
        st.rerun()

    if run_full_demo:
        with st.spinner("Executing Full Judge Story against Hindsight Cloud..."):
            # Step 1: Customer C001 initial query
            s1_res = agent_workflow.process_customer_issue(
                customer_id="C001",
                issue="My payment was deducted but my order was cancelled.",
                actions_already_tried="Refreshed checkout, checked mobile banking",
                auto_retain=False,
            )
            st.session_state["demo_step1_res"] = s1_res

            # Step 2: Human Operator resolves it
            import datetime
            now_ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            s2_res = agent_workflow.record_human_operator_resolution(
                customer="C001",
                original_issue="My payment was deducted but my order was cancelled.",
                agent_recommendation="Initial payment verification",
                human_decision="✓ Resolve Case",
                final_resolution="Manual refund initiated. Customer prefers email.",
                outcome="Resolved",
                recommendation_correct="Yes",
                customer_preference="Prefers email",
                timestamp=now_ts,
            )
            st.session_state["demo_step2_res"] = s2_res

            # Small delay to let bank commit
            import time
            time.sleep(1.5)

            # Step 3, 4, 5: Customer C001 has similar future case
            s3_res = agent_workflow.process_customer_issue(
                customer_id="C001",
                issue="My payment was deducted again and my order was cancelled.",
                actions_already_tried="Payment retry",
                auto_retain=True,
            )
            st.session_state["demo_step3_res"] = s3_res
            st.rerun()

    # Step by Step controls
    s_col1, s_col2, s_col3 = st.columns(3)
    with s_col1:
        if st.button("1️⃣ Run Step 1 (Before Memory)", use_container_width=True):
            with st.spinner("Running Step 1..."):
                s1_res = agent_workflow.process_customer_issue(
                    customer_id="C001",
                    issue="My payment was deducted but my order was cancelled.",
                    actions_already_tried="Refreshed checkout, checked mobile banking",
                    auto_retain=False,
                )
                st.session_state["demo_step1_res"] = s1_res
                st.rerun()
    with s_col2:
        if st.button("2️⃣ Run Step 2 (Human Resolution)", use_container_width=True):
            with st.spinner("Storing Human Resolution in Hindsight..."):
                import datetime
                now_ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                s2_res = agent_workflow.record_human_operator_resolution(
                    customer="C001",
                    original_issue="My payment was deducted but my order was cancelled.",
                    agent_recommendation="Initial payment verification",
                    human_decision="✓ Resolve Case",
                    final_resolution="Manual refund initiated. Customer prefers email.",
                    outcome="Resolved",
                    recommendation_correct="Yes",
                    customer_preference="Prefers email",
                    timestamp=now_ts,
                )
                st.session_state["demo_step2_res"] = s2_res
                st.rerun()
    with s_col3:
        if st.button("3️⃣ Run Steps 3-5 (Recall & Retain)", use_container_width=True):
            with st.spinner("Running Similar Case with Hindsight Memory..."):
                s3_res = agent_workflow.process_customer_issue(
                    customer_id="C001",
                    issue="My payment was deducted again and my order was cancelled.",
                    actions_already_tried="Payment retry",
                    auto_retain=True,
                )
                st.session_state["demo_step3_res"] = s3_res
                st.rerun()

    # -----------------------------------------------------------------
    # STEP 1: BEFORE MEMORY
    # -----------------------------------------------------------------
    st.markdown("---")
    st.markdown("#### 1️⃣ STEP 1 — BEFORE MEMORY")
    st.markdown("**Customer C001:** *\"My payment was deducted but my order was cancelled.\"*")

    s1_res = st.session_state.get("demo_step1_res")
    if s1_res:
        c1_box, c2_box = st.columns(2)
        with c1_box:
            st.markdown(
                f"""
                <div style="background-color: #F8FAFC; border: 1px solid #CBD5E1; border-radius: 6px; padding: 0.9rem;">
                    <strong>Current Issue:</strong><br>
                    <span>My payment was deducted but my order was cancelled.</span><br><br>
                    <strong>Memories Recalled from Bank:</strong><br>
                    <span style="color: #64748B;">{s1_res['step2_recall']['count']} prior memories found for Customer C001</span><br><br>
                    <strong>Agent Recommendation:</strong><br>
                    <span style="font-weight: 600; color: #1E293B;">{s1_res['step4_decision']['recommended_fix']}</span>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with c2_box:
            st.markdown(
                f"""
                <div class="response-box" style="margin-top: 0; min-height: 190px;">
                    <strong>Customer Response:</strong>
                    <pre style="white-space: pre-wrap; font-family: inherit; font-size: 0.9rem; margin-top: 0.5rem; color:#0F172A;">{s1_res['step4_response']}</pre>
                </div>
                """,
                unsafe_allow_html=True,
            )
    else:
        st.info("Click **'1️⃣ Run Step 1 (Before Memory)'** or **'🚀 Run Entire Judge Story'** above to execute Step 1.")

    # -----------------------------------------------------------------
    # STEP 2: HUMAN RESOLUTION
    # -----------------------------------------------------------------
    st.markdown("---")
    st.markdown("#### 2️⃣ STEP 2 — HUMAN RESOLUTION")
    st.markdown("**Human Operator Resolution:** *\"Manual refund initiated. Customer prefers email.\"*")

    s2_res = st.session_state.get("demo_step2_res")
    if s2_res:
        st.markdown(
            f"""
            <div style="background: linear-gradient(135deg, #ECFDF5, #D1FAE5); border: 2px solid #10B981; border-radius: 8px; padding: 1.25rem;">
                <div style="font-size: 1.25rem; font-weight: 800; color: #065F46; display: flex; align-items: center; gap: 0.5rem;">
                    <span>🧠</span>
                    <span>EXPERIENCE STORED</span>
                </div>
                <p style="margin: 0.5rem 0 0 0; font-size: 1.05rem; font-weight: 700; color: #047857;">
                    "Manual refund initiated. Customer prefers email."
                </p>
                <div style="margin-top: 0.5rem; font-size: 0.9rem; color: #047857;">
                    ✅ Retained into Hindsight Cloud Bank: <code>{s2_res.get('bank_id', config.HINDSIGHT_BANK_ID)}</code>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.caption("Awaiting Step 2 execution...")

    # -----------------------------------------------------------------
    # STEP 3: SIMILAR FUTURE CASE
    # -----------------------------------------------------------------
    st.markdown("---")
    st.markdown("#### 3️⃣ STEP 3 — SIMILAR FUTURE CASE")
    st.markdown("**Customer C001:** *\"My payment was deducted again and my order was cancelled.\"*")

    s3_res = st.session_state.get("demo_step3_res")
    if s3_res:
        st.markdown(
            """
            <div style="background-color: #EFF6FF; border: 2px solid #3B82F6; border-radius: 8px; padding: 1.25rem; margin-top: 0.8rem; margin-bottom: 1rem;">
                <div style="font-size: 1.25rem; font-weight: 800; color: #1E40AF; margin-bottom: 0.75rem; display: flex; align-items: center; gap: 0.5rem;">
                    <span>🧠</span>
                    <span>Hindsight recalled previous experience</span>
                </div>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; font-size: 1rem; line-height: 1.6;">
                    <div><strong style="color: #15803D;">✓ What worked before:</strong> Manual refund</div>
                    <div><strong style="color: #DC2626;">✗ What failed before:</strong> Payment retry</div>
                    <div><strong style="color: #1E3A8A;">👤 Customer preference:</strong> Prefers email</div>
                    <div><strong style="color: #B91C1C;">🚫 Troubleshooting already attempted:</strong> Payment retry</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # -----------------------------------------------------------------
        # STEP 4: NEW RECOMMENDATION
        # -----------------------------------------------------------------
        st.markdown("#### 4️⃣ STEP 4 — NEW RECOMMENDATION")
        st.caption("Personalized recommendation applying the verified memory and strictly respecting customer preference:")
        st.markdown(
            f"""
            <div class="response-box" style="margin-top: 0.5rem; margin-bottom: 1rem;">
                <pre style="white-space: pre-wrap; font-family: inherit; font-size: 1rem; margin:0; color:#0F172A;">{s3_res['step4_response']}</pre>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # -----------------------------------------------------------------
        # STEP 5: RETAIN
        # -----------------------------------------------------------------
        st.markdown("#### 5️⃣ STEP 5 — RETAIN")
        st.markdown(
            """
            <div style="background: linear-gradient(135deg, #F0FDF4, #DCFCE7); border: 2px solid #22C55E; border-radius: 8px; padding: 1.25rem; margin-top: 0.8rem;">
                <div style="font-size: 1.25rem; font-weight: 800; color: #166534; display: flex; align-items: center; gap: 0.5rem;">
                    <span>🧠</span>
                    <span>NEW EXPERIENCE LEARNED</span>
                </div>
                <p style="margin: 0.5rem 0 0 0; font-size: 1rem; font-weight: 600; color: #15803D;">
                    "This resolution can now help future support cases."
                </p>
                <div style="margin-top: 0.4rem; color: #166534; font-size: 0.9rem;">
                    Hindsight Cloud has committed the new interaction into memory. Continuous compounding learning achieved!
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.caption("Awaiting Step 3 execution...")

# =============================================================================
# TAB 1: ACTUAL RESOLVEIQ SUPPORT WORKFLOW
# =============================================================================
with tab_workflow:
    st.markdown("### ⚡ Live Support Agent Resolution Workflow")
    st.caption("Demonstrates the 5-step pipeline: Customer Issue → Recall → Reflect → Support Decision → Response → Retain.")

    # Benchmark Scenario Dropdown for Convenience
    scenario_map = {
        "🔁 Demo HITL Loop: Step 1 - Case 1 (C201 - Apple Pay charged, stuck on trial)": {
            "cust_id": "C201",
            "issue": "Payment charged via Apple Pay but subscription status stuck on free trial",
            "tried": "Restarted app, verified Apple receipt in App Store",
        },
        "🔁 Demo HITL Loop: Step 2 - Case 2 (C202 - Similar Apple Pay issue recalls Case 1)": {
            "cust_id": "C202",
            "issue": "Paid through Apple Pay yesterday, money debited from card, but account still says free trial",
            "tried": "Checked bank account, saw Apple Pay charge",
        },
        "Custom Inquiry": {
            "cust_id": "C101",
            "issue": "My payment of $129 was deducted from my bank but the order says cancelled on checkout",
            "tried": "Refreshed the page twice, checked my mobile banking app",
        },
        "Scenario 1 (C101) - Payment deducted but order cancelled": {
            "cust_id": "C101",
            "issue": "Payment deducted from my credit card ($129.00), but website showed order failed/cancelled",
            "tried": "Refreshed checkout twice, checked mobile banking app",
        },
        "Scenario C102 (Never Repeat Myself Example) - Payment retry already attempted": {
            "cust_id": "C102",
            "issue": "Payment deducted but order cancelled",
            "tried": "Payment retry",
        },
        "Scenario 2 (C102) - Duplicate payment charged twice": {
            "cust_id": "C102",
            "issue": "I was charged twice ($89.50 x 2) for a single checkout order",
            "tried": "Checked bank statement showing two identical pending charges",
        },
        "Scenario 3 (C103) - Refund pending past 12 days (ARN tracer)": {
            "cust_id": "C103",
            "issue": "Approved refund of $340 has not arrived after 12 days; bank claims merchant did not release funds",
            "tried": "Contacted card issuer, submitted bank statement PDF",
        },
        "Scenario 4 (C104) - Wrong product delivered (Cross-ship)": {
            "cust_id": "C104",
            "issue": "Wrong product delivered: ordered ErgoPro Keyboard, received membrane model M-10",
            "tried": "Unboxed unit, verified barcode mismatch, uploaded box photos",
        },
        "Scenario 5 (C105) - Delayed parcel stuck at distribution hub": {
            "cust_id": "C105",
            "issue": "Delayed delivery: parcel stuck at regional distribution hub for 6 days with no tracking updates",
            "tried": "Refreshed carrier tracking daily, filed carrier automated inquiry",
        },
        "Scenario 6 (C106) - Account locked / SMS 2FA not arriving": {
            "cust_id": "C106",
            "issue": "Account locked after failed logins; SMS 2FA verification codes are not being received",
            "tried": "Attempted password reset 4 times, switched WiFi to mobile cellular",
        },
        "Scenario 7 (C107) - Subscription cancellation & courtesy refund": {
            "cust_id": "C107",
            "issue": "Annual subscription renewed early due to timezone; requesting cancellation and refund",
            "tried": "Tried to downgrade in settings, submitted ticket immediately",
        },
        "Scenario 8 (C108) - Failed recurring payment / Card declined": {
            "cust_id": "C108",
            "issue": "Subscription payment failing with generic 'Card Declined: Do Not Honor' error",
            "tried": "Re-entered credit card details twice, tried backup debit card",
        },
        "Scenario 9 (C109) - Previous troubleshooting failed (App crash)": {
            "cust_id": "C109",
            "issue": "Desktop client crashes on launch following v2.4 upgrade; knowledge base troubleshooting failed",
            "tried": "Reinstalled app 3 times, cleared cache, updated GPU drivers - still crashing",
        },
        "Scenario 10 (C110) - Strict email-only (Hard of hearing / VAT)": {
            "cust_id": "C110",
            "issue": "Customer needs EU VAT zero-rated invoice updated; STRICTLY EMAIL-ONLY (hard of hearing)",
            "tried": "Attempted to edit billing postal code in form but regex rejected format",
        },
        "Test Uncertainty (C999) - Unknown Novel Issue Signature": {
            "cust_id": "C999",
            "issue": "Superconducting quantum helium manifold has cryogenic thermal leakage in sector 7",
            "tried": "Power cycled helium compressor once",
        },
    }

    selected_key = st.selectbox("🚀 Pre-populate with Benchmark Scenario:", list(scenario_map.keys()), index=1)
    preset = scenario_map[selected_key]

    with st.form("support_issue_form"):
        col_in1, col_in2 = st.columns([1, 3])
        with col_in1:
            inp_cust_id = st.text_input("Customer ID:", value=preset["cust_id"])
        with col_in2:
            inp_issue = st.text_input("Current Support Issue:", value=preset["issue"])

        inp_tried = st.text_input(
            "Actions Customer Already Attempted:",
            value=preset["tried"],
            help="What the customer has already tried on their own or in previous communications.",
        )

        col_opt1, col_opt2 = st.columns(2)
        with col_opt1:
            auto_retain_check = st.checkbox("🔄 Automatically Retain this new interaction into Hindsight Cloud", value=True)
        with col_opt2:
            submitted = st.form_submit_button("⚡ Run ResolveIQ Workflow", type="primary", use_container_width=True)

    if submitted:
        if not inp_issue.strip():
            st.warning("Please provide a support issue.")
        elif not is_configured:
            st.error("HINDSIGHT_API_KEY is not configured in .env.")
        else:
            with st.spinner("Executing ResolveIQ Workflow: Recall → Reflect → Support Decision → Response → Retain..."):
                workflow_output = agent_workflow.process_customer_issue(
                    customer_id=inp_cust_id,
                    issue=inp_issue,
                    actions_already_tried=inp_tried,
                    auto_retain=auto_retain_check,
                )
                st.session_state["workflow_output"] = workflow_output
                st.session_state["active_customer_id"] = inp_cust_id
                st.session_state["active_issue"] = inp_issue
                st.session_state["hitl_stored_record"] = None
                st.session_state["hitl_decision_mode"] = "resolve"

    workflow_output = st.session_state.get("workflow_output")
    if workflow_output:
        active_cust_id = st.session_state.get("active_customer_id", inp_cust_id)
        active_issue = st.session_state.get("active_issue", inp_issue)

        st.markdown("---")
        st.markdown("### 📋 Workflow Execution Pipeline")

        # STEP 1 & 2: RECALL
        st.markdown("#### 1. 🔍 Hindsight Recall (Retrieved Memories)")
        recall_data = workflow_output["step2_recall"]
        st.markdown(f"**Retrieved {recall_data['count']} memories from Hindsight Cloud** for Customer `{active_cust_id}`:")

        if recall_data["memories"]:
            for i, m in enumerate(recall_data["memories"][:4], start=1):
                score_str = f"Score: {m['score']:.2f}" if isinstance(m.get('score'), (int, float)) else f"Score: {m.get('score', 'N/A')}"
                st.markdown(
                    f"""
                    <div class="memory-box">
                        <strong>Memory #{i}</strong> ({score_str})<br>
                        <span style="font-size: 0.95rem; color: #1E293B;">{m.get('text', '')}</span>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
        else:
            st.info("No prior matching experiences found in Hindsight Cloud.")

        # STEP 3: REFLECT & SITUATION COMPARISON
        st.markdown("#### 2. 🧠 Hindsight Reflect & Situation Comparison")
        reflect_data = workflow_output["step3_reflect"]
        decision_data = workflow_output["step4_decision"]
        sit_comp = decision_data.get("situation_comparison", {})

        col_ref1, col_ref2 = st.columns(2)
        with col_ref1:
            st.markdown("**Hindsight Reflect Synthesis:**")
            st.info(reflect_data.get("synthesized_reasoning", "No reflection generated."))
        with col_ref2:
            st.markdown("**Situation Comparison (Avoiding Blind Copying):**")
            st.markdown(f"**Comparison Analysis:** {sit_comp.get('comparison_analysis', 'N/A')}")
            st.markdown(f"**Variance Check:** {sit_comp.get('variance_detected', 'N/A')}")

        # STEP 4: SUPPORT DECISION
        st.markdown("#### 3. ⚖️ Support Decision Synthesis")
        dec_col1, dec_col2, dec_col3 = st.columns(3)

        with dec_col1:
            conf = decision_data.get("confidence", "medium")
            conf_color = "green" if conf == "high" else ("orange" if conf == "medium" else "red")
            st.markdown(f"**Confidence Level:** :{conf_color}[**{conf.upper()}**]")
            st.markdown(f"**Action Category:** `{decision_data.get('action_type')}`")

        with dec_col2:
            st.markdown("**Troubleshooting to Avoid (Never Repeat):**")
            avoid_acts = decision_data.get("avoid_actions", [])
            if avoid_acts:
                for a in avoid_acts:
                    st.markdown(f'<span class="avoid-badge">🚫 {a}</span>', unsafe_allow_html=True)
            else:
                st.caption("None recorded in prior experience.")

        with dec_col3:
            st.markdown("**Applied Customer Preference:**")
            st.markdown(f'<span class="pref-badge">⭐ {decision_data.get("customer_preference_applied")}</span>', unsafe_allow_html=True)

            if decision_data.get("escalation_recommended"):
                st.markdown(f'<span class="escalate-badge">🚨 Escalation Recommended: {decision_data.get("escalation_reason")}</span>', unsafe_allow_html=True)

        # =================================================================
        # HINDSIGHT MENTAL MODEL: CUSTOMER SUPPORT PROFILE
        # =================================================================
        st.markdown("---")
        st.markdown("### 🧠 Customer Profile")
        st.caption("Lightweight Hindsight Mental Model summarizing customer preferences, recurring problems, successful resolutions, and support history.")

        csp = workflow_output.get("mental_model_customer_profile", {})
        cust_label = csp.get("customer_id", active_cust_id)

        st.markdown(
            f"""
            <div style="background-color: #F8FAFC; border: 2px solid #8B5CF6; border-radius: 8px; padding: 1.25rem; margin-bottom: 1.2rem;">
                <div style="display:flex; justify-content:space-between; align-items:center; border-bottom: 1px solid #E2E8F0; padding-bottom: 0.5rem; margin-bottom: 1rem;">
                    <div style="font-weight: 800; font-size: 1.2rem; color: #4C1D95;">Customer {cust_label}</div>
                    <span style="background-color:#EDE9FE; color:#6D28D9; font-weight:700; padding:0.25rem 0.8rem; border-radius:9999px; font-size:0.85rem; border:1px solid #DDD6FE;">
                        Hindsight Mental Model: {csp.get('mental_model_name', 'Customer Support Profile')}
                    </span>
                </div>
                <div style="display:grid; grid-template-columns: 1fr 1fr; gap: 1rem; font-size: 0.95rem; line-height: 1.6;">
                    <div>
                        <strong style="color: #475569;">Communication:</strong><br>
                        <span style="font-weight: 600; color: #1E293B;">{csp.get('communication', 'Prefers email')}</span>
                    </div>
                    <div>
                        <strong style="color: #475569;">Recurring issue:</strong><br>
                        <span style="font-weight: 600; color: #1E293B;">{csp.get('recurring_issue', 'Payment failures')}</span>
                    </div>
                    <div>
                        <strong style="color: #475569;">Known failed approach:</strong><br>
                        <span style="color: #DC2626; font-weight: 700; background-color: #FEE2E2; padding: 0.2rem 0.5rem; border-radius: 4px; display: inline-block;">{csp.get('failed_approach', 'Repeated payment retry')}</span>
                    </div>
                    <div>
                        <strong style="color: #475569;">Successful approach:</strong><br>
                        <span style="color: #15803D; font-weight: 700; background-color: #DCFCE7; padding: 0.2rem 0.5rem; border-radius: 4px; display: inline-block;">{csp.get('successful_approach', 'Manual refund')}</span>
                    </div>
                    <div style="grid-column: span 2;">
                        <strong style="color: #475569;">Support history:</strong><br>
                        <span style="font-weight: 600; color: #1E293B;">{csp.get('support_history', '3 previous cases')}</span>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        with st.expander("📄 View Hindsight Mental Model Bank Synthesis", expanded=False):
            st.markdown(csp.get("mental_model_raw_content") or "Synthesizing mental model across bank...")

        # NEVER MAKE ME REPEAT MYSELF - CUSTOMER MEMORY PANEL
        cust_prof = workflow_output.get("customer_memory_profile", {})
        st.markdown("---")
        st.markdown("### 🧠 Never Make Me Repeat Myself")

        mem_used_count = cust_prof.get("memory_used_count", 3)
        # Display prominent Customer Memory Card matching required schema
        st.markdown(
            f"""
            <div style="background-color: #F8FAFC; border: 2px solid #3B82F6; border-radius: 8px; padding: 1.25rem; margin-bottom: 1.2rem;">
                <div style="display:flex; justify-content:space-between; align-items:center; border-bottom: 1px solid #E2E8F0; padding-bottom: 0.5rem; margin-bottom: 1rem;">
                    <h4 style="margin:0; color:#1E3A8A; font-weight:800; font-size:1.15rem; letter-spacing:0.02em;">👤 CUSTOMER MEMORY</h4>
                    <span style="background-color:#DBEAFE; color:#1D4ED8; font-weight:800; padding:0.35rem 0.9rem; border-radius:9999px; font-size:0.95rem; border:1px solid #BFDBFE;">
                        🧠 Memory used: {mem_used_count} experiences
                    </span>
                </div>
                <div style="display:grid; grid-template-columns: 1fr 1fr; gap: 0.9rem; font-size:0.95rem; line-height:1.5;">
                    <div><strong style="color:#475569;">Customer:</strong> <code style="font-size:1rem; color:#1E293B; font-weight:700;">{cust_prof.get('customer_id', inp_cust_id)}</code></div>
                    <div><strong style="color:#475569;">Communication preference:</strong> <span style="font-weight:600; color:#1E293B;">{cust_prof.get('communication_preference', 'Email')}</span></div>
                    <div style="grid-column: span 2;"><strong style="color:#475569;">Previous issue:</strong> <span style="font-weight:600; color:#1E293B;">{cust_prof.get('previous_issue', 'None')}</span></div>
                    <div style="grid-column: span 2;"><strong style="color:#475569;">Already tried:</strong> <span style="color:#B91C1C; font-weight:700; background-color:#FEE2E2; padding:0.15rem 0.5rem; border-radius:4px;">{cust_prof.get('already_tried', 'None')}</span></div>
                    <div style="grid-column: span 2;"><strong style="color:#475569;">Previous successful resolution:</strong> <span style="color:#15803D; font-weight:700; background-color:#DCFCE7; padding:0.15rem 0.5rem; border-radius:4px;">{cust_prof.get('previous_successful_resolution', 'None')}</span></div>
                    <div><strong style="color:#475569;">Previous escalation:</strong> <span style="font-weight:600;">{cust_prof.get('previous_escalation', 'No')}</span></div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Highlighting the Contrast (Traditional vs ResolveIQ)
        comp_c1, comp_c2 = st.columns(2)
        with comp_c1:
            st.markdown(
                """
                <div style="background-color:#FFF1F2; border:1px solid #FECDD3; border-radius:6px; padding:0.8rem 1rem; min-height:85px;">
                    <strong style="color:#9F1239;">❌ Traditional Support (No Memory):</strong><br>
                    <em style="color:#881337; font-size:0.9rem;">"Please try making the payment again / reinstall the app / repeat all troubleshooting."</em>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with comp_c2:
            first_tried_sample = cust_prof.get('already_tried', 'retrying the payment').split(';')[0].strip()
            st.markdown(
                f"""
                <div style="background-color:#F0FDF4; border:1px solid #BBF7D0; border-radius:6px; padding:0.8rem 1rem; min-height:85px;">
                    <strong style="color:#166534;">✅ ResolveIQ (Memory-Powered):</strong><br>
                    <em style="color:#14532D; font-size:0.9rem;">"I can see that you already {first_tried_sample.lower()} in your previous case, so I won't ask you to repeat that step."</em>
                </div>
                """,
                unsafe_allow_html=True,
            )

        # WHAT WORKED BEFORE? - SIMILAR PAST CASES PANEL
        st.markdown("---")
        st.markdown("### 🔍 What Worked Before?")
        st.caption("Distinguishes between successful resolutions, failed attempts, and escalations to prioritize what actually worked.")

        wwb = workflow_output.get("what_worked_before", {})
        cases_list = wwb.get("similar_past_cases", [])
        learned_summary = wwb.get("learned_summary", "ResolveIQ learned from 3 previous experiences.")

        st.markdown(
            """
            <div style="font-weight: 800; font-size: 1.15rem; color: #0F172A; letter-spacing: 0.05em; margin-bottom: 0.8rem;">
                SIMILAR PAST CASES
            </div>
            """,
            unsafe_allow_html=True,
        )

        if cases_list:
            col_c1, col_c2, col_c3 = st.columns(3)
            cols = [col_c1, col_c2, col_c3]

            for idx, c in enumerate(cases_list[:3]):
                with cols[idx]:
                    sym = c.get("status_symbol", "✓")
                    st_type = c.get("status_type", "success")
                    if st_type == "success":
                        card_border = "#22C55E"
                        sym_color = "#15803D"
                        sym_bg = "#DCFCE7"
                        outcome_color = "#166534"
                    elif st_type == "failed":
                        card_border = "#EF4444"
                        sym_color = "#B91C1C"
                        sym_bg = "#FEE2E2"
                        outcome_color = "#991B1B"
                    else:
                        card_border = "#F59E0B"
                        sym_color = "#B45309"
                        sym_bg = "#FEF3C7"
                        outcome_color = "#92400E"

                    st.markdown(
                        f"""
                        <div style="background-color: #FFFFFF; border: 1.5px solid {card_border}; border-radius: 8px; padding: 1rem; box-shadow: 0 1px 3px rgba(0,0,0,0.05); min-height: 155px;">
                            <div style="font-weight: 800; font-size: 1.05rem; color: #1E293B;">Case #{c.get('case_number', idx+1)}</div>
                            <div style="color: #64748B; font-size: 0.9rem; margin-bottom: 0.5rem;">{c.get('category', 'Payment issue')}</div>
                            <div style="font-size: 0.95rem; font-weight: 700; color: {sym_color}; background-color: {sym_bg}; padding: 0.35rem 0.6rem; border-radius: 6px; display: inline-block; margin-bottom: 0.6rem;">
                                {sym} {c.get('action_text', '')}
                            </div>
                            <div style="font-size: 0.95rem; font-weight: 700; color: {outcome_color};">
                                Outcome: {c.get('outcome', 'Resolved')}
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

        # Prominently show the learned summary
        st.markdown(
            f"""
            <div style="margin-top: 1rem; margin-bottom: 0.5rem; background: linear-gradient(135deg, #EFF6FF, #DBEAFE); border: 1px solid #93C5FD; border-radius: 8px; padding: 0.75rem 1.25rem; font-size: 1.05rem; font-weight: 700; color: #1E40AF; display: flex; align-items: center; gap: 0.5rem;">
                <span>🧠</span>
                <span>"{learned_summary}"</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # STEP 5: FINAL PERSONALIZED SUPPORT RESPONSE
        st.markdown("---")
        st.markdown("#### 4. 💬 Final Personalized Support Response")
        st.markdown(
            f"""
            <div class="response-box">
                <pre style="white-space: pre-wrap; font-family: inherit; font-size: 1rem; margin:0; color:#0F172A;">{workflow_output['step4_response']}</pre>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # =================================================================
        # HUMAN-IN-THE-LOOP OPERATOR REVIEW & LEARNING WORKFLOW
        # =================================================================
        st.markdown("---")
        st.markdown("### 👤 Human-in-the-Loop Operator Review")
        st.caption("Review the agent's proposed response, make human adjustments, and store the verified resolution into Hindsight Cloud so future cases learn from it.")

        # 3 Action Buttons as required
        b_col1, b_col2, b_col3 = st.columns(3)
        with b_col1:
            if st.button("✓ Resolve Case", key="hitl_btn_resolve", use_container_width=True, type="primary"):
                st.session_state["hitl_decision_mode"] = "resolve"
        with b_col2:
            if st.button("✗ Escalate", key="hitl_btn_escalate", use_container_width=True):
                st.session_state["hitl_decision_mode"] = "escalate"
        with b_col3:
            if st.button("↻ Modify Resolution", key="hitl_btn_modify", use_container_width=True):
                st.session_state["hitl_decision_mode"] = "modify"

        current_mode = st.session_state.get("hitl_decision_mode", "resolve")

        # Determine defaults based on active mode
        if current_mode == "resolve":
            default_decision = "✓ Resolve Case"
            default_outcome = "Resolved"
            default_correct = "Yes"
            default_res = decision_data.get("recommended_fix", "Manual refund initiated and verified.")
        elif current_mode == "escalate":
            default_decision = "✗ Escalate"
            default_outcome = "Escalated"
            default_correct = "Partially"
            default_res = f"Escalated ticket to specialist team: {decision_data.get('escalation_reason', 'Specialist review required')}."
        else:  # modify
            default_decision = "↻ Modify Resolution"
            default_outcome = "Resolved"
            default_correct = "Partially"
            default_res = f"{decision_data.get('recommended_fix', '')} - Operator amended: verified order ID in billing portal and upgraded account."

        with st.form("hitl_operator_form"):
            st.markdown(f"**Operator Review Action:** `{default_decision}`")

            h_c1, h_c2 = st.columns(2)
            with h_c1:
                hitl_cust = st.text_input("Customer ID:", value=active_cust_id, disabled=True)
                hitl_decision_val = st.selectbox(
                    "Human Decision:",
                    [
                        "✓ Resolve Case",
                        "✗ Escalate",
                        "↻ Modify Resolution",
                    ],
                    index=0 if current_mode == "resolve" else (1 if current_mode == "escalate" else 2),
                )
                hitl_outcome_val = st.selectbox(
                    "Actual Outcome:",
                    ["Resolved", "Escalated", "Pending Bank Confirmation", "Failed Attempt"],
                    index=0 if default_outcome == "Resolved" else 1,
                )
            with h_c2:
                hitl_correct_val = st.radio(
                    "Was Agent Recommendation Correct?",
                    ["Yes", "Partially", "No"],
                    index=0 if default_correct == "Yes" else 1,
                    horizontal=True,
                )
                discovered_pref = st.text_input(
                    "Customer Preference Discovered:",
                    value=decision_data.get("customer_preference_applied", "Strictly email communication"),
                )

            hitl_agent_rec = decision_data.get("recommended_fix", "Frontline resolution")
            st.markdown(f"**Original Issue:** *{active_issue}*")
            st.markdown(f"**Agent Recommendation:** `{hitl_agent_rec}`")

            hitl_final_res_val = st.text_area(
                "Final Resolution (Human Verified / Modified):",
                value=default_res,
                height=80,
            )

            submit_hitl = st.form_submit_button(
                "💾 Confirm & Store in Hindsight Memory",
                type="primary",
                use_container_width=True,
            )

        if submit_hitl:
            if not is_configured:
                st.error("Hindsight Cloud is not configured.")
            else:
                with st.spinner("Retaining Human-in-the-Loop Experience in Hindsight Cloud..."):
                    import datetime
                    now_ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    hitl_res = memory_service.retain_human_verified_experience(
                        customer=active_cust_id,
                        original_issue=active_issue,
                        agent_recommendation=hitl_agent_rec,
                        human_decision=hitl_decision_val,
                        final_resolution=hitl_final_res_val,
                        outcome=hitl_outcome_val,
                        recommendation_correct=hitl_correct_val,
                        customer_preference=discovered_pref,
                        timestamp=now_ts,
                    )
                    st.session_state["hitl_stored_record"] = {
                        "customer": active_cust_id,
                        "original_issue": active_issue,
                        "agent_recommendation": hitl_agent_rec,
                        "human_decision": hitl_decision_val,
                        "final_resolution": hitl_final_res_val,
                        "outcome": hitl_outcome_val,
                        "recommendation_correct": hitl_correct_val,
                        "customer_preference": discovered_pref,
                        "timestamp": now_ts,
                        "bank_id": hitl_res.get("bank_id"),
                    }

        # Prominently Show "🧠 NEW EXPERIENCE STORED" when retained
        stored_rec = st.session_state.get("hitl_stored_record")
        if stored_rec:
            st.markdown(
                """
                <div style="background: linear-gradient(135deg, #ECFDF5, #D1FAE5); border: 2px solid #10B981; border-radius: 8px; padding: 1.25rem; margin-top: 1.2rem; margin-bottom: 1.2rem;">
                    <div style="font-size: 1.25rem; font-weight: 800; color: #065F46; display: flex; align-items: center; gap: 0.5rem;">
                        <span>🧠</span>
                        <span>NEW EXPERIENCE STORED</span>
                    </div>
                    <p style="margin: 0.5rem 0 0 0; font-size: 1.05rem; font-weight: 700; color: #047857;">
                        "This resolution can now help future support cases."
                    </p>
                </div>
                """,
                unsafe_allow_html=True,
            )

            with st.expander("📄 View Stored Experience Record", expanded=True):
                rec_col1, rec_col2 = st.columns(2)
                with rec_col1:
                    st.markdown(f"**Customer:** `{stored_rec['customer']}`")
                    st.markdown(f"**Human Decision:** `{stored_rec['human_decision']}`")
                    st.markdown(f"**Outcome:** `{stored_rec['outcome']}`")
                    st.markdown(f"**Recommendation Correct?** `{stored_rec['recommendation_correct']}`")
                with rec_col2:
                    st.markdown(f"**Timestamp:** `{stored_rec['timestamp']}`")
                    st.markdown(f"**Customer Preference:** `{stored_rec['customer_preference']}`")
                    st.markdown(f"**Bank ID:** `{stored_rec['bank_id']}`")
                st.markdown(f"**Original Issue:** {stored_rec['original_issue']}")
                st.markdown(f"**Final Resolution:** *{stored_rec['final_resolution']}*")

            # The Loop Explanation Box
            st.markdown(
                """
                <div style="background-color: #F8FAFC; border: 1.5px solid #0284C7; border-radius: 8px; padding: 1rem 1.2rem; margin-top: 0.8rem;">
                    <strong style="color: #0369A1; font-size: 1.05rem;">🔁 The Human-in-the-Loop Learning Loop in Action:</strong>
                    <div style="margin-top: 0.5rem; font-size: 0.95rem; line-height: 1.7; color: #1E293B;">
                        <div><strong>Case 1:</strong> Human resolves it → Hindsight remembers it.</div>
                        <div><strong>Case 2:</strong> Similar issue occurs → Hindsight recalls Case 1 → Agent uses that experience.</div>
                    </div>
                    <div style="margin-top: 0.6rem; color: #475569; font-size: 0.9rem;">
                        💡 <em>To demonstrate Case 2 right now, select <strong>"🔁 Demo HITL Loop: Step 2 - Case 2"</strong> in the benchmark dropdown above and click Run!</em>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        # STEP 6: CONTINUOUS LEARNING / RETAIN
        st.markdown("#### 5. 🔄 Continuous Learning (Hindsight Retain)")
        retained_step = workflow_output.get("step5_retained")
        if retained_step and retained_step.get("success"):
            st.success(
                f"✅ **Interaction Retained in Hindsight Cloud!** "
                f"Bank `{retained_step.get('bank_id')}` has stored this experience so the agent continually learns."
            )
            with st.expander("Inspect Retained Memory Record"):
                st.code(retained_step.get("content_preview", ""), language="text")
        elif retained_step:
            st.warning(f"Retain status: {retained_step.get('error', 'Skipped')}")

# =============================================================================
# TAB 2: RAW RECALL EXPLORER
# =============================================================================
with tab_recall:
    st.markdown("#### Recall Previous Experiences")
    st.caption("Inspect raw memory recall units directly from Hindsight Cloud.")

    recall_col1, recall_col2 = st.columns([3, 1])
    with recall_col1:
        raw_query = st.text_input("Query / Keyword:", value="Payment deducted but order cancelled", key="raw_recall_query")
    with recall_col2:
        raw_cust = st.text_input("Customer ID Filter:", value="C101", key="raw_recall_cust")

    if st.button("Query Hindsight Recall", type="primary", key="btn_query_recall"):
        if not is_configured:
            st.error("HINDSIGHT_API_KEY is not configured.")
        else:
            with st.spinner("Querying Hindsight Cloud..."):
                try:
                    res = memory_service.recall_similar_cases(query=raw_query, customer_id=raw_cust if raw_cust.strip() else None)
                    st.success(f"Retrieved {res.get('count', 0)} memory units!")
                    for idx, mem in enumerate(res.get("memories", []), start=1):
                        st.markdown(
                            f"""
                            <div class="memory-box">
                                <strong>Memory #{idx}</strong> (Score: {mem.get('score', 'N/A')})<br>
                                <span style="font-size:0.95rem;">{mem.get('text', '')}</span>
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )
                except Exception as e:
                    st.error(f"Recall error: {e}")

# =============================================================================
# TAB 3: DIRECT REFLECT ENGINE
# =============================================================================
with tab_reflect:
    st.markdown("#### Direct Hindsight Reflect Engine")
    st.caption("Ask high-level synthesis questions across multiple previous experiences.")

    reflect_prompt_input = st.text_area(
        "Reflection Question:",
        value="What are the top causes of payment deduction issues and what resolutions produced the best outcomes?",
        height=90,
        key="direct_reflect_input",
    )
    if st.button("Synthesize Reasoning with Reflect", type="primary", key="btn_direct_reflect"):
        if not is_configured:
            st.error("HINDSIGHT_API_KEY is not configured.")
        else:
            with st.spinner("Synthesizing reasoning..."):
                try:
                    res = memory_service.reflect_on_cases(query=reflect_prompt_input)
                    st.success("Reflect completed!")
                    st.markdown("##### 💡 Synthesized Reasoning:")
                    st.write(res.get("reasoning", ""))
                    if res.get("based_on"):
                        st.markdown("##### 📌 Based On Citations:")
                        st.write(res.get("based_on"))
                except Exception as e:
                    st.error(f"Reflect error: {e}")

# =============================================================================
# TAB 4: SEEDED BENCHMARK CASES LIBRARY
# =============================================================================
with tab_demo_cases:
    st.markdown("#### 📚 Seeded Experience Cases (10 Benchmark Scenarios)")
    st.caption("These 10 cases represent previous support resolutions rather than simple FAQ knowledge.")

    for i, c in enumerate(demo_data.DEMO_SUPPORT_CASES, start=1):
        with st.expander(f"{i}. [{c['customer_id']}] {c['issue']}"):
            st.markdown(f"**Category:** {c['category']}")
            st.markdown(f"**Actions Attempted:** {', '.join(c['actions_attempted'])}")
            st.markdown(f"**Resolution:** {c['resolution']}")
            st.markdown(f"**Outcome:** {c['outcome']}")
            st.markdown(f"**Customer Preferences:** {c['customer_preferences']}")
            st.markdown(f"**Escalation Required:** `{'Yes' if c['escalation_required'] else 'No'}`")
            st.markdown(f"**Document ID:** `{c['document_id']}` *(Ensures idempotent replace mode)*")

# =============================================================================
# TAB 5: DIAGNOSTICS & HEALTH
# =============================================================================
with tab_diagnostics:
    st.markdown("#### System Diagnostics")

    diag_col1, diag_col2 = st.columns(2)

    with diag_col1:
        st.markdown("**Hindsight Cloud Configuration:**")
        st.write({
            "API Key Configured": "Yes ✅" if env_status["hindsight_api_key_configured"] else "No ❌",
            "API Key (Masked)": env_status["hindsight_api_key_masked"],
            "Bank ID": env_status["hindsight_bank_id"],
            "Base URL": env_status["hindsight_base_url"],
        })

    with diag_col2:
        st.markdown("**Workflow Decision Engine Rules:**")
        st.markdown(
            """
            1. **Customer & Issue ID**: Tracks customer history and parses explicit customer attempts.
            2. **Hindsight Recall**: Extracts verified fixes, actions to avoid, and communication preferences.
            3. **Hindsight Reflect**: Synthesizes reasoning and compares current symptoms vs past precedents.
            4. **Support Decision**: Enforces zero repeated troubleshooting, applies preferences, checks escalation.
            5. **Personalized Response**: Customer-ready response acknowledging context and admitting uncertainty when memory is lacking.
            6. **Continuous Retain**: Automatically saves new resolutions into Hindsight Cloud.
            """
        )
