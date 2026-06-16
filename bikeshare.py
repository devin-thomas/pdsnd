import time
from pathlib import Path

import pandas as pd

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
MONTH_OPTIONS = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
DAY_OPTIONS = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday',
               'saturday', 'sunday']


def get_available_cities():
    """Returns the cities with CSV files available in the local project."""
    available = [city for city, filename in CITY_DATA.items() if Path(filename).exists()]
    return available or list(CITY_DATA)


def prompt_for_choice(label, options):
    """Prompts until the user enters one of the allowed lowercase options."""
    options_text = ', '.join(options)

    while True:
        value = input(f'Please choose a {label} ({options_text}):\n').strip().lower()
        if value in options:
            return value

        print(f"Sorry, '{value}' is not a valid {label}. Please try again.")

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    city = prompt_for_choice('city', get_available_cities())
    month = prompt_for_choice('month', MONTH_OPTIONS)
    day = prompt_for_choice('day', DAY_OPTIONS)

    print('-'*40)
    return city, month, day


def load_city_data(city):
    """Loads a city CSV and prepares the datetime columns used in analysis."""
    file_path = Path(CITY_DATA[city])
    if not file_path.exists():
        raise FileNotFoundError(
            f"Could not find '{file_path.name}' in the project directory."
        )

    df = pd.read_csv(file_path)
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name().str.lower()
    df['start_hour'] = df['Start Time'].dt.hour
    return df


def filter_by_month(df, month):
    """Returns a filtered DataFrame for the selected month when requested."""
    if month == 'all':
        return df

    month_number = MONTH_OPTIONS.index(month)
    return df[df['month'] == month_number]


def filter_by_day(df, day):
    """Returns a filtered DataFrame for the selected day when requested."""
    if day == 'all':
        return df

    return df[df['day_of_week'] == day]


def get_mode(series):
    """Returns the most common value from a Series."""
    return series.mode().iat[0]


def print_counts(series):
    """Prints value counts in a simple label and count format."""
    for label, count in series.value_counts().items():
        print(f'{label}: {count}')


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = load_city_data(city)
    df = filter_by_month(df, month)
    df = filter_by_day(df, day)
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    common_month = MONTH_OPTIONS[get_mode(df['month'])]
    common_day = get_mode(df['day_of_week']).title()
    common_hour = get_mode(df['start_hour'])

    print(f'Most common month: {common_month.title()}')
    print(f'Most common day of week: {common_day}')
    print(f'Most common start hour: {common_hour}')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    common_start_station = get_mode(df['Start Station'])
    common_end_station = get_mode(df['End Station'])
    common_trip = get_mode(df['Start Station'] + ' -> ' + df['End Station'])

    print(f'Most commonly used start station: {common_start_station}')
    print(f'Most commonly used end station: {common_end_station}')
    print(f'Most frequent trip: {common_trip}')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    total_travel_time = df['Trip Duration'].sum()
    mean_travel_time = df['Trip Duration'].mean()

    print(f'Total travel time: {total_travel_time:.0f} seconds')
    print(f'Average travel time: {mean_travel_time:.2f} seconds')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    print('User Types:')
    print_counts(df['User Type'])
    print()

    if 'Gender' in df.columns:
        print('Gender:')
        print_counts(df['Gender'])
        print()
    else:
        print('Gender data is not available for this city.\n')

    if 'Birth Year' in df.columns:
        birth_years = df['Birth Year'].dropna()
        if not birth_years.empty:
            print(f'Earliest birth year: {int(birth_years.min())}')
            print(f'Most recent birth year: {int(birth_years.max())}')
            print(f'Most common birth year: {int(get_mode(birth_years))}')
        else:
            print('Birth year data is not available for this selection.')
    else:
        print('Birth year data is not available for this city.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
