import requests

def get_weather(city, api_key):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        temperature = data["main"]["temp"]
        weather_description = data["weather"][0]["description"]  # Menambahkan deskripsi cuaca
        return {
            "temperature": temperature,
            "description": weather_description
        }
    else:
        return {"error": "Data cuaca tidak ditemukan atau terjadi masalah dengan API."}
