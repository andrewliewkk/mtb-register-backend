# config.py
from pydantic import BaseSettings
from datetime import datetime
import pytz

def get_current_timestamp():
    dateTimeObj = datetime.now(tz=pytz.timezone('Asia/Singapore'))
    timestampStr = [
        dateTimeObj.strftime("%a, %I:%M %p (%d %b %Y)"),
    ]
    return '%0A'.join(str(line) for line in timestampStr)

class Settings(BaseSettings):
    TOKEN: str = '5689105990:AAFHgxeTBmUS49zzm9K0ZIOROqofVS783ec'
    CHAT_ID: str = '-1001794946374'
    MESSAGE_ID: int = 6
    BASE_URL: str = f'https://api.telegram.org/bot{TOKEN}/editMessageText?chat_id={CHAT_ID}&message_id=6&text=hello+world2'
    MONGODB_URL: str ="mongodb+srv://boyrawks:t050829682@mtb.5jq2ed0.mongodb.net/registration?retryWrites=true&w=majority"
    TELEGRAM_NEW_LINE: str = '%0A'
    SCHEDULE_TEXT_TIMESTAMP = get_current_timestamp()

# global instance
settings = Settings()

