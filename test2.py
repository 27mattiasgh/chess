import datetime

x = "Good Morning!" if 5 <= datetime.datetime.now().hour < 12 else "Good Afternoon!" if 12 <= datetime.datetime.now().hour < 18 else "Good Evening!"

