import streamlit as st

st.set_page_config(
    page_title="iThoth APex Alpha",
    page_icon="🛡️",
    layout="wide"
)

def load_css():
    with open("assets/css.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

st.title("🛡️ iThoth APex Alpha")
st.subheader("Independent Trust Control for Autonomous Enterprise Execution")

st.markdown("---")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Autonomous Actions Today", "143", "+12")

with col2:
    st.metric("Protected Enterprise Value", "$612,400", "+8.2%")

with col3:
    st.metric("Blocked Executions", "13", "+3")

with col4:
    st.metric("Review Queue", "21", "-4")

st.markdown("---")

st.info(
    "APex Alpha pilot environment initialized. Governance services coming online."
)

st.markdown("### Trust Infrastructure Stack")

st.markdown("""
**APex** → Autonomous execution governance  
**EPCs** → Transaction-scoped programmable treasury execution  
**SettlementOS** → Governed liquidity-agnostic economic execution infrastructure
""")