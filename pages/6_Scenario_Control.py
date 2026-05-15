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

st.markdown("---")

risk_score = 0
findings = []
policies = []

if amount > 100000:
    risk_score += 35
    findings.append("High-value transaction exceeds autonomous execution threshold.")
    policies.append("Invoice Amount Threshold Enforcement")

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
    st.write(f"Vendor Risk: {vendor_risk}")
    st.write(f"Geography: {geography}")
    st.write(f"Urgency: {urgency}")
    st.write(f"Weekend Execution: {'Yes' if weekend else 'No'}")

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