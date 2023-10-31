from datetime import datetime
import pandas as pd
from requests import *

class GeoCoding:
    
    id = 0
    name = ""
    latitude = 0
    longitude = 0
    elevation = 0.0
    country_code = ""
    country_id = 0
    country = ""

    def __init__(self, obj):
        self.id = obj["results"][0]["id"]
        self.name = obj["results"][0]["name"]
        self.latitude = obj["results"][0]["latitude"]
        self.longitude = obj["results"][0]["longitude"]
        self.elevation = obj["results"][0]["elevation"]
        self.country_code = obj["results"][0]["country_code"]
        self.country_id = obj["results"][0]["country_id"]
        self.country = obj["results"][0]["country"]
        if obj["results"][0]["admin1"]:
            self.state = obj["results"][0]["admin1"]

class Forecast:

    df = pd.DataFrame

    def __init__(self, obj) -> None:
        data = {
            'day': [],
            'precipitation_probability': [],
            'relativehumidity': [],
            'temperature': []
        }

        auxHourly = obj['hourly']

        auxDatetime = auxHourly["time"]
        auxProbability = auxHourly["precipitation_probability"]
        auxHumidity = auxHourly["relativehumidity_2m"]
        auxTemperature = auxHourly["temperature_2m"]
        
        auxDay = []

        for i in range(len(auxDatetime)):
            fmtdatetime = datetime.strptime(auxDatetime[i], "%Y-%m-%dT%H:%M")
            auxDay.append(fmtdatetime.date())

        data['precipitation_probability'] = auxProbability
        data['relativehumidity'] = auxHumidity
        data['temperature'] = auxTemperature
        data['day'] = auxDay

        self.df = self.df.from_dict(data=data)
        self.df.fillna(0, inplace= True)
        self.df = self.df.groupby(['day'], as_index=False).median()
        
        auxDaily = obj['daily']

        auxDatetime = auxDaily["time"]
        auxSunrise = auxDaily["sunrise"]
        auxSunset = auxDaily["sunset"]

        for i in range(len(auxDatetime)):
            fmtdatetime = datetime.strptime(auxDatetime[i], "%Y-%m-%d")
            fmtSunrise = datetime.strptime(auxSunrise[i], "%Y-%m-%dT%H:%M")
            fmtSunset = datetime.strptime(auxSunset[i], "%Y-%m-%dT%H:%M")

            auxDatetime[i] = fmtdatetime.date()
            auxSunrise[i] = fmtSunrise.time()
            auxSunset[i] = fmtSunset.time()
        
        auxData = {
            "day": auxDatetime,
            "MaxTemperature": auxDaily["temperature_2m_max"],
            "MinTemperature": auxDaily["temperature_2m_min"],
            "Sunrise": auxSunrise,
            "Sunset": auxSunset
        }

        auxDf = pd.DataFrame.from_dict(data=auxData)

        self.df = self.df.merge(auxDf, how='inner', on=['day'])

if __name__ == '__main__':
    name = "quito"

    URL_GEOCODING_API = "https://geocoding-api.open-meteo.com/v1/search?name=" + name + "&count=10&language=pt&format=json"
    geo = GeoCoding(get(URL_GEOCODING_API).json())
    latitude = str(geo.latitude)
    longitude = str(geo.longitude)

    URL_WEATHER_API = "https://api.open-meteo.com/v1/forecast?latitude=" + latitude + "&longitude=" + longitude +"&hourly=temperature_2m,relativehumidity_2m,precipitation_probability&daily=temperature_2m_max,temperature_2m_min,sunrise,sunset&forecast_days=16&timezone=America%2FSao_Paulo"
    forecast = Forecast(get(URL_WEATHER_API).json())

    print("Nome: ", geo.name)
    print("Estado: ", geo.state)
    print("País: ", geo.country)
    print("Elevação: ", geo.elevation)
    print(forecast.df.head(5))