import time

BEGIN = time.time()
TIME_DATA = []


def format_time(seconds):
    days = seconds // 86400
    hours = (seconds % 86400) // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60

    days_str = str(days)
    hours_str = str(hours).zfill(2)
    minutes_str = str(minutes).zfill(2)
    seconds_str = str(seconds).zfill(2)
    time_str = ""
    if days > 0:
        time_str += f"{days_str}D {hours_str}h {minutes_str}m {seconds_str}s"
    elif hours > 0:
        time_str += f"{hours_str}h {minutes_str}m {seconds_str}s"
    elif minutes > 0:
        time_str += f"{minutes_str}m {seconds_str}s"
    else:
        time_str += f"{seconds_str}s"
    return time_str
