import time
import datetime
from zoneinfo import ZoneInfo

# print((17 - time.localtime()[3] - 1) * 3600 + (60 - time.localtime()[4]) * 60)
# print(17 - time.localtime()[3] - 1)

localTime = ZoneInfo("Asia/Karachi")

dayLetter = datetime.datetime.now(localTime).strftime("%a")
day = datetime.datetime.now(localTime).hour

print(dayLetter, day, "hello")