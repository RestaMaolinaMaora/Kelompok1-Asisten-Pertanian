# utils/config_reader.py
import toml
import os

def get_api_key():
    # Path ke file config.toml di folder .streamlit
    config_path = os.path.join(os.path.dirname(__file__), "../.streamlit/config.toml")
    config = toml.load(config_path)
    
    weather_api_key = config["general"]["weather_api_key"]  # Ambil weather_api_key
    plant_api_key = config["general"]["plant_api_key"]  # Ambil plant_api_key
    
    return weather_api_key, plant_api_key  # Kembalikan kedua API keys

def get_fertilization_advice(weather_data):
    # Ambil data cuaca dalam 24 jam ke depan
    forecast = weather_data["list"][:8]  # 8 data = 24 jam, karena intervalnya 3 jam
    
    # Analisis data
    rain_expected = any("rain" in hour for hour in forecast)
    extreme_conditions = any(hour["main"]["temp"] > 35 or hour["main"]["temp"] < 15 for hour in forecast)
    
    # Berikan rekomendasi
    if rain_expected:
        return "Hindari pemupukan karena ada prediksi hujan dalam 24 jam ke depan."
    elif extreme_conditions:
        return "Hindari pemupukan karena ada cuaca ekstrem seperti suhu terlalu tinggi atau rendah."
    else:
        return "Waktu ini cocok untuk pemupukan, cuaca diprediksi stabil dan tidak ada hujan."
