import cv2
import torch
from ultralytics import YOLO
import tkinter as tk
from tkinter import filedialog
import threading
import time

model = YOLO("runs/detect/train4/weights/best.pt")

detected_text = ""
last_detection_time = 0  

def clear_text():
    global detected_text
    detected_text = ""
    text_display.delete("1.0", tk.END)

def save_text():
    global detected_text
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
    if file_path:
        with open(file_path, "w") as f:
            f.write(detected_text)

def add_space():
    global detected_text
    detected_text += " "
    update_text_display()

def delete_last_character():
    global detected_text
    detected_text = detected_text[:-1]
    update_text_display()

def update_text_display():
    text_display.delete("1.0", tk.END)
    text_display.insert(tk.END, detected_text)

root = tk.Tk()
root.title("Sign Language Recognition")
root.geometry("500x300")

label = tk.Label(root, text="Detected Text:", font=("Arial", 14))
label.pack()

text_display = tk.Text(root, height=5, font=("Arial", 14))
text_display.pack()

btn_space = tk.Button(root, text="Space", command=add_space)
btn_space.pack()

btn_delete = tk.Button(root, text="Delete", command=delete_last_character)
btn_delete.pack()

btn_clear = tk.Button(root, text="Clear All", command=clear_text)
btn_clear.pack()

btn_save = tk.Button(root, text="Save to Text File", command=save_text)
btn_save.pack()

btn_quit = tk.Button(root, text="Quit", command=root.quit)
btn_quit.pack()


def run_camera():
    global detected_text, last_detection_time
    cap = cv2.VideoCapture(0)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        results = model(frame, conf=0.5)  


        for result in results:
            for box in result.boxes:
                cls = int(box.cls[0])  
                conf = box.conf[0]  

                if conf > 0.5: 
                    current_time = time.time()
                    if current_time - last_detection_time > 1.5:  
                        detected_text += chr(65 + cls)  
                        update_text_display()
                        last_detection_time = current_time  

        # Tampilkan hasil di layar
        annotated_frame = results[0].plot()
        cv2.imshow("YOLO Real-Time Detection", annotated_frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):  # Tekan 'q' untuk keluar
            break

    cap.release()
    cv2.destroyAllWindows()

camera_thread = threading.Thread(target=run_camera, daemon=True)
camera_thread.start()


root.mainloop()
