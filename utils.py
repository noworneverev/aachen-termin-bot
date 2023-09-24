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

if __name__ == "__main__":
    next_months, next_years = get_next_months(4)  # Change the argument to get more or fewer months
    print(next_years)

    # for month, year in zip(next_months, next_years):
    #     print(f"{month} {year}")    
        # month_name = datetime.date(int(year), int(month), 1).strftime('%B')
        # print(f"{month_name} {year}")