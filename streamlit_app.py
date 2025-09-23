import streamlit as st
import pandas as pd
from datetime import datetime, timedelta, time, date
from itertools import product
import re
import matplotlib.pyplot as plt

# --- Page Config ---
st.set_page_config(page_title="JG Portal", layout="wide")

st.markdown("""
    <style>
    .stApp {
        background-color: #0e1117;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# --- Session State ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "active_tab" not in st.session_state:
    st.session_state.active_tab = None

def inject_css():
    st.markdown("""
        <style>
        /* Remove vertical spacing around selectboxes */
        div[data-testid="stSelectbox"] {
            padding-top: 0rem;
            padding-bottom: 0rem;
            margin-top: 0rem;
            margin-bottom: 0rem;
        }

        /* Optional: tighten column spacing */
        [data-testid="column"] > div {
            gap: 0rem !important;
        }

        /* Optional: hide selectbox label space */
        label[data-testid="stLabel"] {
            display: none;
        }
        </style>
    """, unsafe_allow_html=True)


# --- RGB Login Container ---
def rgb_container():
    st.markdown("""
        <style>
        .rgb-box {
            animation: rgbGlow 5s ease-in-out infinite;
            padding: 2rem;
            border-radius: 15px;
            background-color: #0f0f0f;
            color: white;
            text-align: center;
            width: 100%;
        }

        @keyframes rgbGlow {
            0%   { box-shadow: 0 0 20px red; }
            14%  { box-shadow: 0 0 20px orange; }
            28%  { box-shadow: 0 0 20px yellow; }
            42%  { box-shadow: 0 0 20px green; }
            57%  { box-shadow: 0 0 20px cyan; }
            71%  { box-shadow: 0 0 20px blue; }
            85%  { box-shadow: 0 0 20px violet; }
            100% { box-shadow: 0 0 20px red; }
        }

        input[type="password"] {
            background-color: #1e1e1e;
            color: white;
            border: 1px solid #555;
            border-radius: 8px;
            padding: 0.5rem;
            width: 80%;
            margin-top: 1rem;
        }

        .input-row {
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 1rem;
            margin-top: 1rem;
        }

        .input-row input[type="password"] {
            flex: 1;
            width: auto;
        }

        .login-button {
            background-color: #333;
            color: white;
            border: none;
            padding: 0.5rem 1rem;
            border-radius: 8px;
            margin-top: 1rem;
            cursor: pointer;
            flex-shrink: 0;
            transition: background-color 0.4s ease-in-out;
        }

        .login-button:hover {
            background-color: #555;
        }
        </style>

        <form action="" method="get">
            <div class="rgb-box">
                <h4>🔐 Login Portal</h4>
                <div class="input-row">
                    <input name="password_input" type="password" placeholder="Password"/>
                    <button class="login-button">Login</button>
                </div>
            </div>
        </form>
    """, unsafe_allow_html=True)

# --- Main Layout ---
logincol = st.columns([1, 3, 1])
with logincol[1]:
    if not st.session_state.logged_in:
        rgb_container()
        password = st.query_params.get("password_input", "")
        if password:
            if password == "Password123":
                st.session_state.logged_in = True
                st.write ("")
                st.write ("")
                st.success("Access Granted ✅")
                st.markdown("""
                    <div style="
                        border: 2px solid #888;
                        border-radius: 8px;
                        padding: 0.75rem 1rem;
                        background-color: #1e1e1e;
                        color: white;
                        font-style: italic;
                        font-weight: bold;
                        #text-align: center;
                        margin-bottom: 1rem;
                    ">
                        Click any of the buttons below
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.write ("")
                st.write ("")
                st.error("Incorrect Password ❌")

# --- Post-login UI ---
if st.session_state.logged_in:
    cols = st.columns([1, 2, 2, 2, 2, 2, 1])

    with cols[1]:
        if st.button("💰 Funds", key="btn1"):
            st.session_state.active_tab = "funds"
    with cols[2]:
        if st.button("🧮 Calculator", key="btn2"):
            st.session_state.active_tab = "calculator"
    with cols[3]:
        if st.button("🔢 Unique Digit", key="btn3"):
            st.session_state.active_tab = "unique_digit"
    with cols[4]:
        if st.button("🔢 Database Reader", key="btn4"):
            st.session_state.active_tab = "db_reader"
    with cols[5]:
        if st.button("🔢 Funds Reader", key="btn5"):
            st.session_state.active_tab = "fund_reader"
    
    # --- Module Logic ---
    if st.session_state.active_tab == "calculator":
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
        st.markdown("<h3 style='text-align:center;'>🌍 Trip Allowance Calculator</h2>", unsafe_allow_html=True)

        current_year = datetime.now().year
        col0, col1, col2, col3, col4 = st.columns([1,1,1,1,1])
        with col0:
            country = st.selectbox("Select Country", list(country_rates.keys()))
        with col1:
            eta_date = st.date_input("ETA Date", value=date(current_year, 1, 1))
        with col2:
            eta_time = st.time_input("ETA Time", value=time(0, 0))
        with col3:
            etd_date = st.date_input("ETD Date", value=date(current_year, 1, 4))
        with col4:
            etd_time = st.time_input("ETD Time", value=time(0, 0))

        eta = datetime.combine(eta_date, eta_time)
        etd = datetime.combine(etd_date, etd_time)

        # 🍽️ Meal Inputs in Table Format
        st.markdown("<h3 style='text-align:center;'>🍽️ Daily Meal Declarations</h2>", unsafe_allow_html=True)
        meal_inputs = {}
        day_ranges = generate_day_ranges(eta, etd)

        meal_table = []        
        colheader = st.columns(5)
        colheader[0].markdown("<h6 style='text-align: center;'>Date</h4>", unsafe_allow_html=True)
        colheader[1].markdown("<h6 style='text-align: center;'>Country</h4>", unsafe_allow_html=True)
        colheader[2].markdown("<h6 style='text-align: center;'>Breakfast</h4>", unsafe_allow_html=True)
        colheader[3].markdown("<h6 style='text-align: center;'>Lunch</h4>", unsafe_allow_html=True)
        colheader[4].markdown("<h6 style='text-align: center;'>Dinner</h4>", unsafe_allow_html=True)
        for day_str, start, end in day_ranges:
            cols = st.columns(5)
            cols[0].write("")
            cols[0].write("")
            cols[0].markdown(f"<h6 style='text-align: center;'>{day_str}</h6>", unsafe_allow_html=True)
            cols[1].write("")
            cols[1].write("")
            cols[1].markdown(f"<h6 style='text-align: center;'>{country}</h6>", unsafe_allow_html=True)
            b = cols[2].selectbox("", ["NA", "Yes", "No"], key=f"{day_str}_b")
            l = cols[3].selectbox("", ["NA", "Yes", "No"], key=f"{day_str}_l")
            d = cols[4].selectbox("", ["NA", "Yes", "No"], key=f"{day_str}_d")
            meal_inputs[day_str] = {"Breakfast": b, "Lunch": l, "Dinner": d}

        # 🧮 Calculate
        if st.button("Calculate Allowance"):
            total, df = calculate_allowance(day_ranges, country, meal_inputs)
            st.markdown("### 🧾 Trip Summary")
            st.markdown(f"**Total Allowance: ${total:,.2f}**")
            st.markdown("#### 📊 Daily Breakdown")
            st.dataframe(df.style.format({"Final Rate": "${:,.2f}"}))

    elif st.session_state.active_tab == "funds":
        # --- Main App Content ---
        st.markdown("<h3 style='text-align:center;'>💰 Funds Usage Tracker</h2>", unsafe_allow_html=True)
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

        def get_chart_columns(count, max_per_row=5):
            # Always return 5 columns for consistent sizing
            padding = (max_per_row - count) // 2 if count < max_per_row else 0
            layout = [1]*padding + [1]*count + [1]*(max_per_row - count - padding)
            return st.columns(layout), padding

        # --- Department Charts ---
        if selected_departments:
            st.markdown("###### ")
            st.markdown("<h4 style='text-align:center;'>📊 Department View</h4>", unsafe_allow_html=True)

            chart_cols, padding = get_chart_columns(len(selected_departments))

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

            for i in range(0, len(unit_chart_data), 5):
                row_data = unit_chart_data[i:i+5]
                chart_cols, padding = get_chart_columns(len(row_data))

                for j, (dept, unit) in enumerate(row_data):
                    _, allocated = calculate_allocation(funddata, dept, unit)
                    used = calculate_expenses(expdata, dept, unit, "unit")

                    chart_cell = chart_cols[padding + j].container(border=True, height="stretch", vertical_alignment="center")
                    plot_funds_chart(
                        f"Department {dept} Unit {unit} Budget Allocation: ${allocated}",
                        allocated,
                        used,
                        chart_cell
                    )

    elif st.session_state.active_tab == "unique_digit":
        #main app codes        
        st.markdown("<h3 style='text-align:center;'>🔢 Unique 4-Digit Combinations Generator</h2>", unsafe_allow_html=True)
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
            st.subheader(f"**✅ Total Unique Combinations:** {len(df)}")
            st.subheader("📋 Unique Combinations")
            st.dataframe(df, height=1200, use_container_width=True)
            
    elif st.session_state.active_tab == "db_reader":
        # Load CSV from root folder
        df = pd.read_csv("database.csv")

        st.write("📝 Edit CSV Data Below")
        edited_df = st.data_editor(df, num_rows="dynamic")

        # Save button
        if st.button("💾 Save Changes"):
            edited_df.to_csv("database.csv", index=False)
            st.success("✅ Changes saved to database.csv")

        # Calculate totals
        total_a = edited_df[edited_df["Department"] == "A"]["Amount"].sum()
        total_b = edited_df[edited_df["Department"] == "B"]["Amount"].sum()
        grand_total = edited_df["Amount"].sum()

        # Display totals
        st.markdown("### 💰 Department Spending Summary")
        st.write(f"**Department A Total:** ${total_a:,.2f}")
        st.write(f"**Department B Total:** ${total_b:,.2f}")
        st.write(f"**Grand Total:** ${grand_total:,.2f}")

    elif st.session_state.active_tab == "fund_reader":
        def load_and_clean_funds(file_path):
            # Load and rename columns
            df = pd.read_csv(file_path)
            df.columns = ['Type', 'Dept', 'Unit', 'Dept1_Fund', 'Unit_Fund', 'Dept2_Fund']

            # Resolve correct amount based on Type
            def resolve_amount(row):
                if row['Type'] == 'D1':
                    return row['Dept1_Fund']
                elif row['Type'] == 'D2':
                    return row['Dept2_Fund']
                elif row['Type'] == 'U1':
                    return row['Unit_Fund']
                return None

            df['Amount'] = df.apply(resolve_amount, axis=1)

            # Build dictionary
            fund_dict = {
                (row['Type'], row['Dept'], row['Unit']): row['Amount']
                for _, row in df.iterrows()
            }

            return df[['Type', 'Dept', 'Unit', 'Amount']], fund_dict

        # Streamlit UI
        st.title("💰 Fund Allocation Viewer")

        cleaned_df, funds_dict = load_and_clean_funds("funds.csv")

        st.subheader("📊 Cleaned Fund Table")
        st.table(cleaned_df)

        st.subheader("🧠 Fund Dictionary")
        st.json(funds_dict)

