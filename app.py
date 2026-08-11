import streamlit as st
import datetime
import sqlite3
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# ---------------------------------------------------------
# 1. PAGE CONFIGURATION & CUSTOM DARK GLASSMORPHISM CSS
# ---------------------------------------------------------
st.set_page_config(
    page_title="VitalTrack AI | IITM BS",
    page_icon="🌸",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    .stApp {
        background-color: #090d16;
        color: #f8fafc;
    }
    .main-header {
        background: linear-gradient(135deg, #1e1b4b 0%, #312e81 50%, #831843 100%);
        padding: 22px;
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
        margin: 10px 0;
    }
    </style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 2. PERSISTENT SQLITE DATABASE ENGINE
# ---------------------------------------------------------
def get_db_connection():
    conn = sqlite3.connect("vitaltrack.db")
    return conn

def init_db():
    conn = get_db_connection()
    c = conn.cursor()
    # Cycle history table
    c.execute("""
        CREATE TABLE IF NOT EXISTS cycles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_name TEXT,
            start_date DATE,
            cycle_length_days INTEGER,
            period_duration_days INTEGER
        )
    """)
    # Daily symptom log table
    c.execute("""
        CREATE TABLE IF NOT EXISTS symptom_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_name TEXT,
            log_date DATE,
            flow TEXT,
            cramps TEXT,
            mood TEXT,
            energy_level INTEGER,
            symptoms TEXT
        )
    """)
    # Student exams table
    c.execute("""
        CREATE TABLE IF NOT EXISTS exams (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_name TEXT,
            exam_name TEXT,
            exam_date DATE
        )
    """)
    conn.commit()
    conn.close()

init_db()

# ---------------------------------------------------------
# 3. BRANDED HEADER & SIDEBAR NAVIGATION
# ---------------------------------------------------------
col_logo, col_title = st.columns([1, 6])
with col_logo:
    st.image("https://upload.wikimedia.org/wikipedia/en/6/69/IIT_Madras_Logo.svg", width=100)
with col_title:
    st.markdown("""
        <div class="main-header">
            <h1 style="margin:0; font-size: 2.1rem; color: #ffffff;">🌸 VitalTrack AI: Cycle Intelligence & Exam Planner</h1>
            <p style="margin:5px 0 0 0; color: #cbd5e1;">
                Designed & Developed by <span class="badge">Sudhanshu Mishra</span> | <b>IIT Madras BS (Diploma Level)</b>
            </p>
        </div>
    """, unsafe_allow_html=True)

st.sidebar.title("📌 Menu")
module = st.sidebar.radio("Select Module:", [
    "🌸 Statistical Cycle & Phase Engine",
    "📚 Student Exam Risk & Fatigue Planner",
    "📊 Daily Symptom Logger & Analytics",
    "📁 SQLite Database Records"
])

st.sidebar.divider()
st.sidebar.caption("🔒 All medical data is persisted locally in `vitaltrack.db`.")

# ---------------------------------------------------------
# MODULE 1: STATISTICAL CYCLE & PHASE ENGINE
# ---------------------------------------------------------
if module == "🌸 Statistical Cycle & Phase Engine":
    st.header("🌸 Algorithmic Cycle Prediction & Phase Analytics")

    conn = get_db_connection()
    cycles_df = pd.read_sql_query("SELECT * FROM cycles ORDER BY start_date DESC", conn)
    conn.close()

    c1, c2, c3 = st.columns(3)
    with c1:
        input_start = st.date_input("Last Period Start Date:", datetime.date.today() - datetime.timedelta(days=12))
    with c2:
        input_length = st.number_input("Average Cycle Length (Days):", min_value=20, max_value=45, value=28)
    with c3:
        input_duration = st.number_input("Period Duration (Days):", min_value=2, max_value=10, value=5)

    if st.button("Save New Cycle Record to Database"):
        conn = get_db_connection()
        c = conn.cursor()
        c.execute("INSERT INTO cycles (user_name, start_date, cycle_length_days, period_duration_days) VALUES (?, ?, ?, ?)",
                  ("User_1", input_start, input_length, input_duration))
        conn.commit()
        conn.close()
        st.success("Cycle entry permanently saved!")
        st.rerun()

    # Calculate predictions
    today = datetime.date.today()
    days_since_start = (today - input_start).days
    next_period = input_start + datetime.timedelta(days=int(input_length))
    ovulation_day = next_period - datetime.timedelta(days=14)
    fertile_start = ovulation_day - datetime.timedelta(days=5)
    fertile_end = ovulation_day + datetime.timedelta(days=1)

    # Phase calculation
    if days_since_start < input_duration:
        current_phase = "Menstrual Phase 🩸"
        phase_desc = "Estrogen and progesterone are low. Focus on rest, gentle hydration, and iron-rich foods."
    elif today < ovulation_day - datetime.timedelta(days=2):
        current_phase = "Follicular Phase 🌿"
        phase_desc = "Estrogen is rising. High energy, sharp cognitive focus, and strong physical strength."
    elif today <= fertile_end:
        current_phase = "Ovulatory Phase ⚡"
        phase_desc = "LH surge occurs. Peak energy, highest fertility window, and heightened stamina."
    else:
        current_phase = "Luteal Phase 🌙"
        phase_desc = "Progesterone rises then drops. Energy may taper; mild PMS, cravings, or fatigue can occur."

    st.markdown("---")
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown(f"""
            <div class="metric-card">
                <h4 style="color: #f472b6; margin:0;">Next Period</h4>
                <h2 style="margin:5px 0;">{next_period.strftime('%d %b %Y')}</h2>
                <p style="color:#94a3b8; margin:0;">({(next_period - today).days} days away)</p>
            </div>
        """, unsafe_allow_html=True)
    with m2:
        st.markdown(f"""
            <div class="metric-card">
                <h4 style="color: #fbbf24; margin:0;">Estimated Ovulation</h4>
                <h2 style="margin:5px 0;">{ovulation_day.strftime('%d %b %Y')}</h2>
                <p style="color:#94a3b8; margin:0;">Peak Fertility Date</p>
            </div>
        """, unsafe_allow_html=True)
    with m3:
        st.markdown(f"""
            <div class="metric-card">
                <h4 style="color: #34d399; margin:0;">Fertile Window</h4>
                <h3 style="margin:5px 0;">{fertile_start.strftime('%d %b')} - {fertile_end.strftime('%d %b')}</h3>
                <p style="color:#94a3b8; margin:0;">6-Day Conception Window</p>
            </div>
        """, unsafe_allow_html=True)
    with m4:
        st.markdown(f"""
            <div class="metric-card">
                <h4 style="color: #38bdf8; margin:0;">Current Phase</h4>
                <h2 style="margin:5px 0;">{current_phase.split()[0]}</h2>
                <p style="color:#94a3b8; margin:0;">{days_since_start} Days Elapsed</p>
            </div>
        """, unsafe_allow_html=True)

    st.markdown(f"""
        <div class="phase-card">
            <h3 style="margin:0; color:#ec4899;">Active Phase: {current_phase}</h3>
            <p style="margin:5px 0 0 0; color:#cbd5e1;">{phase_desc}</p>
        </div>
    """, unsafe_allow_html=True)

    # Statistical variance & regularity calculation
    if not cycles_df.empty and len(cycles_df) >= 2:
        lengths = cycles_df['cycle_length_days'].values
        std_dev = np.std(lengths)
        mean_len = np.mean(lengths)
        
        st.markdown("---")
        st.subheader("📈 Statistical Cycle Regularity Metrics")
        
        c_stat1, c_stat2 = st.columns(2)
        with c_stat1:
            st.metric(label="Historical Mean Cycle Length", value=f"{mean_len:.1f} Days")
            st.metric(label="Cycle Length Standard Deviation (σ)", value=f"± {std_dev:.1f} Days")
        with c_stat2:
            if std_dev <= 2.5:
                st.success("🟢 **High Regularity Score**: Cycle variance is within standard physiological limits.")
            elif std_dev <= 4.5:
                st.warning("🟡 **Moderate Variance**: Minor fluctuations observed across logged cycles.")
            else:
                st.error("🔴 **High Irregularity Detected**: High standard deviation detected. Consider sharing logs with a gynecologist.")

# ---------------------------------------------------------
# MODULE 2: STUDENT EXAM RISK & FATIGUE PLANNER
# ---------------------------------------------------------
elif module == "📚 Student Exam Risk & Fatigue Planner":
    st.header("📚 Student Exam Schedule & Cycle Alignment Planner")
    st.write("Add your upcoming exams or major tests to analyze whether test dates align with predicted period cramp/fatigue days.")

    with st.form("exam_form"):
        col_e1, col_e2 = st.columns(2)
        with col_e1:
            e_name = st.text_input("Exam / Test Name:", placeholder="e.g. NEET Mock Exam / College Finals")
        with col_e2:
            e_date = st.date_input("Exam Date:", datetime.date.today() + datetime.timedelta(days=10))
        
        e_submit = st.form_submit_button("Save Exam to Schedule")
        if e_submit and e_name.strip():
            conn = get_db_connection()
            c = conn.cursor()
            c.execute("INSERT INTO exams (user_name, exam_name, exam_date) VALUES (?, ?, ?)",
                      ("User_1", e_name, e_date))
            conn.commit()
            conn.close()
            st.success(f"Saved {e_name} on {e_date.strftime('%d %b %Y')}!")
            st.rerun()

    # Load stored exams and evaluate risk
    conn = get_db_connection()
    exams_df = pd.read_sql_query("SELECT * FROM exams ORDER BY exam_date ASC", conn)
    cycles_df = pd.read_sql_query("SELECT * FROM cycles ORDER BY start_date DESC", conn)
    conn.close()

    if not exams_df.empty:
        st.markdown("---")
        st.subheader("🔍 Scheduled Exam Alignment & Fatigue Risk Matrix")

        # Use latest cycle or default 28-day estimation
        base_start = datetime.datetime.strptime(cycles_df.iloc[0]['start_date'], '%Y-%m-%d').date() if not cycles_df.empty else datetime.date.today() - datetime.timedelta(days=12)
        c_len = int(cycles_df.iloc[0]['cycle_length_days']) if not cycles_df.empty else 28
        p_dur = int(cycles_df.iloc[0]['period_duration_days']) if not cycles_df.empty else 5

        risk_data = []
        for _, row in exams_df.iterrows():
            ex_d = datetime.datetime.strptime(row['exam_date'], '%Y-%m-%d').date()
            
            # Find cycle iteration relative to exam
            days_diff = (ex_d - base_start).days
            cycle_day = (days_diff % c_len) + 1
            
            if cycle_day <= p_dur:
                status = "🔴 High Risk (Menstrual Phase / Cramps)"
                advice = "Plan pain-management strategies, stay hydrated, and arrange light revision ahead of exam day."
            elif cycle_day >= (c_len - 5):
                status = "🟡 Moderate Risk (Late Luteal / PMS Fatigue)"
                advice = "Pre-plan sleep schedules and avoid late-night cramming to combat pre-period fatigue."
            else:
                status = "🟢 Optimal Cognitive State (Follicular / Ovulatory)"
                advice = "High energy and peak cognitive focus expected on exam day!"

            risk_data.append({
                "Exam Name": row['exam_name'],
                "Exam Date": ex_d.strftime('%d %b %Y'),
                "Predicted Cycle Day": f"Day {cycle_day}",
                "Status": status,
                "Actionable Guidance": advice
            })

        st.table(pd.DataFrame(risk_data))

# ---------------------------------------------------------
# MODULE 3: DAILY SYMPTOM LOGGER & ANALYTICS
# ---------------------------------------------------------
elif module == "📊 Daily Symptom Logger & Analytics":
    st.header("📊 Daily Symptoms & Energy Logger")

    with st.form("log_form", clear_on_submit=True):
        col_l1, col_l2 = st.columns(2)
        with col_l1:
            l_date = st.date_input("Date:", datetime.date.today())
            l_flow = st.select_slider("Flow Intensity:", options=["None", "Spotting", "Light", "Medium", "Heavy"])
            l_cramps = st.select_slider("Cramp Severity:", options=["None", "Mild", "Moderate", "Severe"])
        with col_l2:
            l_mood = st.selectbox("Mood State:", ["Happy / Focused 😊", "Calm 😌", "Anxious 😟", "Irritable 😠", "Fatigued 😴"])
            l_energy = st.slider("Energy Level (1-10):", 1, 10, 7)
            l_symptoms = st.multiselect("Symptoms:", ["Headache", "Bloating", "Acne", "Back Pain", "Cravings", "Insomnia"])

        l_submit = st.form_submit_button("Save Log Entry to Database")
        if l_submit:
            sym_str = ", ".join(l_symptoms) if l_symptoms else "None"
            conn = get_db_connection()
            c = conn.cursor()
            c.execute("INSERT INTO symptom_logs (user_name, log_date, flow, cramps, mood, energy_level, symptoms) VALUES (?, ?, ?, ?, ?, ?, ?)",
                      ("User_1", l_date, l_flow, l_cramps, l_mood, l_energy, sym_str))
            conn.commit()
            conn.close()
            st.success("Log entry saved to SQLite database!")

    # Analytics Visualization
    conn = get_db_connection()
    logs_df = pd.read_sql_query("SELECT * FROM symptom_logs ORDER BY log_date ASC", conn)
    conn.close()

    if not logs_df.empty:
        st.markdown("---")
        st.subheader("📈 Energy & Symptom Trends Over Time")

        fig = px.line(logs_df, x="log_date", y="energy_level", markers=True,
                      title="Energy Level Trends across Recorded Days",
                      labels={"log_date": "Date", "energy_level": "Energy Level (1-10)"},
                      template="plotly_dark")
        st.plotly_chart(fig, use_container_width=True)

# ---------------------------------------------------------
# MODULE 4: SQLITE DATABASE RECORDS
# ---------------------------------------------------------
elif module == "📁 SQLite Database Records":
    st.header("📁 Saved Database Records (`vitaltrack.db`)")
    st.write("Direct view of stored SQLite data tables.")

    conn = get_db_connection()
    
    st.subheader("1. Cycle History Table")
    cycles_df = pd.read_sql_query("SELECT * FROM cycles", conn)
    if not cycles_df.empty:
        st.dataframe(cycles_df, use_container_width=True)
    else:
        st.info("No cycle records saved yet.")

    st.subheader("2. Scheduled Exams Table")
    exams_df = pd.read_sql_query("SELECT * FROM exams", conn)
    if not exams_df.empty:
        st.dataframe(exams_df, use_container_width=True)
    else:
        st.info("No exam records saved yet.")

    st.subheader("3. Daily Symptom Logs Table")
    sym_df = pd.read_sql_query("SELECT * FROM symptom_logs", conn)
    if not sym_df.empty:
        st.dataframe(sym_df, use_container_width=True)
    else:
        st.info("No daily symptom entries saved yet.")

    conn.close()