import json
import requests
import time
import os
import datetime
import argparse
from forecast_app import WeatherWindow
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

parser = argparse.ArgumentParser()
parser.add_argument('-a', '--alternative', type=bool, metavar='alternative')
parser.add_argument('-s', '--space', type=int, metavar='space')
args = parser.parse_args()
alternative = False
space = 1
if args.alternative is not None:
    alternative = args.alternative
if args.space is not None:
    space = args.space

error_time = 0

json_data = 0


def daytime_mode():
    if "sunset" and "sunrise" in json_data:
        return True
    else:
        return False


def error_handling():
    global error_time
    time.sleep(error_time)
    error_time += 10
    get_weather(alternative)


def get_weather(alternative):
    """Retrieve current weather from weatherapi.com
    """
    global json_data

    # retrieve data from json file
    with open(
            "{}/weather_settings.json".format(
                os.path.dirname(os.path.realpath(__file__))),
            "r") as read_file:
        json_data = json.load(read_file)
    url = json_data['url']
    url_forecast = json_data['url_forecast']
    key = json_data['key']
    parameters = json_data['parameters']

    # retrieve weather from weatherapi.com
    request = "{}?key={}&q={}".format(url, key, parameters)
    response = requests.get(request)
    data = json.loads(response.content)

    # display: alternative data asked by user
    if alternative:
        properties = ""
        if "location" in json_data["alternative"]:
            for property in json_data["alternative"]["location"]:
                properties += " {}".format(data["location"][property])

        elif "current" in json_data["alternative"]:
            for property in json_data["alternative"]["current"]:
                properties += " {}".format(data["current"][property])
        # retrieve forecast
        request = "{}?key={}&q={}".format(url_forecast, key, parameters)
        response = requests.get(request)
        forecast = json.loads(response.content)

        weather_app(forecast)

    # display: icon temp unit
    else:
        unit = "°C" if json_data['unit'] == "Celsius" else "°F"
        if daytime_mode():
            daytime = {
                'sunset': json_data['sunset'],
                'sunrise': json_data['sunrise']
            }
        conditions = data['current']['condition']['text']
        temp = data['current']['temp_c'] if unit == "°C" else data['current']
        ['temp_f']
        if not daytime_mode():
            daytime = data['current']['is_day']

        # determine the icon
        icon = get_icon(conditions, daytime)

        # display weather
        print("{}{}{}{}".format(icon, ' ' * space, int(round(temp)), unit))

    try:
        pass
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
            if daytime_mode():
                # night icon
                if int(hour) > sunset or int(hour) < sunrise:
                    icon = item["icon-night"]
                # day icon
                else:
                    icon = item["icon"]
            else:
                # day icon
                if daytime:
                    icon = item["icon"]
                # night icon
                else:
                    icon = item["icon-night"]

    return icon


def weather_app(forecast):
    window = WeatherWindow(forecast)
    for hour in range(0, 24):
        icon = get_icon(
            forecast["forecast"]["forecastday"][0]["hour"][hour]["condition"]
            ["text"],
            forecast["forecast"]["forecastday"][0]["hour"][hour]["is_day"])
        temp = " {}°C  ".format(
            forecast["forecast"]["forecastday"][0]["hour"][hour]["temp_c"])
        window.display(forecast, hour, icon, temp)
    # launch window
    window.connect("destroy", Gtk.main_quit)
    window.show_all()
    Gtk.main()


get_weather(alternative)
