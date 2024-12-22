import os
import streamlit as st

# Konfigurasi halaman
st.set_page_config(page_title="Asisten Pertanian", layout="wide", page_icon="🌱")

# Atur direktori kerja ke lokasi file ini
current_dir = os.path.dirname(__file__)
asset_dir = os.path.join(current_dir, "asset")

# Helper function untuk memastikan file ditemukan
def get_asset_path(filename):
    path = os.path.join(asset_dir, filename)
    if not os.path.exists(path):
        st.error(f"File tidak ditemukan: {path}")
        st.stop()
    return path

# Header dengan logo dan teks
col1, col2 = st.columns([3, 20])  # Atur proporsi kolom
with col1:
    st.image(get_asset_path("logo.png"), use_container_width=True)

with col2:
    st.markdown(
        """
        <div style="display: flex; justify-content: center; align-items: center; height: 100%;">
            <h1 style="font-family: Arial, sans-serif; color: chocolate; text-align: center; font-size: 90px;">
            Asisten Pertanian
            </h1>
        </div>
        """,
        unsafe_allow_html=True,
    )

# Judul halaman utama
st.markdown(
    """
    <h2 style="text-align: center; font-family: Arial, sans-serif; color: green;">
    ADA YANG DAPAT SAYA BANTU?
    </h2>
    """,
    unsafe_allow_html=True,
)

# Tambahkan CSS untuk tombol hijau dan teks putih
st.markdown(
    """
    <style>
    .button-link {
        display: block;
        background-color: #4CAF50; /* Hijau terang */
        color: white !important;  /* Paksa Teks putih */
        padding: 14px 20px;
        margin: 10px 0;
        text-align: center;
        text-decoration: none;
        font-size: 18px;
        font-weight: bold;
        border-radius: 10px;
        transition: background-color 0.3s ease, transform 0.3s ease;
        box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.2); /* Bayangan tombol */
    }
    .button-link:hover {
        background-color: #388E3C; /* Hijau gelap saat hover */
        transform: translateY(-4px); /* Efek angkat saat hover */
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Layout grid untuk opsi
col1, col2 = st.columns(2)

# Kolom pertama
with col1:
    st.image(get_asset_path("gambar 1.jpg"), use_container_width=True)
    st.markdown(
        '<a href="./weather_forecast" class="button-link">Prakiraan Cuaca</a>',
        unsafe_allow_html=True,
    )
    
    st.image(get_asset_path("gambar 3.jpg"), use_container_width=True)
    st.markdown(
        '<a href="./pestmanagement" class="button-link">Pengelolaan Hama dan Penyakit</a>',
        unsafe_allow_html=True,
    )

# Kolom kedua
with col2:
    st.image(get_asset_path("gambar 2.jpg"), use_container_width=True)
    st.markdown(
        '<a href="./fertilization" class="button-link">Panduan Pemupukan</a>',
        unsafe_allow_html=True,
    )
    
    st.image(get_asset_path("gambar 4.jpg"), use_container_width=True)
    st.markdown(
        '<a href="./plant_recommendation" class="button-link">Rekomendasi Tanaman</a>',
        unsafe_allow_html=True,
    )
