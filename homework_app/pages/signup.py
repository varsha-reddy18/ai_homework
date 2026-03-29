import streamlit as st
import requests

st.set_page_config(
    page_title="Sign Up – AI Homework Assistant",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── CSS ───────────────────────────────────────────────────────────────────────
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
    padding-top: 2.5rem !important;
    max-width: 500px !important;
    margin: 0 auto !important;
}

.stTextInput > div > div > input,
.stSelectbox > div > div {
    border: 1px solid #d1d5db !important;
    border-radius: 8px !important;
    padding: 11px 14px !important;
    font-family: 'Poppins', sans-serif !important;
    font-size: 0.9rem !important;
    background: #f9fafb !important;
    color: #111827 !important;
}
.stTextInput > div > div > input:focus {
    border-color: #3b82f6 !important;
    box-shadow: 0 0 0 3px rgba(59,130,246,0.15) !important;
}
.stTextInput label, .stSelectbox label {
    color: #374151 !important;
    font-family: 'Poppins', sans-serif !important;
    font-size: 0.85rem !important;
    font-weight: 600 !important;
}

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

.ghost button {
    background: transparent !important;
    color: #3b82f6 !important;
    border: 1.5px solid #3b82f6 !important;
    box-shadow: none !important;
}
.ghost button:hover { background: #eff6ff !important; transform: none !important; }

.or-line {
    display:flex; align-items:center; gap:10px;
    color:#9ca3af; font-size:0.8rem; margin:0.75rem 0;
}
.or-line::before,.or-line::after { content:''; flex:1; border-top:1px solid #e5e7eb; }
</style>
""", unsafe_allow_html=True)

# Redirect if already logged in
if st.session_state.get("logged_in"):
    st.switch_page("pages/dashboard.py")

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center;margin-bottom:2rem;">
  <div style="font-size:3.5rem;margin-bottom:0.4rem;">✨</div>
  <h1 style="color:#1e3a8a;font-family:Poppins,sans-serif;font-size:1.8rem;
      font-weight:800;margin-bottom:4px;">Create Account</h1>
  <p style="color:#6b7280;font-size:0.9rem;font-family:Poppins,sans-serif;">
    AI-Powered Homework Assistant</p>
</div>
""", unsafe_allow_html=True)

# ── White card ────────────────────────────────────────────────────────────────
st.markdown("""
<div style="background:white;border-radius:14px;padding:32px 28px;
     box-shadow:0 10px 40px rgba(0,0,0,0.12);margin-bottom:1rem;">
""", unsafe_allow_html=True)

with st.form("signup_form", clear_on_submit=False):
    c1, c2 = st.columns(2)
    with c1:
        first_name = st.text_input("👤 First Name", placeholder="John")
    with c2:
        last_name  = st.text_input("👤 Last Name",  placeholder="Doe")

    email    = st.text_input("📧 Email Address", placeholder="john@example.com")
    password = st.text_input("🔒 Password",       placeholder="Min. 6 characters", type="password")
    confirm  = st.text_input("🔒 Confirm Password",placeholder="Re-enter password",  type="password")

    grade = st.selectbox("🎓 Class / Grade", [
        "Class 6","Class 7","Class 8","Class 9",
        "Class 10","Class 11","Class 12","College / Other",
    ])

    terms = st.checkbox("I agree to the Terms of Service and Privacy Policy")
    submitted = st.form_submit_button("Sign Up", use_container_width=True)

if submitted:
    # ── Validation ────────────────────────────────────────────────────────────
    errors = []
    if not first_name.strip() or not last_name.strip():
        errors.append("Please enter your first and last name.")
    if not email.strip():
        errors.append("Please enter your email address.")
    if len(password.strip()) < 6:
        errors.append("Password must be at least 6 characters.")
    if password.strip() != confirm.strip():
        errors.append("Passwords do not match.")
    if not terms:
        errors.append("Please accept the Terms of Service.")

    if errors:
        for e in errors:
            st.error(f"⚠️ {e}")
    else:
        success = False
        full_name = f"{first_name.strip()} {last_name.strip()}"

        # 1️⃣ Try real backend
        try:
            res = requests.post(
                "http://127.0.0.1:8000/signup",
                json={
                    "name":     full_name,
                    "email":    email.strip(),
                    "password": password.strip(),
                    "grade":    grade,
                },
                timeout=3,
            )
            if res.status_code in (200, 201):
                success = True
            elif res.status_code == 409:
                st.error("❌ An account with this email already exists.")
            else:
                st.warning(f"Backend returned {res.status_code}. Using demo mode.")
        except Exception:
            pass  # Backend offline → fall through to demo mode

        # 2️⃣ Demo / offline mode
        if not success:
            success = True  # Accept registration in demo mode

        if success:
            st.session_state.logged_in = True
            st.session_state.user = {
                "name":  full_name,
                "email": email.strip(),
                "grade": grade,
            }
            st.success("🎉 Account created! Redirecting…")
            st.switch_page("pages/dashboard.py")

st.markdown("</div>", unsafe_allow_html=True)

st.markdown('<div class="or-line">or</div>', unsafe_allow_html=True)
st.markdown("""
<p style="text-align:center;color:#6b7280;font-size:0.85rem;
   font-family:Poppins,sans-serif;margin-bottom:0.5rem;">
  Already have an account?
</p>
""", unsafe_allow_html=True)
st.markdown('<div class="ghost">', unsafe_allow_html=True)
if st.button("🔑 Log In", use_container_width=True, key="go_login"):
    st.switch_page("pages/login.py")
st.markdown("</div>", unsafe_allow_html=True)