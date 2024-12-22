import streamlit as st
import requests
from pathlib import Path
import folium
from streamlit_folium import st_folium

# Fungsi untuk mendapatkan path asset
def get_asset_path(filename):
    current_dir = Path(__file__).parent
    asset_dir = current_dir.parent / 'asset'
    asset_path = asset_dir / filename
    if not asset_path.exists():
        st.error(f"File tidak ditemukan: {asset_path}")
        st.stop()
    return str(asset_path)

# Fungsi untuk mendapatkan cuaca dari OpenWeatherMap
def get_weather(city_name):
    api_key = "b9c0137f52584d83b1b56bf9a52402a6"  # Gantilah dengan API key Anda
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = f"{base_url}q={city_name}&appid={api_key}&units=metric&lang=id"
    
    response = requests.get(complete_url)
    data = response.json()

    if data["cod"] == 200:
        main_data = data["main"]
        weather_data = data["weather"][0]
        coord = data["coord"]
        return {
            "temperature": main_data["temp"],
            "pressure": main_data["pressure"],
            "humidity": main_data["humidity"],
            "description": weather_data["description"],
            "icon": weather_data["icon"],
            "latitude": coord["lat"],
            "longitude": coord["lon"]
        }
    else:
        return None

# Konfigurasi halaman
st.set_page_config(page_title="Prakiraan Cuaca", layout="centered", page_icon="🌱")

# Header
col1, col2 = st.columns([3, 20])
with col1:
    st.image(get_asset_path("logo.png"), width=100)
with col2:
    st.markdown("<h1 style='color: chocolate; justify-content: center;text-align: center;font-size: 50px;'>Prakiraan Cuaca</h1>", unsafe_allow_html=True)

# Input lokasi
message = st.text_input("Masukkan nama kota:", key="message_input", help="Contoh: Jakarta")

# Cek apakah ada cuaca di session state
if "weather_info" not in st.session_state:
    st.session_state.weather_info = None

if st.button("Kirim"):
    if message:
        weather_info = get_weather(message)
        if weather_info:
            st.session_state.weather_info = weather_info  # Simpan di session state
            st.session_state.city_name = message.capitalize()
        else:
            st.warning("Lokasi tidak ditemukan. Coba periksa nama kota.")
    else:
        st.warning("Nama kota tidak boleh kosong!")

# Tampilkan hasil jika ada data cuaca
if st.session_state.weather_info:
    weather_info = st.session_state.weather_info
    city_name = st.session_state.city_name

    st.subheader(f"Cuaca di {city_name}:")
    st.write(f"Suhu: {weather_info['temperature']}°C")
    st.write(f"Tekanan: {weather_info['pressure']} hPa")
    st.write(f"Kelembapan: {weather_info['humidity']}%")
    st.write(f"Kondisi: {weather_info['description'].capitalize()}")
    st.image(f"http://openweathermap.org/img/wn/{weather_info['icon']}@2x.png", width=100)

    # Tambahkan peta lokasi
    m = folium.Map(location=[weather_info["latitude"], weather_info["longitude"]], zoom_start=10)
    folium.Marker(
        [weather_info["latitude"], weather_info["longitude"]],
        popup=f"{city_name} - {weather_info['description'].capitalize()}"
    ).add_to(m)
    st_folium(m, width=700, height=500)
