from .config import settings
import requests

def send_telegram_text_update():
    print("sending request")
    URL: str = f"https://api.telegram.org/bot{settings.TOKEN}/editMessageText?chat_id={settings.CHAT_ID}&message_id={settings.MESSAGE_ID}&text={get_updated_schedule_text()}&parse_mode=html"
    print(URL)
    x = requests.get(URL)
    print(x.text)
    print("Telegram schedule updated")

def get_updated_schedule_text():
    schedule_text = [
        f"Hi, welcome to the TQ scheduler bot!",
        f"Here is the upcoming schedule:",
        f"",
        f"",
        f"",
        f"To add your name in, fill in the form <a href='www.google.com'>here</a>",
        f"",
        f"Last updated:  <b>{settings.SCHEDULE_TEXT_TIMESTAMP}</b>",
    ]
    return settings.TELEGRAM_NEW_LINE.join(str(line) for line in schedule_text)

# def get_registrations_by_date(date):


# def get_upcoming_dates():

# def get_text_from_registrations():