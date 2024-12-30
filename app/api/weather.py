import requests
import pandas as pd

class WeatherApi:
    def __init__(self):
         self.__city_data = pd.read_csv("./app/data/worldcities.csv")
         
    def get_weather(self, query):
        try:
            # Cari kota di CSV
            query = query.lower().replace("weather", "").replace("weather in", "").strip()
            city_row = self.__city_data[self.__city_data['city_ascii'].str.lower() == query]

            if city_row.empty:
                return "I couldn't find the location. Please specify a valid city."

            latitude = city_row.iloc[0]['lat']
            longitude = city_row.iloc[0]['lng']

            # Panggil API Open-Meteo
            url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current_weather=true"
            response = requests.get(url)
            response.raise_for_status()
            weather_data = response.json()

            # Ambil informasi cuaca
            current_weather = weather_data["current_weather"]
            temperature = current_weather["temperature"]
            windspeed = current_weather["windspeed"]
            weather_code = current_weather["weathercode"]

            # Dekripsi kode cuaca
            weather_descriptions = {
                0: "Clear sky",
                1: "Mainly clear",
                2: "Partly cloudy",
                3: "Overcast",
                45: "Fog",
                48: "Depositing rime fog",
                51: "Drizzle: Light",
                53: "Drizzle: Moderate",
                55: "Drizzle: Dense intensity",
                61: "Rain: Slight",
                63: "Rain: Moderate",
                65: "Rain: Heavy intensity",
                71: "Snow fall: Slight",
                73: "Snow fall: Moderate",
                75: "Snow fall: Heavy intensity",
                80: "Rain showers: Slight",
                81: "Rain showers: Moderate",
                82: "Rain showers: Violent",
                95: "Thunderstorm: Slight",
                96: "Thunderstorm: Moderate",
                99: "Thunderstorm: Severe"
            }

            weather_status = weather_descriptions.get(weather_code, "Unknown weather condition")

            return (f"The current weather in {query.title()} is {temperature}°C with a windspeed of {windspeed} km/h. "
                    f"Condition: {weather_status}.")
        except requests.exceptions.RequestException as e:
            return f"An error occurred while fetching the weather: {e}"

