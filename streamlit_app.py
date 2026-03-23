import streamlit as st
import pandas as pd
from datetime import datetime, timedelta, time, date
from itertools import product
import re
import matplotlib.pyplot as plt
import math
import time
import plotly.graph_objects as go

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

        st_autorefresh(interval=1000, limit=None, key="clock_refresh")
        
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

        # --- APP UI ---
        def main():
            local_css()
            st.title("⚽ Soccer Scoreline Baccarat Trends")
            st.markdown("Enter scores separated by commas or spaces (e.g., `1-2, 6-0, 0-0`).")

            default_input = "0-0, 2-0, 0-1, 2-1, 1-4, 0-1, 0-1, 2-2, 2-1, 1-3, 0-0, 0-1, 2-0, 0-1, 1-1, 0-0, 3-1, 0-0, 1-1, 2-2, 2-2, 2-1, 3-1, 3-0, 0-0, 1-2, 2-0, 0-3"
            user_input = st.text_area("Input Scores:", value=default_input, height=100)
            
            if user_input:
                data = parse_scores(user_input)
                if not data:
                    st.warning("Please enter valid scores (e.g., 1-1).")
                    return

                tabs = st.tabs(["The Highway (Bead Plate)", "The Big Road"])
                
                categories = [
                    ('HDA', 'Home / Draw / Away'),
                    ('OU', 'Over / Under 2.5'),
                    ('OE', 'Odd / Even'),
                    ('HC', 'Home Handicap (-2)')
                ]

                with tabs[0]:
                    for key, label in categories:
                        values = [d[key] for d in data]
                        grid = get_highway_grid(values)
                        render_road(grid, label)

                with tabs[1]:
                    for key, label in categories:
                        values = [d[key] for d in data]
                        grid = get_big_road_grid(values)
                        render_road(grid, label)

        if __name__ == "__main__":
            main()