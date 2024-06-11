import requests
from .weather_dict import WeatherResponse, Location, Current, Condition


class WeatherAPI:
    def __init__(self):
        pass

    def get_weather(self, query) -> WeatherResponse:
        url = "https://goweather.floretos.com/current"
        # json body
        # if has only numbers, then zip code
        data = {
            "city": query
        }

        # headers
        headers = {
            "Content-Type": "application/json",
        }
        # make request
        response = requests.post(url, headers=headers, json=data)
        # return WeatherResponse

        # parse json
        json = response.json()
        print(json)
        location = Location(
            json["location"]["name"],
            json["location"]["region"],
            json["location"]["country"],
            json["location"]["lat"],
            json["location"]["lon"],
            json["location"]["tz_id"],
            json["location"]["localtime_epoch"],
            json["location"]["localtime"]
        )

        condition = Condition(
            json['current']['condition']['text'],
            json['current']['condition']['icon'],
            json['current']['condition']['code']
        )

        current = Current(
            json["current"]["last_updated_epoch"],
            json["current"]["last_updated"],
            json["current"]["temp_c"],
            json["current"]["temp_f"],
            json["current"]["is_day"],
            condition,
            json["current"]["wind_mph"],
            json["current"]["wind_kph"],
            json["current"]["wind_degree"],
            json["current"]["wind_dir"],
            json["current"]["pressure_mb"],
            json["current"]["pressure_in"],
            json["current"]["precip_mm"],
            json["current"]["precip_in"],
            json["current"]["humidity"],
            json["current"]["cloud"],
            json["current"]["feelslike_c"],
            json["current"]["feelslike_f"],
            json["current"]["windchill_c"],
            json["current"]["windchill_f"],
            json["current"]["heatindex_c"],
            json["current"]["heatindex_f"],
            json["current"]["dewpoint_c"],
            json["current"]["dewpoint_f"],
            json["current"]["vis_km"],
            json["current"]["vis_miles"],
            json["current"]["uv"],
            json["current"]["gust_mph"],
            json["current"]["gust_kph"]
        )

        weather = WeatherResponse(
            location,
            current
        )

        return weather