# Weather-script
This script aims to be simple and to be used for any project.
The script simply displays an icon, the current weather and the unit.
## Dependencies
- Python (3.x)
- [weatherapi](https://www.weatherapi.com/)

## How to use
 Clone the repository and configure json settings in weather_settings.json as follows:
- `key`: Get your API key on [weatherapi.com](https://www.weatherapi.com/)
- `parameters`: weatherapi parameters (see [here](https://www.weatherapi.com/) for more informations)
- `unit`: celcius or farheinheit
* Optional:
- `sunset`: sunset time in 24 hours format
- `sunrise`: sunrise time in 24 hours format

### Example
``` json
{
    "url": "http://api.weatherapi.com/v1/current.json",
    "key": "your api key",
    "parameters": "London",
    "unit": "celcius",
    "sunset": 22,
    "sunrise": 7
}
```
### Use with Polybar
``` ini
[module/weather]
type = custom/script
interval = 1800
exec = python /path/to/weather/script
```
