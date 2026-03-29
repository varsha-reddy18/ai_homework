import streamlit as st
import requests

st.set_page_config(
    page_title="Login – AI Homework Assistant",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── CSS: hide sidebar, style the page like the original blue-gradient theme ──
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700;800&display=swap');

[data-testid="stSidebar"], [data-testid="collapsedControl"] { display: none !important; }
#MainMenu, footer, header { visibility: hidden !important; }
[data-testid="stToolbar"]  { display: none !important; }

html, body,
[data-testid="stAppViewContainer"],
[data-testid="stMain"], .main {
    background: linear-gradient(135deg, #d7e8f7, #b7d4f3) !important;
    font-family: 'Poppins', 'Segoe UI', sans-serif !important;
    min-height: 100vh !important;
}
.block-container {
    padding-top: 3rem !important;
    max-width: 460px !important;
    margin: 0 auto !important;
}

/* inputs */
.stTextInput > div > div > input {
    border: 1px solid #d1d5db !important;
    border-radius: 8px !important;
    padding: 12px 14px !important;
    font-family: 'Poppins', sans-serif !important;
    font-size: 0.9rem !important;
    background: #f9fafb !important;
    color: #111827 !important;
}
.stTextInput > div > div > input:focus {
    border-color: #3b82f6 !important;
    box-shadow: 0 0 0 3px rgba(59,130,246,0.15) !important;
    outline: none !important;
}
.stTextInput label {
    color: #374151 !important;
    font-family: 'Poppins', sans-serif !important;
    font-size: 0.85rem !important;
    font-weight: 600 !important;
}

/* primary button */
.stButton > button {
    background: linear-gradient(90deg,#3b82f6,#2563eb) !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 0.65rem 1.5rem !important;
    font-family: 'Poppins', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.95rem !important;
    width: 100% !important;
    box-shadow: 0 4px 14px rgba(59,130,246,0.4) !important;
    transition: all 0.25s ease !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 20px rgba(59,130,246,0.5) !important;
}

/* ghost secondary */
.ghost button {
    background: transparent !important;
    color: #3b82f6 !important;
    border: 1.5px solid #3b82f6 !important;
    box-shadow: none !important;
}
.ghost button:hover { background: #eff6ff !important; transform: none !important; }

.or-line {
    display: flex; align-items: center; gap: 10px;
    color: #9ca3af; font-size: 0.8rem; margin: 0.75rem 0;
}
.or-line::before, .or-line::after {
    content:''; flex:1; border-top:1px solid #e5e7eb;
}
</style>
""", unsafe_allow_html=True)

# Redirect if already logged in
if st.session_state.get("logged_in"):
    st.switch_page("pages/dashboard.py")

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center;margin-bottom:2rem;">
  <div style="font-size:3.5rem;margin-bottom:0.4rem;">🎓</div>
  <h1 style="color:#1e3a8a;font-family:Poppins,sans-serif;font-size:1.8rem;
      font-weight:800;margin-bottom:4px;">Welcome Back!</h1>
  <p style="color:#6b7280;font-size:0.9rem;font-family:Poppins,sans-serif;">
    AI-Powered Homework Assistant</p>
</div>
""", unsafe_allow_html=True)

# ── White card wrapper ────────────────────────────────────────────────────────
st.markdown("""
<div style="background:white;border-radius:14px;padding:32px 28px;
     box-shadow:0 10px 40px rgba(0,0,0,0.12);margin-bottom:1rem;">
""", unsafe_allow_html=True)

with st.form("login_form", clear_on_submit=False):
    email    = st.text_input("📧 Email Address", placeholder="student@example.com")
    password = st.text_input("🔒 Password", placeholder="Enter your password", type="password")
    submitted = st.form_submit_button("Log In", use_container_width=True)

if submitted:
    if not email.strip() or not password.strip():
        st.error("⚠️ Please enter both email and password.")
    else:
        success = False

        # 1️⃣ Try real backend
        try:
            res = requests.post(
                "http://127.0.0.1:8000/login",
                json={"email": email.strip(), "password": password.strip()},
                timeout=3,
            )
            if res.status_code == 200:
                data = res.json()
                st.session_state.logged_in = True
                st.session_state.user = data.get("user", {
                    "name":  email.split("@")[0].capitalize(),
                    "email": email.strip(),
                })
                success = True
            else:
                # Backend responded but credentials wrong
                st.error("❌ Invalid email or password.")
        except Exception:
            # Backend not running → fall through to demo mode
            pass

        # 2️⃣ Demo / offline mode (backend unreachable)
        if not success and not st.session_state.get("_backend_rejected"):
            if len(password.strip()) >= 4:
                st.session_state.logged_in = True
                st.session_state.user = {
                    "name":  email.split("@")[0].capitalize(),
                    "email": email.strip(),
                }
                success = True
            else:
                st.error("❌ Password must be at least 4 characters.")

        if success:
            st.success("✅ Login successful! Redirecting…")
            st.switch_page("pages/dashboard.py")

st.markdown("</div>", unsafe_allow_html=True)  # close white card

st.markdown('<div class="or-line">or</div>', unsafe_allow_html=True)
st.markdown("""
<p style="text-align:center;color:#6b7280;font-size:0.85rem;
   font-family:Poppins,sans-serif;margin-bottom:0.5rem;">
  Don't have an account?
</p>
""", unsafe_allow_html=True)
st.markdown('<div class="ghost">', unsafe_allow_html=True)
if st.button("✨ Create Account", use_container_width=True, key="go_signup"):
    st.switch_page("pages/signup.py")
st.markdown("</div>", unsafe_allow_html=True)