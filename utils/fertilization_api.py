from utils.config_reader import get_api_key
import requests

# Ambil API key untuk cuaca
weather_api_key, _ = get_api_key()

def get_weather_forecast(location):
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={location}&appid={weather_api_key}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None
