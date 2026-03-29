import streamlit as st
import base64
from pathlib import Path

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AI Homework Assistant",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------------- HIDE STREAMLIT UI ----------------
st.markdown("""
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
[data-testid="stSidebar"] {display: none !important;}
[data-testid="collapsedControl"] {display: none !important;}

.block-container {
    padding: 0 !important;
    max-width: 100% !important;
}

html, body, [class*="css"] {
    margin: 0;
    padding: 0;
    background: #f3f6fb;
    font-family: "Segoe UI", sans-serif;
}
</style>
""", unsafe_allow_html=True)

# ---------------- IMAGE FUNCTION ----------------
def img_to_base64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

# ---------------- LOAD IMAGE ----------------
img_b64 = ""
img_path = Path(__file__).parent / "images" / "background.png"

if img_path.exists():
    img_b64 = img_to_base64(img_path)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
    font-family: "Segoe UI", sans-serif;
}

body {
    background: #f3f6fb;
}

/* NAVBAR */
.navbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 20px 80px;
    background: white;
}

.logo {
    font-size: 20px;
    font-weight: bold;
    color: #1e3a8a;
}

.navbar-btn {
    padding: 10px 22px;
    background: #2563eb;
    color: white !important;
    border: none;
    border-radius: 20px;
    cursor: pointer;
    text-decoration: none;
    font-weight: 500;
    display: inline-block;
}

.navbar-btn:hover {
    background: #1d4ed8;
}

/* HERO */
.hero {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 80px;
    background: linear-gradient(135deg, #dbeafe, #bfdbfe);
    border-radius: 20px;
    margin: 40px;
    gap: 40px;
}

.hero-left {
    max-width: 500px;
}

.hero-left h1 {
    font-size: 42px;
    color: #1e3a8a;
    margin-bottom: 20px;
    line-height: 1.3;
}

.hero-left p {
    color: #4b5563;
    margin-bottom: 25px;
    font-size: 17px;
    line-height: 1.6;
}

.start-btn {
    padding: 12px 30px;
    background: #3b82f6;
    color: white !important;
    border: none;
    border-radius: 25px;
    font-size: 16px;
    cursor: pointer;
    text-decoration: none;
    display: inline-block;
    font-weight: 600;
}

.start-btn:hover {
    background: #2563eb;
}

.hero-right img {
    width: 420px;
    max-width: 100%;
}

/* FEATURES */
.features {
    display: flex;
    justify-content: center;
    gap: 25px;
    margin: 40px;
    flex-wrap: wrap;
}

.card {
    background: white;
    padding: 25px;
    border-radius: 15px;
    width: 260px;
    text-align: center;
    box-shadow: 0 6px 20px rgba(0,0,0,0.1);
    transition: 0.3s ease;
}

.card:hover {
    transform: translateY(-5px);
}

.card h3 {
    margin-bottom: 10px;
    color: #1e3a8a;
    font-size: 22px;
    line-height: 1.4;
}

.card p {
    color: #6b7280;
    font-size: 14px;
    line-height: 1.6;
}

/* RESPONSIVE */
@media (max-width: 900px) {
    .hero {
        flex-direction: column;
        text-align: center;
        padding: 50px 30px;
    }

    .navbar {
        padding: 20px 30px;
    }

    .hero-left h1 {
        font-size: 34px;
    }

    .hero-right img {
        width: 280px;
        margin-top: 20px;
    }

    .features {
        flex-direction: column;
        align-items: center;
    }
}
</style>
""", unsafe_allow_html=True)

# ---------------- NAVBAR ----------------
st.markdown("""
<div class="navbar">
    <div class="logo">🎓 AI Homework Assistant</div>
    <a href="?page=login" class="navbar-btn">Log In</a>
</div>
""", unsafe_allow_html=True)

# ---------------- HERO SECTION ----------------
st.markdown(f"""
<div class="hero">
    <div class="hero-left">
        <h1>AI-Powered <br> Homework Assistance <br> System</h1>
        <p>
            Get instant answers and step-by-step solutions
            for your homework questions across all subjects.
        </p>
        <a href="?page=signup" class="start-btn">Get Started</a>
    </div>
    <div class="hero-right">
        {"<img src='data:image/png;base64," + img_b64 + "' alt='student'>" if img_b64 else ""}
    </div>
</div>
""", unsafe_allow_html=True)
# ---------------- FEATURES ----------------
st.markdown("<br><br>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3, gap="large")

card_style = """
<style>
.feature-box {
    background: white;
    padding: 35px 25px;
    border-radius: 18px;
    text-align: center;
    box-shadow: 0 6px 20px rgba(0,0,0,0.1);
    min-height: 230px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    transition: 0.3s ease;
}
.feature-box:hover {
    transform: translateY(-5px);
}
.feature-box h3 {
    margin-bottom: 14px;
    color: #1e3a8a;
    font-size: 22px;
    line-height: 1.4;
}
.feature-box p {
    color: #6b7280;
    font-size: 14px;
    line-height: 1.7;
}
</style>
"""
st.markdown(card_style, unsafe_allow_html=True)

with col1:
    st.markdown("""
    <div class="feature-box">
        <h3>🚀 Instant <br> Solutions</h3>
        <p>Get step-by-step solutions to any homework question.</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-box">
        <h3>🎤 Voice & Image Input</h3>
        <p>Ask questions using voice or upload an image.</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-box">
        <h3>📊 Track Progress</h3>
        <p>Monitor your learning and progress over time.</p>
    </div>
    """, unsafe_allow_html=True)
# ---------------- REDIRECT LOGIC ----------------
query_params = st.query_params

if "page" in query_params:
    if query_params["page"] == "login":
        st.switch_page("pages/login.py")
    elif query_params["page"] == "signup":
        st.switch_page("pages/signup.py")