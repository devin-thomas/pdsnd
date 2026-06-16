import time
from pathlib import Path

import pandas as pd
import numpy as np

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

    # display the most common month


    # display the most common day of week


    # display the most common start hour


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station


    # display most commonly used end station


    # display most frequent combination of start station and end station trip


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time


    # display mean travel time


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types


    # Display counts of gender


    # Display earliest, most recent, and most common year of birth


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
