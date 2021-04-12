import time
import datetime
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    # get user input for city (Chicago, New York , Washington).
    input_city_valid = False
    while input_city_valid == False:
        city = input('\nWould you like to see data for Chicago, New York or Washington?\n')
        valid_cities = ['Chicago', 'New York', 'Washington']

        if city not in valid_cities:
            print('\n{} is invalid input. Please try again.\n'.format(city))
        else:
            input_city_valid = True
            print('\nLooks like you want to hear about {}! If this is not true, restart the program now'.format(city))
            city = city.lower()

    # get user input if time filter should be used
    input_time_valid = False
    while input_time_valid == False:
        time_filter = input('\nWould you like to filter the data by month, day, both, or not at all? \nType "none" for no time filter.\n')
        valid_time_filters = ['month', 'day', 'both', 'none']

        if time_filter not in valid_time_filters:
            print('\n{} is invalid input.\n'.format(time_filter))
        else:
            input_time_valid = True

    # get user input for month filter
    if time_filter == 'month':
        day = 'all'
        input_month_valid = False

        while input_month_valid == False:
            month = input('\nWe will make sure to filter by month. Which month?\nJanuary, February, March, April, May or June?\n')
            valid_months = ['January', 'February', 'March', 'April', 'May', 'June']

            if month not in valid_months:
                print('\n{} is invalid input. Please try again.\n'.format(month))
            else:
                input_month_valid = True
                month = month.lower()

    # get user input for day filter
    elif time_filter == 'day':
        month = 'all'
        input_day_valid = False

        while input_day_valid == False:
            day = input('\nWe will make sure to filter by day. Which day?\nMonday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday?\n')
            valid_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

            if day not in valid_days:
                print('\n{} is invalid input. Please try again.\n'.format(day))
            else:
                input_day_valid = True

    # get user input both time filters
    elif time_filter == 'both':
        input_month_valid = False

        while input_month_valid == False:
            month = input('\nWe will make sure to filter by month. Which month?\nJanuary, February, March, April, May or June ?\n')
            valid_months = ['January', 'February', 'March', 'April', 'May', 'June']

            if month not in valid_months:
                print('\n{} is invalid input. Please try again.\n'.format(month))
            else:
                input_month_valid = True
                month = month.lower()

        input_day_valid = False

        while input_day_valid == False:
            day = input('\nWe will make sure to filter by day. Which day?\nMonday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday?\n')
            valid_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

            if day not in valid_days:
                print('\n{} is invalid input. Please try again.\n'.format(day))
            else:
                input_day_valid = True

    # set time filters to 'all'
    elif time_filter == 'none':
        day = 'all'
        month = 'all'

    print('\nJust one moment...\nLoading the data for the city of \'{}\' with a time filter for month of \'{}\' and day of \'{}\'.'.format(city.title(), month.title(), day.title()))
    print('-'*60)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - pandas DataFrame containing city data filtered by month and day
    """

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day]


    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    popular_month = df['month'].mode()[0]
    print('The most popular month is: {}'.format(popular_month))



    # display the most common day of week
    popular_weekday = df['day_of_week'].mode()[0]
    print('The most popular weekday is on a: {}'.format(popular_weekday))


    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print('The most popular hour is at: {} o\'clock'.format(popular_hour))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*60)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print('\nThe most commonly start station is:\n{}'.format(popular_start_station))


    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print('\nThe most commonly end station is:\n{}'.format(popular_end_station))

    # display most frequent combination of start station and end station trip
    popular_combination_station = df.groupby(['Start Station', 'End Station']).size().idxmax()
    print('\nThe most frequent combination of start station and end station trip is:\n{}'.format(popular_combination_station))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*60)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('\nTotal travel time:\n{}'.format(str(datetime.timedelta(seconds = total_travel_time))))


    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('\nThe mean travel time is:\n{}'.format(str(datetime.timedelta(seconds=mean_travel_time))))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    try:
        #Display counts of user types
        count_user_types = df['User Type'].value_counts()
        print('\nThe user types are:\n{}'.format(count_user_types))

        # Display counts of gender
        count_gender =  df['Gender'].value_counts()
        print('\nThe genders are:\n{}'.format(count_gender))

        # Display earliest, most recent, and most common year of birth
        earliest_year_birth = df['Birth Year'].min()
        print('\nThe earliest birth year is:\n{}'.format(int(earliest_year_birth)))

        most_recent_year_birth = df['Birth Year'].max()
        print('\nThe most recent birth year is:\n{}'.format(int(most_recent_year_birth)))

        most_common_year_birth = df['Birth Year'].mode()[0]
        print('\nThe most commmon birth year is:\n{}'.format(int(most_common_year_birth)))

    except KeyError:
        print('\nThis dataset does not have Gender and Birth Year infromation. No stats possible.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*60)

def display_data(df):
     """Displays data 5 rows at a time"""

     view_data = input('\nWould you like to view 5 rows of individual trip data? Enter yes or no\n')
     start_loc = 0
     while (view_data == 'yes'):
        print(df.iloc[start_loc: (start_loc +5)])
        start_loc += 5
        view_data = input("Do you wish to continue?: ").lower()

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break



if __name__ == "__main__":
	main()
