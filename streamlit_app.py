import streamlit as st
import pandas as pd
from datetime import datetime, timedelta, time, date
from itertools import product
import re
import matplotlib.pyplot as plt
import math
import time
import plotly.graph_objects as go
import os

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

hide_streamlit_style = """
            <style>
                /* Hide the Streamlit header and menu */
                header {visibility: hidden;}
                /* Optionally, hide the footer */
                .streamlit-footer {display: none;}
                /* Hide your specific div class, replace class name with the one you identified */
                .st-emotion-cache-uf99v8 {display: none;}
            </style>
            """

st.markdown(hide_streamlit_style, unsafe_allow_html=True)

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
    topcols = st.columns([1,10,1])
    with topcols[1]:
        # --- Custom CSS for Grand Look ---
        st.markdown("""
            <style>
            @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700&display=swap');

            .clock {
                font-family: 'Orbitron', sans-serif;
                font-size: 25px;
                text-align: center;
                margin-top: 100px;
                line-height: 1.6;
                letter-spacing: 8px;
            }

            .date {
                background: linear-gradient(90deg, red, orange, yellow, green, cyan, blue, violet);
                background-size: 400% 100%;
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                animation: hueShift 5s linear infinite;
                filter: hue-rotate(0deg);
            }

            @keyframes hueShift {
                100% { filter: hue-rotate(0deg); }
                0% { filter: hue-rotate(360deg); }
            }

            .stApp {
                background-color: #000000;
            }
            </style>
        """, unsafe_allow_html=True)
        from streamlit_autorefresh import st_autorefresh

        # st_autorefresh(interval=1000, limit=None, key="clock_refresh")
        
        # --- Clock Display ---
        clock_placeholder = st.empty()
        now = datetime.now() + timedelta(hours=8)

        # Format time, day, and date
        current_time = now.strftime("%H:%M:%S")
        current_day = now.strftime("%A")
        current_date = now.strftime("%d %B %Y")
        # Combine into one HTML block
        clock_html = f"""
            <div class='clock'>
                <div class='date'>{current_date} ({current_day}) {current_time}</div>
                <br>
                <div>⚽ <span class='date' style="letter-spacing:25px;">SOCCER TRENDS</span></div>
                <br>
            </div>
        """

        clock_placeholder.markdown(clock_html, unsafe_allow_html=True)

        st.write("")

        def local_css():
            st.markdown("""
            <style>
            .baccarat-cell {
                width: 40px;
                height: 40px;
                border: 1px solid #ddd;
                display: flex;
                align-items: center;
                justify-content: center;
                font-weight: bold;
                font-size: 14px;
                border-radius: 50%;
                margin: 2px;
                color: white;
            }
            .res-H, .res-O, .res-Odd, .res-minus { background-color: #ff4b4b; } /* Red */
            .res-A, .res-U, .res-Even, .res-plus { background-color: #3133ff; } /* Blue */
            .res-D { background-color: #28a745; } /* Green */
            .grid-container {
                display: grid;
                grid-auto-flow: column;
                grid-template-rows: repeat(6, 45px);
                gap: 2px;
                background-color: #f0f2f6;
                padding: 10px;
                border-radius: 5px;
                overflow-x: auto;
                margin-bottom: 20px;
            }
            </style>
            """, unsafe_allow_html=True)

        # --- LOGIC FUNCTIONS ---
        # def load_csv(file_name):
        #     if os.path.exists(file_name):
        #         df = pd.read_csv(file_name)
        #         if df.empty:
        #             st.warning(f"{file_name} is blank. No trend required.")
        #             return None
        #         return df
        #     else:
        #         st.error(f"{file_name} not found in root folder.")
        #         return None
        
        def load_csv(url: str, drop_first_two: bool = False):
            try:
                df = pd.read_csv(url)

                if df.empty:
                    st.warning("CSV is blank. No trend required.")
                    return None

                # Special handling for MLS: drop first two columns
                if drop_first_two:
                    df = df.iloc[:, 2:]

                # Keep only the last 40 rows
                df = df.tail(40)

                # Extract columns D–G (index 3–6 after any dropping)
                df = df.iloc[:, [3,4,5,6]]
                df.columns = ["Home", "Away", "FTHG", "FTAG"]

                # Build new DataFrame
                df_final = pd.DataFrame({
                    "Match": df["Home"] + " vs " + df["Away"],
                    "Score": df["FTHG"].astype(str) + "-" + df["FTAG"].astype(str)
                })

                return df_final

            except Exception as e:
                st.error(f"Error loading CSV: {e}")
                return None


        def parse_scores(input_str):
            # Regex to find patterns like 1-2, 10-2, etc.
            pairs = re.findall(r'(\d+)\s*-\s*(\d+)', input_str)
            data = []
            for h, a in pairs:
                h, a = int(h), int(a)
                total = h + a
                
                # 1. H/D/A
                if h > a: hda = 'H'
                elif a > h: hda = 'A'
                else: hda = 'D'
                
                # 2. Over/Under 2.5
                ou = 'O' if total > 2.5 else 'U'
                
                # 3. Odd/Even
                oe = 'Odd' if total % 2 != 0 else 'Even'
                
                # 4. Home Handicap -2
                # Logic: Home wins by 2 or more = "-", else "+"
                hc = '-' if (h - a) >= 2 else '+'
                
                data.append({'score': f'{h}-{a}', 'HDA': hda, 'OU': ou, 'OE': oe, 'HC': hc})
            return data

        def get_highway_grid(results, rows=6):
            """Fills grid top-to-bottom, then moves to next column."""
            grid = []
            for i in range(0, len(results), rows):
                grid.append(results[i:i+rows])
            return grid

        def get_big_road_grid(results):
            """Fills down, moves column only when result changes (except Draws)."""
            if not results: return []
            
            columns = []
            current_col = []
            last_winner = None
            
            for val in results:
                # Determine if this value forces a column switch
                # In Baccarat, D (Draw) doesn't switch the column
                is_draw = (val == 'D')
                
                if last_winner is None:
                    current_col.append(val)
                    if not is_draw: last_winner = val
                elif is_draw:
                    current_col.append(val)
                elif val == last_winner:
                    current_col.append(val)
                else:
                    columns.append(current_col)
                    current_col = [val]
                    last_winner = val
                    
            columns.append(current_col)
            return columns

        def render_road(grid, title):
            st.subheader(title)
            html = '<div class="grid-container">'
            for col in grid:
                # Each column in our 'grid' list is a list of results
                for i in range(6):
                    if i < len(col):
                        val = col[i]
                        # Clean class name for CSS (replace + with 'plus' and - with 'minus')
                        css_class = val.replace('+', 'plus').replace('-', 'minus')
                        html += f'<div class="baccarat-cell res-{css_class}">{val}</div>'
                    else:
                        # Empty cell to maintain 6-row height
                        html += '<div style="width:40px; height:40px; margin:2px;"></div>'
            html += '</div>'
            st.markdown(html, unsafe_allow_html=True)

        # Row 1: Buttons
        # btn_cols = st.columns(4)
        # with btn_cols[0]: epl_clicked = st.button("EPL")
        # with btn_cols[1]: laliga_clicked = st.button("LaLiga")
        # with btn_cols[2]: aussie_clicked = st.button("Aussie")
        # with btn_cols[3]: fifa_clicked = st.button("Fifa")

        # selected_df, selected_league = None, None
        # if epl_clicked:
        #     selected_df, selected_league = load_csv("EPL.csv"), "EPL"
        # elif laliga_clicked:
        #     selected_df, selected_league = load_csv("LaLiga.csv"), "LaLiga"
        # elif aussie_clicked:
        #     selected_df, selected_league = load_csv("Aussie.csv"), "Aussie"
        # elif fifa_clicked:
        #     selected_df, selected_league = load_csv("Fifa.csv"), "Fifa"
        
        btn_cols = st.columns(6)
        with btn_cols[0]: epl_clicked = st.button("EPL")
        with btn_cols[1]: laliga_clicked = st.button("LaLiga")
        with btn_cols[2]: france_clicked = st.button("France")
        with btn_cols[3]: aussie_clicked = st.button("Aussie")
        with btn_cols[4]: fifa_clicked = st.button("Fifa")
        with btn_cols[5]: mls_clicked = st.button("MLS")

        selected_df, selected_league = None, None

        if epl_clicked:
            selected_df, selected_league = load_csv("https://www.football-data.co.uk/mmz4281/2526/E0.csv"), "EPL"
        elif laliga_clicked:
            selected_df, selected_league = load_csv("https://www.football-data.co.uk/mmz4281/2526/SP1.csv"), "LaLiga"
        elif france_clicked:
            selected_df, selected_league = load_csv("https://www.football-data.co.uk/mmz4281/2526/F1.csv"), "France"
        elif aussie_clicked:
            selected_df, selected_league = load_csv("https://www.football-data.co.uk/mmz4281/2526/A1.csv"), "Aussie"
        elif fifa_clicked:
            selected_df, selected_league = load_csv("https://www.football-data.co.uk/mmz4281/2526/WC.csv"), "Fifa"
        elif mls_clicked:
            selected_df, selected_league = load_csv("https://www.football-data.co.uk/new/USA.csv", drop_first_two=True), "MLS"

        # --- APP UI ---
        def main():
            local_css()

            if selected_df is not None:
                
                # ✅ Reload the saved CSV
                reloaded_df = selected_df

                if reloaded_df is not None and "Score" in reloaded_df.columns:
                    scores_str = "\n".join(reloaded_df["Score"].astype(str).tolist())
                    data = parse_scores(scores_str)

                    if not data:
                        st.warning("Please enter valid scores (e.g., 1-1).")
                        return

                    # --- Tabs ---
                    # tabs = st.tabs(["The Highway (Bead Plate)", "The Big Road"])
                    col0, col1, col2 = st.columns([1,2,2], border=True)
                    categories = [
                        ('HDA', 'Home / Draw / Away'),
                        ('OU', 'Over / Under 2.5'),
                        ('OE', 'Odd / Even'),
                        ('HC', 'Home Handicap (-2)')
                    ]
                    with col0:
                        st.subheader("Scoreline")
                        if selected_df is not None:
                            st.dataframe(selected_df, hide_index=True,height=45 * 35)
                        else:
                            st.info("Load a league to see index values.")

                    with col1:
                        st.subheader("The Highway Trend")
                        for key, label in categories:
                            values = [d[key] for d in data]
                            grid = get_highway_grid(values)
                            render_road(grid, label)

                    with col2:
                        st.subheader("The Big Road Trend")
                        for key, label in categories:
                            values = [d[key] for d in data]
                            grid = get_big_road_grid(values)
                            render_road(grid, label)
                else:
                    st.warning("No 'Score' column found in table.")
            else:
                st.info("Please load a league to begin.")



        if __name__ == "__main__":
            main()