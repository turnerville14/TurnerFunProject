import streamlit as st
import pandas as pd
from itertools import product
import re

#check if there is an active login
if not st.session_state.get("logged_in", False):
    st.warning("🔒 You must log in first.")
    st.switch_page("streamlit_app.py")

# --- Page Config ---
st.set_page_config(page_title="Custom Digit Combinations", layout="wide")

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

st.title("🔢 Unique 4-Digit Combinations Generator")

st.markdown("Enter digit options for each position using commas, spaces, or both. Example: `1 3`, `2,4,0`, or `1, 3 4`")

# Input fields
col1, col2 = st.columns(2)
with col1:
    first_input = st.text_input("1st Digit Options", value="1 3")
    third_input = st.text_input("3rd Digit Options", value="2 4 0")
with col2:
    second_input = st.text_input("2nd Digit Options", value="1 3")
    fourth_input = st.text_input("4th Digit Options", value="2 4 0")

def parse_digits(input_str):
    # Replace commas with spaces, then split on whitespace
    tokens = re.split(r"[,\s]+", input_str.strip())
    try:
        return sorted(set(int(x) for x in tokens if x.isdigit()))
    except ValueError:
        return []

# Parse inputs
first_digits = parse_digits(first_input)
second_digits = parse_digits(second_input)
third_digits = parse_digits(third_input)
fourth_digits = parse_digits(fourth_input)

# Validate
if not all([first_digits, second_digits, third_digits, fourth_digits]):
    st.error("Please enter valid digits for all positions.")
else:
    # Generate all combinations
    raw_combinations = list(product(first_digits, second_digits, third_digits, fourth_digits))

    # Deduplicate based on digit sets
    unique_sets = set()
    unique_combinations = []
    for combo in raw_combinations:
        sorted_tuple = tuple(sorted(combo))
        if sorted_tuple not in unique_sets:
            unique_sets.add(sorted_tuple)
            unique_combinations.append(combo)

    # Display results
    df = pd.DataFrame(unique_combinations, columns=["1st", "2nd", "3rd", "4th"])
    st.subheader("📋 Unique Combinations")
    st.dataframe(df, height=1200, use_container_width=True)
    st.markdown(f"**✅ Total Unique Combinations:** {len(df)}")