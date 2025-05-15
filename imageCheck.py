import os

valid_images_dir = "All_images/valid/images"
valid_labels_dir = "All_images/valid/labels"
test_images_dir = "All_images/test/images"
test_labels_dir = "All_images/test/labels"

# Ambil nama file tanpa ekstensi
valid_images = {os.path.splitext(f)[0] for f in os.listdir(valid_images_dir)}
valid_labels = {os.path.splitext(f)[0] for f in os.listdir(valid_labels_dir)}
test_images = {os.path.splitext(f)[0] for f in os.listdir(test_images_dir)}
test_labels = {os.path.splitext(f)[0] for f in os.listdir(test_labels_dir)}

# Cek gambar tanpa label dan sebaliknya
valid_no_label = valid_images - valid_labels
valid_no_image = valid_labels - valid_images
test_no_label = test_images - test_labels
test_no_image = test_labels - test_images

# Tampilkan hasil
print(f"Valid - Gambar tanpa label: {valid_no_label}")
print(f"Valid - Label tanpa gambar: {valid_no_image}")
print(f"Test - Gambar tanpa label: {test_no_label}")
print(f"Test - Label tanpa gambar: {test_no_image}")
