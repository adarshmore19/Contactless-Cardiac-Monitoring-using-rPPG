import streamlit as st
import time
from PIL import Image

# ---------------- CONFIG ----------------
st.set_page_config(page_title="Heart Monitor", page_icon="❤️", layout="wide")

# ---------------- STYLE ----------------
st.markdown("""
<style>
.card {
    padding: 25px;
    border-radius: 15px;
    background: #1c1f26;
    text-align: center;
    color: white;
    margin-bottom: 20px;
}
.big {
    font-size: 32px;
    font-weight: bold;
}
.label {
    font-size: 16px;
    color: #aaa;
}
.section {
    margin-top: 20px;
    margin-bottom: 10px;
    font-size: 22px;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# ---------------- TITLE ----------------
st.title("❤️ Smart Heart Monitor")

# ---------------- LAYOUT ----------------
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown('<div class="section">📹 Live Feed</div>', unsafe_allow_html=True)
    video_box = st.empty()

    st.markdown('<div class="section">📊 BPM Trend</div>', unsafe_allow_html=True)
    chart_bpm = st.empty()

    st.markdown('<div class="section">📊 HRV Trend</div>', unsafe_allow_html=True)
    chart_hrv = st.empty()

with col2:
    bpm_box = st.empty()
    hrv_box = st.empty()
    status_box = st.empty()

bpm_data = []
hrv_data = []

# ---------------- LOOP ----------------
for _ in range(1000):
    try:
        with open("data.txt", "r") as f:
            content = f.read().strip()

        if content:
            bpm, hrv = content.split(",")
            bpm = float(bpm)
            hrv = float(hrv)

            bpm_data.append(bpm)
            hrv_data.append(hrv)

            if len(bpm_data) > 50:
                bpm_data.pop(0)
                hrv_data.pop(0)

            # -------- CAMERA --------
            try:
                img = Image.open("frame.jpg")
                video_box.image(img, width="stretch")
            except:
                pass

            # -------- CARDS --------
            bpm_box.markdown(f"""
            <div class="card">
                <div class="label">Heart Rate</div>
                <div class="big">{int(bpm)} BPM ❤️</div>
            </div>
            """, unsafe_allow_html=True)

            hrv_box.markdown(f"""
            <div class="card">
                <div class="label">HRV</div>
                <div class="big">{round(hrv, 2)} ms 🧠</div>
            </div>
            """, unsafe_allow_html=True)

            # -------- STRESS --------
            if hrv < 20:
                status = "😰 High Stress"
            elif hrv < 50:
                status = "😐 Moderate"
            else:
                status = "😌 Relaxed"

            status_box.markdown(f"""
            <div class="card">
                <div class="label">Condition</div>
                <div class="big">{status}</div>
            </div>
            """, unsafe_allow_html=True)

            # -------- CHARTS --------
            chart_bpm.line_chart(bpm_data)
            chart_hrv.line_chart(hrv_data)

    except:
        status_box.markdown("""
        <div class="card">
            <div class="big">⏳ Waiting...</div>
        </div>
        """, unsafe_allow_html=True)

    time.sleep(0.3)