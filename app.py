import streamlit as st
import cv2
import time
from ultralytics import YOLO

# =========================
#   LOAD MODEL
# =========================
model = YOLO("runs/detect/train4/weights/best.pt")

# =========================
#   SESSION STATE
# =========================
if "detected_text" not in st.session_state:
    st.session_state.detected_text = ""

if "last_detection_time" not in st.session_state:
    st.session_state.last_detection_time = 0

if "camera_running" not in st.session_state:
    st.session_state.camera_running = False


# =========================
#   PAGE UI
# =========================
st.title("🤟 Sign Language Recognition - Streamlit")

st.write("Real-time Sign Language Detection using YOLO")


# ---------- TEXT AREA ----------
st.subheader("📌 Detected Text")
st.write(st.session_state.detected_text)


# ---------- BUTTONS ----------
col1, col2, col3, col4, col5 = st.columns(5)

if col1.button("Space"):
    st.session_state.detected_text += " "

if col2.button("Delete"):
    st.session_state.detected_text = st.session_state.detected_text[:-1]

if col3.button("Clear All"):
    st.session_state.detected_text = ""

if col4.button("Save to TXT"):
    with open("detected_text.txt", "w") as f:
        f.write(st.session_state.detected_text)
    st.success("Saved as detected_text.txt 👍")

col5.download_button(
    label="Download TXT",
    data=st.session_state.detected_text,
    file_name="detected_text.txt",
    mime="text/plain"
)


# ---------- CAMERA CONTROLS ----------
st.subheader("🎥 Camera")

start = st.button("Start Camera")
stop = st.button("Stop Camera")


if start:
    st.session_state.camera_running = True

if stop:
    st.session_state.camera_running = False


FRAME_WINDOW = st.image([])

# =========================
#   CAMERA LOOP
# =========================
if st.session_state.camera_running:

    cap = cv2.VideoCapture(0)

    while st.session_state.camera_running:

        ret, frame = cap.read()
        if not ret:
            st.write("Camera Not Detected")
            break

        results = model(frame, conf=0.5)

        for result in results:
            for box in result.boxes:
                cls = int(box.cls[0])
                conf = float(box.conf[0])

                # Only accept confident detections
                if conf > 0.5:
                    now = time.time()

                    # Anti-spam timing
                    if now - st.session_state.last_detection_time > 1.5:
                        st.session_state.detected_text += chr(65 + cls)
                        st.session_state.last_detection_time = now

        annotated = results[0].plot()
        annotated = cv2.cvtColor(annotated, cv2.COLOR_BGR2RGB)

        FRAME_WINDOW.image(annotated)

    cap.release()
