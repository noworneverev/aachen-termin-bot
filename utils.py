import datetime
from typing import Final
import enum

KATSCHHOF_CHANNEL_ID_01: Final = '-1001917130132'
KATSCHHOF_CHANNEL_ID_02: Final = '-1001929585127'
KATSCHHOF_CHANNEL_ID_03: Final = '-1001916939289'
KATSCHHOF_CHANNEL_ID_04: Final = '-1001947251124'
KATSCHHOF_CHANNEL_ID_05: Final = '-1001956456096'
KATSCHHOF_CHANNEL_ID_06: Final = '-1001933128610'
KATSCHHOF_CHANNEL_ID_07: Final = '-1001917823310'
KATSCHHOF_CHANNEL_ID_08: Final = '-1001926828618'
KATSCHHOF_CHANNEL_ID_09: Final = '-1001979649417'
KATSCHHOF_CHANNEL_ID_10: Final = '-1001714223745'
KATSCHHOF_CHANNEL_ID_11: Final = '-1001920932827'
KATSCHHOF_CHANNEL_ID_12: Final = '-1001910197421'

BAHNHOFPLATZ_CHANNEL_ID_01: Final = '-1001843530956'
BAHNHOFPLATZ_CHANNEL_ID_02: Final = '-1001835882216'
BAHNHOFPLATZ_CHANNEL_ID_03: Final = '-1001924195962'
BAHNHOFPLATZ_CHANNEL_ID_04: Final = '-1001937927958'
BAHNHOFPLATZ_CHANNEL_ID_05: Final = '-1001669496886'
BAHNHOFPLATZ_CHANNEL_ID_06: Final = '-1001847798054'
BAHNHOFPLATZ_CHANNEL_ID_07: Final = '-1001885031649'
BAHNHOFPLATZ_CHANNEL_ID_08: Final = '-1001972041919'
BAHNHOFPLATZ_CHANNEL_ID_09: Final = '-1001959171341'
BAHNHOFPLATZ_CHANNEL_ID_10: Final = '-1001878260812'
BAHNHOFPLATZ_CHANNEL_ID_11: Final = '-1001904052376'
BAHNHOFPLATZ_CHANNEL_ID_12: Final = '-1001881457658'

class Location(enum.Enum):    
    Katschhof = "Bürgerservice Katschhof"
    Bahnhofplatz = "Bürgerservice Bahnhofplatz"

def get_next_months(num_months):
    current_date = datetime.date.today()
    months = []
    years = []

    for _ in range(num_months):
        current_year = current_date.year
        current_month = current_date.month
        months.append(str(current_month).zfill(2))  # Convert month to string and pad with zeros if needed
        years.append(str(current_year))

        # Calculate the next month
        current_month += 1
        if current_month > 12:
            current_month = 1
            current_year += 1

        current_date = datetime.date(current_year, current_month, 1)

    return months, years

def is_date_within_n_days(date_string: str, days: int) -> bool:
    """
    Extract the date from the string and check if it is within a given number of days from today.
    
    Args:
    date_string (str): The input string containing a date in the format 'Day, dd.mm.yyyy'.
    days (int): The number of days to compare with.
    
    Returns:
    bool: True if the date is within the specified number of days from today, False otherwise.
    """
    from datetime import datetime
    
    date_format = "%d.%m.%Y"
    extracted_date = datetime.strptime(date_string.split(", ")[1], date_format)
    
    today = datetime.today()
    
    date_difference = abs((extracted_date - today).days)
    
    return date_difference < days

def get_channel_id(loc: Location, month: str):
    month_dict = {}
    if loc == Location.Katschhof:
        month_dict = {
            "01": KATSCHHOF_CHANNEL_ID_01,
            "02": KATSCHHOF_CHANNEL_ID_02,
            "03": KATSCHHOF_CHANNEL_ID_03,
            "04": KATSCHHOF_CHANNEL_ID_04,
            "05": KATSCHHOF_CHANNEL_ID_05,
            "06": KATSCHHOF_CHANNEL_ID_06,
            "07": KATSCHHOF_CHANNEL_ID_07,
            "08": KATSCHHOF_CHANNEL_ID_08,
            "09": KATSCHHOF_CHANNEL_ID_09,
            "10": KATSCHHOF_CHANNEL_ID_10,
            "11": KATSCHHOF_CHANNEL_ID_11,
            "12": KATSCHHOF_CHANNEL_ID_12
        }
    elif loc == Location.Bahnhofplatz:
        month_dict = {
            "01": BAHNHOFPLATZ_CHANNEL_ID_01,
            "02": BAHNHOFPLATZ_CHANNEL_ID_02,
            "03": BAHNHOFPLATZ_CHANNEL_ID_03,
            "04": BAHNHOFPLATZ_CHANNEL_ID_04,
            "05": BAHNHOFPLATZ_CHANNEL_ID_05,
            "06": BAHNHOFPLATZ_CHANNEL_ID_06,
            "07": BAHNHOFPLATZ_CHANNEL_ID_07,
            "08": BAHNHOFPLATZ_CHANNEL_ID_08,
            "09": BAHNHOFPLATZ_CHANNEL_ID_09,
            "10": BAHNHOFPLATZ_CHANNEL_ID_10,
            "11": BAHNHOFPLATZ_CHANNEL_ID_11,
            "12": BAHNHOFPLATZ_CHANNEL_ID_12
        }
    
    return month_dict.get(month, "CHANNEL_ID_NOT_FOUND")
