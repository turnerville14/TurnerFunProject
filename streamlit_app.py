import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import re
import os

# --- Page Config ---
st.set_page_config(page_title="JG Portal", layout="wide")

# --- Styling ---
st.markdown("""
    <style>
    .stApp {
        background-color: #0e1117;
        color: white;
    }
    header {visibility: hidden;}
    .streamlit-footer {display: none;}
    .st-emotion-cache-uf99v8 {display: none;}
    </style>
""", unsafe_allow_html=True)

# --- Session State ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

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
        .login-button {
            background-color: #333;
            color: white;
            border: none;
            padding: 0.5rem 1rem;
            border-radius: 8px;
            margin-top: 1rem;
            cursor: pointer;
            transition: background-color 0.4s ease-in-out;
        }
        .login-button:hover { background-color: #555; }
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

# --- CSV Loader ---
def load_csv(file_name):
    if os.path.exists(file_name):
        df = pd.read_csv(file_name)
        if df.empty:
            st.warning(f"{file_name} is blank. No trend required.")
            return None
        return df
    else:
        st.error(f"{file_name} not found in root folder.")
        return None

# --- Parse Scores Logic (unchanged from your code) ---
def parse_scores(input_str):
    pairs = re.findall(r'(\d+)\s*-\s*(\d+)', input_str)
    data = []
    for h, a in pairs:
        h, a = int(h), int(a)
        total = h + a
        if h > a: hda = 'H'
        elif a > h: hda = 'A'
        else: hda = 'D'
        ou = 'O' if total > 2.5 else 'U'
        oe = 'Odd' if total % 2 != 0 else 'Even'
        hc = '-' if (h - a) >= 2 else '+'
        data.append({'score': f'{h}-{a}', 'HDA': hda, 'OU': ou, 'OE': oe, 'HC': hc})
    return data

def get_highway_grid(results, rows=6):
    grid = []
    for i in range(0, len(results), rows):
        grid.append(results[i:i+rows])
    return grid

def get_big_road_grid(results):
    if not results: return []
    columns, current_col, last_winner = [], [], None
    for val in results:
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
        for i in range(6):
            if i < len(col):
                val = col[i]
                css_class = val.replace('+', 'plus').replace('-', 'minus')
                html += f'<div class="baccarat-cell res-{css_class}">{val}</div>'
            else:
                html += '<div style="width:40px; height:40px; margin:2px;"></div>'
    html += '</div>'
    st.markdown(html, unsafe_allow_html=True)

# --- Main Layout ---
logincol = st.columns([1, 3, 1])
with logincol[1]:
    if not st.session_state.logged_in:
        rgb_container()
        password = st.query_params.get("password_input", "")
        if password:
            if password == "Password123":
                st.session_state.logged_in = True
                st.success("Access Granted ✅")
                st.markdown("<div style='border:2px solid #888; border-radius:8px; padding:0.75rem 1rem; background-color:#1e1e1e; color:white; font-style:italic; font-weight:bold; margin-bottom:1rem;'>Click any of the buttons below</div>", unsafe_allow_html=True)
            else:
                st.error("Incorrect Password ❌")

# --- Post-login UI ---
if st.session_state.logged_in:
    # Row 1: Buttons
    btn_cols = st.columns(4)
    with btn_cols[0]: epl_clicked = st.button("Load EPL")
    with btn_cols[1]: laliga_clicked = st.button("Load LaLiga")
    with btn_cols[2]: aussie_clicked = st.button("Load Aussie")
    with btn_cols[3]: fifa_clicked = st.button("Load Fifa")

    selected_df, selected_league = None, None
    if epl_clicked:
        selected_df, selected_league = load_csv("EPL.csv"), "EPL"
    elif laliga_clicked:
        selected_df, selected_league = load_csv("LaLiga.csv"), "LaLiga"
    elif aussie_clicked:
        selected_df, selected_league = load_csv("Aussie.csv"), "Aussie"
    elif fifa_clicked:
        selected_df, selected_league = load_csv("Fifa.csv"), "Fifa"

    # Row 2: Editable table + roads
    if selected_df is not None:
        col1, col2, col3 = st.columns([1, 2, 2])
        with col1:
            st.subheader(f"{selected_league} Editable Table")
            edited_df = st.data_editor(selected_df, num_rows="dynamic")
            if st.button("Save Changes"):
                edited_df.to_csv(f"{selected_league}.csv", index=False)
                st.success(f"{selected_league}.csv updated successfully!")

        with col2:
            st.subheader(f"{selected_league} Main Road")
            data = parse_scores(" ".join(edited_df['Score'].astype(str)))
            for key, label in [('HDA','Home/Draw/Away'),('OU','Over/Under 2.5'),('OE','Odd/Even'),('HC','Home Handicap (-2)')]:
                values = [d[key] for d in data]
                grid = get_big_road_grid(values)
                render_road(grid, label)

        with col3:
            st.subheader(f"{selected_league} Bead Road")
            for key, label in [('HDA','Home/Draw/Away'),
                               ('OU','Over/Under 2.5'),
                               ('OE','Odd/Even'),
                               ('HC','Home Handicap (-2)')]:
                values = [d[key] for d in data]
                grid = get_highway_grid(values)
                render_road(grid, label)