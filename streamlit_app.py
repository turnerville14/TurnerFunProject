import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Page config
st.set_page_config(page_title="Funds Usage Tracker", layout="wide")

# Title
st.title("💰 Funds Usage Tracker")
st.markdown("Track your allocated budget, expenses, and remaining funds by Department and Unit.")

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

# --- User Input ---
st.sidebar.header("🔍 Filter Criteria")
selected_departments = st.sidebar.multiselect("Select Departments", sorted(funddata["Department"].unique()))
selected_units = st.sidebar.multiselect("Select Units", sorted(funddata["Unit"].unique()))

# --- Helper Functions ---
def calculate_allocation(df, dept, unit):
    dept_count = df[df["Department"] == dept].shape[0]
    unit_count = df[(df["Department"] == dept) & (df["Unit"] == unit)].shape[0]
    return dept_count * budget_dict["Department"], unit_count * budget_dict["Unit"]

def calculate_expenses(df, dept, unit, level):
    if level == "department":
        # Department-level expenses: Unit should be 0
        return df[(df["Type"] == "Dept") & (df["Department"] == dept) & (df["Unit"] == 0)]["Amount"].sum()
    elif level == "unit":
        # Unit-level expenses: Match both department and unit
        return df[(df["Type"] == "Unit") & (df["Department"] == dept) & (df["Unit"] == unit)]["Amount"].sum()
    return 0

def plot_funds_chart(title, allocated, used, container):
    remaining = allocated - used
    labels = [f"Used: ${used}", f"Remaining: ${remaining}"]
    sizes = [used, remaining]
    colors = ["#F44336", "#4CAF50"]

    fig, ax = plt.subplots(figsize=(4, 4))
    wedges, texts, autotexts = ax.pie(
        sizes,
        labels=labels,
        colors=colors,
        autopct=lambda pct: f"${int(round(pct * allocated / 100))}",
        startangle=90,
        textprops={'fontsize': 8}
    )
    ax.set_title(title, fontsize=10)
    container.pyplot(fig)

# --- Visualization Containers ---
st.subheader("📊 Department View")
dept_container = st.container()
cols_dept = dept_container.columns(5)

for i, dept in enumerate(selected_departments):
    if i % 5 == 0:
        cols_dept = dept_container.columns(5)  # Start a new row every 5 charts

    allocated, _ = calculate_allocation(funddata, dept, 0)
    used = calculate_expenses(expdata, dept, 0, "department")

    plot_funds_chart(
        f"Department {dept} Budget Allocation: ${allocated}",
        allocated,
        used,
        cols_dept[i % 5]
    )

st.subheader("📊 Unit View")
unit_container = st.container()
cols_unit = unit_container.columns(5)
unit_chart_index = 0

for unit in selected_units:
    for dept in selected_departments:
        # Only proceed if this (dept, unit) combo exists in funddata
        if not funddata[(funddata["Department"] == dept) & (funddata["Unit"] == unit)].empty:
            # Start a new row every 5 charts
            if unit_chart_index % 5 == 0:
                cols_unit = unit_container.columns(5)

            _, allocated = calculate_allocation(funddata, dept, unit)
            used = calculate_expenses(expdata, dept, unit, "unit")

            plot_funds_chart(
                f"Department {dept} Unit {unit} Budget Allocation: ${allocated}",
                allocated,
                used,
                cols_unit[unit_chart_index % 5]
            )

            unit_chart_index += 1