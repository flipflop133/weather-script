import subprocess
import json
import requests
import time
import os

error_time = 0


def error_handling():
    global error_time
    time.sleep(error_time)
    error_time += 10
    get_weather()


def get_weather():
    """Retrieve current weather from weatherapi.com
    """
    try:
        # retrieve data from json file
        with open(
                "{}/weather_settings.json".format(
                    os.path.dirname(os.path.realpath(__file__))),
                "r") as read_file:
            data = json.load(read_file)
        url = data['url']
        key = data['key']
        unit = "°C" if data['unit'] == "celcius" else "°F"
        parameters = data['parameters']
        daytime = {'sunset': data['sunset'], 'sunrise': data['sunrise']}

        # retrieve weather from weatherapi.com
        request = "{}?key={}&q={}".format(url, key, parameters)
        response = requests.get(request)
        data = json.loads(response.content)
        conditions = data['current']['condition']['text']
        temp = data['current']['temp_c']

        # determine the icon
        icon = get_icon(conditions, daytime)

        # display weather
        print("{} {}{}".format(icon, int(temp), unit))
    except requests.ConnectionError:
        print("no internet")
    except json.JSONDecodeError:
        print("error in weather_settings.json file")
    except Exception as e:
        print(e)
        error_handling()


def get_icon(conditions, daytime):
    """ Determine weather icon in function of the current weather conditions
    and hour.
    """
    # retrieve data from json file
    with open(
            "{}/weather_icons.json".format(
                os.path.dirname(os.path.realpath(__file__))),
            "r") as read_file:
        data = json.load(read_file)
    # determine day or night
    hour = subprocess.run(['date', '+%H'],
                          check=True,
                          stdout=subprocess.PIPE,
                          universal_newlines=True)
    hour = (hour.stdout).strip()
    sunset = daytime['sunset']
    sunrise = daytime['sunrise']

    # get icon
    icon = ''
    for item in data:
        if item["day"] == conditions or item["night"] == conditions:
            # night icon
            if int(hour) > sunset or int(hour) < sunrise:
                icon = item["icon"]
            # day icon
            else:
                icon = item["icon-night"]

    return icon


get_weather()
