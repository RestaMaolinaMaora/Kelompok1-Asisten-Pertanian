import os
import streamlit as st
import pandas as pd
import tensorflow as tf
import numpy as np
from PIL import Image

# Fungsi untuk menambahkan pesan ke riwayat chat
def add_message(sender, message, img=None):
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    st.session_state.chat_history.append({"sender": sender, "message": message, "img": img})
    if len(st.session_state.chat_history) > 50:  # Batasi jumlah pesan yang disimpan
        st.session_state.chat_history.pop(0)

# Fungsi untuk memuat solusi dari file CSV
def load_solutions():
    current_dir = os.path.dirname(__file__)  # Dapatkan direktori saat ini
    file_path = os.path.join(current_dir, '..', 'dataset', 'solutions.csv')  # Menyesuaikan path relatif
    try:
        return pd.read_csv(file_path)
    except FileNotFoundError:
        st.error(f"Gagal memuat file solusi: {file_path} tidak ditemukan.")
        return None

# Fungsi untuk mendapatkan solusi berdasarkan class_name
def get_solution(class_name):
    if solutions_df is not None:
        solution_row = solutions_df[solutions_df['class_name'] == class_name]
        if not solution_row.empty:
            nama_bahasa = solution_row.iloc[0]['nama_bahasa_indonesia']
            solusi = solution_row.iloc[0]['Solusi']
            return f"**Nama**: {nama_bahasa}\n\n**Solusi**: {solusi}"
        else:
            return "Solusi tidak ditemukan untuk class ini."
    return "Dataset solusi tidak tersedia."

# Fungsi untuk memprediksi gambar
def predict_image(img):
    if not model_loaded:
        return "Model belum dimuat, prediksi tidak dapat dilakukan."

    class_labels = list(solutions_df['class_name'])  # Gunakan class_name dari dataset solusi
    try:
        img = img.convert('RGB')  # Ubah gambar ke RGB jika belum
        img_array = np.array(img).astype('float32')  # Ubah menjadi numpy array
        img_array = tf.image.resize(img_array, (224, 224))  # Resize gambar sesuai ukuran input model
        img_array = np.expand_dims(img_array, axis=0) / 255.0  # Normalisasi gambar (0-1)

        predictions = model.predict(img_array)  # Prediksi dengan model
        predicted_class_index = np.argmax(predictions, axis=-1)[0]  # Ambil class dengan prediksi tertinggi
        
        if predicted_class_index < len(class_labels):
            return class_labels[predicted_class_index]  # Kembalikan label class yang diprediksi
        else:
            return "Unknown"  # Jika ada kesalahan dalam indeks
    except Exception as e:
        return f"Gagal memproses gambar: {e}"

# Set page configuration
st.set_page_config(page_title="Hama dan Penyakit", layout="centered", page_icon="🌱")

# Tambahkan CSS untuk balon chat
st.markdown(
    """
    <style>
    .chat-box {
        max-width: 70%;
        padding: 10px;
        margin: 10px;
        border-radius: 10px;
        font-family: Arial, sans-serif;
        font-size: 14px;
        clear: both;
    }
    .chat-user {
        background-color: #DCF8C6;
        color: black;
        text-align: left;
        float: right;
        border-top-right-radius: 0;
    }
    .chat-assistant {
        background-color: #E4E6EB;
        color: black;
        text-align: left;
        float: left;
        border-top-left-radius: 0;
    }
    .chat-container {
        display: flex;
        flex-direction: column;
        max-height: 400px;
        overflow-y: auto;
        padding: 10px;
        border: 1px solid #ccc;
        border-radius: 10px;
        background-color: #f9f9f9;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Load model dan solusi
model_loaded = False
try:
    model = tf.keras.models.load_model('model_hama_plant.keras')
    model_loaded = True
except Exception as e:
    st.error(f"Gagal memuat model: {e}")

solutions_df = load_solutions()
if solutions_df is None:
    st.warning("Dataset solusi tidak tersedia. Pastikan file CSV sudah ada di folder dataset.")

# Membuat header dengan logo dan teks
col1, col2 = st.columns([3, 10])
with col1:
    st.image("asset/logo.png", width=100)
with col2:
    st.markdown(
        """
        <h1 style="font-family: Arial, sans-serif; color: chocolate; text-align: left;">
        Hama dan Penyakit
        </h1>
        """,
        unsafe_allow_html=True,
    )

# Input pesan pengguna
st.write("### Kirim Pesan kepada Assistant")
message = st.text_input("Pesan Anda:", key="message_input", help="Ketik pesan Anda di sini...")

# Upload file gambar
uploaded_file = st.file_uploader("Upload Gambar (Opsional)", type=["png", "jpg", "jpeg"])

# Tombol Kirim
if st.button("Kirim"):
    if message:
        add_message("user", message)

        # Analisis gambar jika ada
        if uploaded_file:
            try:
                image = Image.open(uploaded_file)
                predicted_class = predict_image(image)
                solution = get_solution(predicted_class)
                response = f"Prediksi: {predicted_class}\n\n{solution}"
                add_message("assistant", response, img=image)
            except Exception as e:
                st.error(f"Gagal memuat gambar: {e}")
        else:
            response = "Pesan Anda telah diterima. Silakan unggah gambar untuk analisis lebih lanjut."
            add_message("assistant", response)
    else:
        st.warning("Pesan tidak boleh kosong!")

# Menampilkan riwayat chat
st.markdown('<div class="chat-container">', unsafe_allow_html=True)
if "chat_history" in st.session_state:
    for chat in st.session_state.chat_history:
        if chat["sender"] == "user":
            st.markdown(f'<div class="chat-box chat-user">{chat["message"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="chat-box chat-assistant">{chat["message"]}</div>', unsafe_allow_html=True)
            # Menampilkan gambar jika ada
            if chat["img"]:
                st.image(chat["img"], width=100)
st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown(
    """
    <style>
    .footer {
        position: fixed;
        bottom: 0;
        width: 100%;
        background-color: #f1f1f1;
        text-align: center;
        padding: 10px;
        font-size: 14px;
    }
    </style>
    <div class="footer">
    © 2024 Agriculture Assistant. All rights reserved.
    </div>
    """,
    unsafe_allow_html=True,
)
