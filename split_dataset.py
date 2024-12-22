import os
import shutil
import random

# Tentukan direktori dataset
source_dir = 'dataset/plantvilage'
train_dir = 'dataset/train'
val_dir = 'dataset/validation'
test_dir = 'dataset/test'

# Persiapkan folder tujuan jika belum ada
for folder in [train_dir, val_dir, test_dir]:
    if not os.path.exists(folder):
        os.makedirs(folder)

# Fungsi untuk menghitung jumlah gambar dalam folder
def count_images_in_dir(directory):
    count = 0
    for class_name in os.listdir(directory):
        class_path = os.path.join(directory, class_name)
        if os.path.isdir(class_path):
            count += len([img for img in os.listdir(class_path) if img.lower().endswith(('.jpg', '.png', '.jpeg'))])
    return count

# Fungsi untuk membagi dataset
def split_dataset(source_dir, train_dir, val_dir, test_dir, train_ratio=0.8, val_ratio=0.1, test_ratio=0.1):
    # Loop untuk setiap kelas (subfolder) dalam dataset
    for class_name in os.listdir(source_dir):
        class_path = os.path.join(source_dir, class_name)
        
        # Memastikan folder ada dan memiliki gambar
        if os.path.isdir(class_path):
            print(f"Memeriksa folder: {repr(class_name)}")
            # Membuat folder untuk setiap kelas (subkategori) di dalam train, validation, dan test
            os.makedirs(os.path.join(train_dir, class_name), exist_ok=True)
            os.makedirs(os.path.join(val_dir, class_name), exist_ok=True)
            os.makedirs(os.path.join(test_dir, class_name), exist_ok=True)

            # Ambil semua gambar dalam kelas ini
            images = [img for img in os.listdir(class_path) if img.lower().endswith(('.jpg', '.png', '.jpeg'))]
            
            # Cek apakah ada gambar dalam folder ini
            if not images:
                print(f"Tidak ada gambar di folder: {repr(class_name)}")
                continue  # Jika tidak ada gambar, lanjutkan ke kelas berikutnya

            # Shuffle gambar agar pembagian acak
            random.shuffle(images)

            # Tentukan jumlah gambar untuk training, validation, dan testing
            train_size = int(train_ratio * len(images))
            val_size = int(val_ratio * len(images))
            test_size = len(images) - train_size - val_size  # Sisanya untuk test

            # Pindahkan gambar ke folder tujuan
            for i, img in enumerate(images):
                img_path = os.path.join(class_path, img)

                if i < train_size:
                    shutil.copy(img_path, os.path.join(train_dir, class_name, img))
                elif i < train_size + val_size:
                    shutil.copy(img_path, os.path.join(val_dir, class_name, img))
                else:
                    shutil.copy(img_path, os.path.join(test_dir, class_name, img))

# Panggil fungsi untuk membagi dataset
split_dataset(source_dir, train_dir, val_dir, test_dir)

# Output jumlah gambar di masing-masing folder
print(f"Jumlah gambar di folder train: {count_images_in_dir(train_dir)}")
print(f"Jumlah gambar di folder validation: {count_images_in_dir(val_dir)}")
print(f"Jumlah gambar di folder test: {count_images_in_dir(test_dir)}")

print("Pembagian dataset selesai!")
