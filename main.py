import requests
import smtplib
from twilio.rest import Client
import os

MY_EMAIL = os.environ.get("MY_EMAIL")
MY_PASSWORD = os.environ.get("MY_PASSWORD")

account_sid = os.environ.get("ACCOUNT_SID")
auth_token = os.environ.get("AUTH_TOKEN")


# api_key = os.environ.get("OWM_API_KEY")
api_key = "7879606910a9c3080a6767c5690fff1e"

parameters = {
    "lat": 52.084770,
    "lon": 0.436800,
    "appid": api_key,
    "cnt": 4,
}
response = requests.get(url="https://api.openweathermap.org/data/2.5/forecast", params=parameters)
response.raise_for_status()
weather_data = response.json()

will_rain = False
for hour_data in weather_data["list"]:
    condition_code = hour_data["weather"][0]["id"]
    if condition_code < 700:
        will_rain = True
if will_rain:
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(MY_EMAIL, MY_PASSWORD)
        connection.sendmail(
            from_addr=MY_EMAIL,
            to_addrs="jackblakework@gmail.com",
            msg="Subject: Weather Notification!\n\nIn for a chance of rain today, take an umbrella!"
        )
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        body="In for a chance of rain today, take an umbrella!☂️",
        from_="+447455717206",
        to="+447821003400",
    )
print(message.status)
