import streamlit as st
import json
from datetime import datetime

from services.evaluator import evaluate_action
from services.audit import load_audit_log, save_audit_log

st.set_page_config(layout="wide")

def load_css():
    with open("assets/css.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

with open("data/scenarios.json") as f:
    actions = json.load(f)

st.title("Governance Decision Center")
st.caption("Forensic review and governance intervention for autonomous execution")

selected = st.selectbox(
    "Select Autonomous Action",
    actions,
    format_func=lambda x: f"{x['id']} — {x['vendor_name']}"
)

evaluation = evaluate_action(selected)

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

st.markdown("### APex Trust Evaluation")

trust_col = st.columns([1, 1])

with trust_col[0]:
    st.markdown(
        f"""
        <div style="
            background:#fee2e2;
            padding:24px;
            border-radius:16px;
            text-align:center;
            border:1px solid #fca5a5;
        ">
            <h2>{evaluation['decision']}</h2>
            <h3>APex Risk Score: {evaluation['risk_score']}</h3>
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown("---")

st.subheader("Operator Controls")

button_col = st.columns([1, 1, 1, 4])

risk = evaluation["risk_score"]

with button_col[0]:
    execute_clicked = False
    if risk >= 75:
        execute_clicked = st.button("Override")
    else:
        execute_clicked = st.button("Execute")

with button_col[1]:
    hold_clicked = False
    if risk >= 75:
        hold_clicked = st.button("Escalate")
    else:
        hold_clicked = st.button("Hold")

with button_col[2]:
    third_clicked = False
    if 25 < risk < 75:
        third_clicked = st.button("Escalate")
    elif risk >= 75:
        third_clicked = st.button("Block")

alert_col = st.columns([1, 1])

with alert_col[0]:
    if execute_clicked:
        if risk >= 75:
            st.warning("Override pathway initiated.")
        else:
            st.success("Execution initiated.")

    if hold_clicked:
        if risk >= 75:
            st.warning("Action escalated for executive review.")
        else:
            st.warning("Execution placed on hold.")

    if third_clicked:
        if risk >= 75:
            st.error("Execution blocked.")
        else:
            st.warning("Action escalated for human review.")

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