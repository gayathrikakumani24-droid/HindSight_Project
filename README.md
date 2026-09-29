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

## 🩺 Health & Diagnostics

The app includes an integrated health and diagnostic panel in both the sidebar and the main dashboard:
- Checks if `HINDSIGHT_API_KEY` and `HINDSIGHT_BANK_ID` are configured.
- Masks API keys to prevent accidental leaks during presentations.
- Provides a one-click connection test against Hindsight Cloud.
- Features initial Retain & Recall memory operations for the hackathon MVP.
