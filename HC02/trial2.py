import cv2
import mediapipe as mp
import numpy as np
from scipy.signal import butter, filtfilt, find_peaks
import time

# ---------------- FILTER ----------------
def bandpass_filter(signal, fs=30, low=0.7, high=4):
    nyquist = 0.5 * fs
    low /= nyquist
    high /= nyquist
    b, a = butter(3, [low, high], btype='band')
    return filtfilt(b, a, signal)

# ---------------- INIT ----------------
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(
    static_image_mode=False,
    max_num_faces=1,
    refine_landmarks=True
)

cap = cv2.VideoCapture(0)

signals = {
    "forehead": [],
    "left_cheek": [],
    "right_cheek": []
}

regions = {
    "forehead": [10, 338, 297, 332, 284, 54, 103, 67, 109],
    "left_cheek": [50, 205, 206, 207, 187, 147, 213, 192, 214, 212, 210, 211, 32, 111, 116],
    "right_cheek": [280, 425, 426, 427, 411, 376, 433, 416, 434, 432, 430, 431, 262, 340, 345]
}

colors = {
    "forehead": (0, 0, 255),
    "left_cheek": (255, 0, 0),
    "right_cheek": (0, 255, 0)
}

fs = 30
bpm = 0
hrv = 0

bpm_buffer = []
hrv_buffer = []

# 🔥 frame save control
last_save_time = 0
SAVE_INTERVAL = 0.2  # seconds (5 FPS)

# ---------------- MAIN LOOP ----------------
while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb)

    face_detected = False
    weak_signal_flag = False

    # ---------------- FACE PROCESSING ----------------
    if results.multi_face_landmarks:
        face_detected = True

        for face_landmarks in results.multi_face_landmarks:

            if len(face_landmarks.landmark) < 400:
                continue

            for name, indices in regions.items():
                pts = []

                for idx in indices:
                    lm = face_landmarks.landmark[idx]
                    x, y = int(lm.x * w), int(lm.y * h)
                    pts.append([x, y])

                pts = np.array(pts, dtype=np.int32)
                hull = cv2.convexHull(pts)

                cv2.polylines(frame, [hull], True, colors[name], 2)

                mask = np.zeros(frame.shape[:2], dtype=np.uint8)
                cv2.fillPoly(mask, [hull], 255)

                roi = cv2.bitwise_and(frame, frame, mask=mask)
                pixels = roi[mask == 255]

                if len(pixels) > 0:
                    avg_color = np.mean(pixels, axis=0)
                    signals[name].append(avg_color)

                    if len(signals[name]) > 300:
                        signals[name].pop(0)

    # ---------------- SIGNAL PROCESSING ----------------
    try:
        if face_detected and len(signals["forehead"]) > 150:

            forehead = np.array([x[1] for x in signals["forehead"]])
            left = np.array([x[1] for x in signals["left_cheek"]])
            right = np.array([x[1] for x in signals["right_cheek"]])

            combined = (forehead + left + right) / 3
            combined = combined - np.mean(combined)

            filtered = bandpass_filter(combined)

            signal_strength = np.std(filtered)

            if signal_strength < 0.5:
                weak_signal_flag = True
            else:
                peaks, _ = find_peaks(filtered, distance=fs*0.5)

                if len(peaks) > 1:
                    rr_intervals = np.diff(peaks) / fs

                    avg_rr = np.mean(rr_intervals)
                    new_bpm = 60 / avg_rr

                    diff_rr = np.diff(rr_intervals)
                    rmssd = np.sqrt(np.mean(diff_rr**2))
                    new_hrv = rmssd * 1000

                    if 40 < new_bpm < 180:
                        bpm_buffer.append(new_bpm)
                        hrv_buffer.append(new_hrv)

                        if len(bpm_buffer) > 5:
                            bpm_buffer.pop(0)
                            hrv_buffer.pop(0)

                        bpm = np.mean(bpm_buffer)
                        hrv = np.mean(hrv_buffer)

                        with open("data.txt", "w") as f:
                            f.write(f"{bpm},{hrv}")

    except:
        pass

    # ---------------- STATUS TEXT ----------------
    if not face_detected:
        cv2.putText(frame, "No Face Detected", (30, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    elif weak_signal_flag:
        cv2.putText(frame, "Weak Signal", (30, 90),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)

    # ---------------- DISPLAY ----------------
    cv2.putText(frame, f"BPM: {int(bpm)}", (30, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.putText(frame, f"HRV: {int(hrv)} ms", (30, 120),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 0), 2)

    # ---------------- SAVE FRAME (OPTIMIZED) ----------------
    current_time = time.time()
    if current_time - last_save_time > SAVE_INTERVAL:
        cv2.imwrite("frame.jpg", frame)
        last_save_time = current_time

    cv2.imshow("rPPG Backend", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()