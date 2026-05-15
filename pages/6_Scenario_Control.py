import streamlit as st
from services.ui_helpers import decision_color

st.set_page_config(layout="wide")

st.title("Scenario Control")
st.caption("Interactive what-if governance simulation environment")

st.markdown("---")

st.subheader("Scenario Variables")

amount = st.slider(
    "Transaction Amount ($)",
    min_value=5000,
    max_value=500000,
    value=125000,
    step=5000
)

agent_confidence = st.slider(
    "Agent Confidence (%)",
    min_value=50,
    max_value=100,
    value=92,
    step=1
)

vendor_risk = st.selectbox(
    "Vendor Risk Profile",
    ["Low", "Medium", "High"]
)

geography = st.selectbox(
    "Execution Geography",
    ["Domestic", "Cross-Border", "High-Risk Jurisdiction"]
)

urgency = st.selectbox(
    "Execution Urgency",
    ["Standard", "Urgent", "Emergency"]
)

weekend = st.toggle("Weekend Execution Request")
vendor_bank_modified = st.toggle("Vendor Banking Modified")
approval_complete = st.toggle("Approval Chain Complete", value=True)
duplicate_submission = st.toggle("Duplicate Submission Suspected")

st.markdown("---")

risk_score = 0
findings = []
policies = []

if amount > 100000:
    risk_score += 35
    findings.append("High-value transaction exceeds autonomous execution threshold.")
    policies.append("Invoice Amount Threshold Enforcement")

if agent_confidence < 85:
    risk_score += 20
    findings.append("Reduced agent confidence increases governance uncertainty.")
    policies.append("AI Confidence Review")

if agent_confidence < 70:
    risk_score += 35
    findings.append("Agent confidence below safe autonomous execution threshold.")
    policies.append("AI Confidence Escalation")

if vendor_risk == "Medium":
    risk_score += 15
    findings.append("Vendor risk profile elevated.")
    policies.append("Dynamic Vendor Trust Scoring")

if vendor_risk == "High":
    risk_score += 35
    findings.append("High-risk vendor requires governance review.")
    policies.append("Vendor Risk Escalation")

if geography == "Cross-Border":
    risk_score += 20
    findings.append("Cross-border execution requires heightened governance.")
    policies.append("Cross-Border Payment Review")

if geography == "High-Risk Jurisdiction":
    risk_score += 40
    findings.append("Execution destination classified as high-risk.")
    policies.append("High-Risk Geography Review")

if urgency == "Urgent":
    risk_score += 10
    findings.append("Urgent execution introduces elevated operational risk.")
    policies.append("Execution Timing Risk")

if urgency == "Emergency":
    risk_score += 20
    findings.append("Emergency execution requires exception handling review.")
    policies.append("Emergency Exception Pathway")

if weekend:
    risk_score += 15
    findings.append("Weekend execution violates standard operating controls.")
    policies.append("Weekend Execution Restriction")

if vendor_bank_modified:
    risk_score += 30
    findings.append("Vendor banking details recently modified.")
    policies.append("Vendor Bank Account Change Hold")

if not approval_complete:
    risk_score += 25
    findings.append("Approval chain incomplete.")
    policies.append("Approval Completeness Validation")

if duplicate_submission:
    risk_score += 35
    findings.append("Possible duplicate submission detected.")
    policies.append("Duplicate Invoice Detection")

if risk_score <= 25:
    decision = "EXECUTE"
elif risk_score < 75:
    decision = "REVIEW REQUIRED"
else:
    decision = "HARD BLOCK"

color = decision_color(decision)

col1, col2 = st.columns(2)

with col1:
    st.subheader("Simulated Autonomous Proposal")

    st.write(f"Transaction Amount: ${amount:,.0f}")
    st.write(f"Agent Confidence: {agent_confidence}%")
    st.write(f"Vendor Risk: {vendor_risk}")
    st.write(f"Geography: {geography}")
    st.write(f"Urgency: {urgency}")
    st.write(f"Weekend Execution: {'Yes' if weekend else 'No'}")
    st.write(f"Vendor Banking Modified: {'Yes' if vendor_bank_modified else 'No'}")
    st.write(f"Approval Chain Complete: {'Yes' if approval_complete else 'No'}")
    st.write(f"Duplicate Submission Suspected: {'Yes' if duplicate_submission else 'No'}")

with col2:
    st.subheader("APex Trust Evaluation")

    st.markdown(
        f"""
        <div style="
            background:{color};
            padding:20px;
            border-radius:16px;
            color:white;
            text-align:center;
        ">
            <h2>{decision}</h2>
            <h3>APex Risk Score: {risk_score}</h3>
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown("---")

st.subheader("Triggered Findings")

if findings:
    for item in findings:
        st.write(f"• {item}")
else:
    st.success("No governance concerns detected.")

st.markdown("---")

st.subheader("Triggered Policies")

if policies:
    for policy in policies:
        st.write(f"• {policy}")
else:
    st.success("No policy interventions triggered.")