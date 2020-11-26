import json
import requests
import time
import os
import datetime

error_time = 0

data = 0


def daytime_mode():
    if "sunset" and "sunrise" in data:
        return True
    else:
        return False


def error_handling():
    global error_time
    time.sleep(error_time)
    error_time += 10
    get_weather()


def get_weather():
    """Retrieve current weather from weatherapi.com
    """
    global data
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
        if daytime_mode():
            daytime = {'sunset': data['sunset'], 'sunrise': data['sunrise']}

        # retrieve weather from weatherapi.com
        request = "{}?key={}&q={}".format(url, key, parameters)
        response = requests.get(request)
        data = json.loads(response.content)
        conditions = data['current']['condition']['text']
        temp = data['current']['temp_c'] if unit == "°C" else data['current']
        ['temp_f']
        if not daytime_mode():
            daytime = data['current']['is_day']

        # determine the icon
        icon = get_icon(conditions, daytime)

        # display weather
        print("{} {}{}".format(icon, int(round(temp)), unit))
    except requests.ConnectionError:
        error_handling()
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
    if daytime_mode():
        hour = datetime.datetime.now().strftime("%H")
        sunset = daytime['sunset']
        sunrise = daytime['sunrise']

    # get icon
    icon = ''
    for item in data:
        if item["day"] == conditions or item["night"] == conditions:
            # night icon
            if daytime_mode():
                if int(hour) > sunset or int(hour) < sunrise:
                    icon = item["icon"]
                # day icon
                else:
                    icon = item["icon-night"]
            else:
                if datetime:
                    icon = item["icon"]
                # day icon
                else:
                    icon = item["icon-night"]

    return icon


get_weather()
