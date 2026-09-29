"""ResolveIQ - Memory-Powered Customer Support Agent.

Hackathon MVP powered by Streamlit and Hindsight Cloud.
"Support that learns from every resolution and never makes customers repeat themselves."
"""

import streamlit as st
import config
from hindsight_service import hindsight_service

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
    .metric-value {
        font-weight: 700;
        font-size: 1.1rem;
    }
    .highlight-badge {
        display: inline-block;
        padding: 0.2rem 0.6rem;
        border-radius: 9999px;
        font-size: 0.8rem;
        font-weight: 600;
    }
    .badge-success {
        background-color: #DCFCE7;
        color: #166534;
    }
    .badge-warning {
        background-color: #FEF9C3;
        color: #854D0E;
    }
    .badge-info {
        background-color: #E0F2FE;
        color: #075985;
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
        st.markdown("**LLM Detected:** `None (Ready for config)`")

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

# Main App Header
st.markdown('<div class="main-title">ResolveIQ 🧠</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="sub-title"><em>"Support that learns from every resolution and never makes customers repeat themselves."</em></div>',
    unsafe_allow_html=True,
)

# Status banner on top of main window
if not is_configured:
    st.info(
        "👋 **Welcome to the ResolveIQ MVP Skeleton!** "
        "Hindsight Cloud credentials are not configured yet. "
        "You can inspect the configuration status in the sidebar or below. "
        "Create a `.env` file based on `.env.example` to connect your active Hindsight bank.",
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
            <h4>💡 1. Recall</h4>
            <p>Queries Hindsight memory to retrieve past customer tickets, preferences, and verified solutions before answering.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
with col2:
    st.markdown(
        """
        <div class="status-card">
            <h4>⚡ 2. Resolve</h4>
            <p>Synthesizes resolution with context so customers never need to repeat previously solved problems.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
with col3:
    st.markdown(
        """
        <div class="status-card">
            <h4>🔄 3. Retain</h4>
            <p>Retains the new resolution into Hindsight Cloud so the entire support team learns automatically.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("### 🧪 Memory Operations Playground")

tab_recall, tab_retain, tab_diagnostics = st.tabs([
    "🔍 Recall Customer Context",
    "📝 Retain Resolution Memory",
    "🛠️ Diagnostics & Health",
])

# Tab 1: Recall Memory
with tab_recall:
    st.markdown("#### Test Memory Recall")
    st.caption("Enter a customer inquiry to test context recall against your Hindsight memory bank.")
    
    query = st.text_input(
        "Customer Inquiry:",
        placeholder="e.g., Customer is asking about resetting 2FA on their Pro workspace",
        key="recall_query",
    )
    
    if st.button("Recall Past Resolutions", type="primary", key="btn_recall"):
        if not query.strip():
            st.warning("Please enter a customer inquiry to recall.")
        elif not is_configured:
            st.error("Cannot recall: HINDSIGHT_API_KEY is not set in `.env`.")
        else:
            with st.spinner("Searching Hindsight Bank..."):
                success, result = hindsight_service.recall_memory(query)
                if success:
                    st.success("Recall successful!")
                    st.json(result if isinstance(result, (dict, list)) else {"raw_response": str(result)})
                else:
                    st.error(result)

# Tab 2: Retain Resolution
with tab_retain:
    st.markdown("#### Retain a New Resolution")
    st.caption("Store a solved ticket into Hindsight so future inquiries automatically learn from this solution.")
    
    customer_id = st.text_input(
        "Customer ID / Account (Optional):",
        placeholder="e.g., cust_98412 or Acme Corp",
        key="retain_cust_id",
    )
    
    resolution_text = st.text_area(
        "Resolution Details:",
        placeholder="e.g., Resolved billing invoice issue: customer switched from annual to monthly, issued prorated credit of $45.",
        key="retain_text",
        height=120,
    )
    
    if st.button("Retain Resolution into Memory", key="btn_retain"):
        if not resolution_text.strip():
            st.warning("Please provide resolution details.")
        elif not is_configured:
            st.error("Cannot retain: HINDSIGHT_API_KEY is not set in `.env`.")
        else:
            with st.spinner("Saving to Hindsight Cloud..."):
                success, message = hindsight_service.retain_resolution(
                    content=resolution_text,
                    customer_id=customer_id if customer_id.strip() else None,
                )
                if success:
                    st.success(message)
                else:
                    st.error(message)

# Tab 3: Diagnostics & Health
with tab_diagnostics:
    st.markdown("#### Environment & System Configuration")
    
    diag_col1, diag_col2 = st.columns(2)
    
    with diag_col1:
        st.markdown("**Hindsight Configuration:**")
        st.write({
            "API Key Status": "Configured ✅" if env_status["hindsight_api_key_configured"] else "Missing ❌",
            "API Key (Masked)": env_status["hindsight_api_key_masked"],
            "Bank ID": env_status["hindsight_bank_id"],
            "Base URL": env_status["hindsight_base_url"],
        })
        
    with diag_col2:
        st.markdown("**Optional LLM Providers:**")
        st.write({
            "OpenAI API Key": "Configured ✅" if env_status["openai_configured"] else "Not configured",
            "Groq API Key": "Configured ✅" if env_status["groq_configured"] else "Not configured",
            "Anthropic API Key": "Configured ✅" if env_status["anthropic_configured"] else "Not configured",
        })

    st.markdown("---")
    st.markdown("#### Quick Verification Commands")
    st.code("streamlit run app.py", language="bash")
