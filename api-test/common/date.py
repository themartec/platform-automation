from datetime import date


def get_date_as_yyyymmdd():
    # Get the current date object
    today = date.today()

    # Format the date object as YYYY-MM-DD
    return today.strftime("%Y-%m-%d")
