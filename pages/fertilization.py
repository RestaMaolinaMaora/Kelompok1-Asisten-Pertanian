import os
import streamlit as st
import pandas as pd

# Fungsi untuk menambahkan pesan ke riwayat chat
def add_message(sender, message):
    if "fertilization_history" not in st.session_state:
        st.session_state.fertilization_history = []
    st.session_state.fertilization_history.append({"sender": sender, "message": message})

# Fungsi untuk membaca dataset CSV
def load_fertilization_data():
    # Path ke file CSV
    csv_path = os.path.join("dataset", "Panduan Pemupukan.csv")
    
    # Pastikan file ada sebelum membacanya
    if not os.path.exists(csv_path):
        st.error(f"File {csv_path} tidak ditemukan!")
        return None
    
    # Membaca file CSV dan mengembalikan DataFrame
    df = pd.read_csv(csv_path)
    return df

# Set konfigurasi halaman
st.set_page_config(page_title="Panduan Pemupukan", layout="centered", page_icon="🌱")

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
        float: right; /* User chat box di sebelah kanan */
        border-top-right-radius: 0; /* Membuat sudut atas kanan menjadi datar */
    }
    .chat-assistant {
        background-color: #E4E6EB;
        color: black;
        text-align: left;
        float: left; /* Assistant chat box di sebelah kiri */
        border-top-left-radius: 0; /* Membuat sudut atas kiri menjadi datar */
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
    .input-box {
        margin-top: 20px;
        padding: 10px;
        width: 100%;
        font-size: 16px;
        border: 1px solid #4CAF50;
        border-radius: 10px;
        outline: none;
    }
    .send-button {
        background-color: #4CAF50;
        color: white;
        padding: 10px 20px;
        border: none;
        border-radius: 10px;
        cursor: pointer;
        width: 100%;
        margin-top: 10px;
    }
    .send-button:hover {
        background-color: #45a049;
    }
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
    """,
    unsafe_allow_html=True,
)

# Membuat header dengan logo dan teks
col1, col2 = st.columns([3, 20])  # Atur proporsi kolom: logo kecil, teks lebih besar

with col1:
    st.image("asset/logo.png", width=100)  # Ganti dengan path logo Anda

with col2:
    st.markdown(
        """
        <div style="display: flex; justify-content: center; align-items: center; height: 100%;">
            <h1 style="font-family: Arial, sans-serif; color: chocolate; text-align: center; font-size: 50px;">
            Panduan Pemupukan
            </h1>
        </div>
        """,
        unsafe_allow_html=True,
    )

# Fitur Pemupukan: Rekomendasi Pemupukan Berdasarkan Nama Tanaman
st.write("### Rekomendasi Pemupukan Berdasarkan Tanaman")
message = st.text_input("Pesan Anda:", key="message_input", help="Ketik tanaman yang ingin Anda cari rekomendasi pemupukannya")

if st.button("Kirim"):
    if message:
        # Tambahkan pesan pengguna ke riwayat chat
        add_message("user", message)
        
        # Membaca dataset dan mencari rekomendasi pemupukan berdasarkan tanaman
        fertilization_data = load_fertilization_data()
        if fertilization_data is not None:
            # Normalisasi input pengguna (case-insensitive)
            user_input = message.strip().lower()
            matching_plants = fertilization_data[fertilization_data['Nama Tanaman'].str.contains(user_input, case=False, na=False)]
            
            if not matching_plants.empty:
                # Ambil informasi pemupukan pertama yang cocok
                plant_info = matching_plants.iloc[0]  # Ambil baris pertama yang cocok
                advice = (
                    f"Jenis Pupuk: {plant_info['Jenis Pupuk']}\n"
                    f"Dosis (kg/ha): {plant_info['Dosis (kg/ha)']}\n"
                    f"Waktu Pemupukan: {plant_info['Waktu Pemupukan']}\n"
                    f"Cara Pemupukan: {plant_info['Cara Pemupukan']}\n"
                    f"Manfaat: {plant_info['Manfaat']}"
                )
                # Pisahkan informasi ke baris baru
                advice = advice.replace("\n", "<br>")
                add_message("assistant", advice)
            else:
                add_message("assistant", "Tanaman tidak ditemukan. Silakan coba nama lain.")
    else:
        st.warning("Pesan tidak boleh kosong!")

# Menampilkan riwayat chat pemupukan
if "fertilization_history" in st.session_state:
    for chat in st.session_state.fertilization_history:
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

# Footer
st.markdown(
    """
    <div class="footer">
        © 2024 Agriculture Assistant. All rights reserved.
    </div>
    """,
    unsafe_allow_html=True,
)
