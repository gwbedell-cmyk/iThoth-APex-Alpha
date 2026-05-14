import streamlit as st
import json
from datetime import datetime

from services.evaluator import evaluate_action
from services.ui_helpers import decision_color
from services.audit import load_audit_log, save_audit_log

st.set_page_config(layout="wide")

with open("data/scenarios.json") as f:
    actions = json.load(f)

st.title("Governance Decision Center")

selected = st.selectbox(
    "Select Autonomous Action",
    actions,
    format_func=lambda x: f"{x['id']} — {x['vendor_name']}"
)

evaluation = evaluate_action(selected)
color = decision_color(evaluation["decision"])

st.subheader("Proposed Autonomous Action")

st.write(f"Agent: {selected['agent_id']}")
st.write(f"Vendor: {selected['vendor_name']}")
st.write(f"Invoice: {selected['invoice_id']}")
st.write(f"Amount: ${selected['amount']:,.0f}")
st.write(f"Agent Confidence: {int(selected['confidence'] * 100)}%")

st.markdown("---")

st.subheader("Triggered Findings")

for item in evaluation["explanations"]:
    st.write(f"• {item}")

st.markdown("---")

st.markdown(
    f"""
    <div style="
        background:{color};
        padding:24px;
        border-radius:16px;
        color:white;
        text-align:center;
    ">
        <h2>{evaluation['decision']}</h2>
        <h3>Risk Score: {evaluation['risk_score']}</h3>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown("---")

st.subheader("Operator Controls")

c1, c2, c3 = st.columns(3)

if c1.button("Approve Execution"):
    st.success("Execution approved.")

if c2.button("Escalate Review"):
    st.warning("Action escalated for human review.")

if c3.button("Block Execution"):
    st.error("Execution blocked.")

st.markdown("---")

st.subheader("Executive Override Authorization")

override_reason = st.text_area(
    "Business justification required"
)

if st.button("Override Decision"):
    if override_reason.strip():
        log = load_audit_log()

        log.append({
            "timestamp": datetime.utcnow().isoformat(),
            "action_id": selected["id"],
            "agent_id": selected["agent_id"],
            "vendor_name": selected["vendor_name"],
            "decision": "EXECUTIVE OVERRIDE",
            "risk_score": evaluation["risk_score"],
            "triggered_policies": evaluation["triggered_policies"],
            "findings": [override_reason]
        })

        save_audit_log(log)

        st.success("Executive override recorded in Black Box Recorder.")
    else:
        st.error("Override justification required.")