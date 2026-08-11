import streamlit as st
import datetime
import sqlite3
import pandas as pd
import hashlib
import plotly.express as px

# ---------------------------------------------------------
# 1. PAGE CONFIGURATION & DARK GLASSMORPHISM STYLING
# ---------------------------------------------------------
st.set_page_config(
    page_title="VitalTrack Health | IITM BS",
    page_icon="🌸",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
    <style>
    .stApp {
        background-color: #090d16;
        color: #f8fafc;
    }
    .main-header {
        background: linear-gradient(135deg, #1e1b4b 0%, #312e81 50%, #831843 100%);
        padding: 20px;
        border-radius: 16px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.5);
        margin-bottom: 20px;
    }
    .badge {
        background-color: #f59e0b;
        color: #000;
        padding: 4px 12px;
        border-radius: 20px;
        font-weight: bold;
        font-size: 0.85rem;
    }
    .metric-card {
        background: rgba(30, 41, 59, 0.7);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 16px;
        border-radius: 12px;
        text-align: center;
    }
    .phase-card {
        background: rgba(15, 23, 42, 0.8);
        border-left: 4px solid #ec4899;
        padding: 14px 18px;
        border-radius: 0 12px 12px 0;
        margin: 15px 0;
    }
    .overdue-banner {
        background: rgba(153, 27, 27, 0.4);
        border: 1px solid #ef4444;
        border-left: 6px solid #f87171;
        padding: 16px 20px;
        border-radius: 12px;
        margin: 15px 0;
    }
    </style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 2. SQLITE DATABASE ENGINE
# ---------------------------------------------------------
def hash_password(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

def get_db_connection():
    return sqlite3.connect("vitaltrack_users.db")

def init_db():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS user_cycles (
            username TEXT PRIMARY KEY,
            last_period_date DATE,
            cycle_length INTEGER,
            period_duration INTEGER
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS user_exams (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            exam_name TEXT,
            exam_date DATE
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS user_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            log_date DATE,
            flow TEXT,
            cramps TEXT,
            mood TEXT,
            energy INTEGER,
            symptoms TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""

# ---------------------------------------------------------
# 3. BRANDED HEADER (REMOVED AI TITLE)
# ---------------------------------------------------------
col_logo, col_title = st.columns([1, 6])
with col_logo:
    st.image("https://upload.wikimedia.org/wikipedia/en/6/69/IIT_Madras_Logo.svg", width=95)
with col_title:
    st.markdown("""
        <div class="main-header">
            <h1 style="margin:0; font-size: 2rem; color: #ffffff;">🌸 VitalTrack: Student Cycle & Health Portal</h1>
            <p style="margin:4px 0 0 0; color: #cbd5e1;">
                Designed & Developed by <span class="badge">Sudhanshu Mishra</span> | <b>IIT Madras BS (Diploma Level)</b>
            </p>
        </div>
    """, unsafe_allow_html=True)

# ---------------------------------------------------------
# 4. LOGIN / REGISTER SECTION
# ---------------------------------------------------------
if not st.session_state.logged_in:
    st.subheader("🔐 Student Portal Access")
    tab_login, tab_signup = st.tabs(["Log In to Your ID", "Create New Student Account"])

    with tab_login:
        with st.form("login_form"):
            login_user = st.text_input("Username / Student ID:")
            login_pass = st.text_input("Password:", type="password")
            btn_login = st.form_submit_button("Log In")

            if btn_login:
                conn = get_db_connection()
                c = conn.cursor()
                c.execute("SELECT password FROM users WHERE username = ?", (login_user.strip(),))
                record = c.fetchone()
                conn.close()

                if record and record[0] == hash_password(login_pass):
                    st.session_state.logged_in = True
                    st.session_state.username = login_user.strip()
                    st.success(f"Welcome back, {login_user.strip()}!")
                    st.rerun()
                else:
                    st.error("Invalid Username or Password.")

    with tab_signup:
        with st.form("signup_form"):
            new_user = st.text_input("Choose Username / Student ID:")
            new_pass = st.text_input("Choose Password:", type="password")
            btn_signup = st.form_submit_button("Register Account")

            if btn_signup:
                if new_user.strip() and new_pass.strip():
                    conn = get_db_connection()
                    c = conn.cursor()
                    try:
                        c.execute("INSERT INTO users (username, password) VALUES (?, ?)",
                                  (new_user.strip(), hash_password(new_pass)))
                        default_date = datetime.date.today() - datetime.timedelta(days=12)
                        c.execute("INSERT INTO user_cycles (username, last_period_date, cycle_length, period_duration) VALUES (?, ?, ?, ?)",
                                  (new_user.strip(), default_date, 28, 5))
                        conn.commit()
                        st.success("Account created successfully! Please log in above.")
                    except sqlite3.IntegrityError:
                        st.error("Username already exists. Please choose a different ID.")
                    finally:
                        conn.close()
                else:
                    st.warning("Please fill in both fields.")

    st.stop()

# ---------------------------------------------------------
# 5. LOGGED-IN DASHBOARD
# ---------------------------------------------------------
user = st.session_state.username

col_user, col_logout = st.columns([5, 1])
with col_user:
    st.markdown(f"👤 **Active Student ID:** `{user}`")
with col_logout:
    if st.button("Log Out"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.rerun()

st.divider()

# Fetch User Settings
conn = get_db_connection()
c = conn.cursor()
c.execute("SELECT last_period_date, cycle_length, period_duration FROM user_cycles WHERE username = ?", (user,))
cycle_row = c.fetchone()
conn.close()

if cycle_row:
    db_last_date = datetime.datetime.strptime(cycle_row[0], '%Y-%m-%d').date() if isinstance(cycle_row[0], str) else cycle_row[0]
    db_cycle_length = cycle_row[1]
    db_period_duration = cycle_row[2]
else:
    db_last_date = datetime.date.today() - datetime.timedelta(days=12)
    db_cycle_length = 28
    db_period_duration = 5

st.subheader("🌸 1. Cycle Settings & Dynamic Phase Engine")

c1, c2, c3 = st.columns(3)
with c1:
    last_period_date = st.date_input("Start Date of Last Period:", value=db_last_date, key="last_period_in")
with c2:
    cycle_length = st.number_input("Average Cycle Length (Days):", min_value=20, max_value=45, value=int(db_cycle_length), key="cycle_len_in")
with c3:
    period_duration = st.number_input("Period Duration (Days):", min_value=2, max_value=10, value=int(db_period_duration), key="period_dur_in")

# Auto-update database on parameter change
if (last_period_date != db_last_date) or (cycle_length != db_cycle_length) or (period_duration != db_period_duration):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("""
        INSERT INTO user_cycles (username, last_period_date, cycle_length, period_duration)
        VALUES (?, ?, ?, ?)
        ON CONFLICT(username) DO UPDATE SET
            last_period_date=excluded.last_period_date,
            cycle_length=excluded.cycle_length,
            period_duration=excluded.period_duration
    """, (user, last_period_date, cycle_length, period_duration))
    conn.commit()
    conn.close()

# Dynamic Cycle Logic
today = datetime.date.today()
expected_next_period = last_period_date + datetime.timedelta(days=int(cycle_length))
days_overdue = (today - expected_next_period).days

# Determine projected cycle iteration
projected_period = expected_next_period
while projected_period < today:
    projected_period += datetime.timedelta(days=int(cycle_length))

ovulation_day = projected_period - datetime.timedelta(days=14)
fertile_start = ovulation_day - datetime.timedelta(days=5)
fertile_end = ovulation_day + datetime.timedelta(days=1)

# Overdue Guidance Banner
if days_overdue > 0:
    st.markdown(f"""
        <div class="overdue-banner">
            <h3 style="margin:0; color:#f87171;">💙 Do Not Panic: Period Overdue by {days_overdue} Day(s)</h3>
            <p style="margin:8px 0 0 0; color:#f1f5f9; font-size: 0.95rem;">
                Your expected start date was <b>{expected_next_period.strftime('%d %b %Y')}</b>. Menstrual cycles naturally vary due to routine shifts, exam stress, dietary changes, or sleep disruptions.
            </p>
            <hr style="border-color: rgba(255,255,255,0.2); margin: 10px 0;">
            <p style="margin:0; color:#cbd5e1; font-size: 0.88rem;">
                <b>What to do next:</b><br>
                1. 🧘 <b>Manage Stress:</b> High cortisol from exams/prep delays ovulation.<br>
                2. 💧 <b>Hydrate & Rest:</b> Ensure 7-8 hours of sleep and adequate nutrition.<br>
                3. 🩺 <b>Medical Guidance:</b> If your period is delayed by more than 14-21 days or if you experience severe pain, consult a healthcare professional.
            </p>
        </div>
    """, unsafe_allow_html=True)

# Metrics Cards Display
m1, m2, m3, m4 = st.columns(4)
with m1:
    if days_overdue > 0:
        st.markdown(f"""
            <div class="metric-card">
                <h4 style="color: #f87171; margin:0;">Expected Date Was</h4>
                <h2 style="margin:5px 0;">{expected_next_period.strftime('%d %b %Y')}</h2>
                <p style="color:#f87171; margin:0;">({days_overdue} days overdue)</p>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
            <div class="metric-card">
                <h4 style="color: #f472b6; margin:0;">Next Period Starts</h4>
                <h2 style="margin:5px 0;">{expected_next_period.strftime('%d %b %Y')}</h2>
                <p style="color:#94a3b8; margin:0;">({(expected_next_period - today).days} days away)</p>
            </div>
        """, unsafe_allow_html=True)

with m2:
    st.markdown(f"""
        <div class="metric-card">
            <h4 style="color: #fbbf24; margin:0;">Projected Ovulation</h4>
            <h2 style="margin:5px 0;">{ovulation_day.strftime('%d %b %Y')}</h2>
            <p style="color:#94a3b8; margin:0;">Next Projected Cycle</p>
        </div>
    """, unsafe_allow_html=True)

with m3:
    st.markdown(f"""
        <div class="metric-card">
            <h4 style="color: #34d399; margin:0;">Fertile Window</h4>
            <h3 style="margin:5px 0;">{fertile_start.strftime('%d %b')} - {fertile_end.strftime('%d %b')}</h3>
            <p style="color:#94a3b8; margin:0;">Projected Window</p>
        </div>
    """, unsafe_allow_html=True)

with m4:
    days_since_start = (today - last_period_date).days
    st.markdown(f"""
        <div class="metric-card">
            <h4 style="color: #38bdf8; margin:0;">Elapsed Time</h4>
            <h2 style="margin:5px 0;">Day {days_since_start + 1}</h2>
            <p style="color:#94a3b8; margin:0;">Since Last Period</p>
        </div>
    """, unsafe_allow_html=True)

st.divider()

# --- SECTION 2: EXAM RISK MATRIX ---
st.subheader("📚 2. Scheduled Exams & Dynamic Risk Alignment")

col_ex1, col_ex2, col_ex3 = st.columns([2, 2, 1])
with col_ex1:
    new_exam_name = st.text_input("Exam / Test Name:", placeholder="e.g. Physics Final / NEET Mock", key="ex_name_input")
with col_ex2:
    new_exam_date = st.date_input("Exam Date:", value=today + datetime.timedelta(days=15), key="ex_date_input")
with col_ex3:
    st.write(" ")
    st.write(" ")
    if st.button("Save Exam"):
        if new_exam_name.strip():
            conn = get_db_connection()
            c = conn.cursor()
            c.execute("INSERT INTO user_exams (username, exam_name, exam_date) VALUES (?, ?, ?)",
                      (user, new_exam_name.strip(), new_exam_date))
            conn.commit()
            conn.close()
            st.rerun()

conn = get_db_connection()
exams_df = pd.read_sql_query("SELECT id, exam_name, exam_date FROM user_exams WHERE username = ? ORDER BY exam_date ASC", conn, params=(user,))
conn.close()

if not exams_df.empty:
    risk_table_data = []
    for _, ex in exams_df.iterrows():
        ex_date = datetime.datetime.strptime(ex["exam_date"], '%Y-%m-%d').date() if isinstance(ex["exam_date"], str) else ex["exam_date"]
        
        days_diff = (ex_date - last_period_date).days
        cycle_day = (days_diff % int(cycle_length)) + 1
        
        if cycle_day <= int(period_duration):
            status = "🔴 High Risk (Menstrual Phase / Cramps)"
            advice = "Prepare pain management ahead of time, stay hydrated, and do light revision."
        elif cycle_day >= (int(cycle_length) - 5):
            status = "🟡 Moderate Risk (Late Luteal / PMS Fatigue)"
            advice = "Pre-plan sleep schedules and avoid late-night cramming to prevent fatigue."
        else:
            status = "🟢 Optimal State (Follicular / Ovulatory)"
            advice = "High energy and sharp cognitive focus expected on exam day!"

        risk_table_data.append({
            "Exam Name": ex["exam_name"],
            "Exam Date": ex_date.strftime('%d %b %Y'),
            "Calculated Cycle Day": f"Day {cycle_day}",
            "Risk Assessment": status,
            "Actionable Strategy": advice
        })

    st.table(pd.DataFrame(risk_table_data))

    if st.button("Delete All My Exams"):
        conn = get_db_connection()
        c = conn.cursor()
        c.execute("DELETE FROM user_exams WHERE username = ?", (user,))
        conn.commit()
        conn.close()
        st.rerun()

st.divider()

# --- SECTION 3: DAILY SYMPTOM LOGGER ---
st.subheader("📊 3. Persistent Daily Symptom & Energy Log")

col_l1, col_l2 = st.columns(2)
with col_l1:
    log_date = st.date_input("Log Date:", today, key="log_date_input")
    flow = st.select_slider("Flow Intensity:", options=["None", "Spotting", "Light", "Medium", "Heavy"], key="flow_input")
    cramps = st.select_slider("Cramp Severity:", options=["None", "Mild", "Moderate", "Severe"], key="cramps_input")
with col_l2:
    mood = st.selectbox("Mood State:", ["Happy / Focused 😊", "Calm 😌", "Anxious 😟", "Irritable 😠", "Fatigued 😴"], key="mood_input")
    energy = st.slider("Energy Level (1-10):", 1, 10, 7, key="energy_input")
    symptoms = st.multiselect("Symptoms:", ["Headache", "Bloating", "Acne", "Back Pain", "Cravings", "Insomnia"], key="sym_input")

if st.button("Save Daily Log Record"):
    sym_str = ", ".join(symptoms) if symptoms else "None"
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("""
        INSERT INTO user_logs (username, log_date, flow, cramps, mood, energy, symptoms)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (user, log_date, flow, cramps, mood, energy, sym_str))
    conn.commit()
    conn.close()
    st.success("Entry saved permanently to your ID!")
    st.rerun()

conn = get_db_connection()
logs_df = pd.read_sql_query("SELECT log_date, flow, cramps, mood, energy, symptoms FROM user_logs WHERE username = ? ORDER BY log_date ASC", conn, params=(user,))
conn.close()

if not logs_df.empty:
    col_chart, col_df = st.columns([1, 1])
    with col_chart:
        fig = px.line(
            logs_df, x="log_date", y="energy", markers=True,
            title="Your Historical Energy Level Trends",
            labels={"log_date": "Date", "energy": "Energy Level (1-10)"},
            template="plotly_dark"
        )
        st.plotly_chart(fig, use_container_width=True)
    with col_df:
        st.write("**Your Saved Log Records:**")
        st.dataframe(logs_df, use_container_width=True)