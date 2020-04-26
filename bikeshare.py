import pandas as pd
from datetime import datetime
from datetime import timedelta
import time

city_data = { 'Chicago': 'chicago.csv',
              'New York city': 'new_york_city.csv',
              'Washington': 'washington.csv' }
## Filenames
#chicago = 'chicago.csv'
#new_york_city = 'new_york_city.csv'
#washington = 'washington.csv'


def input_data(in_dict):
    input_data = ""
    while input_data.lower() not in in_dict.keys():
        input_data = input()
        if input_data.lower() not in in_dict.keys():
            print('..')
            print('Given NUMBER only :) Please try again')
    input_data = in_dict[input_data.lower()]
    return input_data


def get_city():
    '''Asks the user for a city and returns the filename for that city's bike share data.
    Args:
        none.
    Returns:
        (str) Filename for a city's bikeshare data.
    '''
    city = ""
    city_dict = {'1': 'Chicago', '2': 'New York city', '3': 'Washington'}
    in_dict = city_dict
    city = input_data(in_dict)
    return city


def get_month():
    '''Asks the user for a month and returns the specified month.
    Args:
        none.
    Returns:
        (tuple) Lower limit, upper limit of month for the bikeshare data.
    '''
    print('Which month?')
    print('[1]January, [2]February, [3]March,[4] April, [5]May, [6]June  :')
    month = ""
    month_dict = {'1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6}
    in_dict = month_dict
    month = input_data(in_dict)
    return ('2017-{}'.format(month), '2017-{}'.format(month + 1))


def get_day():
    '''Asks the user for a day and returns the specified day.
    Args:
        none.
    Returns:
        (tuple) Lower limit, upper limit of date for the bikeshare data.
    '''
    this_month = get_month()[0]
    month = int(this_month[5:])
    valid_date = False
    while valid_date == False:
        is_int = False
        day = input('\nWhich day? Please type your response as an integer.\n')
        while is_int == False:
            try:
                day = int(day)
                is_int = True
            except ValueError:
                print('Sorry, I do not understand your input. Please type your'
                      ' response as an integer.')
                day = input('\nWhich day? Please type your response as an integer.\n')
        try:
            start_date = datetime(2017, month, day)
            valid_date = True
        except ValueError as e:
            print(str(e).capitalize())
    end_date = start_date + timedelta(days=1)
    return (str(start_date), str(end_date))

def popular_month(df):
    '''Finds and prints the most popular month for start time.
    Args:
        bikeshare dataframe
    Returns:
        most_pop_month
    '''
    months = ['January', 'February', 'March', 'April', 'May', 'June']
    index = int(df['start_time'].dt.month.mode())
    most_pop_month = months[index - 1]
    return most_pop_month


def popular_day(df):
    '''Finds and prints the most popular day of week (Monday, Tuesday, etc.) for start time.
    Args:
        bikeshare dataframe
    Returns:
        most_pop_day
    '''
    days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday',
                    'Saturday', 'Sunday']
    index = int(df['start_time'].dt.dayofweek.mode())
    most_pop_day = days_of_week[index]
    return most_pop_day

def popular_hour(df):
    '''Finds and prints the most popular hour of day for start time.
    Args:
        bikeshare dataframe
    Returns:
        pop_hour_readable, am_pm
    '''
    most_pop_hour = int(df['start_time'].dt.hour.mode())
    if most_pop_hour == 0:
        am_pm = 'am'
        pop_hour_readable = 12
    elif 1 <= most_pop_hour < 13:
        am_pm = 'am'
        pop_hour_readable = most_pop_hour
    elif 13 <= most_pop_hour < 24:
        am_pm = 'pm'
        pop_hour_readable = most_pop_hour - 12

    return pop_hour_readable, am_pm

def trip_duration(df):
    '''Finds and prints the total trip duration and average trip duration in
       hours, minutes, and seconds.
    Args:
        bikeshare dataframe
    Returns:
        hour, minute, m
    '''
    total_duration = df['trip_duration'].sum()
    minute, second = divmod(total_duration, 60)
    hour, minute = divmod(minute, 60)


    average_duration = round(df['trip_duration'].mean())
    m, s = divmod(average_duration, 60)
    return hour, minute, m



def popular_stations(df):
    '''Finds and prints the most popular start station and most popular end station.
    Args:
        bikeshare dataframe
    Returns:
        pop_start, pop_end, 1,0
    '''
    pop_start = df['start_station'].mode().to_string(index = False)
    pop_end = df['end_station'].mode().to_string(index = False)
    if pop_start==pop_end:
        return pop_start, 0
    else:
        return pop_start, pop_end, 1

def popular_trip(df):
    '''Finds and prints the most popular trip.
    Args:
        bikeshare dataframe
    Returns:
        most_pop_trip
    '''
    most_pop_trip = df['journey'].mode().to_string(index = False)
    return  most_pop_trip

def users(df):
    '''Finds and prints the counts of each user type.
    Args:
        bikeshare dataframe
    Returns:
        subs, cust
    '''
    subs = df.query('user_type == "Subscriber"').user_type.count()
    cust = df.query('user_type == "Customer"').user_type.count()
    return subs, cust

def gender(df):
    '''Finds and prints the counts of gender.
    Args:
        bikeshare dataframe
    Returns:
        male_count, female_count
    '''
    male_count = df.query('gender == "Male"').gender.count()
    female_count = df.query('gender == "Female"').gender.count()
    return male_count, female_count

def birth_years(df):
    ''' Finds and prints the earliest (i.e. oldest user), most recent (i.e.
        youngest user), and most popular birth years.
    Args:
        bikeshare dataframe
    Returns:
        earliest, latest, mode
    '''
    earliest = int(df['birth_year'].min())
    latest = int(df['birth_year'].max())
    mode = int(df['birth_year'].mode())
    return earliest, latest, mode



def random_data(df):
    '''Displays five lines of data if the user specifies that they would like to.
    After displaying five lines, ask the user if they would like to see five more,
    continuing asking until they say stop.
    Args:
        data frame
    Returns:
        none
    '''
    head = 0
    tail = 5
    random_input = ""
    random_dict = {'1': 1, '2': 2, '3': 3}
    in_dict = random_dict
    random_more = 1
    while random_more == 1:
        print("\nDo you want to view indiviual trip data?")
        print("[1]Yes, [2]No, I'm done, [3]I'm excited to explore more. Restart")
        random_input = input_data(in_dict)
        if random_input == 1:
            print(df[df.columns[0:-1]].iloc[head:tail])
            head += 5
            tail += 5
        elif random_input == 2:
            break
        elif random_input == 3:
            statistics()



def get_filter(df):
    '''Asks the user for a time period and returns the specified filter.
    Args:
        none.
    Returns:
        (str) Time filter for the bikeshare data.
    '''
    get_filter_dict = {'1': 'month', '2': 'day', '3': 'none'}
    in_dict = get_filter_dict
    filter = input_data(in_dict)
    if filter == 'none':
        df_filter = df
        filter_lower = df['start_time'].min()
        filter_upper = df['end_time'].max()
    elif filter == 'month' or filter == 'day':
        if filter == 'month':
            filter_lower, filter_upper = get_month()
        elif filter == 'day':
            filter_lower, filter_upper = get_day()
        print('Filtering data...')
        df_filter = df[(df['start_time'] >= filter_lower) & (df['start_time'] < filter_upper)]
    return df_filter,  filter_lower, filter_upper

def new_collumn(df):
    '''creates a 'journey' column'''
    new_labels = []
    for col in df.columns:
        new_labels.append(col.replace(' ', '_').lower())
    df.columns = new_labels
    pd.set_option('max_colwidth', 100)
    df['journey'] = df['start_station'].str.cat(df['end_station'], sep=' to ')


def statistics():
    '''Calculates and prints out the descriptive statistics about a city and
    time period specified by the user via raw input.
    Args:
        none.
    Returns:
        none.
    '''
    # Filter by city (Chicago, New York, Washington)
    print('Hi. Let explore Bikeshare figures of Chicago, New York or Washington')
    print('Which city do you most interested in')
    print('[1]Chicago,[2]]New York,[3]Washington: ')
    city = get_city()
    print('......................................')
    df = pd.read_csv(city_data[city], parse_dates = ['Start Time', 'End Time'])

    new_collumn(df)

    d1 = popular_month(df)
    print ('\n Significant of {} custumer used Bikeshare in {}. Do you interested more in'.format(city,d1))
    print('[1]a specific Month,\n[2]a specific day,\n[3]more detail, please. ')
    start_time = time.time()

    d0 = get_filter(df)
    df_filtered = d0[0]
    d2=popular_day(df_filtered)
    d3=popular_hour(df_filtered)
    d4=trip_duration(df_filtered)
    d5=popular_stations(df_filtered)
    d6=popular_trip(df_filtered)
    d7=users(df_filtered)

    print ('Data from {} to {}'.format(d0[1],d0[2]))
    print ('The service was busiest at {}{}. Bikeshare served {} hours and {} minutes with the average trip is {} minutes.{} seemed to be the most popular station, while custumer loved using Bikeshare to travel from{}'.format(d3[0],d3[1],d4[0],d4[1],d4[2],d5[0],d6))
    if city == 'Chicago' or city == 'New York city':
        d8 = gender(df_filtered)
        d9=birth_years(df_filtered)
        d10=2017-d9[2]
        print ('\nBikeshare had {} Subscribers and {} Customers during the given time, {} male and {} female with average age is {}. The oldest and youngest users are born in {} and {}, respectively'.format(d7[0],d7[1],d8[0],d8[1],d10,d9[0],d9[1]))
    if city == 'Washington':
        print('\nBikeshare had {} Subscribers and {} Customers during the given time. Unfortunately,no gender and birth year data available for {}'.format(d7[0],d7[1],city))

    print("\nEnd Report!.\nThat took %s seconds." % (time.time() - start_time))
    print("")

    random_data(df_filtered) # Display five lines from data



if __name__ == "__main__":
	statistics()
