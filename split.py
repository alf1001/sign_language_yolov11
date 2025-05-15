import os
import shutil
import random

# Path direktori utama
base_dir = "All_images"
train_images_dir = os.path.join(base_dir, "train", "images")
train_labels_dir = os.path.join(base_dir, "train", "labels")
valid_dir = os.path.join(base_dir, "valid")
test_dir = os.path.join(base_dir, "test")

# Buat folder valid dan test jika belum ada
os.makedirs(valid_dir, exist_ok=True)
os.makedirs(os.path.join(valid_dir, "images"), exist_ok=True)
os.makedirs(os.path.join(valid_dir, "labels"), exist_ok=True)
os.makedirs(test_dir, exist_ok=True)
os.makedirs(os.path.join(test_dir, "images"), exist_ok=True)
os.makedirs(os.path.join(test_dir, "labels"), exist_ok=True)

# Dapatkan semua file gambar dan label
image_exts = (".jpg", ".jpeg", ".png")  # Sesuaikan dengan format dataset
all_images = [f for f in os.listdir(train_images_dir) if f.endswith(image_exts)]
all_labels = [f for f in os.listdir(train_labels_dir) if f.endswith(".txt")]

# Pastikan file gambar dan label cocok
image_names = set(os.path.splitext(f)[0] for f in all_images)
label_names = set(os.path.splitext(f)[0] for f in all_labels)
common_files = list(image_names & label_names)

# Acak urutan file
random.shuffle(common_files)

# Tentukan rasio split
train_ratio = 0.7
valid_ratio = 0.2
test_ratio = 0.1

train_count = int(len(common_files) * train_ratio)
valid_count = int(len(common_files) * valid_ratio)

train_files = common_files[:train_count]
valid_files = common_files[train_count:train_count + valid_count]
test_files = common_files[train_count + valid_count:]

# Fungsi untuk memindahkan file
def move_files(file_list, dest_images, dest_labels):
    for file in file_list:
        img_path = os.path.join(train_images_dir, file + ".jpg")  # Sesuaikan dengan ekstensi
        label_path = os.path.join(train_labels_dir, file + ".txt")

        if os.path.exists(img_path):
            shutil.move(img_path, os.path.join(dest_images, file + ".jpg"))
        if os.path.exists(label_path):
            shutil.move(label_path, os.path.join(dest_labels, file + ".txt"))

# Pindahkan file ke folder valid dan test
move_files(valid_files, os.path.join(valid_dir, "images"), os.path.join(valid_dir, "labels"))
move_files(test_files, os.path.join(test_dir, "images"), os.path.join(test_dir, "labels"))

print(f"Dataset dibagi: {len(train_files)} train, {len(valid_files)} valid, {len(test_files)} test.")
