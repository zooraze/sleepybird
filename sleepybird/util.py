import datetime

def current_time():
    """Current date and time.

    Returns:
        str: YYYY-MM-DD HH:MM:SS
    """
    currentDT = datetime.datetime.now()

    return currentDT.strftime("%Y-%m-%d %H:%M:%S")