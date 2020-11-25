import subprocess
import json
import requests
import time
import os

error_time = 0


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
        print("{}  {}{}".format(icon, int(temp), unit))
    except OSError:
        print("weather_settings.json file not found")
    except json.JSONDecodeError:
        print("error in weather_settings.json file")
    except Exception as e:
        print(e)
        global error_time
        time.sleep(error_time)
        error_time += 10
        print(error_time)
        get_weather()


def get_icon(conditions, daytime):
    """ Determine weather icon in function of the current weather conditions
    and hour.
    """
    icon = ''
    hour = subprocess.run(['date', '+%H'],
                          check=True,
                          stdout=subprocess.PIPE,
                          universal_newlines=True)
    hour = (hour.stdout).strip()
    sunset = daytime['sunset']
    sunrise = daytime['sunrise']
    # night icons
    if int(hour) > sunset or int(hour) < sunrise:
        if "cloud" in conditions:
            icon = ''
        elif "sun" in conditions:
            icon = ''
        elif "rain" in conditions:
            icon = ''
        elif "clear" in conditions:
            icon = ''
        else:
            icon = ''
    # day icons
    else:
        if "partly cloudy" in conditions:
            icon = ''
        elif "cloud" in conditions:
            icon = ''
        elif "sun" in conditions:
            icon = ''
        elif "rain" in conditions:
            icon = ''
        elif "clear" in conditions:
            icon = ''
        elif "fair" in conditions:
            icon = ''
        else:
            icon = ''
    return icon


get_weather()
