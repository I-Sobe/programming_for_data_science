import time
#import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import calendar

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
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
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input("Which city would you like to explore. Type 'Chicago', 'New York City' or 'Washington'?\n").lower()
        if city in CITY_DATA: 
            break
        else:
            print(f"'{city}' is invalid. Please input 'Chicago', 'New York' or 'Washington'.")

    # would you like to filter data by month, day or both. Type None for no time filter

    # get user input for month (all, january, february, ... , june)
    while True:
        month = input("Input first three letter of the month (e.g April=apr) to filter by, or 'all' to apply no month filter.\n").lower()
        if month in ['all', 'jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']:
            break
        else:
            print(f"'{month}' is invalid. Please input 'all' or first three letters only (e.g january=jan).")

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input("Input the first three letters of the day (e.g Monday=mon) to filter by, or 'all' to apply no day filter.\n").lower()
        if day in ['all', 'mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']:
            break
        else:
            print(f"'{day}' is invalid. Please input 'all' or first three letter only (e.g Monday=mon).")
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

    print(f'Loading data for: Location = {city}. Month filter = {month}, Day filter = {day}...')
    # Load data into dataframe
    df = pd.read_csv(CITY_DATA[city])
    # Convert Start Time into datetime format
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # Extract Month and day of week from Start Time
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.strftime('%A')
    df['hour'] = df['Start Time'].dt.hour

    # Filter by month if applicable
    if month != 'all':
        # Use the index of the months list to get the corresponding int
        months = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']
        month = months.index(month) + 1  # Adding 1 to match the month numeric values

        # Filter by month to create the new dataframe
        df = df[df['month'] == month]

    # Filter by day of the week if applicable
    if day != 'all':
        # Filter by day of the week to create the new dataframe
        #df = df[df['day_of_week'] == day.title()]  # Title case to match the day names in the DataFrame
        df = df[df['day_of_week'].str.startswith(day.capitalize())]

    # drop the first column
    df = df.drop(df.columns[0], axis=1)
    return df

def describe(df):
    """
    describes dataframe selected
    """

    print('\nDescribing the selected dataframe...\n')
    start_time = time.time()

    # display the columns in the selected dataframe
    column_values = df.columns.values
    print("Column Values:\n", column_values)

    #briefly explain data contained in dataset.
    if df.shape[1] != '11':
        description = '''
        This dataframe contains 12 datasets as displayed above. Namely:
        Start and End Time: This records the time a ride started and ended. Like the Start Time, it records the time and date of the ride.
        Trip Duration: This records the duration of each trip.
        Start and End Station: This shows the station where each trip commenced and ended.
        User Type: This displays the kind of user that used the ride.
        Gender: Shows the gender of each rider.
        Birth Year: records the Birth year of each user.
        Month: This is a derived dataset, that contains the month each ride was taken.
        Day of Week: This is also a derived dataset and housed the day in the week when the ride was taken,
        Hour: This contains the starting hour of each ride.
        '''
        print(description) 
    else:
        short_description = '''
        This dataframe contains 10 datasets as displayed above. Namely:
        Start and End Time: This records the time a ride started and ended. Like the Start Time, it records the time and date of the ride.
        Trip Duration: This records the duration of each trip.
        Start and End Station: This shows the station where each trip commenced and ended.
        User Type: This displays the kind of user that used the ride.
        Month: This is a derived dataset, that contains the month each ride was taken.
        Day of Week: This is also a derived dataset and housed the day in the week when the ride was taken,
        Hour: This contains the starting hour of each ride.
        
        '''
        print(short_description)   


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    
    # display the most common month
    if not df.empty and 'month' in df:
        common_month_num = df['month'].mode().iloc[0]
        common_month = calendar.month_name[common_month_num]
        print(f"Most Common Month is: {common_month}")
    else:
        print("Sorry, there is no data for the selection made")
    # display the most common day of week
    common_day = df['day_of_week'].mode().iloc[0]
    print("Most Common trip day of week:", common_day)
    # display the most common start hour
    common_hour = df['hour'].mode().iloc[0]
    print(f"Most Common Start Hour is the {common_hour}hr")
    

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    if not df.empty and 'Start Station' in df and 'End Station' in df:
        common_start_station = df['Start Station'].mode().iloc[0]
        print("Most Common Start Station:", common_start_station)
        #display most commonly used end station
        common_end_station = df['End Station'].mode().iloc[0]
        print("Most Common End Station:", common_end_station)
        # display most frequent combination of start station and end station trip
        df['Trip'] = df['Start Station'] + ' to ' + df['End Station']
        common_trip = df['Trip'].mode().iloc[0]
        print("Most Frequent Trip Combination:", common_trip)
    else:
        print("Sorry there is no Trip data for the selection made ")
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration in seconds...\n')
    start_time = time.time()
    if not df.empty and 'Trip Duration' in df:
        # display total travel time
        total_travel_time = df['Trip Duration'].sum()
        print(f"Total Travel time is {total_travel_time}sec")

        # display mean travel time
        mean_travel_time = df['Trip Duration'].mean()
        print("Mean Travel Time:", mean_travel_time) 
    else:
        print("Sorry, there is no data for the selection made.")
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()
    if not df.empty and 'User Type' in df:
        # Display counts of user types
        user_types = df['User Type'].value_counts()
        print("Counts of User Types:\n", user_types)
    else: 
        print("Sorry, there is no data for the selection made.")
    # Display counts of gender. some dataset does't have gender and birth column
    if not df.empty and 'Gender' in df:
        gender_counts = df['Gender'].value_counts()
        print(f'\nCounts of Gender: \n {gender_counts}')
    else:
        print(f"\n There's no 'Gender' data for the selection made.")

    # Display earliest, most recent, most common year of birth and users by age group(generations)
    if not df.empty and 'Birth Year' in df:
        earliest_birth_year = int(df['Birth Year'].min())
        most_recent_birth_year = int(df['Birth Year'].max())
        most_common_birth_year = int(df['Birth Year'].mode().iloc[0])
        print(f'\nOldest rider is: \n {earliest_birth_year}')
        print(f'Youngest Rider is: \n {most_recent_birth_year}')
        print(f'Most Common Birth Year is: {most_common_birth_year}')

        df['age'] = 2023 - df['Birth Year'] 
        # using pandas_cut function to cut the age column.
        # create the bin_edges that will be used to cut the data into groups.
        bin_edges = [1, 22, 38.0, 54.0, 100]

        # create labels for the new categories.
        # Gen_Z(1-22), Milennials(19-38.0), Gen_X(38.0-54.0), Bloomers(54-100)
        bin_names = ['Gen Z', 'Millennials', 'Gen X', 'Bloomers']

        # puting the pandas_cut function to use
        df['age_groups'] = pd.cut(df['age'], bin_edges, labels = bin_names)

        #display age stratification
        age_group_counts = df['age_groups'].value_counts()
        print(f'Age distribution is: {age_group_counts}')

    else:
        print(f"Sorry, there's no 'Birth year' data for the selection made.")
 
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        describe(df)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        start = 0
        batch_size = 5

        while start < len(df):
            show_raw_data = input("\nType 'yes' if you would like to see the next 5 lines of raw data or 'no' to exit.\n").lower()
    
            if show_raw_data in ['yes', 'yea', 'yeah']:
                if not df.empty:
                    pd.set_option('display.max_columns', None)
                    raw_data = df.iloc[start:start+batch_size, :]
                    print(raw_data)
                    start += batch_size
                else:
                    print("Sorry, there is no raw data to display based on your selection.")
            elif show_raw_data in ['no']:
                break
        else:
            print("Invalid input. Please type 'yes' to see more data or 'no' to exit.")


        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
