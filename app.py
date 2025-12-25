import streamlit as st
import time
from ultralytics import YOLO
from PIL import Image
import numpy as np

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

# =========================
#   PAGE UI
# =========================
st.title("🤟 Sign Language Recognition - Streamlit")
st.write("Sign Language Detection using YOLO (Image Upload Mode)")

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

# =========================
#   IMAGE UPLOAD
# =========================
st.subheader("🖼 Upload Image")
uploaded_file = st.file_uploader(
    "Upload image containing hand sign",
    type=["jpg", "png"]
)

if uploaded_file:
    img = Image.open(uploaded_file).convert("RGB")
    img_array = np.array(img)

    results = model(img_array, conf=0.5)

    now = time.time()
    for box in results[0].boxes:
        cls = int(box.cls[0])
        conf = float(box.conf[0])

        if conf > 0.5 and now - st.session_state.last_detection_time > 1.5:
            st.session_state.detected_text += chr(65 + cls)
            st.session_state.last_detection_time = now

    annotated = results[0].plot()
    st.image(annotated, caption="Detection Result", use_column_width=True)
