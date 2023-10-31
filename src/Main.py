from requests import *
from datetime import *
from Models import GeoCoding, Forecast
from azure import Azure
import PySimpleGUI as sg
import pyautogui as pg


sg.theme('DarkAmber')   # Add a touch of color
# All the stuff inside your window.
layout = [  [sg.Text('Cidade:'), sg.InputText()],
            [sg.Text('Data:'), sg.InputText(), sg.CalendarButton(button_text="Escolher", format="%d/%m/%Y")],
            [sg.Button('Ok'), sg.Button('Cancel')] ]

# Create the Window
window = sg.Window('Window Title', layout)
# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
        break
    name = values[0]
    selectedDate = date.today()
    if values[1] != "":
        selectedDate = datetime.strptime(values[1], "%d/%m/%Y").date()

    # #TODO Tratar os erros (Ex: Cidade inválida)
    URL_GEOCODING_API = "https://geocoding-api.open-meteo.com/v1/search?name=" + name + "&count=10&language=pt&format=json"
    geo = GeoCoding(get(URL_GEOCODING_API).json())
    latitude = str(geo.latitude)    
    longitude = str(geo.longitude)

    URL_WEATHER_API = "https://api.open-meteo.com/v1/forecast?latitude=" + latitude + "&longitude=" + longitude +"&hourly=temperature_2m,relativehumidity_2m,precipitation_probability&daily=temperature_2m_max,temperature_2m_min,sunrise,sunset&forecast_days=16&timezone=America%2FSao_Paulo"
    forecast = Forecast(get(URL_WEATHER_API).json())

    resultado = forecast.df.loc[forecast.df['day'] == selectedDate]

    Azure.save(name, str(selectedDate.strftime("%d/%m/%Y")), geo, resultado)

    sg.popup_no_buttons("Nome: " + str(geo.name),
                        "Estado: " + str(geo.state),
                        "País: " + str(geo.country),
                        "Data: " + str(selectedDate.strftime("%d/%m/%Y")),
                        "Elevação: " + str(geo.elevation) + "m",
                        "Probabilidade de precipitação: " + str(resultado['precipitation_probability'].values[0]) + "%",
                        "Humidade relativa: " + str(resultado['relativehumidity'].values[0]),
                        "Temperatura média: " + str(resultado['temperature'].values[0]) + "ºC",
                        "Temperatura máxima: " + str(resultado['MaxTemperature'].values[0]) + "ºC",
                        "Temperatura mínima: " + str(resultado['MinTemperature'].values[0]) + "ºC",
                        "Nascer do Sol: " + str(resultado['Sunrise'].values[0]),
                        "Pôr do Sol: " + str(resultado['Sunset'].values[0]),
                        title="Resultado")

window.close()