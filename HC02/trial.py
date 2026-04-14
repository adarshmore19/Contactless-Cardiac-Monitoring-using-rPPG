import cv2
import mediapipe as mp
import numpy as np

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

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb)

    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:

            for name, indices in regions.items():
                pts = []

                for idx in indices:
                    lm = face_landmarks.landmark[idx]
                    x, y = int(lm.x * w), int(lm.y * h)
                    pts.append([x, y])

                pts = np.array(pts, dtype=np.int32)

                # 🔥 CONVEX HULL MAGIC
                hull = cv2.convexHull(pts)

                # Draw smooth region
                cv2.polylines(frame, [hull], True, colors[name], 2)

                # Create mask
                mask = np.zeros(frame.shape[:2], dtype=np.uint8)
                cv2.fillPoly(mask, [hull], 255)

                roi = cv2.bitwise_and(frame, frame, mask=mask)
                pixels = roi[mask == 255]

                if len(pixels) > 0:
                    avg_color = np.mean(pixels, axis=0)
                    signals[name].append(avg_color)

                    if len(signals[name]) > 300:
                        signals[name].pop(0)

    cv2.imshow("Convex Hull rPPG", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()