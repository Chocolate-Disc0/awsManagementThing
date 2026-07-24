import time
import datetime

# print((17 - time.localtime()[3] - 1) * 3600 + (60 - time.localtime()[4]) * 60)
# print(17 - time.localtime()[3] - 1)

dayLetter = datetime.datetime.now().strftime("%a")
day = datetime.datetime.now().weekday()

print(dayLetter, day)