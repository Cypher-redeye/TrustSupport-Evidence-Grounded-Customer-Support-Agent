import streamlit as st
import requests
import time
import os
from src.ui.evidence_formatter import format_evidence_text

API_URL = os.environ.get("API_URL", "http://localhost:8000/chat")
HEALTH_URL = os.environ.get("HEALTH_URL", "http://localhost:8000/health")

st.set_page_config(page_title="TrustSupport", page_icon="🛡️", layout="wide")

# Custom CSS
st.markdown("""
<style>
    .badge {
        display: inline-block;
        padding: 0.25em 0.5em;
        font-size: 0.7em;
        font-weight: 500;
        line-height: 1;
        text-align: center;
        border-radius: 0.25rem;
        background-color: #374151;
        color: #D1D5DB;
        margin-right: 0.4em;
        margin-bottom: 0.4em;
    }
    .escalation-card {
        background-color: rgba(239, 68, 68, 0.1);
        border-left: 4px solid #ef4444;
        padding: 1rem;
        border-radius: 0.25rem;
        margin-top: 1rem;
        margin-bottom: 1rem;
    }
    .status-safe { color: #10B981; font-weight: bold; font-size: 0.85em; margin-top: 0.5em; }
    .status-caution { color: #F59E0B; font-weight: bold; font-size: 0.85em; margin-top: 0.5em; }
    .status-escalated { color: #EF4444; font-weight: bold; font-size: 0.85em; margin-top: 0.5em; }
    .status-abstained { color: #9CA3AF; font-weight: bold; font-size: 0.85em; margin-top: 0.5em; }
    .evidence-item { font-size: 0.9em; margin-bottom: 0.5rem; }
    .diagnostics-text { font-size: 0.85em; line-height: 1.2; }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------
st.sidebar.title("🛡️ TrustSupport")
st.sidebar.markdown("Evidence-grounded gaming support assistant.")
system_status_placeholder = st.sidebar.empty()

with st.sidebar.expander("About the Architecture", expanded=True):
    st.markdown("""
    **Pipeline:**
    1. **Query**
    2. **Intent Detection**
    3. **Risk Detection**
    4. **OOD Detection**
    5. **Evidence Retrieval**
    6. **Routing**
    7. **Grounded Response**
    8. **Safety Validation**
    """)

# Check API Health
try:
    health = requests.get(HEALTH_URL, timeout=2).json()
    if health.get("status") == "healthy":
        system_status_placeholder.markdown("🟢 **Backend Online**")
    else:
        system_status_placeholder.markdown("🟡 **Backend Starting Up**")
except Exception:
    system_status_placeholder.markdown("🔴 **Backend Offline**")

if st.sidebar.button("🗑️ Clear Conversation", use_container_width=True):
    st.session_state.messages = []
    st.rerun()

# ---------------------------------------------------------
# MAIN AREA
# ---------------------------------------------------------
st.title("🛡️ TrustSupport")
st.markdown("**Evidence-Grounded AI Customer Support**  \n*Safe responses. Retrieved evidence. Transparent decisions.*")
st.markdown("""
<div style="margin-bottom: 1rem;">
    <span class="badge">FastAPI</span>
    <span class="badge">Sentence Transformers</span>
    <span class="badge">Logistic Regression</span>
    <span class="badge">FAISS</span>
    <span class="badge">Evidence Grounding</span>
    <span class="badge">Safety Routing</span>
</div>
""", unsafe_allow_html=True)

st.subheader("Explore TrustSupport")
st.caption("Try a scenario to see how the agent understands, retrieves evidence, and responds safely.")

col1, col2, col3 = st.columns(3)
with col1:
    if st.button("🎮 Technical Support", help="My game keeps crashing when I launch it.", use_container_width=True):
        st.session_state.demo_query = "My game keeps crashing when I launch it."
    if st.button("🎁 Missing Rewards", help="I completed the challenge but didn't receive my reward.", use_container_width=True):
        st.session_state.demo_query = "I completed the challenge but didn't receive my reward."
with col2:
    if st.button("🚫 Ban Appeal", help="I was banned for no reason.", use_container_width=True):
        st.session_state.demo_query = "I was banned for no reason."
    if st.button("🔐 Account Security", help="Someone hacked my account.", use_container_width=True):
        st.session_state.demo_query = "Someone hacked my account."
with col3:
    if st.button("⚔️ Game Integrity", help="This player is using an aimbot.", use_container_width=True):
        st.session_state.demo_query = "This player is using an aimbot."
    if st.button("🌐 Out-of-Domain", help="How do I cook pasta?", use_container_width=True):
        st.session_state.demo_query = "How do I cook pasta?"

st.divider()

if "messages" not in st.session_state:
    st.session_state.messages = []

# Empty State
if not st.session_state.messages:
    st.info("👋 **How can I help?** Ask a support question or choose a demo scenario above.")

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"], unsafe_allow_html=True)
        
        # Display response metadata if available
        if msg["role"] == "assistant" and "metadata" in msg:
            data = msg["metadata"]
            mode = data.get("reply_mode", "")
            
            # Status line
            if mode == "GROUNDED_REPLY":
                st.markdown("<div class='status-safe'>🟢 SAFE • Evidence-grounded response</div>", unsafe_allow_html=True)
            elif mode == "CAUTIOUS_REPLY" or mode == "CLARIFY":
                st.markdown("<div class='status-caution'>🟡 CAUTION • Cautious reply or clarification</div>", unsafe_allow_html=True)
            elif mode == "ESCALATE":
                st.markdown("<div class='status-escalated'>🔴 ESCALATED • Severe risk detected</div>", unsafe_allow_html=True)
            elif mode == "ABSTAIN":
                st.markdown("<div class='status-abstained'>⚪ ABSTAINED • No reliable evidence / OOD</div>", unsafe_allow_html=True)
            
            # Single compact diagnostics expander
            with st.expander("🔍 How TrustSupport handled this request"):
                safety = data.get("safety_validation", {})
                flags = ", ".join([f["risk_flag"] for f in data.get("risk_flags", [])]) or "None"
                evidence_count = len(data.get("evidence_details", []))
                st.markdown(f"""
                <div class="diagnostics-text">
                <b>Intent</b>: {data.get('intent', 'N/A')} (Confidence: {data.get('confidence', 0.0):.2f})<br/>
                <b>Risk Flags</b>: {flags}<br/>
                <b>Safety Validation</b>: {'Passed' if safety.get('passed', True) else 'Failed'}<br/>
                <b>Reply Mode</b>: {mode}<br/>
                <b>Evidence Count</b>: {evidence_count} (Max Similarity: {data.get('max_similarity', 0.0):.2f})<br/>
                <b>Generation Source</b>: {data.get('generation_source', 'N/A')}
                </div>
                """, unsafe_allow_html=True)
            
            # Evidence Explorer
            evidence = data.get("evidence_details", [])
            if evidence:
                with st.expander("📚 View Retrieved Evidence"):
                    for i, ev in enumerate(evidence[:3]):
                        clean_text = format_evidence_text(ev.get('response', ''))
                        st.markdown(f"""
                        <div class="evidence-item">
                        <b>Support Example {i+1}</b> (Similarity: {ev.get('similarity', 0.0):.2f})<br/>
                        <i>{clean_text}</i>
                        </div>
                        """, unsafe_allow_html=True)
                        if i < len(evidence[:3]) - 1:
                            st.markdown("<hr style='margin: 0.5em 0;'/>", unsafe_allow_html=True)
                        else:
                            # Optional Developer Details at the bottom
                            st.caption(f"Source Reference: {ev.get('evidence_id')}")

# Process User Input
prompt = st.chat_input("Ask a support question...")
if hasattr(st.session_state, 'demo_query') and st.session_state.demo_query:
    prompt = st.session_state.demo_query
    del st.session_state.demo_query

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)
        
    with st.chat_message("assistant"):
        status_text = st.empty()
        status_text.markdown("🧠 Understanding your request...")
        time.sleep(0.3)
        status_text.markdown("🔎 Searching relevant support evidence...")
        time.sleep(0.3)
        status_text.markdown("🛡️ Checking safety and generating response...")
        
        try:
            res = requests.post(API_URL, json={"query": prompt}, timeout=10)
            status_text.empty() # Clear loading text
            
            if res.status_code != 200:
                err_data = res.json()
                st.error(f"API Error: {err_data.get('detail', {}).get('message', res.text)}")
            else:
                data = res.json()
                reply = data.get("reply_text", "")
                
                # Format escalation correctly
                if data.get("reply_mode") == "ESCALATE":
                    flags = ", ".join([f["risk_flag"] for f in data.get("risk_flags", [])])
                    reply = f"""
<div class="escalation-card">
    <h4 style="margin-top: 0; margin-bottom: 0.5rem;">⚠️ Safety Escalation</h4>
    <p style="margin-bottom: 0.5rem;">This request requires additional review.</p>
    <p style="margin-bottom: 0.5rem;"><strong>Reason:</strong> {flags}</p>
    <p style="margin-bottom: 0.5rem; font-size: 0.9em; opacity: 0.9;">TrustSupport has intentionally avoided generating an unsupported response.</p>
    <p style="margin-bottom: 0;"><strong>Recommended Action:</strong> Contact the appropriate support channel.</p>
</div>
"""
                    st.markdown(reply, unsafe_allow_html=True)
                else:
                    st.write(reply)
                
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": reply,
                    "metadata": data
                })
                
                st.rerun()
        except requests.exceptions.ConnectionError:
            status_text.empty()
            st.error("🚨 Backend API is unreachable. Ensure FastAPI is running on port 8000.")
        except Exception as e:
            status_text.empty()
            st.error(f"An unexpected error occurred: {e}")
