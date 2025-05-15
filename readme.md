# 📸 Sign Language Detection with YOLO

Aplikasi Python sederhana untuk mendeteksi bahasa isyarat huruf alfabet menggunakan model YOLO dan menampilkannya di GUI berbasis Tkinter.

## 📦 Fitur

- Deteksi huruf alfabet dari bahasa isyarat secara real-time via webcam.
- Teks hasil deteksi ditampilkan di jendela aplikasi.
- Tombol untuk:
  - Menambah spasi.
  - Menghapus karakter terakhir.
  - Menghapus seluruh teks.
  - Menyimpan hasil ke file `.txt`.

## 🛠️ Teknologi

- Python
- OpenCV
- YOLO (Ultralytics)
- Tkinter

## 📌 Cara Menjalankan

1. **Clone repository**
   ```bash
   git clone https://github.com/username/nama-repo.git
   cd nama-repo

2. **Install library dependencies**
    ```bash
    pip install -r requirements.txt

3. **Pastikan model hasil training berada di:**
    ```bash
    runs/detect/train4/weights/best.pt

4. **Jalankan program**
    ```bash
    python app.py

## 📄 Catatan

Tekan q di jendela kamera untuk keluar.

Webcam harus aktif sebelum aplikasi dijalankan.