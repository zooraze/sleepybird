import datetime
import json


def current_time():
    """Current date and time.

    Returns:
        str: YYYY-MM-DD HH:MM:SS
    """
    currentDT = datetime.datetime.now()

    return currentDT.strftime("%Y-%m-%d %H:%M:%S")


def cache_results(self, results):
    """Cache query results.

    Args:
        results (iterator): 

    """
