import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

MONTH_DATA = ['all', 'january', 'february', 'march', 'april', 'may', 'june']

DAY_DATA = ['all', 'monday', 'tuesday', 'wednesday', 'friday', 'saturday', 'sunday']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter

    Would you like to see data for Chicago, New York, or Washington?
    Would you like to filter the data by month, day, or not at all?
    (If they chose month) Which month - January, February, March, April, May, or June?
    (If they chose day) Which day - Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday?

    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input("\nWould you like to see data for Chicago, New York City, or Washington?\n").lower()
        if city.lower() not in CITY_DATA.keys():
            print("Sorry, There is no data about this city in our database. Please try again.")
            continue
        else:
            break

    # get user input for month (all, january, february, ... , june)
    while True:
        month = input("\nWould you like to filter the data by month or not at all? Enter any one of the first 6 months or enter 'All' to select all 6 months.\n").lower()

        if month.lower() not in MONTH_DATA:
            print("Sorry, This is not a month or one of the first 6 months. Please try again.")
            continue
        else:
            break

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input("\nWould you like to filter the data by weekday or not at all, if not at all please enter 'all'\n").lower()

        if day.lower() not in DAY_DATA:
            print("Sorry, This is not a weekday. Please try again.")
            continue
        else:
            break

    print('-'*40)
    return city, month, day


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

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    ## replace dt.weekday_name to day_name since it didn't work on my pc
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
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    common_month = df['month'].mode()[0]
    count_month = df[df['month'] == common_month].shape[0]
    common_month = MONTH_DATA[common_month].title()
    print('Most Common Month: {} Count: {}'.format(common_month,count_month))

    # display the most common day of week
    common_day = df['day_of_week'].mode()[0]
    count_day = df[df['day_of_week'] == common_day].shape[0]
    print('Most Common day: {} Count: {}'.format(common_day,count_day))

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    common_hour = df['hour'].mode()[0]
    count_hour = df[df['hour'] == common_hour].shape[0]
    print('Most Common Hour: {} Count: {}'.format(common_hour,count_hour))

    print("\nThis took %s seconds." % round((time.time() - start_time),3))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start = df['Start Station'].mode()[0]
    count_01 = df[df['Start Station'] == common_start].shape[0]
    print('Most Commonly Used Start Station: {} Count: {}'.format(common_start,count_01))

    # display most commonly used end station
    common_end = df['End Station'].mode()[0]
    count_02 = df[df['End Station'] == common_end].shape[0]
    print('Most Commonly Used End Station: {} Count: {}'.format(common_end,count_02))

    # display most frequent combination of start station and end station trip
    group = df.groupby(['Start Station','End Station']).count()

    common_station_quantity = group['Unnamed: 0'].max()
    common_station_list = group[group['Unnamed: 0'] == common_station_quantity].index.tolist()

    for i in common_station_list:
        print('Most Frequent Combination of Start Station and End Station Trip: Start:{} and End:{}   Count: {}'.format(i[0],i[1],common_station_quantity))

    print("\nThis took %s seconds." % round((time.time() - start_time),3))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('Total Travel Time: {} Seconds'.format(total_travel_time))

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('Mean_Travel_Time: {} Seconds'.format(mean_travel_time))    

    print("\nThis took %s seconds." % round((time.time() - start_time),3))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print('Counts of User Types: ')
    print(user_types)

    # Display counts of gender
    if 'Gender' in df:
        gender_types = df['Gender'].value_counts()
        print('\nCounts of Gender: ')
        print(gender_types)

    # Display earliest, most recent, and most common year of birth

    if 'Birth Year' in df:

        print('\nStats of Birth Year: ')
        earliest_year = int(df['Birth Year'].min())
        most_recent_year = int(df['Birth Year'].max())
        most_common_year = int(df['Birth Year'].mode()[0])
        print('Earliest Birth Year: {}'.format(earliest_year))
        print('Most Recent Birth Year: {}'.format(most_recent_year))
        print('Most Common Birth Year: {}'.format(most_common_year) )

    print("\nThis took %s seconds." % round((time.time() - start_time),3))
    print('-'*40)

def raw_data(df):

    index = 5
    ans_initial = input('\nWould you like to check raw data? (Yes or No).\n')
    if ans_initial.lower() == 'yes':
        # set_option('display.max_columns',200) means display all the columns
        pd.set_option('display.max_columns',200)
        print(df.head())

        while True:
            ans_second = input('\nWould you like to check next 5 raw data? (Yes or No).\n')
            if ans_second.lower() == 'yes':
                pd.set_option('display.max_columns',200)
                print(df.iloc[index:index+5])
                index += 5
            else:
                break


def main():
    while True:
        city, month, day = get_filters()

        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        raw_data(df)

        while True:
            restart = input('\nWould you like to restart? Enter yes or no.\n')

            if restart.lower() == 'yes':
                break
            elif restart.lower() == 'no':
                exit()
            else:
                print('\nTry again, Enter yes or no.\n')
                continue

if __name__ == "__main__":
	main()
