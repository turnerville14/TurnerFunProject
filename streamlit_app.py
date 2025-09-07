import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# --- Page Config ---
st.set_page_config(page_title="Funds Usage Tracker", layout="wide")

# --- Session State for Login ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# --- Login Component ---
if not st.session_state.logged_in:
    st.markdown("## 🔐 Please log in to continue")

    cols = st.columns([1, 2, 1])  # Center the login box
    with cols[1].container(border=True, height="stretch", vertical_alignment="center"):
        st.markdown("### Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            if username == "admin" and password == "Password123":  # Replace with secure logic
                st.session_state.logged_in = True
                st.success("Login successful!")
            else:
                st.error("Invalid credentials")

# --- Stop App if Not Logged In ---
if not st.session_state.get("logged_in", False):
    st.stop()

# --- Main App Content ---
st.markdown("<h2 style='text-align:center;'>💰 Funds Usage Tracker</h2>", unsafe_allow_html=True)
st.markdown(
    "<div style='text-align:center;'>Track your allocated budget, expenses, and remaining funds by Department and Unit.</div>",
    unsafe_allow_html=True
)
st.markdown("###### ")

# --- Data Setup ---
funddata = pd.DataFrame([
    ("Name", "Department", "Unit"),
    ("Name 1", "A", 1), ("Name 2", "A", 1), ("Name 3", "A", 2), ("Name 4", "A", 2),
    ("Name 5", "A", 3), ("Name 6", "A", 3), ("Name 7", "A", 4), ("Name 8", "A", 4),
    ("Name 9", "A", 5), ("Name 10", "B", 1), ("Name 11", "B", 1), ("Name 12", "B", 2),
    ("Name 13", "B", 2), ("Name 14", "B", 2), ("Name 15", "B", 2), ("Name 16", "B", 3),
    ("Name 17", "B", 3), ("Name 18", "B", 3), ("Name 19", "C", 1), ("Name 20", "C", 2),
    ("Name 21", "C", 3), ("Name 22", "C", 3), ("Name 23", "C", 3), ("Name 24", "D", 1),
    ("Name 25", "D", 2), ("Name 26", "D", 2), ("Name 27", "D", 3), ("Name 28", "D", 3),
    ("Name 29", "D", 3), ("Name 30", "D", 3), ("Name 31", "D", 4), ("Name 32", "D", 4),
    ("Name 33", "D", 4), ("Name 34", "D", 5), ("Name 35", "D", 6), ("Name 36", "D", 6),
    ("Name 37", "D", 6), ("Name 38", "D", 7), ("Name 39", "D", 7), ("Name 40", "D", 7)
], columns=["Name", "Department", "Unit"]).iloc[1:]

expdata = pd.DataFrame([
    ("Type", "Department", "Unit", "Amount"),
    ("Dept", "A", 0, 5), ("Dept", "B", 0, 10), ("Dept", "C", 0, 5), ("Dept", "D", 0, 8),
    ("Unit", "A", 1, 5), ("Unit", "A", 2, 10), ("Unit", "A", 3, 5), ("Unit", "A", 3, 8),
    ("Unit", "A", 3, 5), ("Unit", "A", 4, 10), ("Unit", "B", 1, 5), ("Unit", "B", 2, 8),
    ("Unit", "B", 3, 10), ("Unit", "B", 3, 5), ("Unit", "B", 3, 8), ("Unit", "B", 3, 5),
    ("Unit", "D", 2, 10), ("Unit", "D", 3, 5), ("Unit", "D", 4, 8), ("Unit", "D", 5, 10),
    ("Unit", "D", 6, 5), ("Unit", "D", 7, 8), ("Unit", "D", 2, 5), ("Unit", "D", 3, 10),
    ("Unit", "D", 4, 5), ("Unit", "D", 5, 8)
], columns=["Type", "Department", "Unit", "Amount"]).iloc[1:]

budget_dict = {"Department": 80, "Unit": 50}

# --- Filter UI ---
st.markdown("<h4 style='text-align:center;'>🔍 Filter Criteria</h4>", unsafe_allow_html=True)
layout_cols = st.columns([2, 6, 2])  # Center everything in col[1]

with layout_cols[1]:
    filter_cols = st.columns([1, 1])  # Side-by-side filters

    # --- Department Selector ---
    with filter_cols[0].container(border=True, height="stretch", vertical_alignment="center"):
        selected_departments = st.multiselect(
            "Select Departments",
            options=sorted(funddata["Department"].unique())
        )

    # --- Filter Units Based on Selected Departments ---
    if selected_departments:
        filtered_units = sorted(
            funddata[funddata["Department"].isin(selected_departments)]["Unit"].unique()
        )
    else:
        filtered_units = []

    # --- Unit Selector ---
    with filter_cols[1].container(border=True, height="stretch", vertical_alignment="center"):
        selected_units = st.multiselect(
            "Select Units",
            options=filtered_units
        )

# --- Helper Functions ---
def calculate_allocation(df, dept, unit):
    dept_count = df[df["Department"] == dept].shape[0]
    unit_count = df[(df["Department"] == dept) & (df["Unit"] == unit)].shape[0]
    return dept_count * budget_dict["Department"], unit_count * budget_dict["Unit"]

def calculate_expenses(df, dept, unit, level):
    if level == "department":
        return df[(df["Type"] == "Dept") & (df["Department"] == dept) & (df["Unit"] == 0)]["Amount"].sum()
    elif level == "unit":
        return df[(df["Type"] == "Unit") & (df["Department"] == dept) & (df["Unit"] == unit)]["Amount"].sum()
    return 0

def plot_funds_chart(title, allocated, used, container):
    remaining = allocated - used
    labels = [f"Used: ${used}", f"Remaining: ${remaining}"]
    sizes = [used, remaining]
    colors = ["#FF6B6B", "#4CAF50"]

    fig, ax = plt.subplots(figsize=(4, 4), facecolor="#1e1e1e")
    ax.set_facecolor("#1e1e1e")
    wedges, texts, autotexts = ax.pie(
        sizes,
        labels=labels,
        colors=colors,
        autopct=lambda pct: f"${int(round(pct * allocated / 100))}",
        startangle=90,
        textprops={'color': 'white', 'fontsize': 8}
    )
    ax.set_title(title, fontsize=10, color='white')
    container.pyplot(fig)

# --- Department Charts ---
if selected_departments:
    st.markdown("###### ")
    st.markdown("<h4 style='text-align:center;'>📊 Department View</h4>", unsafe_allow_html=True)

    chart_count = len(selected_departments)
    padding = (5 - chart_count) // 2 if chart_count < 5 else 0
    chart_cols = st.columns([1]*padding + [1]*chart_count + [1]*padding)

    for i, dept in enumerate(selected_departments):
        allocated, _ = calculate_allocation(funddata, dept, 0)
        used = calculate_expenses(expdata, dept, 0, "department")

        chart_cell = chart_cols[padding + i].container(border=True, height="stretch", vertical_alignment="center")
        plot_funds_chart(
            f"Department {dept} Budget Allocation: ${allocated}",
            allocated,
            used,
            chart_cell
        )

# --- Unit Charts ---
unit_chart_data = [
    (dept, unit)
    for unit in selected_units
    for dept in selected_departments
    if not funddata[(funddata["Department"] == dept) & (funddata["Unit"] == unit)].empty
]

if unit_chart_data:
    st.markdown("<h4 style='text-align:center;'>📊 Unit View</h4>", unsafe_allow_html=True)

    chart_count = len(unit_chart_data)
    padding = (5 - chart_count % 5) // 2 if chart_count % 5 and chart_count < 5 else 0

    for i, (dept, unit) in enumerate(unit_chart_data):
        if i % 5 == 0:
            row_count = min(5, chart_count - i)
            row_padding = (5 - row_count) // 2
            chart_cols = st.columns([1]*row_padding + [1]*row_count + [1]*row_padding)

        _, allocated = calculate_allocation(funddata, dept, unit)
        used = calculate_expenses(expdata, dept, unit, "unit")

        chart_cell = chart_cols[(i % 5) + row_padding].container(border=True, height="stretch", vertical_alignment="center")
        plot_funds_chart(
            f"Department {dept} Unit {unit} Budget Allocation: ${allocated}",
            allocated,
            used,
            chart_cell
        )
