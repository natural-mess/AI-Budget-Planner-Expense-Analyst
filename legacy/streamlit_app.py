import streamlit as st
import sys, os

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
from main_agent import MainAgent

st.set_page_config(page_title="AI Budget Planner", page_icon="💰")

st.title("💰 AI Budget Planner & Expense Analyst")
st.markdown("An autonomous multi-agent system featuring PII redaction and HITL security.")

if "agent" not in st.session_state:
    st.session_state.agent = MainAgent()
if "messages" not in st.session_state:
    st.session_state.messages = []
if "awaiting_approval" not in st.session_state:
    st.session_state.awaiting_approval = False
if "draft_budget" not in st.session_state:
    st.session_state.draft_budget = None

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# HITL Approval UI
if st.session_state.awaiting_approval:
    st.warning("⚠️ Security Manager: Human-In-The-Loop Approval Required! A category exceeds $1000.")
    st.json(st.session_state.draft_budget)
    
    if st.button("✅ Approve Budget", use_container_width=True):
        st.session_state.awaiting_approval = False
        result = st.session_state.agent.approve_budget(st.session_state.draft_budget)
        st.session_state.messages.append({"role": "assistant", "content": result["response"]})
        st.rerun()
    st.stop()  # Halt chat input until approved

if prompt := st.chat_input("Enter your financial goals (e.g., I need a budget to save for a house...)"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Agents are processing..."):
            result = st.session_state.agent.handle_message(prompt)
            
            if result["status"] == "awaiting_approval":
                st.session_state.awaiting_approval = True
                st.session_state.draft_budget = result["budget"]
                st.rerun()
            else:
                st.markdown(result["response"])
                st.session_state.messages.append({"role": "assistant", "content": result["response"]})
