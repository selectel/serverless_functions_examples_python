import os
import json
import asyncio
import datetime
from urllib import request

# OpenWeatherMap API endpoint.
# For more information see: https://openweathermap.org/forecast5#geo5
OPENWEATHERMAP_URL = "http://api.openweathermap.org/data/2.5/forecast" \
                     "?units=metric&lat={lat}&lon={lon}&appid={key}"
OPENWEATHERMAP_API_KEY = os.environ.get('OWM_API_KEY')


async def get_forecast(lat, lon):
    try:
        # Fetch data.
        url = OPENWEATHERMAP_URL.format(lat=lat, lon=lon,
                                        key=OPENWEATHERMAP_API_KEY)
        response = request.urlopen(url)
        data = json.load(response)
        # Transform data.
        return data.get('list') or []
    except Exception as e:
        # Log errors and not raise it.
        print(str(e))
        return []


# OpenExchangeRates API endpoint.
# For more information see: https://openexchangerates.org
OPENEXCHANGERATES_URL = "https://openexchangerates.org/api/latest.json" \
                        "?app_id={key}"
OPENEXCHANGERATES_API_KEY = os.environ.get('OXR_API_KEY')


async def get_exchange_rates():
    try:
        # Fetch data.
        url = OPENEXCHANGERATES_URL.format(key=OPENEXCHANGERATES_API_KEY)
        response = request.urlopen(url)
        data = json.load(response)
        # Transform data.
        return data.get('rates') or {}
    except Exception as e:
        # Log errors and not raise it.
        print(str(e))
        return {}


async def run_chain(lat, lon):
    weather, exchange_rates = await asyncio.gather(
        get_forecast(lat, lon),
        get_exchange_rates()
    )
    return {
        "dt": datetime.datetime.now().isoformat(),
        "weather": weather,
        "exchange_rates": exchange_rates,
    }


def main(**kwargs):
    return asyncio.run(run_chain(**kwargs))
