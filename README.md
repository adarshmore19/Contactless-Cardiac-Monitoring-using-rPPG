# 💓 Contactless Cardiac Monitoring using rPPG

A real-time heart monitoring system that estimates **Heart Rate (BPM)** and **Heart Rate Variability (HRV)** using just a webcam — no physical sensors required.

---

## 🚀 Overview

This project uses **remote photoplethysmography (rPPG)** to detect subtle color changes in the face caused by blood flow. By processing these signals, the system calculates heart rate and stress-related metrics in real time.

---

## 🎯 Features

* 🎥 Real-time webcam-based monitoring
* 🧠 HRV (Heart Rate Variability) calculation
* ❤️ BPM (Heart Rate) estimation
* 📊 Live charts using Streamlit
* 🧩 Multi-region face tracking (forehead + cheeks)
* ⚡ Signal filtering and peak detection
* ⚠️ Weak signal & no-face detection

---

## 🛠️ Tech Stack

* **Python**
* **OpenCV** – Video processing
* **MediaPipe** – Face landmark detection
* **NumPy** – Numerical operations
* **SciPy** – Signal filtering & peak detection
* **Streamlit** – Web UI

---

## 🧪 How It Works

1. 📷 Capture video from webcam
2. 🧍 Detect face using MediaPipe Face Mesh
3. 📍 Extract Regions of Interest (ROI):

   * Forehead
   * Left Cheek
   * Right Cheek
4. 🎨 Extract green channel signal from skin
5. 🧹 Apply bandpass filtering (removes noise)
6. 📈 Detect peaks (heartbeats)
7. ❤️ Calculate BPM
8. 🧠 Compute HRV (stress indicator)
9. 🌐 Display results on UI

---

## ▶️ Usage

### Run Backend

```bash
python trial2.py
```

### Run UI

```bash
streamlit run app.py
```

---

## 📊 Output

* **BPM (Heart Rate)**
* **HRV (Heart Rate Variability)**
* **Live Graphs**
* **Webcam Feed with ROI detection**

---

## ⚠️ Limitations

* Sensitive to lighting conditions
* Requires stable face positioning
* Accuracy may vary across users
* Not a medical-grade system

---

## 🔮 Future Improvements

* 📱 Mobile application support
* 🤖 AI-based stress detection
* ☁️ Cloud deployment
* 🏥 Clinical validation

---

## 👨‍💻 Contributors

* Adarsh More
* Anamika Sahu
* Anuj Auti

---

## 📜 License

This project is for educational purposes only.

---

## 💡 Inspiration

Exploring how **computer vision + signal processing** can enable **non-contact health monitoring systems**.

---

> Built with curiosity, caffeine, questionable decision and sleep schedules ☕
