import streamlit as st
import cv2
import numpy as np
import datetime
import sqlite3
import pandas as pd
from scipy.signal import find_peaks
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase

# ---------------------------------------------------------
# 1. PAGE CONFIG & CUSTOM CSS
# ---------------------------------------------------------
st.set_page_config(
    page_title="VitalTrack AI | IITM BS",
    page_icon="🌸",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    .stApp { background-color: #0d1117; color: #f0f6fc; }
    .main-header {
        background: linear-gradient(135deg, #4c1d95 0%, #7c3aed 50%, #db2777 100%);
        padding: 20px; border-radius: 16px; color: white; margin-bottom: 20px;
    }
    .badge { background-color: #f59e0b; color: #000; padding: 4px 12px; border-radius: 20px; font-weight: bold; }
    .metric-card { background: rgba(30, 41, 59, 0.7); border: 1px solid rgba(255, 255, 255, 0.1); padding: 16px; border-radius: 12px; text-align: center; }
    </style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 2. SQLITE DATABASE SETUP
# ---------------------------------------------------------
def init_db():
    conn = sqlite3.connect("vitaltrack.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS cycle_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_name TEXT,
            log_date DATE,
            flow_intensity TEXT,
            cramp_intensity TEXT,
            symptoms TEXT,
            water_intake REAL
        )
    """)
    conn.commit()
    conn.close()

def save_log(user_name, log_date, flow, cramps, symptoms_str, water):
    conn = sqlite3.connect("vitaltrack.db")
    c = conn.cursor()
    c.execute("""
        INSERT INTO cycle_logs (user_name, log_date, flow_intensity, cramp_intensity, symptoms, water_intake)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (user_name, log_date, flow, cramps, symptoms_str, water))
    conn.commit()
    conn.close()

def load_logs():
    conn = sqlite3.connect("vitaltrack.db")
    df = pd.read_sql_query("SELECT * FROM cycle_logs ORDER BY log_date DESC", conn)
    conn.close()
    return df

init_db()

# ---------------------------------------------------------
# 3. HEADER & NAVIGATION
# ---------------------------------------------------------
col_logo, col_title = st.columns([1, 6])
with col_logo:
    st.image("https://upload.wikimedia.org/wikipedia/en/6/69/IIT_Madras_Logo.svg", width=100)
with col_title:
    st.markdown("""
        <div class="main-header">
            <h1 style="margin:0; font-size: 2rem;">🌸 VitalTrack AI: Vision, PPG & Cycle Health</h1>
            <p style="margin:5px 0 0 0;">
                Designed & Developed by <span class="badge">Sudhanshu Mishra</span> | <b>IIT Madras BS (Diploma Level)</b>
            </p>
        </div>
    """, unsafe_allow_html=True)

st.sidebar.title("📌 Navigation")
module = st.sidebar.radio("Select Module:", [
    "❤️ Real PPG Optical Heart Rate Monitor",
    "📷 Real OpenCV Face Detection",
    "🌸 Menstrual & Ovulation Predictor",
    "📊 Persistent Health & Symptom Log (SQLite)"
])

# ---------------------------------------------------------
# MODULE 1: REAL PPG OPTICAL HEART RATE MONITOR
# ---------------------------------------------------------
if module == "❤️ Real PPG Optical Heart Rate Monitor":
    st.header("❤️ Real Optical PPG Heart Rate Processing")
    st.write("Place your index finger **lightly over your camera lens** (with flashlight enabled if on mobile). The algorithm processes green channel mean intensity changes frame-by-frame to extract blood pulse peaks.")

    class PPGTransformer(VideoTransformerBase):
        def __init__(self):
            self.green_means = []
            self.bpm = 0.0
            self.fps = 30

        def transform(self, frame):
            img = frame.to_ndarray(format="bgr24")
            
            h, w, _ = img.shape
            roi = img[int(h*0.3):int(h*0.7), int(w*0.3):int(w*0.7)]
            mean_green = np.mean(roi[:, :, 1])
            
            self.green_means.append(mean_green)
            
            if len(self.green_means) > 150:
                self.green_means.pop(0)

            if len(self.green_means) >= 90:
                signal = np.array(self.green_means)
                signal = signal - np.mean(signal)
                
                min_distance = int(self.fps * 60 / 180)
                peaks, _ = find_peaks(signal, distance=min_distance, prominence=0.5)

                if len(peaks) > 1:
                    peak_intervals = np.diff(peaks) / self.fps
                    avg_interval = np.mean(peak_intervals)
                    if avg_interval > 0:
                        calculated_bpm = 60.0 / avg_interval
                        if 40 <= calculated_bpm <= 180:
                            self.bpm = round(calculated_bpm, 1)

            display_text = f"BPM: {self.bpm if self.bpm > 0 else 'Calculating...'}"
            cv2.putText(img, display_text, (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 3)
            
            return img

    webrtc_streamer(
        key="ppg-heartrate",
        video_transformer_factory=PPGTransformer,
        rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]}
    )

    st.info("🔬 **Engineering Mechanism:** Photoplethysmography measures light absorption variations caused by blood volume changes during cardiac cycles. Peak distances ($\Delta t$) determine pulse frequency ($60 / \Delta t$).")

# ---------------------------------------------------------
# MODULE 2: REAL OPENCV FACE DETECTION
# ---------------------------------------------------------
elif module == "📷 Real OpenCV Face Detection":
    st.header("📷 Real-Time OpenCV Face Detection")
    st.write("Click **Start** below to stream your camera feed. OpenCV Haar Cascade runs frame-by-frame face localization.")

    class FaceTransformer(VideoTransformerBase):
        def __init__(self):
            self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

        def transform(self, frame):
            img = frame.to_ndarray(format="bgr24")
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
                cv2.putText(img, "Face Detected", (x, y - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

            return img

    webrtc_streamer(
        key="face-detection",
        video_transformer_factory=FaceTransformer,
        rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]}
    )

# ---------------------------------------------------------
# MODULE 3: MENSTRUAL & OVULATION PREDICTOR
# ---------------------------------------------------------
elif module == "🌸 Menstrual & Ovulation Predictor":
    st.header("🌸 Algorithmic Cycle & Ovulation Predictor")

    c1, c2, c3 = st.columns(3)
    with c1:
        last_period = st.date_input("Start Date of Last Period:", datetime.date.today() - datetime.timedelta(days=14))
    with c2:
        cycle_length = st.number_input("Average Cycle Length (Days):", min_value=20, max_value=45, value=28)
    with c3:
        period_duration = st.number_input("Period Duration (Days):", min_value=2, max_value=10, value=5)

    next_period = last_period + datetime.timedelta(days=cycle_length)
    ovulation_day = next_period - datetime.timedelta(days=14)
    fertile_start = ovulation_day - datetime.timedelta(days=5)
    fertile_end = ovulation_day + datetime.timedelta(days=1)

    st.markdown("---")
    m1, m2, m3 = st.columns(3)
    with m1:
        st.markdown(f"""
            <div class="metric-card">
                <h4 style="color: #f472b6; margin:0;">Next Period Starts</h4>
                <h2 style="margin:5px 0;">{next_period.strftime('%d %b %Y')}</h2>
                <p style="color:#94a3b8; margin:0;">({(next_period - datetime.date.today()).days} days remaining)</p>
            </div>
        """, unsafe_allow_html=True)
    with m2:
        st.markdown(f"""
            <div class="metric-card">
                <h4 style="color: #fbbf24; margin:0;">Estimated Ovulation Day</h4>
                <h2 style="margin:5px 0;">{ovulation_day.strftime('%d %b %Y')}</h2>
                <p style="color:#94a3b8; margin:0;">Peak Conception Date</p>
            </div>
        """, unsafe_allow_html=True)
    with m3:
        st.markdown(f"""
            <div class="metric-card">
                <h4 style="color: #34d399; margin:0;">Fertile Window</h4>
                <h3 style="margin:5px 0;">{fertile_start.strftime('%d %b')} - {fertile_end.strftime('%d %b')}</h3>
                <p style="color:#94a3b8; margin:0;">6-Day High-Fertility Range</p>
            </div>
        """, unsafe_allow_html=True)

# ---------------------------------------------------------
# MODULE 4: PERSISTENT SQLITE SYMPTOM LOG
# ---------------------------------------------------------
elif module == "📊 Persistent Health & Symptom Log (SQLite)":
    st.header("📊 Persistent Cycle & Symptom Logger (SQLite Database)")

    with st.form("symptom_form", clear_on_submit=True):
        user_name = st.text_input("User ID / Name:", value="User_1")
        log_date = st.date_input("Date:", datetime.date.today())
        flow = st.select_slider("Flow Intensity:", options=["None", "Spotting", "Light", "Medium", "Heavy"])
        cramps = st.select_slider("Cramp Intensity:", options=["None", "Mild", "Moderate", "Severe"])
        symptoms = st.multiselect("Logged Symptoms:", ["Headache", "Bloating", "Acne", "Mood Swings", "Fatigue", "Cravings"])
        water_intake = st.slider("Water Intake (Liters):", 0.0, 5.0, 2.0, 0.5)

        submitted = st.form_submit_button("Save Log Entry to SQLite")

        if submitted:
            symptoms_str = ", ".join(symptoms) if symptoms else "None"
            save_log(user_name, log_date, flow, cramps, symptoms_str, water_intake)
            st.success("Record permanently saved to SQLite database `vitaltrack.db`!")

    st.markdown("---")
    st.subheader("📁 Saved Log Records (Persisted Across Reloads)")
    
    logs_df = load_logs()
    if not logs_df.empty:
        st.dataframe(logs_df, use_container_width=True)
    else:
        st.info("No saved logs in the SQLite database yet. Fill out the form above to add an entry.")