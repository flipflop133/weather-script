# Weather-script
This script aims to be simple and to be used for any project.
The script simply displays an icon, the current weather and the unit.
## Dependencies
- Python (3.x)
- [weatherapi](https://www.weatherapi.com/)

## How to use
 Clone the repository and configure json settings in weather_settings.json as follows:
- ### Required
    - `key`: string (Get your API key on [weatherapi.com](https://www.weatherapi.com/), e.g:"c92jef" )
    - `parameters`: string (weatherapi parameters (see "Request Parameters" section [here](https://www.weatherapi.com/docs/) for more informations), e.g: "Namen,Belgium")
    - `unit`: string ("Celsius" or "Farhenheit")
- ### Optional
    - `sunset`: number (sunset time in 24 hours format, e.g: 22)
    - `sunrise`: number (sunrise time in 24 hours format, e.g: 7)
    - `icon-position`: string ("left" or "right")

### Example
``` json
{
    "url": "http://api.weatherapi.com/v1/current.json",
    "key": "c92jef",
    "parameters": "Namen,Belgium",
    "unit": "Celsius"
}
```
### Use with Polybar
``` ini
[module/weather]
type = custom/script
interval = 1800
exec = python -O /path/to/weather/script
```
