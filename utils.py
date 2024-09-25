import datetime

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

# Example usage
# is_date_within_n_days("Mittwoch, 04.11.2024", 50)


if __name__ == "__main__":
    next_months, next_years = get_next_months(4) 
    print(next_years)
