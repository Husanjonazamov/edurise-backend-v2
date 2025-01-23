from datetime import datetime, timedelta

def isDayPairOrEvenCheck(days):
    today = datetime.today()
    week_day = today.weekday()
    if days == 'Toq kunlari' and week_day in [0, 2, 4, 6]:
        return True
    elif days == 'Juft kunlari' and week_day in [1, 3, 5]:
        return True
    return False