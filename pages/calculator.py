import streamlit as st
import pandas as pd
from datetime import datetime, timedelta, time, date

st.set_page_config(layout="centered", page_title="Trip Allowance Calculator")

# --- Session State for Login ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# --- Redirect if Not Logged In ---
if not st.session_state.logged_in:
    errorcols = st.columns([1, 2, 1])  # Center the login box 
    with errorcols[1].container(height="stretch", vertical_alignment="center"):
        st.error("❌ Invalid Login Session! ❌")
        st.markdown("""
            <meta http-equiv="refresh" content="0; url=/" />
        """, unsafe_allow_html=True)
    st.stop()

# --- Stop App if Not Logged In ---
if not st.session_state.get("logged_in", False):
    st.stop()

# 🌍 Country Daily Rates
country_rates = {
    "Singapore": 100,
    "Cambodia": 120,
    "Thailand": 130,
    "Indonesia": 140
}

# 🍽️ Meal Eligibility Logic
def is_meal_provided(b, l, d):
    combo = [b, l, d]
    yes_count = combo.count("Yes")
    na_count = combo.count("NA")
    return yes_count >= 1 and na_count >= 2 or yes_count == 2 and na_count == 1

# 📉 Monthly Discount Logic
def get_discount_for_date(date, eta):
    month_diff = (date.year - eta.year) * 12 + (date.month - eta.month)
    if month_diff == 0:
        return 1.0
    elif month_diff in [1, 2]:
        return 0.75
    else:
        return 0.5

# 🕒 Generate True 24-Hour Blocks from ETA
def generate_day_ranges(eta, etd):
    ranges = []
    current_start = eta
    while current_start < etd:
        current_end = current_start + timedelta(hours=24)
        if current_end > etd:
            current_end = etd
        ranges.append((current_start.date().strftime("%Y-%m-%d"), current_start, current_end))
        current_start = current_end
    return ranges

# 🧮 Core Calculation
def calculate_allowance(ranges, country, meal_inputs):
    base_rate = country_rates.get(country, 0)
    breakdown = []
    total_allowance = 0

    for day_str, start, end in ranges:
        duration = round((end - start).total_seconds() / 3600)
        is_partial = duration < 24
        meals = meal_inputs.get(day_str, {"Breakfast": "NA", "Lunch": "NA", "Dinner": "NA"})
        meals_yes = is_meal_provided(meals["Breakfast"], meals["Lunch"], meals["Dinner"])
        modifier = 0.33 if meals_yes else 1.0
        discount = get_discount_for_date(start.date(), ranges[0][1].date())
        final_rate = base_rate * discount * modifier
        total_allowance += final_rate

        breakdown.append({
            "Date": day_str,
            "Time Range": f"{start.strftime('%H:%M')} → {end.strftime('%H:%M')}",
            "Duration (hrs)": f"{duration}" + (" 🟡" if is_partial else ""),
            "Breakfast": meals["Breakfast"],
            "Lunch": meals["Lunch"],
            "Dinner": meals["Dinner"],
            "Meals Provided": "Yes" if meals_yes else "No",
            "Rate Modifier": f"{int(modifier * 100)}%",
            "Discount": f"{int(discount * 100)}%",
            "Final Rate": round(final_rate, 2)
        })

    df = pd.DataFrame(breakdown)
    return total_allowance, df

# 🖥️ UI
st.markdown("## 🌍 Trip Allowance Calculator")

current_year = datetime.now().year
col1, col2 = st.columns(2)
with col1:
    eta_date = st.date_input("ETA Date", value=date(current_year, 1, 1))
    eta_time = st.time_input("ETA Time", value=time(0, 0))
    eta = datetime.combine(eta_date, eta_time)
with col2:
    etd_date = st.date_input("ETD Date", value=date(current_year, 1, 4))
    etd_time = st.time_input("ETD Time", value=time(0, 0))
    etd = datetime.combine(etd_date, etd_time)

country = st.selectbox("Select Country", list(country_rates.keys()))

# 🍽️ Meal Inputs in Table Format
st.markdown("### 🍽️ Daily Meal Declarations")
meal_inputs = {}
day_ranges = generate_day_ranges(eta, etd)

meal_table = []
for day_str, start, end in day_ranges:
    cols = st.columns(4)
    cols[0].markdown(f"**{day_str}**")
    b = cols[1].selectbox("Breakfast", ["Yes", "No", "NA"], key=f"{day_str}_b")
    l = cols[2].selectbox("Lunch", ["Yes", "No", "NA"], key=f"{day_str}_l")
    d = cols[3].selectbox("Dinner", ["Yes", "No", "NA"], key=f"{day_str}_d")
    meal_inputs[day_str] = {"Breakfast": b, "Lunch": l, "Dinner": d}

# 🧮 Calculate
if st.button("Calculate Allowance"):
    total, df = calculate_allowance(day_ranges, country, meal_inputs)
    st.markdown("### 🧾 Trip Summary")
    st.markdown(f"**Total Allowance: ${total:,.2f}**")
    st.markdown("#### 📊 Daily Breakdown")
    st.dataframe(df.style.format({"Final Rate": "${:,.2f}"}))