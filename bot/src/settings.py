from decouple import config


BASE_URL = "https://www.bet365.com/#/HO/"

API_URL = config("API_URL", default="http://localhost:5000")
API_ENDPOINTS = {
    "get_entradas": {
        "URL": API_URL + "/entrada/",
        "METHOD": "get"
    },
    "bet_entradas": {
        "URL": API_URL + "/entrada/",
        "METHOD": "post"
    }
}


CHROME_APP_CONFIG = {
    "app_name": "google-chrome",
    "command": "google-chrome --remote-debugging-port=9222 --user-data-dir=/tmp/selenum/ChromeProfile",
    "flags": [
        "--remote-debugging-port=9222",
        "--user-data-dir=/tmp/selenum/ChromeProfile"
    ]
}

USERNAME = config("BETS_USERNAME", default="")
PASSWORD = config("BETS_PASSWORD", default="")
