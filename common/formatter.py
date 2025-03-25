import time

BEGIN = time.time()
TIME_DATA = []


def format_time(seconds: int) -> str:
    days = seconds // 86400
    hours = (seconds % 86400) // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60

    days_str = str(days)
    hours_str = str(hours).zfill(2)
    minutes_str = str(minutes).zfill(2)
    seconds_str = str(seconds).zfill(2)
    if days > 0:
        return f"{days_str}D {hours_str}h {minutes_str}m {seconds_str}s"
    if hours > 0:
        return f"{hours_str}h {minutes_str}m {seconds_str}s"
    if minutes > 0:
        return f"{minutes_str}m {seconds_str}s"
    return f"{seconds_str}s"
