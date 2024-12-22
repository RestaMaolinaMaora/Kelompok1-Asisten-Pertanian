import os
import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.preprocessing.image import ImageDataGenerator

# Fungsi untuk menghitung jumlah gambar dalam sebuah direktori
def count_images_in_directory(directory):
    num_images = 0
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(('.jpg', '.jpeg', '.png')):  # Memperpendek kondisi
                num_images += 1
    return num_images

# Fungsi untuk menghitung jumlah kelas dalam sebuah direktori
def count_classes_in_directory(directory):
    num_classes = len([d for d in os.listdir(directory) if os.path.isdir(os.path.join(directory, d))])
    return num_classes

def train_model(train_dir, validation_dir, epochs=5, batch_size=32):
    # Hitung jumlah gambar dan kelas di dataset
    train_images = count_images_in_directory(train_dir)
    validation_images = count_images_in_directory(validation_dir)
    train_classes = count_classes_in_directory(train_dir)
    validation_classes = count_classes_in_directory(validation_dir)
    
    # Menampilkan jumlah gambar dan kelas
    print(f"Jumlah gambar di folder train: {train_images}")
    print(f"Jumlah gambar di folder validation: {validation_images}")
    print(f"Jumlah kelas di folder train: {train_classes}")
    print(f"Jumlah kelas di folder validation: {validation_classes}")
    
    # Data augmentation untuk pelatihan
    train_datagen = ImageDataGenerator(
        rescale=1./255,
        rotation_range=40,
        width_shift_range=0.2,
        height_shift_range=0.2,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True,
        fill_mode='nearest'
    )

    val_datagen = ImageDataGenerator(rescale=1./255)

    # Membaca data dari folder
    train_generator = train_datagen.flow_from_directory(
        train_dir,
        target_size=(224, 224),  # Ukuran gambar yang diinginkan
        batch_size=batch_size,
        class_mode='categorical'  # Untuk klasifikasi multi-kelas
    )

    validation_generator = val_datagen.flow_from_directory(
        validation_dir,
        target_size=(224, 224),
        batch_size=batch_size,
        class_mode='categorical'
    )

    # **Membangun Model CNN**
    model = models.Sequential([
        layers.Conv2D(32, (3, 3), activation='relu', input_shape=(224, 224, 3)),
        layers.MaxPooling2D((2, 2)),
        layers.Conv2D(64, (3, 3), activation='relu'),
        layers.MaxPooling2D((2, 2)),
        layers.Conv2D(128, (3, 3), activation='relu'),
        layers.MaxPooling2D((2, 2)),
        layers.Flatten(),
        layers.Dense(128, activation='relu'),
        layers.Dropout(0.5),  # Mencegah overfitting
        layers.Dense(train_classes, activation='softmax')  # Output layer
    ])

    # Kompilasi Model
    model.compile(optimizer='adam',
                  loss='categorical_crossentropy',
                  metrics=['accuracy'])

    # Melatih Model
    history = model.fit(
        train_generator,
        steps_per_epoch=train_generator.samples // train_generator.batch_size,
        epochs=epochs,
        validation_data=validation_generator,
        validation_steps=validation_generator.samples // validation_generator.batch_size
    )

    # Menyimpan Model
    model.save('model_hama_plant.keras')  # Menyimpan model ke file .keras

    # Menampilkan pesan sukses
    print("Model telah dilatih ulang dan disimpan.")

    return model, history

if __name__ == "__main__":
    # Definisi folder dataset
    train_dir = 'dataset/train'
    validation_dir = 'dataset/validation'

    # Menentukan jumlah epoch dan batch size
    epochs = 10  # Anda bisa mengubah sesuai kebutuhan
    batch_size = 16

    # Menghapus model lama jika ada
    model_path = 'model_hama_plant.keras'
    if os.path.exists(model_path):
        os.remove(model_path)
        print("Model lama telah dihapus.")

    # Menjalankan pelatihan ulang model
    model, history = train_model(train_dir, validation_dir, epochs=epochs, batch_size=batch_size)
    print("Pelatihan selesai.")
