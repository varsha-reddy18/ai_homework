"""
dashboard.py — AI-Powered Homework Assistance System
Run: streamlit run dashboard.py
"""

import streamlit as st
import requests
import time
import random

st.set_page_config(
    page_title="AI Homework Assistant",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)
st.markdown("""
    <style>
        section[data-testid="stSidebar"] {
            display: block !important;
            visibility: visible !important;
            transform: translateX(0%) !important;
        }
    </style>
""", unsafe_allow_html=True)

BACKEND = "http://127.0.0.1:8000"

# ── Session State ──
_defaults = {
    "section": "home", "selected_subject": "",
    "chat_history": {}, "chat_session_id": str(int(time.time())),
    "user_id": None, "streak": 2, "dark_mode": False,
    "quiz_active": False, "quiz_index": 0, "quiz_score": 0, "quiz_done": False,
    "flashcards": [], "flash_index": 0, "flash_flipped": False,
    "pomo_seconds": 1500, "pomo_running": False,
    "grammar_topic": "", "grammar_result": "",
    "geo_result": [], "geo_title": "",
    "puzzle_word": "", "puzzle_scramble": "", "puzzle_result": "",
}
for k, v in _defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

DARK   = st.session_state.dark_mode
BG     = "#0f172a" if DARK else "#eef2ff"
CARD   = "#1e293b" if DARK else "#ffffff"
TEXT   = "#f1f5f9" if DARK else "#1e293b"
SUB    = "#94a3b8" if DARK else "#64748b"
BORDER = "#334155" if DARK else "#e2e8f0"

# ══════════════════════════════════════════════════════════
#  CSS
# ══════════════════════════════════════════════════════════
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;500;600;700;800;900&display=swap');
*,*::before,*::after{{box-sizing:border-box;margin:0;padding:0;}}
html,body,[data-testid="stAppViewContainer"]{{
    font-family:'Nunito',sans-serif!important;
    background:{BG}!important; color:{TEXT}!important;
}}
[data-testid="stAppViewContainer"]>.main{{background:transparent!important;}}
[data-testid="block-container"]{{padding:0!important;max-width:100%!important;}}
[data-testid="stSidebarNav"]{{display:none!important;}}
[data-testid="stToolbar"]{{display:none!important;}}
[data-testid="stDecoration"]{{display:none!important;}}
[data-testid="stStatusWidget"]{{display:none!important;}}
#MainMenu,footer,header{{visibility:hidden!important;}}
[data-testid="stSidebarNav"]{{display:none!important;}}
/* TOPBAR */
.topbar{{
    display:flex;align-items:center;justify-content:space-between;
    padding:0 28px;
    background:linear-gradient(90deg,#3b4fd8 0%,#5b6ef5 60%,#7c3aed 100%);
    color:white;height:64px;
    box-shadow:0 4px 20px rgba(59,79,216,0.3);
    border-radius:0 0 16px 16px;margin-bottom:6px;
}}
.topbar-logo{{display:flex;align-items:center;gap:10px;font-size:17px;font-weight:800;}}
.topbar-right{{display:flex;align-items:center;gap:12px;font-size:14px;font-weight:700;}}
.streak-badge{{background:rgba(255,255,255,0.2);padding:5px 12px;border-radius:20px;font-size:13px;font-weight:700;}}
.moon-badge{{background:rgba(255,255,255,0.2);padding:5px 10px;border-radius:20px;font-size:15px;}}
.profile-circle{{width:38px;height:38px;border-radius:50%;background:rgba(255,255,255,0.9);display:flex;align-items:center;justify-content:center;font-size:18px;}}
.backend-on{{background:rgba(34,197,94,.2);color:#86efac;padding:4px 12px;border-radius:999px;font-size:12px;font-weight:700;}}
.backend-off{{background:rgba(239,68,68,.2);color:#fca5a5;padding:4px 12px;border-radius:999px;font-size:12px;font-weight:700;}}

/* SIDEBAR */
/* SIDEBAR */
[data-testid="stSidebar"]{{
    background:linear-gradient(180deg,#1e3a8a 0%,#2d50c0 60%,#3b65e0 100%)!important;
    min-width:260px!important;
    width:260px!important;
    display:block!important;
    visibility:visible!important;
    transform:translateX(0)!important;
    margin-left:0!important;
}}

section[data-testid="stSidebar"]{{
    display:block!important;
    visibility:visible!important;
    transform:translateX(0)!important;
}}

[data-testid="stSidebar"] > div:first-child{{
    padding-top:12px!important;
    width:260px!important;
}}

[data-testid="stSidebar"] *{{
    color:rgba(255,255,255,0.9)!important;
    font-family:'Nunito',sans-serif!important;
}}

[data-testid="stSidebarNav"]{{
    display:none!important;
}}

[data-testid="collapsedControl"]{{
    display:none!important;
}}

button[kind="header"]{{
    display:none!important;
}}

[data-testid="stSidebarHeader"]{{
    display:none!important;
}}

[data-testid="stSidebarCollapseButton"]{{
    display:none!important;
}}


[data-testid="stSidebar"] .stButton>button{{
    width:100%!important;
    background:transparent!important;
    color:rgba(255,255,255,0.88)!important;
    border:none!important;
    border-radius:12px!important;
    font-size:15px!important;
    font-weight:600!important;
    text-align:left!important;
    padding:11px 16px!important;
    margin-bottom:2px!important;
    transition:background .18s!important;
    box-shadow:none!important;
}}

[data-testid="stSidebar"] .stButton>button:hover{{
    background:rgba(255,255,255,0.15)!important;
    color:white!important;
    transform:none!important;
    box-shadow:none!important;
}}

/* MAIN BUTTONS */
.main-pad .stButton>button{{
    border-radius:14px!important;font-family:'Nunito',sans-serif!important;
    font-weight:700!important;font-size:14px!important;
    transition:all .2s ease!important;border:1.5px solid {BORDER}!important;
    background:{CARD}!important;color:{TEXT}!important;padding:10px 12px!important;
    box-shadow:0 2px 8px rgba(0,0,0,0.04)!important;
}}
.main-pad .stButton>button:hover{{
    background:linear-gradient(135deg,#4361ee,#6366f1)!important;
    color:white!important;border-color:transparent!important;
    transform:translateY(-2px)!important;
    box-shadow:0 8px 20px rgba(67,97,238,0.25)!important;
}}
.main-pad .stButton>button[kind="primary"]{{
    background:linear-gradient(135deg,#4361ee,#6366f1)!important;
    color:white!important;border-color:transparent!important;
    box-shadow:0 6px 18px rgba(67,97,238,0.3)!important;
}}

/* HERO */
.hero-card{{
    background:linear-gradient(135deg,#4361ee 0%,#6366f1 100%);
    border-radius:20px;padding:30px 32px;color:white;margin-bottom:20px;
    box-shadow:0 12px 36px rgba(67,97,238,0.3);position:relative;overflow:hidden;
}}
.hero-card h2{{font-size:24px;font-weight:800;margin-bottom:8px;}}
.hero-card p{{font-size:14px;opacity:.9;font-weight:500;}}

/* CARD */
.card{{
    background:{CARD};border-radius:18px;
    box-shadow:0 4px 18px rgba(0,0,0,0.06);
    padding:20px 22px;margin-bottom:20px;border:1px solid {BORDER};
}}
.card-title{{font-size:16px;font-weight:800;margin-bottom:14px;color:{TEXT};}}

/* VIDEO */
.video-card-ui{{border-radius:14px;overflow:hidden;box-shadow:0 6px 18px rgba(0,0,0,0.10);transition:all .3s;background:white;cursor:pointer;border:1px solid #e2e8f0;}}
.video-card-ui img{{width:100%;display:block;}}
.video-card-ui:hover{{transform:translateY(-5px);box-shadow:0 14px 30px rgba(0,0,0,0.15);}}

/* CHAT */
.subj-mode-badge{{display:inline-flex;align-items:center;gap:6px;background:#eef2ff;color:#4f46e5;border:1px solid #c7d2fe;padding:5px 14px;border-radius:999px;font-size:12px;font-weight:700;margin-bottom:14px;}}
.chat-box{{background:{'#1e293b' if DARK else '#f8fafc'};border-radius:16px;border:1px solid {BORDER};padding:20px;min-height:340px;max-height:460px;overflow-y:auto;margin-bottom:14px;display:flex;flex-direction:column;gap:14px;}}
.chat-box::-webkit-scrollbar{{width:4px;}}
.chat-box::-webkit-scrollbar-thumb{{background:#c7d2fe;border-radius:10px;}}
.user-bubble{{display:flex;justify-content:flex-end;}}
.user-bubble .msg{{background:linear-gradient(135deg,#4361ee,#6366f1);color:white;padding:12px 18px;border-radius:20px 20px 6px 20px;max-width:70%;font-size:14px;line-height:1.7;font-weight:500;box-shadow:0 4px 16px rgba(67,97,238,0.25);}}
.ai-row{{display:flex;align-items:flex-start;gap:12px;max-width:85%;}}
.ai-avatar{{width:36px;height:36px;border-radius:12px;background:linear-gradient(135deg,#6366f1,#8b5cf6);display:flex;align-items:center;justify-content:center;font-size:17px;flex-shrink:0;box-shadow:0 4px 12px rgba(99,102,241,0.25);}}
.ai-bubble{{background:{CARD};border:1px solid {BORDER};border-radius:8px 20px 20px 20px;padding:12px 18px;color:{TEXT};font-size:14px;line-height:1.8;box-shadow:0 3px 12px rgba(0,0,0,0.05);flex:1;word-break:break-word;}}
.subject-banner-ui{{text-align:center;padding:40px 20px;color:{SUB};}}
.subject-banner-ui .bicon{{font-size:50px;}}
.subject-banner-ui h3{{font-size:22px;color:{TEXT};margin:12px 0 6px;font-weight:800;}}
.subject-banner-ui p{{font-size:14px;max-width:360px;margin:auto;}}

/* PLANNER */
.perf-excellent{{background:linear-gradient(135deg,#16a34a,#22c55e);color:white;border-radius:16px;padding:22px;text-align:center;margin:14px 0;}}
.perf-good{{background:linear-gradient(135deg,#2563eb,#3b82f6);color:white;border-radius:16px;padding:22px;text-align:center;margin:14px 0;}}
.perf-average{{background:linear-gradient(135deg,#f59e0b,#fbbf24);color:white;border-radius:16px;padding:22px;text-align:center;margin:14px 0;}}
.perf-poor{{background:linear-gradient(135deg,#dc2626,#ef4444);color:white;border-radius:16px;padding:22px;text-align:center;margin:14px 0;}}
.mark-result-card{{background:{CARD};border-radius:14px;padding:16px;text-align:center;box-shadow:0 4px 14px rgba(0,0,0,0.06);margin-bottom:10px;border:1px solid {BORDER};}}
.mark-result-card h4{{font-size:13px;margin-bottom:6px;color:{SUB};font-weight:700;}}
.mark-result-card p{{font-size:22px;font-weight:800;color:#6366f1;}}
.week-day-box{{background:{CARD};border-radius:12px;padding:12px 6px;text-align:center;font-weight:800;font-size:13px;color:{TEXT};box-shadow:0 3px 10px rgba(0,0,0,0.06);border:1px solid {BORDER};}}
.week-day-box span{{display:block;margin-top:5px;font-size:11px;font-weight:700;color:#6366f1;}}
.analysis-box{{border-radius:14px;padding:18px;background:{CARD};box-shadow:0 4px 14px rgba(0,0,0,0.06);margin-bottom:12px;border:1px solid {BORDER};}}
.analysis-box h3{{font-size:15px;margin-bottom:10px;color:{TEXT};font-weight:800;}}
.analysis-box ul{{padding-left:18px;line-height:2;color:{SUB};font-size:14px;font-weight:500;}}

/* QUIZ */
.quiz-start-box{{background:linear-gradient(135deg,#4361ee,#6366f1);border-radius:24px;padding:60px 40px;text-align:center;color:white;box-shadow:0 20px 50px rgba(67,97,238,0.35);max-width:800px;margin:30px auto;}}
.quiz-big-title{{font-size:72px;font-weight:900;letter-spacing:4px;margin-bottom:28px;}}
.quiz-card-ui{{background:{CARD};border-radius:20px;padding:32px;text-align:center;box-shadow:0 10px 28px rgba(0,0,0,0.08);max-width:600px;margin:20px auto;border:1px solid {BORDER};}}
.quiz-card-ui h3{{font-size:18px;margin-bottom:20px;color:{TEXT};line-height:1.5;font-weight:700;}}

/* GRAMMAR */
.grammar-card-ui{{background:{CARD};padding:20px;border-radius:16px;cursor:pointer;box-shadow:0 4px 14px rgba(0,0,0,0.06);transition:all .25s;color:{TEXT};margin-bottom:12px;border:1px solid {BORDER};}}
.grammar-card-ui:hover{{transform:translateY(-4px);box-shadow:0 10px 24px rgba(67,97,238,0.18);border-color:#6366f1;}}
.grammar-card-ui h3{{margin-bottom:7px;font-size:15px;font-weight:800;}}
.grammar-card-ui p{{font-size:13px;color:{SUB};font-weight:500;line-height:1.6;}}
.tense-col-present{{background:#fdf4ff;border-radius:16px;padding:16px;}}
.tense-col-past{{background:#fefce8;border-radius:16px;padding:16px;}}
.tense-col-future{{background:#fff7ed;border-radius:16px;padding:16px;}}
.tense-col-present h3,.tense-col-past h3,.tense-col-future h3{{text-align:center;margin-bottom:12px;font-size:15px;font-weight:800;color:#1e293b;}}
.tense-card-box{{background:white;border-radius:10px;padding:12px;margin-bottom:8px;box-shadow:0 2px 8px rgba(0,0,0,0.05);}}
.tense-card-box h4{{margin-bottom:5px;font-size:13px;color:#1e293b;font-weight:700;}}
.tense-card-box p{{font-size:12px;color:#475569;line-height:1.6;}}
.pos-card{{border-radius:12px;padding:14px;margin-bottom:10px;box-shadow:0 3px 10px rgba(0,0,0,0.05);}}
.pos-card h3{{font-size:14px;margin-bottom:5px;color:#1e293b;font-weight:800;}}
.pos-card p{{font-size:12px;color:#475569;line-height:1.6;}}
.pos-noun{{border-left:5px solid #ff7a59;background:#fff5f0;}}
.pos-pronoun{{border-left:5px solid #4f8ef7;background:#f0f5ff;}}
.pos-verb{{border-left:5px solid #c23c8b;background:#fff0f7;}}
.pos-adjective{{border-left:5px solid #55b949;background:#f0fff0;}}
.pos-adverb{{border-left:5px solid #9d6dfd;background:#f5f0ff;}}
.pos-preposition{{border-left:5px solid #f39c12;background:#fffbf0;}}
.pos-conjunction{{border-left:5px solid #8e44ad;background:#fdf0ff;}}
.pos-interjection{{border-left:5px solid #b9770e;background:#fffaf0;}}
.voice-card-active{{border-top:6px solid #16a085;background:white;border-radius:14px;padding:20px;box-shadow:0 4px 14px rgba(0,0,0,0.07);}}
.voice-card-passive{{border-top:6px solid #27ae60;background:white;border-radius:14px;padding:20px;box-shadow:0 4px 14px rgba(0,0,0,0.07);}}
.voice-card-active h3,.voice-card-passive h3{{font-size:17px;margin-bottom:9px;color:#1e293b;font-weight:800;}}
.voice-card-active p,.voice-card-passive p{{font-size:13px;color:#475569;line-height:1.6;}}
.formula-box{{background:#f0f4ff;padding:9px 13px;border-radius:9px;font-weight:700;margin:10px 0;font-size:13px;color:#3730a3;}}
.vocab-card{{background:white;border-radius:14px;padding:16px;box-shadow:0 4px 14px rgba(0,0,0,0.07);}}
.vocab-card h3{{font-size:15px;margin-bottom:10px;text-align:center;color:#1e293b;font-weight:800;}}
.vocab-card ul{{padding-left:16px;line-height:2;color:#374151;font-size:13px;}}
.vocab-beginner{{border-top:6px solid #e74c3c;}}
.vocab-intermediate{{border-top:6px solid #3498db;}}
.vocab-advanced{{border-top:6px solid #8e44ad;}}
.punc-card{{background:#fff8f0;border-left:5px solid #ff6b35;border-radius:12px;padding:12px;margin-bottom:8px;box-shadow:0 2px 8px rgba(0,0,0,0.04);}}
.punc-card h3{{color:#d62828;margin-bottom:4px;font-size:13px;font-weight:700;}}
.punc-card p{{font-size:12px;color:#475569;}}
.sentence-card{{background:white;border-radius:14px;padding:20px;text-align:center;box-shadow:0 4px 14px rgba(0,0,0,0.07);}}
.sentence-card h3{{font-size:16px;margin-bottom:7px;color:#1e293b;font-weight:800;}}
.sentence-card p{{font-size:12px;color:#475569;}}
.sentence-card .example{{margin-top:10px;font-size:13px;font-weight:700;color:#4b4bb7;}}
.sentence-simple{{border-top:6px solid #95a5a6;}}
.sentence-compound{{border-top:6px solid #7f8c8d;}}
.sentence-complex{{border-top:6px solid #c2185b;}}
.sentence-cc{{border-top:6px solid #8e44ad;}}
.grammar-result-box{{background:#eef2ff;border-left:4px solid #6366f1;border-radius:12px;padding:14px 18px;margin-top:12px;font-size:14px;color:{TEXT};font-weight:500;}}

/* PUZZLE */
.scramble-box{{font-size:30px;font-weight:900;letter-spacing:10px;background:linear-gradient(135deg,#4361ee,#6366f1);color:white;padding:26px;border-radius:16px;text-align:center;margin:16px 0;box-shadow:0 10px 26px rgba(67,97,238,0.3);}}

/* FLASHCARD */
.flashcard-ui{{width:100%;max-width:520px;margin:16px auto;height:180px;border-radius:16px;display:flex;align-items:center;justify-content:center;font-size:18px;font-weight:700;text-align:center;padding:20px;}}
.fc-front{{background:linear-gradient(135deg,#4361ee,#6366f1);color:white;}}
.fc-back{{background:#eef2ff;color:#1e293b;border:2px solid #c7d2fe;}}
.flash-mini-grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:12px;margin-top:14px;}}
.flash-mini-card{{background:linear-gradient(135deg,#4361ee,#6366f1);color:white;padding:12px;border-radius:10px;min-height:80px;display:flex;align-items:center;justify-content:center;text-align:center;font-size:13px;font-weight:700;}}

/* POMODORO */
.pomo-wrap{{background:{CARD};border-radius:22px;padding:36px 28px;text-align:center;max-width:480px;margin:0 auto;box-shadow:0 10px 36px rgba(0,0,0,0.08);border:1px solid {BORDER};}}
.pomo-title{{font-size:20px;font-weight:800;margin-bottom:24px;color:{TEXT};}}
.pomo-circle{{width:190px;height:190px;border-radius:50%;background:linear-gradient(135deg,#ef4444,#f87171);display:flex;align-items:center;justify-content:center;margin:0 auto 16px;box-shadow:0 12px 36px rgba(239,68,68,0.35);font-size:38px;font-weight:900;color:white;}}
.pomo-hint{{font-size:13px;color:{SUB};margin-bottom:22px;font-weight:500;}}

/* GK */
.gk-section{{background:{CARD};border-radius:18px;padding:22px;margin-bottom:18px;box-shadow:0 4px 16px rgba(0,0,0,0.06);border:1px solid {BORDER};}}
.gk-section h2{{font-size:17px;font-weight:800;color:#1d4ed8;margin-bottom:14px;}}
.geo-item-ui{{background:{'#1e293b' if DARK else '#f8fafc'};border-radius:12px;padding:14px 12px;text-align:center;border:1px solid {BORDER};box-shadow:0 3px 10px rgba(0,0,0,0.05);color:{TEXT};position:relative;overflow:hidden;margin-bottom:10px;}}
.geo-item-ui::before{{content:"";position:absolute;top:0;left:0;width:100%;height:4px;background:linear-gradient(135deg,#4361ee,#6366f1);}}
.geo-item-ui h4{{font-size:13px;font-weight:800;margin-bottom:3px;padding-top:4px;}}
.geo-item-ui p{{font-size:11px;color:{SUB};font-weight:500;}}

/* MISC */
.sec-head{{font-size:24px;font-weight:900;color:{TEXT};margin-bottom:4px;}}
.sec-sub{{font-size:13px;color:{SUB};margin-bottom:20px;font-weight:500;}}
.divider{{height:1px;background:{BORDER};margin:18px 0;}}

.stTextInput>div>div>input,
.stTextArea>div>div>textarea,
.stNumberInput>div>div>input{{
    background:{'#1e293b' if DARK else '#f8fafc'}!important;
    color:{TEXT}!important;border:1.5px solid {'#334155' if DARK else '#dbeafe'}!important;
    border-radius:12px!important;font-family:'Nunito',sans-serif!important;
    font-size:14px!important;font-weight:500!important;
}}
.stTextInput>div>div>input:focus,
.stTextArea>div>div>textarea:focus{{
    border-color:#6366f1!important;
    box-shadow:0 0 0 3px rgba(99,102,241,0.12)!important;
}}
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════
#  STATIC DATA
# ══════════════════════════════════════════════════════════
SUBJECT_META = {
    "Maths":     {"icon":"➗","tips":["Solve an equation","Explain Pythagoras","What is integration?"]},
    "Physics":   {"icon":"⚡","tips":["Newton's laws","What is gravity?","Speed of light"]},
    "Chemistry": {"icon":"🧪","tips":["Periodic table","What is a covalent bond?","Explain pH"]},
    "Biology":   {"icon":"🧬","tips":["What is mitosis?","Explain photosynthesis","DNA structure"]},
    "Telugu":    {"icon":"🅣","tips":["ఒక కవిత రాయి","అర్థం చెప్పు","వాక్యం రాయి"]},
    "Hindi":     {"icon":"🅗","tips":["एक वाक्य लिखो","अर्थ बताओ","व्याकरण समझाओ"]},
    "English":   {"icon":"📖","tips":["Synonyms of brave","Explain tense","Write a paragraph"]},
    "Social":    {"icon":"🌍","tips":["French Revolution","What is democracy?","World War II"]},
    "Computer":  {"icon":"💻","tips":["What is an algorithm?","Explain HTML","Python basics"]},
}

QUIZ_QUESTIONS = [
    {"q":"Value of π?","opts":["3.12","3.14","3.16","3.18"],"a":"3.14"},
    {"q":"√144?","opts":["10","11","12","13"],"a":"12"},
    {"q":"HCF of 12 & 18?","opts":["3","6","9","12"],"a":"6"},
    {"q":"Chemical symbol of Sodium?","opts":["So","Na","S","N"],"a":"Na"},
    {"q":"Speed of light?","opts":["3×10⁸ m/s","3×10⁶ m/s","3×10⁵ m/s","3×10³ m/s"],"a":"3×10⁸ m/s"},
    {"q":"Who proposed relativity?","opts":["Newton","Einstein","Bohr","Tesla"],"a":"Einstein"},
    {"q":"Atomic number of Carbon?","opts":["4","6","8","12"],"a":"6"},
    {"q":"pH of neutral substance?","opts":["5","6","7","8"],"a":"7"},
    {"q":"Largest gland in body?","opts":["Heart","Liver","Kidney","Lung"],"a":"Liver"},
    {"q":"Unit of power?","opts":["Joule","Watt","Newton","Volt"],"a":"Watt"},
    {"q":"(a+b)² formula?","opts":["a²+b²","a²+2ab+b²","a²-2ab+b²","2a+b"],"a":"a²+2ab+b²"},
    {"q":"Area of circle?","opts":["πr²","2πr","πd","r²"],"a":"πr²"},
    {"q":"Photosynthesis needs?","opts":["O₂","CO₂","N₂","H₂"],"a":"CO₂"},
    {"q":"SI unit of force?","opts":["Watt","Joule","Newton","Pascal"],"a":"Newton"},
    {"q":"Which is not a metal?","opts":["Iron","Gold","Oxygen","Copper"],"a":"Oxygen"},
    {"q":"Longest bone?","opts":["Femur","Tibia","Fibula","Humerus"],"a":"Femur"},
    {"q":"Resistance unit?","opts":["Volt","Ampere","Ohm","Watt"],"a":"Ohm"},
    {"q":"Who discovered electron?","opts":["Bohr","Rutherford","Thomson","Newton"],"a":"Thomson"},
    {"q":"Largest desert?","opts":["Sahara","Thar","Gobi","Kalahari"],"a":"Sahara"},
    {"q":"Synonym of rapid?","opts":["Slow","Fast","Weak","Late"],"a":"Fast"},
    {"q":"10²?","opts":["10","100","1000","10000"],"a":"100"},
    {"q":"Angle in straight line?","opts":["90°","180°","270°","360°"],"a":"180°"},
    {"q":"Electric current unit?","opts":["Volt","Ohm","Ampere","Watt"],"a":"Ampere"},
    {"q":"Cell powerhouse?","opts":["Nucleus","Mitochondria","Ribosome","Golgi"],"a":"Mitochondria"},
    {"q":"Boiling point of water (K)?","opts":["273K","373K","100K","200K"],"a":"373K"},
    {"q":"Who wrote Constitution of India?","opts":["Nehru","Ambedkar","Gandhi","Patel"],"a":"Ambedkar"},
    {"q":"Largest island?","opts":["Greenland","Australia","Borneo","Madagascar"],"a":"Greenland"},
    {"q":"Antonym of expand?","opts":["Grow","Increase","Shrink","Spread"],"a":"Shrink"},
    {"q":"Gas used in balloons?","opts":["Oxygen","Hydrogen","Helium","Nitrogen"],"a":"Helium"},
    {"q":"Unit of pressure?","opts":["Pascal","Newton","Joule","Watt"],"a":"Pascal"},
]

PUZZLE_WORDS = ["grammar","noun","verb","adjective","adverb","sentence","paragraph","synonym","antonym","tense","voice","clause","phrase","history","culture","society","economy","democracy","constitution","citizen","geography","climate","continent","trade","addition","subtraction","multiplication","division","fraction","decimal","percentage","ratio","equation","algebra","geometry","angle","triangle","circle","perimeter","experiment","hypothesis","theory","observation","research","matter","energy","force","motion","element","compound","mixture","reaction","analysis","velocity","acceleration","gravity","friction","pressure","light","reflection","refraction","electricity","magnetism","cell","tissue","organ","organism","photosynthesis","respiration","digestion","circulation","enzyme","evolution","species","habitat","ecosystem","biodiversity","atom","molecule","neutron","proton","electron","formula","solution","density"]

GEO_DATA = {
    "countries":  [{"name":"India","info":"Capital: New Delhi"},{"name":"USA","info":"Capital: Washington DC"},{"name":"Japan","info":"Capital: Tokyo"},{"name":"France","info":"Capital: Paris"},{"name":"Brazil","info":"Capital: Brasília"},{"name":"Australia","info":"Capital: Canberra"},{"name":"Canada","info":"Capital: Ottawa"},{"name":"China","info":"Capital: Beijing"},{"name":"Russia","info":"Capital: Moscow"},{"name":"Germany","info":"Capital: Berlin"}],
    "india":      [{"name":"Andhra Pradesh","info":"Capital: Amaravati"},{"name":"Telangana","info":"Capital: Hyderabad"},{"name":"Tamil Nadu","info":"Capital: Chennai"},{"name":"Karnataka","info":"Capital: Bengaluru"},{"name":"Kerala","info":"Capital: Thiruvananthapuram"},{"name":"Maharashtra","info":"Capital: Mumbai"},{"name":"Gujarat","info":"Capital: Gandhinagar"},{"name":"Rajasthan","info":"Capital: Jaipur"},{"name":"Uttar Pradesh","info":"Capital: Lucknow"},{"name":"West Bengal","info":"Capital: Kolkata"},{"name":"Madhya Pradesh","info":"Capital: Bhopal"},{"name":"Bihar","info":"Capital: Patna"},{"name":"Punjab","info":"Capital: Chandigarh"},{"name":"Odisha","info":"Capital: Bhubaneswar"},{"name":"Assam","info":"Capital: Dispur"}],
    "oceans":     [{"name":"Pacific Ocean","info":"Largest ocean"},{"name":"Atlantic Ocean","info":"2nd largest"},{"name":"Indian Ocean","info":"3rd largest"},{"name":"Arctic Ocean","info":"Smallest"},{"name":"Southern Ocean","info":"Around Antarctica"}],
    "continents": [{"name":"Asia","info":"Largest continent"},{"name":"Africa","info":"2nd largest"},{"name":"North America","info":"3rd largest"},{"name":"South America","info":"4th largest"},{"name":"Antarctica","info":"5th largest"},{"name":"Europe","info":"6th largest"},{"name":"Australia","info":"Smallest continent"}],
    "deserts":    [{"name":"Sahara","info":"North Africa — largest hot desert"},{"name":"Thar Desert","info":"India / Pakistan"},{"name":"Gobi Desert","info":"China / Mongolia"},{"name":"Kalahari","info":"Southern Africa"},{"name":"Patagonian","info":"South America"},{"name":"Arabian Desert","info":"Middle East"}],
    "rivers":     [{"name":"Ganga","info":"India — sacred river"},{"name":"Yamuna","info":"India"},{"name":"Brahmaputra","info":"India / Bangladesh"},{"name":"Indus","info":"Pakistan"},{"name":"Nile","info":"Africa — world's longest"},{"name":"Amazon","info":"South America — largest by flow"},{"name":"Yangtze","info":"China"},{"name":"Mississippi","info":"USA"}],
    "places":     [{"name":"Taj Mahal","info":"Agra, India"},{"name":"Charminar","info":"Hyderabad, India"},{"name":"Red Fort","info":"Delhi, India"},{"name":"Gateway of India","info":"Mumbai"},{"name":"Qutub Minar","info":"Delhi"},{"name":"Mysore Palace","info":"Mysore, Karnataka"},{"name":"India Gate","info":"Delhi"},{"name":"Golden Temple","info":"Amritsar"},{"name":"Hawa Mahal","info":"Jaipur"}],
}

SCIENCE_DATA = {
    "physics":     [{"name":"Gravity","info":"Force attracting objects toward Earth"},{"name":"Velocity","info":"Speed with direction"},{"name":"Energy","info":"Ability to do work"},{"name":"Force","info":"Push or pull on an object"},{"name":"Electricity","info":"Flow of electric charge"},{"name":"Wave","info":"Disturbance that transfers energy"}],
    "chemistry":   [{"name":"Atom","info":"Basic unit of matter"},{"name":"Molecule","info":"Group of atoms bonded together"},{"name":"Element","info":"Pure substance, one type of atom"},{"name":"Compound","info":"Combination of two or more elements"},{"name":"Reaction","info":"Process where substances change"},{"name":"pH","info":"Measure of acidity/alkalinity (0–14)"}],
    "biology":     [{"name":"Cell","info":"Basic unit of life"},{"name":"DNA","info":"Genetic material of organisms"},{"name":"Photosynthesis","info":"Plants make food using sunlight"},{"name":"Respiration","info":"Energy release process in cells"},{"name":"Organism","info":"Any living being"},{"name":"Mitosis","info":"Cell division for growth"}],
    "space":       [{"name":"Sun","info":"Star at centre of solar system"},{"name":"Moon","info":"Earth's natural satellite"},{"name":"Planet","info":"Body orbiting a star"},{"name":"Galaxy","info":"System of billions of stars"},{"name":"Black Hole","info":"Region with extreme gravity"},{"name":"Comet","info":"Icy body orbiting the Sun"}],
    "environment": [{"name":"Ecosystem","info":"Living + non-living interaction"},{"name":"Pollution","info":"Harmful substances in environment"},{"name":"Climate","info":"Weather pattern over long period"},{"name":"Biodiversity","info":"Variety of life forms"},{"name":"Conservation","info":"Protection of natural resources"},{"name":"Ozone Layer","info":"Protects Earth from UV radiation"}],
    "inventions":  [{"name":"Electric Bulb","info":"Invented by Thomas Edison"},{"name":"Telephone","info":"Invented by Alexander Graham Bell"},{"name":"Internet","info":"Global computer network"},{"name":"Computer","info":"Electronic computing device"},{"name":"Airplane","info":"Invented by Wright Brothers"},{"name":"Printing Press","info":"Invented by Johannes Gutenberg"}],
}

# ══════════════════════════════════════════════════════════
#  BACKEND
# ══════════════════════════════════════════════════════════
def api_ask(question, subject):
    try:
        r = requests.post(f"{BACKEND}/ask", json={"question":question,"subject":subject,"session_id":st.session_state.chat_session_id,"user_id":st.session_state.user_id}, timeout=60)
        r.raise_for_status()
        return r.json().get("answer","⚠️ No answer received.")
    except requests.exceptions.ConnectionError:
        return "⚠️ Cannot connect to backend. Make sure FastAPI is running on port 8000."
    except Exception as e:
        return f"⚠️ Error: {e}"

def api_ask_image(file_bytes, filename, mime, question):
    try:
        r = requests.post(f"{BACKEND}/ask-from-image", files={"file":(filename,file_bytes,mime)}, data={"question":question}, timeout=90)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        return {"answer":f"⚠️ Error: {e}","extracted_text":""}

def api_grammar(text):
    try:
        r = requests.post(f"{BACKEND}/grammar-check", json={"text":text}, timeout=30)
        r.raise_for_status()
        return r.json().get("corrected_text","⚠️ No result.")
    except Exception as e:
        return f"⚠️ Error: {e}"

def check_backend():
    try:
        return requests.get(f"{BACKEND}/health", timeout=3).status_code == 200
    except:
        return False

# ══════════════════════════════════════════════════════════
#  PUZZLE
# ══════════════════════════════════════════════════════════
def scramble(word):
    chars = list(word); random.shuffle(chars); s = "".join(chars)
    return s if s != word else scramble(word)

def new_puzzle():
    w = random.choice(PUZZLE_WORDS)
    st.session_state.puzzle_word     = w
    st.session_state.puzzle_scramble = scramble(w)
    st.session_state.puzzle_result   = ""

if not st.session_state.puzzle_word:
    new_puzzle()

# ══════════════════════════════════════════════════════════
#  TOPBAR
# ══════════════════════════════════════════════════════════
backend_ok = check_backend()
st.markdown(f"""
<div class="topbar">
  <div class="topbar-logo"><span>🎓</span> AI-Powered Homework Assistance System</div>
  <div class="topbar-right">
    <span style="font-weight:700;">Hello Student!</span>
    <span class="{'backend-on' if backend_ok else 'backend-off'}">{'● Backend Connected' if backend_ok else '● Backend Offline'}</span>
    <span class="streak-badge">🔥 {st.session_state.streak}</span>
    <span class="moon-badge">🌙</span>
    <div class="profile-circle">👩‍🎓</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════
#  SIDEBAR — only nav items, no login/signup
# ══════════════════════════════════════════════════════════
NAV = [
    ("🏠", "Dashboard",         "home"),
    ("🤖", "Ask AI",            "ask"),
    ("📅", "Planner",           "planner"),
    ("❓", "Quiz",              "quiz"),
    ("✏️", "Grammar",           "grammar"),
    ("🎮", "Puzzle",            "puzzle"),
    ("🧠", "Flashcards",        "flashcards"),
    ("🍅", "Pomodoro",          "pomodoro"),
    ("🌍", "General Knowledge", "geo"),
]

with st.sidebar:
    st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)
    for icon, label, key in NAV:
        is_active = (st.session_state.section == key)
        # inject per-button active style using unique key
        if is_active:
            st.markdown(f"""
            <style>
            [data-testid="stSidebar"] [data-testid="baseButton-secondary"][aria-label="{icon}  {label}"] {{
                background: white !important;
                color: #1e3a8a !important;
                font-weight: 800 !important;
                box-shadow: 0 4px 14px rgba(0,0,0,0.15) !important;
            }}
            </style>
            """, unsafe_allow_html=True)
        if st.button(f"{icon}  {label}", key=f"nav_{key}", use_container_width=True):
            st.session_state.section = key
            st.rerun()

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
    if st.button("🌙 Dark Mode" if not DARK else "☀️ Light Mode", key="dark_btn", use_container_width=True):
        st.session_state.dark_mode = not DARK
        st.rerun()
    st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)
    if st.button("🚪 Logout", key="logout_btn", use_container_width=True):
        for k in list(st.session_state.keys()):
            del st.session_state[k]
        st.rerun()

if not backend_ok:
    st.markdown("""<div style="background:#fef2f2;border:1px solid #fca5a5;border-radius:12px;padding:10px 16px;margin:6px 0;font-size:13px;color:#991b1b;">
    ⚠️ <b>FastAPI backend is offline.</b> Run: <code style="background:#fee2e2;padding:2px 7px;border-radius:5px;">uvicorn main:app --reload</code>
    </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════
#  PAGES
# ══════════════════════════════════════════════════════════
section = st.session_state.section
st.markdown('<div class="main-pad">', unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────
#  HOME / DASHBOARD
# ─────────────────────────────────────────────────────────
if section == "home":
    st.markdown("""
    <div class="hero-card">
      <h2>🤖 AI Homework Assistant</h2>
      <p>Get instant help with maths, science, Telugu, Hindi, and more — anytime you need it.</p>
    </div>""", unsafe_allow_html=True)

    st.markdown(f'<div class="card"><div class="card-title">📚 Subjects</div>', unsafe_allow_html=True)

    # Row 1: 5 subjects
    r1_labels = ["Math",   "Physics",  "Chemistry", "Biology", "తెలుగు"]
    r1_keys   = ["Maths",  "Physics",  "Chemistry", "Biology", "Telugu"]
    cols1 = st.columns(5)
    for col, lbl, key in zip(cols1, r1_labels, r1_keys):
        with col:
            if st.button(lbl, key=f"hs1_{key}", use_container_width=True):
                st.session_state.selected_subject = key
                st.session_state.section = "ask"
                if key not in st.session_state.chat_history:
                    st.session_state.chat_history[key] = []
                st.rerun()

    # Row 2: 4 subjects (leave 1 column empty)
    r2_labels = ["हिन्दी", "English", "Social", "Computer"]
    r2_keys   = ["Hindi",  "English", "Social", "Computer"]
    cols2 = st.columns(5)
    for col, lbl, key in zip(cols2, r2_labels, r2_keys):
        with col:
            if st.button(lbl, key=f"hs2_{key}", use_container_width=True):
                st.session_state.selected_subject = key
                st.session_state.section = "ask"
                if key not in st.session_state.chat_history:
                    st.session_state.chat_history[key] = []
                st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("### 🎥 Learning Shorts")
    vcols = st.columns(4)
    for vc, vid in zip(vcols, ["q01E63DwN1c","vacGRuHDtO0","OQXanWrIUF8","PGUdWfB8nLg"]):
        with vc:
            st.markdown(f'<a href="https://www.youtube.com/watch?v={vid}" target="_blank"><div class="video-card-ui"><img src="https://img.youtube.com/vi/{vid}/0.jpg"/></div></a>', unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────
#  ASK AI
# ─────────────────────────────────────────────────────────
elif section == "ask":
    left, right = st.columns([1, 2.6])

    with left:
        st.markdown(f'<div style="background:{CARD};border-radius:14px;padding:14px 10px;border:1px solid {BORDER};margin-bottom:6px;"><div style="font-size:11px;font-weight:800;letter-spacing:1.2px;color:#6366f1;margin-bottom:10px;padding:0 4px;">SUBJECTS</div></div>', unsafe_allow_html=True)
        for icon, key in [("➗","Maths"),("⚡","Physics"),("🧪","Chemistry"),("🧬","Biology"),("🅣","Telugu"),("🅗","Hindi"),("📖","English"),("🌍","Social"),("💻","Computer")]:
            active = st.session_state.selected_subject == key
            if st.button(f"{icon}  {key}", key=f"as_{key}", use_container_width=True, type="primary" if active else "secondary"):
                st.session_state.selected_subject = key
                st.session_state.chat_session_id  = f"chat_{int(time.time())}"
                if key not in st.session_state.chat_history:
                    st.session_state.chat_history[key] = []
                st.rerun()

    with right:
        subject = st.session_state.selected_subject
        if not subject:
            st.markdown(f"""
            <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:14px;">
              <div style="font-size:18px;font-weight:800;color:{TEXT};">🤖 Ask AI Assistant</div>
              <div style="background:#eef2ff;color:#6366f1;padding:5px 14px;border-radius:999px;font-size:12px;font-weight:700;border:1px solid #c7d2fe;">Select a subject</div>
            </div>
            <div style="background:{CARD};border-radius:16px;border:1px solid {BORDER};height:380px;display:flex;align-items:center;justify-content:center;">
              <div style="text-align:center;color:{SUB};">
                <div style="font-size:46px;margin-bottom:12px;">🤖</div>
                <div style="font-size:16px;font-weight:800;color:{TEXT};margin-bottom:6px;">Select a subject to begin</div>
                <div style="font-size:13px;">Choose from the list on the left</div>
              </div>
            </div>""", unsafe_allow_html=True)
        else:
            meta    = SUBJECT_META.get(subject, {"icon":"📘","tips":[]})
            history = st.session_state.chat_history.get(subject, [])

            st.markdown(f'<div class="subj-mode-badge">{meta["icon"]} {subject} Mode</div>', unsafe_allow_html=True)

            if meta["tips"]:
                tc = st.columns(len(meta["tips"]))
                for i,(col,tip) in enumerate(zip(tc, meta["tips"])):
                    with col:
                        if st.button(tip, key=f"tip_{subject}_{i}"):
                            st.session_state[f"_pre_{subject}"] = tip
                            st.rerun()

            chat_html = '<div class="chat-box">'
            if not history:
                chat_html += f'<div class="subject-banner-ui"><div class="bicon">{meta["icon"]}</div><h3>{subject} AI Tutor</h3><p>Ask me anything about {subject}. I\'m here to help!</p></div>'
            else:
                for msg in history:
                    qt = str(msg["q"]).replace("<","&lt;").replace(">","&gt;")
                    chat_html += f'<div class="user-bubble"><div class="msg">{qt}</div></div><div class="ai-row"><div class="ai-avatar">🤖</div><div class="ai-bubble">{str(msg["a"])}</div></div>'
            chat_html += '</div>'
            st.markdown(chat_html, unsafe_allow_html=True)

            prefill = st.session_state.pop(f"_pre_{subject}", "")
            ci, cb  = st.columns([5,1])
            with ci:
                question = st.text_input("Q", value=prefill, key=f"qi_{subject}", placeholder="Type your question and press Ask ➤", label_visibility="collapsed")
            with cb:
                send = st.button("➤ Ask", key="ask_send", use_container_width=True, type="primary")

            uploaded = st.file_uploader("📷 Upload image / PDF (optional)", type=["jpg","jpeg","png","bmp","webp","pdf"], key=f"up_{subject}")

            if send and question.strip():
                q = question.strip()
                if uploaded:
                    with st.spinner("🤖 Reading file…"):
                        res = api_ask_image(uploaded.read(), uploaded.name, uploaded.type, q)
                    ans = res.get("answer","⚠️ No answer.")
                    ext = res.get("extracted_text","")
                    if ext: ans = f'<span style="opacity:.7;font-size:.85em">📄 <b>Extracted:</b> {ext[:200]}…</span><br><br>' + ans
                else:
                    with st.spinner(f"🤖 {subject} tutor thinking…"):
                        ans = api_ask(q, subject)

                ans_html = ans.replace("\n\n","<br><br>").replace("\n","<br>")
                if subject not in st.session_state.chat_history:
                    st.session_state.chat_history[subject] = []
                st.session_state.chat_history[subject].append({"q":q,"a":ans_html})
                st.rerun()

            if history:
                c1,c2 = st.columns(2)
                with c1:
                    if st.button("✨ New Chat", key="new_chat"):
                        st.session_state.chat_history[subject] = []
                        st.session_state.chat_session_id = f"chat_{int(time.time())}"
                        st.rerun()
                with c2:
                    if st.button("🗑️ Clear History", key="clr_hist"):
                        st.session_state.chat_history[subject] = []
                        st.rerun()

# ─────────────────────────────────────────────────────────
#  PLANNER
# ─────────────────────────────────────────────────────────
elif section == "planner":
    st.markdown(f'<div style="text-align:center;padding:10px 0 20px;"><div style="font-size:34px;">📅</div><h1 style="font-size:26px;font-weight:900;color:{TEXT};margin:8px 0 6px;">Smart Study Planner</h1><p style="font-size:14px;color:{SUB};font-weight:500;">Enter your previous marks and get performance analysis & a personalised plan.</p></div>', unsafe_allow_html=True)

    with st.form("planner_form"):
        c1,c2,c3 = st.columns(3)
        with c1: name = st.text_input("👩‍🎓 Student Name")
        with c2: cls  = st.text_input("🏫 Class (e.g. 10th / Inter)")
        with c3: date = st.date_input("📅 Date")
        st.markdown("### 📊 Enter Previous Marks")
        m1,m2,m3 = st.columns(3)
        with m1:
            eng  = st.number_input("📘 English",  0,100,0)
            mths = st.number_input("➗ Maths",    0,100,0)
        with m2:
            sci  = st.number_input("🔬 Science",  0,100,0)
            soc  = st.number_input("🌍 Social",   0,100,0)
        with m3:
            comp = st.number_input("💻 Computer", 0,100,0)
            opt  = st.number_input("📝 Optional", 0,100,0)
        goal = st.text_area("🎯 Study Goal", placeholder="e.g. I want to score above 90% in exams")
        submitted = st.form_submit_button("🚀 Generate My Study Planner", use_container_width=True, type="primary")

    if submitted:
        if not name or not cls:
            st.warning("⚠️ Please fill Student Name and Class.")
        else:
            marks = [{"subject":"English","mark":eng},{"subject":"Maths","mark":mths},{"subject":"Science","mark":sci},{"subject":"Social","mark":soc},{"subject":"Computer","mark":comp},{"subject":"Optional","mark":opt}]
            avg   = sum(m["mark"] for m in marks)/len(marks)
            sa    = sorted(marks, key=lambda x:x["mark"])
            sd    = sorted(marks, key=lambda x:x["mark"], reverse=True)

            if avg>=90:   perf,pcls="🌟 Excellent","perf-excellent"
            elif avg>=75: perf,pcls="✅ Good","perf-good"
            elif avg>=50: perf,pcls="⚠️ Average","perf-average"
            else:         perf,pcls="❌ Poor","perf-poor"

            tips_map = {"perf-excellent":["Maintain your strong study routine.","Solve advanced-level questions.","Take weekly mock tests.","Revise every weekend.","Stay consistent."],"perf-good":["Consistency is key.","Focus on high-weight chapters.","Practice neat answer writing.","Revise weekly.","Take mini tests."],"perf-average":["More consistency daily.","Extra time on weak subjects.","Practice textbook questions.","Use flashcards.","Study in focused sessions."],"perf-poor":["Start with basics first.","Study daily in short sessions.","Focus on weakest subjects.","Ask teachers when in doubt.","Revise every day."]}
            plan_map  = {"perf-excellent":["📘 1 hr concept revision","🧠 45 min mock test","📝 30 min short notes","📚 30 min weak topic"],"perf-good":["📘 1 hr revision","✍️ 45 min practice","📚 30 min revision","🎯 20 min improvement"],"perf-average":["📘 45 min concept","✍️ 45 min practice","🔁 30 min revision","🧠 20 min formulas"],"perf-poor":["📘 30 min basics","✍️ 30 min easy practice","🔁 20 min revision","🧠 20 min formulas","📚 20 min support"]}

            st.markdown(f'<div style="background:linear-gradient(135deg,#eef2ff,#f5f3ff);border-radius:16px;padding:20px;text-align:center;margin:12px 0;border:1px solid #ddd6fe;"><h2 style="color:{TEXT};">👩‍🎓 {name}\'s Study Report</h2><p style="margin-top:8px;color:#4b5563;font-weight:500"><b>Class:</b> {cls} &nbsp;|&nbsp; <b>Date:</b> {date} &nbsp;|&nbsp; <b>Goal:</b> {goal or "Not specified"}</p></div>', unsafe_allow_html=True)
            st.markdown(f'<div class="{pcls}"><h2>{perf}</h2><p>Average: <b>{avg:.1f}%</b></p></div>', unsafe_allow_html=True)

            mk = st.columns(3)
            for i,m in enumerate(marks):
                with mk[i%3]:
                    st.markdown(f'<div class="mark-result-card"><h4>{m["subject"]}</h4><p>{m["mark"]}/100</p></div>', unsafe_allow_html=True)

            wc,sc2 = st.columns(2)
            with wc:
                st.markdown(f'<div class="analysis-box" style="border-top:5px solid #ef4444;"><h3>📉 Weak Subjects</h3><ul><li>{sa[0]["subject"]} — {sa[0]["mark"]}/100</li><li>{sa[1]["subject"]} — {sa[1]["mark"]}/100</li></ul></div>', unsafe_allow_html=True)
            with sc2:
                st.markdown(f'<div class="analysis-box" style="border-top:5px solid #10b981;"><h3>📈 Strong Subjects</h3><ul><li>{sd[0]["subject"]} — {sd[0]["mark"]}/100</li><li>{sd[1]["subject"]} — {sd[1]["mark"]}/100</li></ul></div>', unsafe_allow_html=True)

            tc2,pc2 = st.columns(2)
            with tc2:
                li = "".join(f"<li>{t}</li>" for t in tips_map[pcls])
                st.markdown(f'<div class="analysis-box"><h3>💡 Study Tips</h3><ul>{li}</ul></div>', unsafe_allow_html=True)
            with pc2:
                li = "".join(f"<li>{p}</li>" for p in plan_map[pcls])
                st.markdown(f'<div class="analysis-box"><h3>📅 Daily Plan</h3><ul>{li}</ul></div>', unsafe_allow_html=True)

            st.markdown("### 🗓️ Weekly Strategy")
            days    = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]
            assigns = [sa[0]["subject"],sa[1]["subject"],"Revision",sd[0]["subject"],sd[1]["subject"],"Mock Test","Light Revision"]
            dcols   = st.columns(7)
            for day,col,assign in zip(days,dcols,assigns):
                with col:
                    st.markdown(f'<div class="week-day-box">{day}<span>{assign}</span></div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────
#  QUIZ
# ─────────────────────────────────────────────────────────
elif section == "quiz":
    if not st.session_state.quiz_active and not st.session_state.quiz_done:
        st.markdown('<div class="quiz-start-box"><div class="quiz-big-title">START<br>QUIZ</div></div>', unsafe_allow_html=True)
        _,mid,_ = st.columns([2,1,2])
        with mid:
            if st.button("▶ Start Quiz", key="sq", use_container_width=True, type="primary"):
                st.session_state.quiz_active=True; st.session_state.quiz_index=0
                st.session_state.quiz_score=0;  st.session_state.quiz_done=False
                st.rerun()

    elif st.session_state.quiz_active:
        idx=st.session_state.quiz_index; total=len(QUIZ_QUESTIONS); q=QUIZ_QUESTIONS[idx]
        st.progress(idx/total, text=f"Question {idx+1} of {total}")
        st.markdown(f'<div class="quiz-card-ui"><h3>Q{idx+1}. {q["q"]}</h3></div>', unsafe_allow_html=True)
        o1,o2=st.columns(2)
        for i,opt in enumerate(q["opts"]):
            with (o1 if i%2==0 else o2):
                if st.button(opt, key=f"opt_{idx}_{i}", use_container_width=True):
                    if opt==q["a"]: st.session_state.quiz_score+=1; st.success("✅ Correct!")
                    else: st.error(f"❌ Wrong! Answer: **{q['a']}**")
                    time.sleep(0.8)
                    st.session_state.quiz_index+=1
                    if st.session_state.quiz_index>=total:
                        st.session_state.quiz_active=False; st.session_state.quiz_done=True
                    st.rerun()

    elif st.session_state.quiz_done:
        score=st.session_state.quiz_score; total=len(QUIZ_QUESTIONS); pct=int(score/total*100)
        emoji="🌟" if pct>=80 else "✅" if pct>=60 else "📚"
        st.markdown(f'<div class="quiz-start-box" style="padding:40px;"><div style="font-size:52px">{emoji}</div><h2 style="font-size:32px;margin:14px 0;">Your Score</h2><div style="font-size:70px;font-weight:900;">{score}/{total}</div><p style="font-size:17px;opacity:.85;">{pct}% correct</p></div>', unsafe_allow_html=True)
        _,mid,_=st.columns([2,1,2])
        with mid:
            if st.button("🔄 Play Again", key="qa", use_container_width=True, type="primary"):
                st.session_state.quiz_active=False; st.session_state.quiz_done=False
                st.session_state.quiz_index=0;   st.session_state.quiz_score=0
                st.rerun()

# ─────────────────────────────────────────────────────────
#  GRAMMAR
# ─────────────────────────────────────────────────────────
elif section == "grammar":
    st.markdown('<div class="sec-head">✏️ Grammar Learning</div>', unsafe_allow_html=True)

    topics = [("📘 Tenses","tenses","Understand Present, Past and Future tenses."),("🧩 Parts of Speech","parts","Noun, Verb, Adjective, Adverb, Pronoun explained."),("🔄 Active & Passive","voice","Sentences change from active to passive voice."),("📚 Vocabulary","vocabulary","Improve synonyms, antonyms and word meanings."),("✍️ Punctuation","punctuation","Master commas, full stops, question marks."),("📝 Sentence Structure","sentence","Build correct sentences: Subject + Verb + Object.")]
    gc = st.columns(3)
    for i,(lbl,key,desc) in enumerate(topics):
        with gc[i%3]:
            st.markdown(f'<div class="grammar-card-ui"><h3>{lbl}</h3><p>{desc}</p></div>', unsafe_allow_html=True)
            if st.button("Open", key=f"gram_{key}", use_container_width=True):
                st.session_state.grammar_topic=key; st.rerun()

    topic = st.session_state.grammar_topic
    if not topic:
        st.markdown(f'<div style="text-align:center;padding:32px 20px;color:{SUB};"><div style="font-size:36px;margin-bottom:10px;">📚</div><div style="font-size:15px;font-weight:800;color:{TEXT};margin-bottom:5px;">Select a Grammar Topic</div><div style="font-size:13px;">Click any card above to learn.</div></div>', unsafe_allow_html=True)

    if topic == "tenses":
        st.markdown("#### 📘 Tenses Chart")
        t1,t2,t3=st.columns(3)
        present=[("Simple Present","Subject+V1","I always speak the truth."),("Present Continuous","Subject+is/am/are+V1+ing","Ali is riding a bicycle."),("Present Perfect","Subject+has/have+V3","The sun has set."),("Present Perfect Continuous","Subject+has/have+been+V1+ing","Sun has been shining since morning.")]
        past=[("Simple Past","Subject+V2","We went to the zoo yesterday."),("Past Continuous","Subject+was/were+V1+ing","He was smiling."),("Past Perfect","Subject+had+V3","They had finished work."),("Past Perfect Continuous","Subject+had been+V1+ing","He had been working for days.")]
        future=[("Simple Future","Subject+will+V1","You will pass."),("Future Continuous","Subject+will+be+V1+ing","They will be visiting."),("Future Perfect","Subject+will+have+V3","I shall have finished."),("Future Perfect Continuous","Subject+will+have been+V1+ing","She will have been sleeping.")]
        with t1:
            st.markdown('<div class="tense-col-present"><h3>Present</h3>', unsafe_allow_html=True)
            for n,s,e in present: st.markdown(f'<div class="tense-card-box"><h4>{n}</h4><p><b>Structure:</b> {s}</p><p><b>Example:</b> {e}</p></div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        with t2:
            st.markdown('<div class="tense-col-past"><h3>Past</h3>', unsafe_allow_html=True)
            for n,s,e in past: st.markdown(f'<div class="tense-card-box"><h4>{n}</h4><p><b>Structure:</b> {s}</p><p><b>Example:</b> {e}</p></div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        with t3:
            st.markdown('<div class="tense-col-future"><h3>Future</h3>', unsafe_allow_html=True)
            for n,s,e in future: st.markdown(f'<div class="tense-card-box"><h4>{n}</h4><p><b>Structure:</b> {s}</p><p><b>Example:</b> {e}</p></div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

    elif topic == "parts":
        st.markdown("#### 🧩 Parts of Speech")
        pos_data=[("Noun","Naming person, place, thing or idea.","cat, John, park","noun"),("Pronoun","Takes place of a noun.","she, they, it","pronoun"),("Verb","Expresses action or state.","runs, sings, are","verb"),("Adjective","Describes a noun.","fluffy, tall","adjective"),("Adverb","Modifies a verb or adjective.","quickly, beautifully","adverb"),("Preposition","Shows relationship.","under, through","preposition"),("Conjunction","Connects words/clauses.","and, or, because","conjunction"),("Interjection","Expresses emotion.","Wow!, Ouch!","interjection")]
        pc=st.columns(2)
        for i,(n,d,e,c) in enumerate(pos_data):
            with pc[i%2]: st.markdown(f'<div class="pos-card pos-{c}"><h3>{n}</h3><p><b>Definition:</b> {d}</p><p><b>Examples:</b> {e}</p></div>', unsafe_allow_html=True)

    elif topic == "voice":
        st.markdown("#### 🔄 Active & Passive Voice")
        vc1,vc2=st.columns(2)
        with vc1: st.markdown('<div class="voice-card-active"><h3>Active Voice</h3><p>Subject performs the action on the object.</p><div class="formula-box">Subject + Verb + Object</div><ul style="padding-left:16px;font-size:13px;line-height:1.9;color:#475569;"><li>Anna painted the house.</li><li>The teacher answers questions.</li><li>Ali posted the video.</li></ul></div>', unsafe_allow_html=True)
        with vc2: st.markdown('<div class="voice-card-passive"><h3>Passive Voice</h3><p>The subject is acted upon by the object.</p><div class="formula-box">Object + Verb + Subject</div><ul style="padding-left:16px;font-size:13px;line-height:1.9;color:#475569;"><li>The house was painted by Anna.</li><li>Questions are answered by the teacher.</li><li>The video was posted by Ali.</li></ul></div>', unsafe_allow_html=True)

    elif topic == "vocabulary":
        st.markdown("#### 📚 Vocabulary Levels")
        vb1,vb2,vb3=st.columns(3)
        for col,level,cls2,words in [(vb1,"Beginner","beginner",["keep","run","walk","wait","happy","sad","afraid","tiny","cold","big"]),(vb2,"Intermediate","intermediate",["hold","jog","stroll","delay","glad","anxious","starving","clear","massive","simple"]),(vb3,"Advanced","advanced",["retain","sprint","wander","postpone","delighted","terrified","famished","enormous","intricate","effortless"])]:
            with col:
                items="".join(f"<li>{w}</li>" for w in words)
                st.markdown(f'<div class="vocab-card vocab-{cls2}"><h3>{level}</h3><ul>{items}</ul></div>', unsafe_allow_html=True)

    elif topic == "punctuation":
        st.markdown("#### ✍️ Punctuation Marks")
        puncs=[("Period (.)","Sophia loves playing hockey."),("Question Mark (?)","Are you hungry?"),("Comma (,)","I like novels, stories, and poems."),("Exclamation Mark (!)","Wow! What a lovely scene!"),("Colon (:)","She likes: Italy, USA, UAE."),("Semicolon (;)","I won't take cola; I'll drink juice."),("Braces { }","Choose: {red, pink, black}."),("Parentheses ( )","I love UK (United Kingdom)."),("Dashes (—)","USA—Japan flight is 13 hours."),("Brackets [ ]","She [Jenny] loves driving."),("Hyphen (-)","I love ice-cream."),('Quotation (" ")','Ali asked, "When can I leave?"'),("Ellipsis (...)","Julie... is the girl who..."),("Apostrophe (')","Roger's dog is weak.")]
        pp1,pp2=st.columns(2)
        for i,(n,e) in enumerate(puncs):
            with (pp1 if i%2==0 else pp2): st.markdown(f'<div class="punc-card"><h3>{n}</h3><p>{e}</p></div>', unsafe_allow_html=True)

    elif topic == "sentence":
        st.markdown("#### 📝 Sentence Structures")
        ss1,ss2=st.columns(2)
        sent=[("Simple Sentence","1 Independent Clause","Children played.","simple"),("Compound Sentence","2 Independent Clauses","Children played, and parents chatted.","compound"),("Complex Sentence","1 Independent + 1 Dependent","Children played after rain stopped.","complex"),("Compound-Complex","2+ Independent + 1+ Dependent","After rain stopped, children played, and parents chatted.","cc")]
        for i,(n,d,e,c) in enumerate(sent):
            with (ss1 if i%2==0 else ss2): st.markdown(f'<div class="sentence-card sentence-{c}"><h3>{n}</h3><p><b>{d}</b></p><div class="example">{e}</div></div>', unsafe_allow_html=True)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown("### 🔍 Check Your Grammar")
    gram_text = st.text_area("Type sentence…", height=130, key="gram_ta", placeholder="Type your sentence here…")
    if st.button("✨ Check Grammar", key="chk_gram", type="primary"):
        if gram_text.strip():
            with st.spinner("Checking…"):
                st.session_state.grammar_result = api_grammar(gram_text)
        else:
            st.warning("⚠️ Please enter a sentence first.")
    if st.session_state.grammar_result:
        st.markdown(f'<div class="grammar-result-box">✅ <b>Corrected:</b> {st.session_state.grammar_result}</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────
#  PUZZLE
# ─────────────────────────────────────────────────────────
elif section == "puzzle":
    _,center,_=st.columns([1,2,1])
    with center:
        st.markdown(f'<div style="background:{CARD};border-radius:22px;padding:36px 28px;text-align:center;box-shadow:0 10px 36px rgba(0,0,0,0.08);border:1px solid {BORDER};"><div style="font-size:20px;font-weight:900;color:{TEXT};margin-bottom:20px;">🧩 Word Scramble</div><div class="scramble-box">{st.session_state.puzzle_scramble.upper()}</div></div>', unsafe_allow_html=True)
        user_ans=st.text_input("Enter correct word", key="puzz_ans", placeholder="Enter correct word")
        p1,p2=st.columns(2)
        with p1:
            if st.button("✔ Check", key="chk_puzz", use_container_width=True, type="primary"):
                if user_ans.strip().lower()==st.session_state.puzzle_word: st.session_state.puzzle_result="✅ Correct! 🎉"
                else: st.session_state.puzzle_result=f"❌ Try Again! ({len(st.session_state.puzzle_word)} letters)"
        with p2:
            if st.button("🔄 New", key="new_puzz", use_container_width=True):
                new_puzzle(); st.rerun()
        if st.session_state.puzzle_result:
            color="#16a34a" if "✅" in st.session_state.puzzle_result else "#dc2626"
            st.markdown(f'<div style="text-align:center;font-size:19px;font-weight:800;color:{color};margin:14px 0">{st.session_state.puzzle_result}</div>', unsafe_allow_html=True)
        if st.button("💡 Reveal Answer", key="reveal_puzz", use_container_width=True):
            st.info(f"The answer is: **{st.session_state.puzzle_word.upper()}**")

# ─────────────────────────────────────────────────────────
#  FLASHCARDS
# ─────────────────────────────────────────────────────────
elif section == "flashcards":
    st.markdown(f'<div style="text-align:center;margin-bottom:22px;"><span style="font-size:34px;">🧠</span><h2 style="font-size:24px;font-weight:900;color:{TEXT};margin:8px 0 0;">Flashcards</h2></div>', unsafe_allow_html=True)

    fi1,fi2,fi3=st.columns([2,2,1])
    with fi1: nq=st.text_input("Question", key="fq", placeholder="Enter Question")
    with fi2: na=st.text_input("Answer",   key="fa", placeholder="Enter Answer")
    with fi3:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("➕ Add Card", key="add_fc", use_container_width=True, type="primary"):
            if nq and na:
                st.session_state.flashcards.append({"q":nq,"a":na})
                st.session_state.flash_index=len(st.session_state.flashcards)-1
                st.session_state.flash_flipped=False; st.rerun()
            else: st.warning("Enter both question and answer.")

    cards=st.session_state.flashcards
    if not cards:
        st.markdown(f'<div style="background:linear-gradient(135deg,#4361ee,#6366f1);border-radius:16px;padding:60px 20px;text-align:center;color:white;font-size:15px;font-weight:700;margin:14px 0;">No cards yet. Add one above! 👆</div>', unsafe_allow_html=True)
        bc1,bc2,bc3=st.columns(3)
        with bc1: st.button("← Prev", use_container_width=True, key="fc_pe", disabled=True)
        with bc2: st.button("Next →", use_container_width=True, key="fc_ne", disabled=True)
        with bc3: st.button("🗑 Delete", use_container_width=True, key="fc_de", disabled=True)
    else:
        idx=st.session_state.flash_index % len(cards)
        flipped=st.session_state.flash_flipped
        card=cards[idx]; display=card["a"] if flipped else card["q"]
        fc_cls="fc-back" if flipped else "fc-front"

        st.markdown(f'<div class="flashcard-ui {fc_cls}">{"💡 " if flipped else "❓ "}{display}</div><div style="text-align:center;color:{SUB};font-size:13px;margin-bottom:10px;font-weight:500;">Card {idx+1} of {len(cards)}</div>', unsafe_allow_html=True)

        bc1,bc2,bc3=st.columns(3)
        with bc1:
            if st.button("← Prev", use_container_width=True, key="fc_prev"):
                st.session_state.flash_index=max(0,idx-1); st.session_state.flash_flipped=False; st.rerun()
        with bc2:
            if st.button("Next →", use_container_width=True, key="fc_next"):
                st.session_state.flash_index=min(len(cards)-1,idx+1); st.session_state.flash_flipped=False; st.rerun()
        with bc3:
            if st.button("🗑 Delete", use_container_width=True, key="fc_del"):
                cards.pop(idx); st.session_state.flash_index=max(0,idx-1); st.session_state.flash_flipped=False; st.rerun()

        _,fc_mid,_=st.columns([1,1,1])
        with fc_mid:
            if st.button("🔄 Flip", use_container_width=True, key="fc_flip", type="primary"):
                st.session_state.flash_flipped=not flipped; st.rerun()

        st.markdown(f'<div style="margin-top:18px;font-size:14px;font-weight:800;color:{TEXT};">📚 All Flashcards</div>', unsafe_allow_html=True)
        mini_html='<div class="flash-mini-grid">'+''.join(f'<div class="flash-mini-card">{c["q"]}</div>' for c in cards)+'</div>'
        st.markdown(mini_html, unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────
#  POMODORO
# ─────────────────────────────────────────────────────────
elif section == "pomodoro":
    secs=st.session_state.pomo_seconds
    time_str=f"{secs//60:02d}:{secs%60:02d}"

    _,center,_=st.columns([1,1.4,1])
    with center:
        st.markdown(f'<div class="pomo-wrap"><div class="pomo-title">🍅 Pomodoro Timer</div><div class="pomo-circle">{time_str}</div><div class="pomo-hint">Focus for 25 minutes, then take a short break ☕</div></div>', unsafe_allow_html=True)

        pc1,pc2,pc3=st.columns(3)
        with pc1:
            if st.button("▶ Start", use_container_width=True, key="pm_start", type="primary"):
                st.session_state.pomo_running=True
        with pc2:
            if st.button("⏸ Pause", use_container_width=True, key="pm_pause"):
                st.session_state.pomo_running=False
        with pc3:
            if st.button("🔄 Reset", use_container_width=True, key="pm_reset"):
                st.session_state.pomo_running=False; st.session_state.pomo_seconds=1500; st.rerun()

        if st.session_state.pomo_running:
            if secs>0:
                time.sleep(1); st.session_state.pomo_seconds-=1; st.rerun()
            else:
                st.session_state.pomo_running=False; st.balloons(); st.success("🎉 Time's up! Take a 5-minute break.")

        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        st.markdown("#### ⚙️ Custom Timer")
        custom_min=st.slider("Set minutes",1,60,25,key="pomo_slider")
        if st.button("⏱ Set Timer", key="pomo_set", use_container_width=True):
            st.session_state.pomo_seconds=custom_min*60; st.session_state.pomo_running=False; st.rerun()

# ─────────────────────────────────────────────────────────
#  GENERAL KNOWLEDGE
# ─────────────────────────────────────────────────────────
elif section == "geo":
    st.markdown(f'<div style="text-align:center;margin-bottom:22px;"><span style="font-size:34px;">🌍</span><h2 style="font-size:24px;font-weight:900;color:{TEXT};margin:8px 0 0;">General Knowledge Explorer</h2></div>', unsafe_allow_html=True)

    st.markdown(f'<div class="gk-section"><h2>🌍 Geography Explorer</h2>', unsafe_allow_html=True)
    gb=st.columns(7)
    for col,(lbl,key) in zip(gb,[("🌎 Countries","countries"),("🇮🇳 India States","india"),("🌊 Oceans","oceans"),("🌐 Continents","continents"),("🏜 Deserts","deserts"),("🏞 Rivers","rivers"),("🏛 Places","places")]):
        with col:
            if st.button(lbl, key=f"geo_{key}", use_container_width=True):
                st.session_state.geo_result=GEO_DATA[key]; st.session_state.geo_title=lbl; st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown(f'<div class="gk-section"><h2>🔬 Science Explorer</h2>', unsafe_allow_html=True)
    sb=st.columns(6)
    for col,(lbl,key) in zip(sb,[("⚡ Physics","physics"),("🧪 Chemistry","chemistry"),("🧬 Biology","biology"),("🚀 Space","space"),("🌱 Environment","environment"),("💡 Inventions","inventions")]):
        with col:
            if st.button(lbl, key=f"sci_{key}", use_container_width=True):
                st.session_state.geo_result=SCIENCE_DATA[key]; st.session_state.geo_title=lbl; st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    if st.session_state.geo_result:
        st.markdown(f"#### {st.session_state.geo_title}")
        items=st.session_state.geo_result
        gcols=st.columns(min(4,len(items)))
        for i,item in enumerate(items):
            with gcols[i%min(4,len(items))]:
                info=item.get("info","")
                st.markdown(f'<div class="geo-item-ui"><h4>{item["name"]}</h4>{"<p>"+info+"</p>" if info else ""}</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)