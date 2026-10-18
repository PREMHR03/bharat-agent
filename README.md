# 🤖 BharatAgent: Autonomous Multilingual Voice & Action Gateway

Official submission for the **Hacktoberfest 2026 In-Person Hack Day (Bengaluru Track)**.

## 🏆 The Problem Statement
Over **80% of regional citizens in India** are locked out of active digital civic infrastructure, municipal databases, and automated service pipelines because standard technical frameworks are engineered almost exclusively around English text strings [4.1]. This project removes the literacy and typing barrier completely, allowing non-English speaking individuals to query active system metrics, track municipal database states, and execute critical infrastructure commands natively through their local dialects.

## 🧠 Key Features & Architecture
- 🌐 **Pan-India Coverage:** Sidebar localization matrix supporting **all 22 officially scheduled languages of India** seamlessly.
- 🎤 **Hybrid Transcription Pipeline:** Leverages **Sarvam AI Saaras STT** cloud engine with an integrated local on-device transcription fallback system.
- ⚙️ **Autonomous Agentic Router:** Simulates an open-weight LLM tool-calling architecture to interpret localized intents, execute system tool workflows, dynamically route tickets to targeted utility entities (like **BESCOM** or **BWSSB**), and automatically manage urgency priority metrics.
- 📤 **Compact Citizen Portal canvas:** Instantly formats dynamic status receipts, tracking identifiers, and resolution notices back into high-fidelity local scripts side-by-side with backend execution terminal logs.

## 🛠️ Tech Stack & Dependencies
- **Core Orchestration Language:** Python 3.10+
- **Frontend Presentation Layer:** Streamlit Framework
- **Localization Infrastructure Engine:** Sarvam AI SDK & REST API Matrix
- **Audio Capture Framework:** In-memory `io.BytesIO` streams & local SpeechRecognition assets

## 🚀 Local Deployment Setup
1. Clone the active open-source repository link.
2. Configure project dependencies:
   ```bash
   pip install streamlit sarvamai pandas speechrecognition
   ```
3. Inject your working authentication token key string securely inside `app.py`, then execute the local application server matrix:
   ```bash
   streamlit run app.py
   ```
