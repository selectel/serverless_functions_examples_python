import json
from urllib import request

# Example API Key. Use your own, please.
API_KEY = '38a6944238fc7e2ec20bf31b5cb643c0'

# OpenWeatherMap API endpoint.
# For more information see:
# https://openweathermap.org/forecast5#geo5
URL = "http://api.openweathermap.org/data/2.5/forecast?units=metric" \
      "&lat={lat}&lon={lon}&appid={key}"


def get_forecast(lat, lon):
    response = request.urlopen(URL.format(lat=lat, lon=lon, key=API_KEY))
    return json.load(response)


if __name__ == '__main__':
    print(get_forecast(lat='59.887327', lon='30.329750'))
