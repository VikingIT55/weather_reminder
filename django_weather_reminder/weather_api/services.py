import requests
from django.conf import settings
from requests.exceptions import RequestException


def make_weather_request(city_name):
    url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        'q': city_name,
        'appid': settings.WEATHER_API_KEY,
        'units': 'metric'
    }
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except RequestException as e:
        print(f"HTTP error or network issue: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
    return None

def validate_and_parse_weather_data(data):
    if not isinstance(data, dict):
        raise ValueError("Invalid response format: data is not a dictionary")
    main_data = data.get('main', {})
    weather_data = data.get('weather', [{}])[0]
    if not isinstance(main_data, dict) or not isinstance(weather_data, dict):
        raise ValueError("Invalid response format: 'main' or 'weather' is not a dictionary")
    temperature = main_data.get('temp')
    conditions = weather_data.get('description')
    humidity = main_data.get('humidity')
    if temperature is None or conditions is None or humidity is None:
        raise ValueError("Incomplete weather data: missing 'temp', 'description', or 'humidity'")
    return {
        'temperature': temperature,
        'conditions': conditions,
        'humidity': humidity,
    }


def fetch_weather(city_name):
    data = make_weather_request(city_name)
    if data is None:
        return None
    try:
        return validate_and_parse_weather_data(data)
    except ValueError as e:
        print(f"Data validation error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
    return None
