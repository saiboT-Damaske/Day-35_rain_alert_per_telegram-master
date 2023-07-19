import requests



# ----------------------- Telegram message function -------------------------- #


def telegram_bot_send_text(bot_message: str):
    bot_token = ''
    bot_chat_id = '' # my personal chat id
    # bot_chat_id = ""  
    send_text = 'https://api.telegram.org/bot' \
                + bot_token \
                + '/sendMessage?chat_id=' \
                + bot_chat_id + '&parse_mode=Markdown&text=' \
                + bot_message

    telegram_response = requests.get(send_text)

    return telegram_response.json()


# ------------------------ Weather check --------------------------------------- #


api_key = ""
# api_key = os.environ.get("API_KEY_ENV")

# my coords
MY_LAT = 0.00001
MY_LONG = 0.00001
# # rainy place in russia
# MY_LAT= 61.808434
# MY_LONG = 36.53

parameters = {
    "lat": MY_LAT,
    "lon": MY_LONG,
    "exclude": "current,minutely,daily",
    "appid": api_key,
}


response = requests.get(url="https://api.openweathermap.org/data/2.8/onecall", params=parameters)
response.raise_for_status()
weather_data = response.json()

weather_slice = weather_data["hourly"][:12]

will_rain = False

for hour_data in weather_slice:
    condition_code = int(hour_data["weather"][0]["id"])
    if condition_code < 700:
        will_rain = True

if will_rain:
    my_message = "Es wird innerhalb der nächsten 12 Stunden regnen.\n" \
                 "Du solltest einen Regenschirm mitnehmen. "
else:
    my_message = "Heute regnet es nicht. Hol das Rad raus und spring mal in den Eisbach!"

message_results_json = telegram_bot_send_text(bot_message=my_message)
print(message_results_json)

# print(weather_data["hourly"][6]["weather"][0]["id"])
# print(round(response.json()["hourly"][47]["temp"]-273.15, 3))
