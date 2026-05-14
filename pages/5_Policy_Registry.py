import streamlit as st

st.set_page_config(layout="wide")

st.title("Policy Registry")

policies = [
    ("P-12", "Vendor Change Risk"),
    ("P-19", "Approval Completeness"),
    ("P-27", "Duplicate Detection"),
    ("P-31", "Threshold Variance"),
    ("P-42", "Vendor Risk Escalation")
]

for pid, name in policies:
    st.markdown(f"### {pid}")
    st.write(name)