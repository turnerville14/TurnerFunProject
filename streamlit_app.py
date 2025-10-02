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
        # 🌍 Load rates
        oldrate = pd.read_csv("oldrate.csv")
        newrate = pd.read_csv("newrate.csv")

        # Helper to parse datetime from separate date and time inputs
        def combine_datetime(date, time_str):
            return datetime.combine(date, datetime.strptime(time_str, "%H:%M").time())

        # Helper to generate 24-hour blocks
        def generate_period_blocks(start_dt, end_dt):
            blocks = []
            current_start = start_dt
            while current_start + timedelta(hours=24) < end_dt:
                current_end = current_start + timedelta(hours=24)
                blocks.append((current_start, current_end))
                current_start = current_end
            blocks.append((current_start, end_dt))
            return blocks

        # Step 1 - Flight Details
        with st.container(border=True):
        
            st.markdown("#### ✈️ Step 1 - Indicate your Travel Segments")
            
            flight_type = st.radio("Choose your trip type",["Single Country", "Multiple Country/Transit Included"],index=0)

            segments = []
            country_options = newrate["Country"].dropna().unique().tolist()
            
            if flight_type == "Single Country":
                with st.container(border=True):
                    st.markdown("###### Flight Details")

                    cols = st.columns([2, 2, 2, 2, 2])  # Add extra column for country
                    selected_country = cols[0].selectbox("Country", options=country_options, key="country_single")
                    eta_date_default = datetime.today().date()
                    eta_date = cols[1].date_input("ETA Date", value=eta_date_default, key="eta_date_single")
                    eta_time = cols[2].text_input(f"ETA Time", value="00:00", help="Enter time in 24-hour format, e.g. 18:00", key=f"eta_time_single")
                    etd_date_default = eta_date + timedelta(days=1)
                    etd_date = cols[3].date_input("ETD Date", value=etd_date_default, key="etd_date_single")
                    etd_time = cols[4].text_input("ETD Time", value="00:00", help="Enter time in 24-hour format, e.g. 12:45", key="etd_time_single")

                    try:
                        start_dt = combine_datetime(eta_date, eta_time)
                        end_dt = combine_datetime(etd_date, etd_time)
                        segments.append({
                            "start": start_dt,
                            "end": end_dt,
                            "country": selected_country
                        })
                    except ValueError:
                        st.error(f"❌ Invalid time format. Please use hh:mm (e.g. 18:00).")

            elif flight_type == "Multiple Country/Transit Included":
                with st.container(border=True):
                    cols = st.columns([2, 6])
                    with cols[0]:
                        flight_count = st.number_input("Number of flight segments", min_value=2, max_value=10, value=2)

                    for i in range(flight_count):
                        with st.container(border=True):
                            st.markdown(f"###### {'Flight 1 Details' if i == 0 else f'Flight {i+1} or Transit Details'}")

                            cols = st.columns([2, 2, 2, 2, 2])
                            selected_country = cols[0].selectbox("Country", options=country_options, key=f"country_single_{i}")

                            # Default ETA Date for next flight = ETD Date of previous flight
                            if i == 0:
                                eta_date_default = datetime.today().date()
                            else:
                                eta_date_default = segments[i - 1]["end"].date()

                            eta_date_default = datetime.today().date() if i == 0 else segments[i - 1]["end"].date()
                            eta_date = cols[1].date_input(f"ETA Date {i+1}", value=eta_date_default, key=f"eta_date_{i}")
                            eta_time = cols[2].text_input(
                                f"ETA Time {i+1}", value="00:00",
                                help="Enter time in 24-hour format, e.g. 18:00",
                                key=f"eta_time_{i}"
                            )
                            etd_date_default = eta_date + timedelta(days=1)
                            etd_date = cols[3].date_input(f"ETD Date {i+1}", value=etd_date_default, key=f"etd_date_{i}")

                            etd_time = cols[4].text_input(
                                f"ETD Time {i+1}", value="00:00",
                                help="Enter time in 24-hour format, e.g. 12:45",
                                key=f"etd_time_{i}"
                            )

                            try:
                                start_dt = combine_datetime(eta_date, eta_time)
                                end_dt = combine_datetime(etd_date, etd_time)
                                segments.append({
                                    "start": start_dt,
                                    "end": end_dt,
                                    "country": selected_country
                                })
                            except ValueError:
                                st.error(f"❌ Invalid time format in Flight {i+1}. Please use hh:mm (e.g. 18:00).")

        # Generate travel blocks with country info
        travel_blocks = []
        for seg in segments:
            blocks = generate_period_blocks(seg["start"], seg["end"])
            for block in blocks:
                travel_blocks.append({
                    "start": block[0],
                    "end": block[1],
                    "country": seg.get("country", None)  # fallback if not set
                })
        
        # Step 2 - Meal declaration
        with st.container(border=True):
            
            st.markdown("#### 🍽️ Step 2 - Meals Declaration")

            full_meals = st.radio("Was at least 1 full meal provided throughout your trip?",["Yes", "No"],index=0)

            if full_meals == "Yes":
                st.markdown("##### 🗓️ Declare meals")
                country_options = newrate["Country"].dropna().unique().tolist()

                editable_data = pd.DataFrame([{
                    "Country": block["country"],
                    "Airport": "",
                    "Period": f"{block['start'].strftime('%d %b %y %H:%M')} to {block['end'].strftime('%d %b %y %H:%M')}",
                    "Breakfast": "No",
                    "Lunch": "No",
                    "Dinner": "No"
                } for block in travel_blocks])

                edited_table = st.data_editor(
                    editable_data,
                    hide_index=True,
                    column_config={
                        "Country": st.column_config.SelectboxColumn("Country", options=country_options),
                        "Breakfast": st.column_config.SelectboxColumn("Breakfast", options=["No", "Yes", "NA"]),
                        "Lunch": st.column_config.SelectboxColumn("Lunch", options=["No", "Yes", "NA"]),
                        "Dinner": st.column_config.SelectboxColumn("Dinner", options=["No", "Yes", "NA"]),
                    }
                )
            else:
                st.info("I hereby declare that no full meals were provided throughout my trip. Meal breakdown will not be required.")

        # Step 3 - Calculator
        with st.container(border=True):
            
            # Count how many calendar month boundaries have passed since trip_start
            from dateutil.relativedelta import relativedelta

            def get_month_tier(block_start, trip_start):
                month_1_end = trip_start + relativedelta(months=1) - timedelta(days=1)
                month_2_end = trip_start + relativedelta(months=2) - timedelta(days=1)
                month_3_end = trip_start + relativedelta(months=3) - timedelta(days=1)

                if block_start <= month_1_end:
                    return 1
                elif block_start <= month_2_end:
                    return 2
                elif block_start <= month_3_end:
                    return 3
                else:
                    return 4


            st.markdown("#### 💰 Step 3 - Allowance Calculator")

            cutoff_date = datetime(2025, 3, 31)
            calculation_rows = []
            total_amount = 0.0

            # Use edited_table only if full_meals == "Yes"
            if full_meals == "Yes":
                source_table = edited_table
            else:
                # Build fallback table from travel_blocks
                source_table = pd.DataFrame([{
                    "Country": block["country"],
                    "Start": block["start"],
                    "End": block["end"],
                    "Breakfast": "NA",
                    "Lunch": "NA",
                    "Dinner": "NA"
                } for block in travel_blocks])

            trip_start = min(seg["start"] for seg in segments)

            month_tiers_used = []
            fullmeals = "Not Provided"

            for idx, row in source_table.iterrows():
                country = row["Country"]
                start = row["Start"] if full_meals == "No" else datetime.strptime(row["Period"].split(" to ")[0], "%d %b %y %H:%M")
                end = row["End"] if full_meals == "No" else datetime.strptime(row["Period"].split(" to ")[1], "%d %b %y %H:%M")
                hours = (end - start).total_seconds() / 3600

                # Determine rate source
                rate_table = oldrate if start.date() <= cutoff_date.date() else newrate
                rate_row = rate_table[rate_table["Country"] == country]
                if rate_row.empty:
                    st.warning(f"No rate found for {country}. Skipping row {idx+1}.")
                    continue
                daily_rate = rate_row.iloc[0]["Rates"]

                # Determine month tier
                month_tier = get_month_tier(start, trip_start)
                if month_tier == 1:
                    base_pct = 1.0
                elif month_tier in [2, 3]:
                    base_pct = 0.5
                else:
                    base_pct = 0.25

                month_tiers_used.append(month_tier)
                
                # Meal logic
                if full_meals == "Yes":
                    # Count how many meals are marked "Yes"
                    yes_count = sum(row[meal] == "Yes" for meal in ["Breakfast", "Lunch", "Dinner"])
                    # Count how many meals are marked "NA"
                    na_count = sum(row[meal] == "NA" for meal in ["Breakfast", "Lunch", "Dinner"])

                    # Full meals are considered provided if:
                    # - All three are "Yes"
                    # - Or if one or two are "Yes" and the rest are "NA"
                    if yes_count + na_count == 3 and yes_count >= 1:
                        allowance_pct = base_pct * (0.33 if hours >= 12 else 0.0)
                        fullmeals = "Provided"
                    else:
                        allowance_pct = base_pct * (1.0 if hours >= 12 else 0.5)
                        fullmeals = "Not Provided"
                else:
                    allowance_pct = base_pct * (1.0 if hours >= 12 else 0.5)
                    fullmeals = "Not Applicable"

                amount = daily_rate * allowance_pct
                total_amount += amount
                
                row_data = {
                    "Country": country,
                    "Start": start.strftime("%d %b %y %H:%M"),
                    "End": end.strftime("%d %b %y %H:%M"),
                    "Hours": f"{hours:.0f}",
                    "Rate Source": "Old" if rate_table is oldrate else "New",
                    "Daily Rate": f"${daily_rate:.0f}",
                    "Full Meals": {fullmeals},
                    "Step Down": f"Month {month_tier}",
                    "Allowance %": f"{allowance_pct*100:.0f}%",
                    "Amount": f"${amount:.2f}"
                }

                calculation_rows.append(row_data)
            
            avg_month_tier = sum(month_tiers_used) / len(month_tiers_used)

            with st.container(border=True):
                st.markdown(f"##### 🧾 Total Claimable Amount: **${total_amount:,.2f}**")
            if any("Month Block" in row for row in calculation_rows):
                st.markdown("##### 📆 Monthly Segmentation Applied")    
            if not avg_month_tier == 1:
                st.dataframe(pd.DataFrame(calculation_rows), hide_index=True)
            else:
                df = pd.DataFrame(calculation_rows)
                df = df.drop(columns=["Step Down"])
                st.dataframe(df, hide_index=True)

        # Step 4 - Print PDF
        with st.container(border=True):
            from reportlab.lib.pagesizes import A4, landscape
            from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
            from reportlab.lib import colors
            from reportlab.lib.styles import getSampleStyleSheet
            import tempfile

            st.markdown("#### 📄 Step 4 - Print PDF")

            styles = getSampleStyleSheet()
            elements = []

            # Step 1 - Travel Segments
            elements.append(Paragraph("Step 1 - Travel Segments", styles['Heading2']))
            travel_data = [["Country", "Start", "End"]] + [
                [seg['country'], seg['start'].strftime('%d %b %y %H:%M'), seg['end'].strftime('%d %b %y %H:%M')]
                for seg in segments
            ]
            travel_table = Table(travel_data, hAlign="LEFT")
            travel_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
            ]))
            elements.append(travel_table)
            elements.append(Spacer(1, 12))

            # Step 2 - Meals Declaration
            elements.append(Paragraph("Step 2 - Meals Declaration", styles['Heading2']))
            if full_meals == "Yes":
                meals_data = [["Country", "Airport", "Period", "Breakfast", "Lunch", "Dinner"]] + [
                    [row['Country'], row.get('Airport', ''), row['Period'], row['Breakfast'], row['Lunch'], row['Dinner']]
                    for _, row in edited_table.iterrows()
                ]
            else:
                meals_data = [["No full meals declared"]]
            meals_table = Table(meals_data, hAlign="LEFT")
            meals_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
            ]))
            elements.append(meals_table)
            elements.append(Spacer(1, 12))

            # Step 3 - Allowance Calculator
            elements.append(Paragraph("Step 3 - Allowance Calculator", styles['Heading2']))
            allowance_data = [["Country", "Start", "End", "Hours", "Rate Source", "Daily Rate", "Full Meals", "Step Down", "Allowance %", "Amount"]] + [
                [row['Country'], row['Start'], row['End'], row['Hours'], row['Rate Source'], row['Daily Rate'],
                row['Full Meals'], row['Step Down'], row['Allowance %'], row['Amount']]
                for row in calculation_rows
            ]
            allowance_table = Table(allowance_data, hAlign="LEFT")
            allowance_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
            ]))
            elements.append(allowance_table)
            elements.append(Spacer(1, 12))

            # Total Amount
            elements.append(Paragraph(f"<b>Total Claimable Amount: ${total_amount:,.2f}</b>", styles['Heading3']))

            # Generate PDF
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmpfile:
                doc = SimpleDocTemplate(tmpfile.name, pagesize=landscape(A4), rightMargin=20, leftMargin=20, topMargin=20, bottomMargin=20)
                doc.build(elements)

                with open(tmpfile.name, "rb") as f:
                    st.download_button(
                        label="📥 Download PDF",
                        data=f.read(),
                        file_name="Travel_Allowance_Claim.pdf",
                        mime="application/pdf"
                    )






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

