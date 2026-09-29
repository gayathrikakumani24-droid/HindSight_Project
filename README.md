# ResolveIQ 🧠

> *"Support that learns from every resolution and never makes customers repeat themselves."*

ResolveIQ is a memory-powered customer support agent built for hackathon speed and continuous learning using **Hindsight Cloud**.

---

## ⚡ Tech Stack

- **Python** (3.10+)
- **Streamlit** (UI / Interactive Agent Playground)
- **Hindsight Cloud** & `hindsight-client` (Continuous Resolution Memory)
- **python-dotenv** (Secure credential management)

---

## 📁 Project Structure

```text
HindSight/
├── .env.example              # Template for environment variables
├── .gitignore                # Protects secrets, API keys, and environment files
├── app.py                    # Streamlit application entrypoint & UI
├── config.py                 # Environment configuration loader
├── hindsight_service.py      # Hindsight Cloud client initialization & service
├── requirements.txt          # Python dependencies
└── README.md                 # Project documentation
```

---

## 🚀 Quickstart

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment

Copy the example configuration file:

```bash
cp .env.example .env
```

Edit `.env` with your Hindsight Cloud credentials:

```env
HINDSIGHT_API_KEY=your_hindsight_api_key_here
HINDSIGHT_BANK_ID=resolveiq-support-bank
HINDSIGHT_BASE_URL=https://api.hindsight.vectorize.io
```

### 3. Run the Application

```bash
streamlit run app.py
```

---

## 🔍 "What Worked Before?" Feature

For every recalled support experience, ResolveIQ distinguishes between:
- **✓ Successful resolution**
- **✗ Failed attempt**
- **⚠ Escalated case**

When generating a response, ResolveIQ automatically prioritizes solutions that previously produced successful outcomes for similar problems, avoiding complicated manual scoring systems and relying on Hindsight's retrieved memories and LLM reasoning.

### UI Display:

```text
SIMILAR PAST CASES

Case #1
Payment issue
✓ Manual refund
Outcome: Resolved

Case #2
Payment issue
✗ Payment retry
Outcome: Failed

Case #3
Payment issue
⚠ Billing escalation
Outcome: Resolved

"ResolveIQ learned from 3 previous experiences."
```

---

## 🧠 "Never Make Me Repeat Myself" Feature

ResolveIQ extracts and visually displays the customer's historical experience before responding:

```text
CUSTOMER MEMORY
Customer: C102
Previous issue: Duplicate payment charged twice
Already tried: Payment retry; checked bank statement
Previous successful resolution: Voided second pending transaction
Communication preference: Email receipt with reference ID
Previous escalation: Yes (Finance Ops)

🧠 Memory used: 3 experiences
```

---

## 👤 Human-in-the-Loop Learning Workflow

ResolveIQ pairs automated memory retrieval with human operator verification:

### 1. Operator Controls
After the agent generates a response, the support operator is presented with 3 review actions:
- `[✓ Resolve Case]`
- `[✗ Escalate]`
- `[↻ Modify Resolution]`

### 2. Operator Outcome Input
The operator specifies the actual resolution details:
- **customer**
- **original issue**
- **agent recommendation**
- **human decision**
- **final resolution**
- **outcome**
- **whether the agent recommendation was correct**
- **any customer preference discovered**
- **timestamp**

### 3. Persistent Memory Retention
When the case is resolved, a new Hindsight experience is retained:

```text
🧠 NEW EXPERIENCE STORED
"This resolution can now help future support cases."
```

### 4. Case 1 → Case 2 Learning Cycle
- **Case 1**: Human resolves it → Hindsight remembers it.
- **Case 2**: Similar issue occurs → Hindsight recalls Case 1 → Agent uses that experience.

### Contrast Demonstrating Memory-Powered Support:
- ❌ **Traditional Generic Agent (No Memory):** *"Please try making the payment again."*
- ✅ **ResolveIQ Agent (Memory-Powered):** *"I can see that you already retried the payment in your previous case, so I won't ask you to repeat that step."*

---

## ⚡ 5-Step Support Workflow

ResolveIQ includes a built-in experience memory seeder with **10 realistic support cases**:

1. **Case 1 (C101)**: Payment deducted ($129.00) but order cancelled on website.
2. **Case 2 (C102)**: Duplicate payment charged twice ($89.50 x 2) for single checkout.
3. **Case 3 (C103)**: Refund pending past 12 days (ARN bank tracer request).
4. **Case 4 (C104)**: Wrong product delivered (ErgoPro vs Membrane keyboard cross-ship).
5. **Case 5 (C105)**: Delayed delivery stuck at regional hub for 6 days (Saturday priority reroute).
6. **Case 6 (C106)**: Account locked after failed logins (SMS 2FA spam block bypass + TOTP enrollment).
7. **Case 7 (C107)**: Subscription cancellation requested with prorated courtesy refund.
8. **Case 8 (C108)**: Failed recurring payment (Bank merchant block resolved + grace period).
9. **Case 9 (C109)**: Previous troubleshooting failed (App crash resolved via stale SQLite lock deletion).
10. **Case 10 (C110)**: Strict email-only communication (Deaf / hard of hearing accessibility flag & EU VAT correction).

### Idempotent Duplicate Prevention
The seeder assigns deterministic `document_id` values and uses `update_mode='replace'` so clicking **"🌱 Seed Demo Memories"** updates records rather than duplicating them.

---

## 🩺 Health & Diagnostics

The app includes an integrated health and diagnostic panel in both the sidebar and the main dashboard:
- Checks if `HINDSIGHT_API_KEY` and `HINDSIGHT_BANK_ID` are configured.
- Masks API keys to prevent accidental leaks during presentations.
- Provides a one-click connection test against Hindsight Cloud.
- Features Retain, Recall, and Reflect operations for the hackathon MVP.
