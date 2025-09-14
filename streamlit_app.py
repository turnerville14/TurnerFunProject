import streamlit as st

# --- Page Config ---
st.set_page_config(page_title="Login Page", layout="wide")

# --- Session State for Login ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# code to style the login box
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
            gap: 1rem; /* spacing between input and button */
            margin-top: 1rem;
        }

        .input-row input[type="password"] {
            flex: 1;
            width: auto; /* override fixed width */
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


# --- Layout with Columns ---
col1, col2, col3 = st.columns([1, 3, 1])
with col2:
    #Only show login box if session state is not logged in
    if not st.session_state.logged_in:
        rgb_container()

    # ✅ Updated to use st.query_params
    password = st.query_params.get("password_input", "")

    if password:
        if password == "Password123":
            st.session_state.logged_in = True
            st.write("")
            st.write("")
            st.success("Access Granted ✅")
            st.success("Navigate via the side panel")
            st.switch_page("pages/loginpage.py")
        else:
            st.write("")
            st.write("")
            st.error("Incorrect Password ❌")

# # --- Stop App if Not Logged In ---
# if not st.session_state.get("logged_in", False):
#     st.stop()

# # --- Session State for Login ---
# if "logged_in" not in st.session_state:
#     st.session_state.logged_in = False

# def rgb_glow_container(text):
#     st.markdown(f"""
#     <style>
#     .rgb-box {{
#         position: relative;
#         width: 100%;
#         max-width: 500px;
#         margin: auto;
#         padding: 20px;
#         border-radius: 12px;
#         background-color: #111;
#         color: white;
#         text-align: center;
#         font-size: 1.2rem;
#         overflow: hidden;
#         border: 2px solid transparent;
#     }}

#     .rgb-box::after {{
#         content: "";
#         position: absolute;
#         width: 100%;
#         height: 100%;
#         border-radius: 12px;
#         box-sizing: border-box;
#         border: 2px solid transparent;
#         background: none;
#         pointer-events: none;
#         animation: rgbTrail 4s linear infinite;
#         mask-image: linear-gradient(to right, transparent 0%, black 10%, black 90%, transparent 100%);
#     }}

#     @keyframes rgbTrail {{
#         0% {{
#             border-image: linear-gradient(0deg, red, orange, yellow, green, cyan, blue, violet) 1;
#         }}
#         20% {{
#             border-image: linear-gradient(72deg, red, orange, yellow, green, cyan, blue, violet) 1;
#         }}
#         40% {{
#             border-image: linear-gradient(144deg, red, orange, yellow, green, cyan, blue, violet) 1;
#         }}
#         60% {{
#             border-image: linear-gradient(216deg, red, orange, yellow, green, cyan, blue, violet) 1;
#         }}
#         80% {{
#             border-image: linear-gradient(288deg, red, orange, yellow, green, cyan, blue, violet) 1;
#         }}
#         100% {{
#             border-image: linear-gradient(360deg, red, orange, yellow, green, cyan, blue, violet) 1;
#         }}
#     }}
#     </style>
#     <div class="rgb-box">
#         {text}
#     </div>
#     """, unsafe_allow_html=True)


# cols0 = st.columns([1, 2, 1])  # Center the login box
# with cols0[1]:
#     rgb_glow_container("🚀 <strong>Welcome</strong>")
#     st.write("###")

# # --- Login Component ---
# if not st.session_state.logged_in:
#     cols = st.columns([1, 2, 1])  # Center the login box
#     with cols[1].container(border=True, height="stretch", vertical_alignment="center"):
#         st.markdown("### 🔐 Please log in to continue")
#         password = st.text_input("Password", type="password")
        
#         if st.button("Login"):
#             if password == "Password123":  # Replace with secure logic
#                 st.session_state.logged_in = True
#                 st.success("Login successful!")
#             else:
#                 st.error("Invalid password")

# # --- Stop App if Not Logged In ---
# if not st.session_state.get("logged_in", False):
#     st.stop()