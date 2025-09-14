import streamlit as st

#check if there is an active login
if not st.session_state.get("logged_in", False):
    st.warning("🔒 You must log in first.")
    st.switch_page("streamlit_app.py")

# --- Page Config ---
st.set_page_config(page_title="Home Page", layout="wide")

# Create 5 columns for layout (padding on sides)
cols = st.columns([1, 2, 2, 2, 1])

with cols[1]:
    if st.button("💰 Funds", key="btn1"):
        st.switch_page("pages/funds.py")

with cols[2]:
    if st.button("🧮 Calculator", key="btn2"):
        st.switch_page("pages/calculator.py")

with cols[3]:
    if st.button("🔢 Unique Digit", key="btn3"):
        st.switch_page("pages/uniquedigit.py")