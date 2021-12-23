"""Small script to generate weather data."""
import json
import os
import time
from sys import stdout
import requests
from json import dumps

SOURCE = "irm"


class Irm:
    weather_data = {}

    def get_data(self):
        import requests
        from bs4 import BeautifulSoup

        URL = "https://www.meteo.be/fr/saint-leger"
        page = requests.get(URL)

        soup = BeautifulSoup(page.content, "html.parser")

        results = soup.find_all("observation-comp", )
        description_fr = results[0].get("weatherdescription")
        self.weather_data["description_fr"] = description_fr
        temp = results[0].get("temp")
        self.weather_data["temp"] = temp
        wind = results[0].get("windamount")
        wind_unit = results[0].get("windunit")
        wind_direction = results[0].get("winddirectiontxt")
        self.weather_data["wind"] = f"{wind} {wind_unit} {wind_direction}"

        # Retrieve description
        URL = "https://www.meteo.be/en/saint-leger"
        page = requests.get(URL)

        soup = BeautifulSoup(page.content, "html.parser")

        results = soup.find_all("forecast-hourly-item")
        results = results[0].find_all("g")[105].find_all("title")[0].text
        self.weather_data["description"] = results.split(",")[0].capitalize()


class Weather:
    """Weather data is managed here."""

    error_time = 0
    data = {}
    script_path = ''
    irm_data_dict = {}

    def __init__(self):
        self.script_path = os.path.dirname(os.path.realpath(__file__))
        self.get_weather()

    def get_weather(self):
        """Retrieve current weather from weatherapi.com."""
        try:
            # Handle IRM source
            if SOURCE == "irm":
                irm_data = Irm()
                irm_data.get_data()
                self.irm_data_dict = irm_data.weather_data
            # retrieve data from json file
            with open(f"{self.script_path}/weather_settings.json",
                      "r",
                      encoding="UTF-8") as read_file:
                self.data = json.load(read_file)
            url = "api.weatherapi.com/v1/current.json"
            key = self.data['key']
            unit = "°C" if self.data['unit'] == "Celsius" else "°F"
            parameters = self.data['parameters']
            icon_pos = self.icon_position()

            # retrieve weather from weatherapi.com
            request = f"http://{url}?key={key}&q={parameters}"
            response = requests.get(request)
            self.data = json.loads(response.content)
            temp = self.data['current']['temp_c'] if unit == "°C" \
                else self.data['current']['temp_f']

            # determine the icon
            icon = self.get_icon()

            # display weather
            if icon_pos == "left":
                text = f"{icon} {int(round(temp))}{unit}"
            else:
                text = f"{int(round(temp))}{unit} {icon} "
            if SOURCE == "irm":
                temp = int(self.irm_data_dict["temp"])
                tooltip = "{}\n{}".format(self.irm_data_dict["description_fr"],
                                          self.irm_data_dict["wind"])
            output = {
                'text':
                text,
                'alt':
                self.irm_data_dict["wind"],
                'tooltip':
                tooltip if (SOURCE == "irm") else
                self.data['current']['condition']['text']
            }
            self.output(output)
        except requests.ConnectionError:
            self.error_handling()
        except json.JSONDecodeError:
            print("error in weather_settings.json file")

    def error_handling(self):
        """Handle errors."""
        time.sleep(self.error_time)
        self.error_time += 10
        self.get_weather()

    def get_icon(self):
        """Determine weather icon in function of the current\
        weather conditions and hour."""
        # retrieve data from json file
        with open(f"{self.script_path}/weather_icons.json",
                  "r",
                  encoding="UTF-8") as read_file:
            data = json.load(read_file)
        # get icon
        icon = ''
        condition = self.data['current']['condition']['text']
        for item in data:
            if condition in (item["night"], item["day"]):
                if self.data['current']['is_day'] == 1:
                    icon = item["icon"]
                else:
                    icon = item["icon-night"]
        return icon

    def icon_position(self):
        """Determine icon position."""
        if "icon-position" in self.data:
            return self.data["icon-position"]
        return "right"

    def output(self, output):
        stdout.write(dumps(output) + '\n')
        stdout.flush()


Weather()
