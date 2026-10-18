import streamlit as st
import pandas as pd
import random
import time
from sarvamai import SarvamAI

# 1. Project Authentication Setup
SARVAM_KEY = "sk_mvtc7ugq_fhnhDb0pzvHr4SgGbTDbpt4n"
client_sarvam = SarvamAI(api_subscription_key=SARVAM_KEY)

# Initialize global session storage
if "ticket_ledger" not in st.session_state:
    st.session_state["ticket_ledger"] = [
        {"ID": "BLR-849201", "Lang": "kn-IN", "Dept": "BESCOM (Electricity Board)", "Priority": "Critical", "Status": "Crew Dispatched"},
        {"ID": "BLR-374920", "Lang": "hi-IN", "Dept": "BWSSB (Water Supply)", "Priority": "High", "Status": "Valve Repaired"},
    ]

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "current_screen" not in st.session_state:
    st.session_state["current_screen"] = "SSO_CHOOSE"
if "selected_provider" not in st.session_state:
    st.session_state["selected_provider"] = None

class CivicAgentRouter:
    def __init__(self):
        self.departments = {
            "water": {"name": "BWSSB (Water Supply & Sewage)", "sla": "4 Hours", "priority": "High"},
            "road": {"name": "BBMP Infrastructure (Roads/Potholes)", "sla": "24 Hours", "priority": "Medium"},
            "power": {"name": "BESCOM (Electricity Board)", "sla": "2 Hours", "priority": "Critical"},
            "health": {"name": "Public Health & Sanitation", "sla": "12 Hours", "priority": "Medium"}
        }

    def analyze_urgency(self, text_to_analyze: str):
        text_lower = text_to_analyze.lower()
        target_sector = "general"
        for key in self.departments.keys():
            if key in text_lower or ("leak" in text_lower and key == "water") or ("light" in text_lower and key == "power") or ("electricity" in text_lower and key == "power") or ("current" in text_lower and key == "power") or ("bescom" in text_lower and key == "power") or ("road" in text_lower and key == "road") or ("pothole" in text_lower and key == "road"):
                target_sector = key
                break
        is_hazard = any(w in text_lower for w in ["dangerous", "broken", "flood", "shock", "spark", "accident", "emergency", "urgent", "danger", "fire", "illa", "bega", "paani", "bijli", "turtu", "jal", "sari"])
        
        if target_sector != "general":
            dept_info = self.departments[target_sector]
            return {"assigned_node": dept_info["name"], "target_sla": "1 Hour" if is_hazard else dept_info["sla"], "calculated_priority": "Critical" if is_hazard else dept_info["priority"]}
        return {"assigned_node": "Emergency Control Desk" if is_hazard else "Central Municipal Command", "target_sla": "30 Minutes" if is_hazard else "48 Hours", "calculated_priority": "Critical" if is_hazard else "Low"}

agent_system = CivicAgentRouter()

# --- SCREEN 1: AUTHENTICATION ---
if not st.session_state["logged_in"]:
    st.title("🔐 BharatAgent Gateway Sign-In")
    st.caption("Secure Portal for Indian Citizens & Municipal Admin Nodes")
    st.divider()
    
    if st.session_state["current_screen"] == "SSO_CHOOSE":
        st.markdown("### Continue with Single Sign-On")
        if st.button("Google Login", use_container_width=True):
            st.session_state["current_screen"] = "GOOGLE_FORM"
            st.rerun()
        if st.button("GitHub Login", use_container_width=True):
            st.session_state["current_screen"] = "GITHUB_FORM"
            st.rerun()
                
        st.markdown("---")
        st.markdown("### Sign In with Municipal Credentials")
        username = st.text_input("Username:")
        password = st.text_input("Password:", type="password")
        if st.button("Sign In", use_container_width=True):
            if (username == "admin" and password == "hacktober2026") or (username == "citizen" and password == "1234"):
                st.session_state["current_screen"] = "HANDSHAKE"
                st.session_state["selected_provider"] = "Municipal Service"
                st.rerun()
            else:
                st.error("Invalid credentials.")

    elif st.session_state["current_screen"] == "GOOGLE_FORM":
        st.title("🌐 Sign in with Google")
        g_email = st.text_input("Email or phone")
        g_pass = st.text_input("Password", type="password")
        if st.button("Next", type="primary"):
            if g_email and g_pass:
                st.session_state["current_screen"] = "HANDSHAKE"
                st.session_state["selected_provider"] = "Google Identity"
                st.rerun()
        if st.button("Back"):
            st.session_state["current_screen"] = "SSO_CHOOSE"
            st.rerun()

    elif st.session_state["current_screen"] == "GITHUB_FORM":
        st.title("🐙 Sign in to GitHub")
        gh_user = st.text_input("Username")
        gh_pass = st.text_input("Password", type="password")
        if st.button("Sign In", type="primary"):
            if gh_user and gh_pass:
                st.session_state["current_screen"] = "HANDSHAKE"
                st.session_state["selected_provider"] = "GitHub Developer"
                st.rerun()
        if st.button("Cancel"):
            st.session_state["current_screen"] = "SSO_CHOOSE"
            st.rerun()

    elif st.session_state["current_screen"] == "HANDSHAKE":
        provider = st.session_state["selected_provider"]
        st.title(f"Authenticating via {provider}...")
        time.sleep(1.0)
        st.success("Verification Cleared.")
        st.session_state["logged_in"] = True
        st.rerun()

# --- SCREEN 2: MAIN SITE ---
else:
    st.sidebar.title("🤖 Menu")
    app_mode = st.sidebar.radio("Navigate Pages:", ["Citizen Portal", "Admin Dashboard"])
    
    if st.sidebar.button("Sign Out"):
        st.session_state["logged_in"] = False
        st.session_state["current_screen"] = "SSO_CHOOSE"
        st.rerun()

    if app_mode == "Citizen Portal":
        st.title("🎙️ BharatAgent Gateway")
        language_map = {
            "Kannada": "kn-IN", "Hindi": "hi-IN", "Tamil": "ta-IN", "Telugu": "te-IN"
        }
        selected_lang = st.sidebar.selectbox("Language", list(language_map.keys()))
        lang_code = language_map[selected_lang]

        user_query = st.text_input(f"Type complaint in {selected_lang}:")

        if user_query:
            st.divider()
            st.subheader("Live Agent Logs")
            try:
                to_eng_payload = client_sarvam.text.translate(input=user_query, source_language_code=lang_code, target_language_code="en-IN")
                english_intent = getattr(to_eng_payload, 'translated_text', str(to_eng_payload))
            except Exception:
                english_intent = user_query
            st.code(f"Decoded English Intent: '{english_intent}'")
            
            routing_analysis = agent_system.analyze_urgency(english_intent)
            st.json(routing_analysis)
            
            generated_ticket_id = f"BLR-{random.randint(100000, 999999)}"
            raw_res = f"Tracking ID {generated_ticket_id}. Routed to {routing_analysis['assigned_node']}."
            
            new_ticket = {"ID": generated_ticket_id, "Lang": lang_code, "Dept": routing_analysis['assigned_node'], "Priority": routing_analysis['calculated_priority'], "Status": "Pending Review"}
            if new_ticket not in st.session_state["ticket_ledger"]:
                st.session_state["ticket_ledger"].append(new_ticket)

            st.subheader("Citizen Confirmation")
            try:
                to_native_payload = client_sarvam.text.translate(input=raw_res, source_language_code="en-IN", target_language_code=lang_code)
                native_response_string = getattr(to_native_payload, 'translated_text', str(to_native_payload))
            except Exception:
                native_response_string = raw_res
            
            st.success(f"Tracking ID: {generated_ticket_id}")
            st.warning(native_response_string)

    else:
        st.title("📊 Operations Dashboard")
        admin_df = pd.DataFrame(st.session_state["ticket_ledger"])
        st.dataframe(admin_df, use_container_width=True)
