import streamlit as st
import os
import pandas as pd

# Fungsi untuk menambahkan pesan ke riwayat chat
def add_message(sender, message):
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    st.session_state.chat_history.append({"sender": sender, "message": message})

# Fungsi untuk merekomendasikan tanaman berdasarkan kondisi input
def get_plant_recommendations(ph_soil, humidity, temp, soil_type, dataset):
    # Pastikan dataset tidak kosong
    dataset = dataset.dropna(subset=['pH_Tanah', 'Kelembaban', 'Suhu', 'Jenis_Tanah', 'Tanaman_Cocok'])  # Menghapus data yang missing

    recommendations = dataset[
        (dataset['pH_Tanah'] >= ph_soil - 0.5) & (dataset['pH_Tanah'] <= ph_soil + 0.5) &
        (dataset['Kelembaban'] >= humidity - 10) & (dataset['Kelembaban'] <= humidity + 10) &
        (dataset['Suhu'] >= temp - 2) & (dataset['Suhu'] <= temp + 2) &
        (dataset['Jenis_Tanah'] == soil_type)
    ]

    if not recommendations.empty:
        recommended_plants = recommendations['Tanaman_Cocok'].tolist()
        return f"Tanaman yang cocok berdasarkan input Anda: {', '.join(recommended_plants)}"
    else:
        return "Tidak ada tanaman yang cocok ditemukan berdasarkan kondisi ini."

# Set konfigurasi halaman
st.set_page_config(page_title="Rekomendasi Tanaman", layout="centered", page_icon="🌱")

# Path logo
current_dir = os.path.dirname(__file__)
asset_dir = os.path.join(current_dir, "../asset")
logo_path = os.path.join(asset_dir, "logo.png")

# Validasi keberadaan logo
if not os.path.exists(logo_path):
    st.error(f"Logo tidak ditemukan di lokasi: {logo_path}")
    st.stop()

# Tambahkan CSS untuk balon chat dan menghapus garis bawah tombol
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
    }
    .chat-assistant {
        background-color: #E4E6EB;
        color: black;
        text-align: left;
        float: left;
    }
    .chat-container {
        display: flex;
        flex-direction: column;
        max-height: 400px;
        overflow-y: auto;
        padding: 10px;
        background-color: #f9f9f9;
        border: none;
        border-radius: 10px;
    }
    .stButton > button {
        background-color: transparent;
        color: black;
        border: 2px solid none;
        outline: none;
        box-shadow: none;
        transition: background-color 0.3s, color 0.3s;
    }
    .stButton > button:hover {
        background-color: #4CAF50;
        color: white;
    }
    .stButton {
        margin-bottom: 0 !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Membuat header dengan logo dan teks
col1, col2 = st.columns([3, 20])
with col1:
    st.image(logo_path, width=100)
with col2:
    st.markdown(
        """
        <div style="display: flex; justify-content: center; align-items: center; height: 100%; margin-left: -50px;">
            <h1 style="font-family: Arial, sans-serif; color: chocolate; text-align: center; font-size: 50px;">
            Rekomendasi Tanaman
            </h1>
        </div>
        """,
        unsafe_allow_html=True,
    )

# Input untuk rekomendasi tanaman
ph_soil = st.number_input("pH Tanah", min_value=0.0, max_value=14.0, step=0.1, format="%.1f", key="ph_soil")
humidity = st.slider("Kelembaban Tanah (%)", min_value=0, max_value=100, step=1, key="humidity")
temp = st.number_input("Suhu (°C)", min_value=-50.0, max_value=50.0, step=0.1, format="%.1f", key="temp")
soil_type = st.selectbox("Jenis Tanah", ["Liat", "Pasir", "Gambut", "Andosol", "Humus"], key="soil_type")

# Tombol Kirim
if st.button("Kirim"):
    if ph_soil and humidity and temp and soil_type:
        dataset_path = os.path.join(current_dir, "../dataset/Rekomendasi_tanaman.csv")
        if not os.path.exists(dataset_path):
            add_message("assistant", "Dataset tidak ditemukan!")
        else:
            dataset = pd.read_csv(dataset_path)
            dataset.columns = dataset.columns.str.strip()  # Menghapus spasi yang tidak perlu
            recommendation = get_plant_recommendations(ph_soil, humidity, temp, soil_type, dataset)
            add_message("assistant", recommendation)
    else:
        st.warning("Pastikan semua input sudah diisi!")

# Menampilkan riwayat chat
st.markdown('<div class="chat-container">', unsafe_allow_html=True)
if "chat_history" in st.session_state:
    for chat in st.session_state.chat_history:
        if chat["sender"] == "user":
            st.markdown(
                f"""
                <div class="chat-box chat-user">
                    {chat['message']}
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f"""
                <div class="chat-box chat-assistant">
                    {chat['message']}
                </div>
                """,
                unsafe_allow_html=True,
            )
st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown(
    """
    <div class="footer">
        © 2024 Agriculture Assistant. All rights reserved.
    </div>
    """,
    unsafe_allow_html=True,
)
