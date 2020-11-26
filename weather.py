import json
import requests
import time
import os
import datetime
import argparse
from sys import stdout
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

parser = argparse.ArgumentParser()
parser.add_argument('-a', '--alternative', type=bool, metavar='alternative')
args = parser.parse_args()
alternative = False
if args.alternative is not None:
    alternative = args.alternative

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


def get_weather(alternative):
    """Retrieve current weather from weatherapi.com
    """
    global data

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
            daytime = {'sunset': data['sunset'], 'sunrise': data['sunrise']}
        conditions = data['current']['condition']['text']
        temp = data['current']['temp_c'] if unit == "°C" else data['current']
        ['temp_f']
        if not daytime_mode():
            daytime = data['current']['is_day']

        # determine the icon
        icon = get_icon(conditions, daytime)

        # display weather
        print("{} {}{}".format(icon, int(round(temp)), unit), end='')

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
            # night icon
            if daytime_mode():
                if int(hour) > sunset or int(hour) < sunrise:
                    icon = item["icon"]
                # day icon
                else:
                    icon = item["icon-night"]
            else:
                if daytime:
                    icon = item["icon"]
                # day icon
                else:
                    icon = item["icon-night"]

    return icon


def weather_app(forecast):
    # display alternative weather informations
    # init gtk window
    win = Gtk.Window(title="Weather Forecast")
    grid = Gtk.Grid()
    # current date

    vbox_infos_icon = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
    label = Gtk.Label(label="{}".format("Icon"))
    label.set_markup("<span size='16000'>{}</span>".format("Icon"))
    vbox_infos_icon.pack_start(label, True, True, 0)

    vbox_infos_hour = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
    label = Gtk.Label(label="{}".format("Hour"))
    label.set_markup("<span size='16000'>{}</span>".format("Hour"))

    vbox_infos_hour.pack_start(label, True, True, 0)

    vbox_infos_temp = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
    label = Gtk.Label(label="{}".format("Temp"))
    label.set_markup("<span size='16000'>{}</span>".format("Temp"))

    vbox_infos_temp.pack_start(label, True, True, 0)

    vbox_infos = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
    vbox_infos.pack_start(label, True, True, 0)
    vbox_infos.add(vbox_infos_hour)
    vbox_infos.add(vbox_infos_icon)
    vbox_infos.add(vbox_infos_temp)
    grid.add(vbox_infos)

    for hour in range(0, 24):
        icon = get_icon(
            forecast["forecast"]["forecastday"][0]["hour"][hour]["condition"]
            ["text"],
            forecast["forecast"]["forecastday"][0]["hour"][hour]["is_day"])
        temp = " {}°C  ".format(
            forecast["forecast"]["forecastday"][0]["hour"][hour]["temp_c"])
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        label = Gtk.Label(label="{}h".format(str(hour + 1)))
        vbox.pack_start(label, True, True, 0)

        vbox_icon = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        label = Gtk.Label(label="{}".format(icon))
        label.set_markup("<span size='24000'>{}</span>".format(icon))
        vbox_icon.pack_start(label, True, True, 0)

        vbox_temp = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        label = Gtk.Label(label="{}".format(str(temp)))
        vbox_temp.pack_start(label, True, True, 0)

        vbox_final = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        vbox_final.add(vbox)
        vbox_final.add(vbox_icon)
        vbox_final.add(vbox_temp)
        vbox_final.set_size_request(70, 100)
        vbox_final.pack_start(label, True, True, 0)

        grid.add(vbox_final)

    # launch window
    win.add(grid)
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()


get_weather(alternative)
