from datetime import datetime, timedelta


today = datetime.today().strftime('%Y-%m-%d')


def valid_date(date):
    return True


def within_seven_days(start, end):
    return True


def get_days_prior(n_days):
    dates = [today]
    for i in range(n_days):
        current_day = dates[i]
        yyyy, mm, dd = current_day.split('-')
        current_day = datetime(int(yyyy), int(mm), int(dd))
        previous_day = current_day - timedelta(1)
        dates.append(previous_day.strftime('%Y-%m-%d'))

    return sorted(dates)


def format_date(date):
    return date.strftime('%Y-%m-%d')
