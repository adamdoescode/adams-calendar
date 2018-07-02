'''
<<<    calendar v3    >>>

This file contains backend features for Adam's first calendar.
TODO
- Create "view week" functionality

- create a text based tkinter GUI to explore calendar and create user defined cal_events
'''
from __future__ import print_function #because it's easier to use
import datetime as dt
import os

TEST_FOLDER_DIR = 'C:\\Users\\laserbeams\\Dropbox\\pythoncode\\calendar\\test_data\\'

MONTH_DICT = {0:'January',1:'Febuary',2:'March',3:'April',4:'May',5:'June',6:'July',7:'August',8:'September',9:'October',10:'November',11:'December'}

class cal_event:
    def __init__(self, entered_date, entered_title):
        self.date = entered_date #should be a datetime.date object
        self.title = entered_title #should be a string

    #these class methods add various attributes to the event if required
    def location(self, location):
        self.location = location

    def description(self, description):
        self.description = description

    ''' #Breaks when I try to save cal_event objects to file
    def specific_time(self, start_time, end_time):
        self.start_time = start_time
        self.end_time = end_time
    '''

class calendar_year:
    #creates a calendar year based off input 'year' var with format: [month][day][event object index]
    def __init__(self, year):
        feb_day_count = is_leap_year(year)
        days_per_month = [31,feb_day_count,31,30,31,30,31,31,30,31,30,31]
        
        #initialise date_list att with months
        self.date_list = [[] for x in range(len(days_per_month))]

        #add days to each month
        for i in range(len(days_per_month)):
            for j in range(days_per_month[i]):
                self.date_list[i].append([dt.date(year,i+1,j+1)])

def is_leap_year(year):
    #checks if (year) is a leap year and then returns the number of days in febuary for that year
    if ((year % 4 == 0) and (year % 100 != 0)) or (year % 400 == 0):
        return 29
    else:
        return 28

def write_to_file(event):
    '''Attributes for event objects are a three letter code that precedes what the attribute contains. E.g 'dat' indicates that what follows is a date '''
    #writes an event object to file. Needs to include all atts and the date
    save_file = open(TEST_FOLDER_DIR + 'cal_events.txt', 'a') #TODO in final version you need to make this not overwrite the existing file
    
    event_str = '<dat' + str(event.date) + '<tit' + str(event.title)
    if type(event.location) == str:
        event_str += '<loc' + str(event.location)
    if type(event.description) == str:
        event_str += '<des' + str(event.description)

    event_str += '//' #signals end of event written to file
    
    save_file.write(event_str)
    save_file.close()

def read_from_file(calendar_dict):
        #reads events from file and populates the calendar
        save_file = open(TEST_FOLDER_DIR + 'cal_events.txt', 'r')
        save_file_str = save_file.read()
        events_from_file = save_file_str.split('//')
        for event in events_from_file:
            #reset variables:
            year = 0
            month = 0
            day = 0
            title = ''
            location = ''
            description = ''

            if event != '':
                #process individual events...
                event_atts = event.split('<')
                for att in event_atts:

                    if att[0:3] == 'dat': #date YYYY-MM-DD
                        dat_atts = att.split('-')
                        year = int(str(dat_atts[0][3:7]))
                        month = int(str(dat_atts[1]))
                        day = int(str(dat_atts[2]))
                    
                    if att[0:3] == 'tit':
                        title = str(att[3:])
                    
                    if att[0:3] == 'des':
                        description = att[3:]
                    
                    if att[0:3] == 'loc':
                        location = att[3:]

                #adds attributes to a new cal_event object
                new_event = cal_event(dt.date(year,month,day),title)
                new_event.description(description)
                new_event.location(location)

                calendar_dict[year].date_list[month-1][day-1].append(new_event)

def generate_calendar(start_year, end_year):
    calendar_dict = {}
    for i in range(start_year, end_year, 1):
        calendar_dict[i] = calendar_year(i)
    return calendar_dict

def print_events(event_list):
    for i in range(1, len(event_list)):
        print('Event ', i)
        print('date:', event_list[i].date)
        print('title:', event_list[i].title)
        print('description:', event_list[i].description)
        print('location:', event_list[i].location, '\n')

def print_a_month(year, month, calendar_dict):
    print('Showing\t', MONTH_DICT[month], '\n', end='')
    counter = 0
    for i in calendar_dict[year].date_list[month]:
        counter += 1
        print(i[0].day, '*'*(len(i)-1), '\t', end ='')
        if counter % 7 == 0:
            print('\n', end='')
    print('\n\n', end='')

class debug():
    def __init__(self):
        print('Debug code initialised')

    def basic_front(self):
        #below is debug code, needed to generate a calendar dictionary
        calendar_dict = generate_calendar(1900,2100) #stores the entire calendar data structure: calendar_dict[year] = calendar_year object([month][day][event object index])

        read_from_file(calendar_dict)

        event_list = calendar_dict[2017].date_list[2][4]

        print_events(event_list)
    
    def generate_events_to_save(self):
        save_file = open('cal_events.txt', 'w')
        save_file.close()

        event = cal_event(dt.date(2017,3,4), 'go to school')
        event.description = 'cake for recess'
        calendar_dict[2017].date_list[2][3].append(event)
        write_to_file(event)

        event2 = cal_event(dt.date(2017,3,6), 'job interview cake')
        event2.location('Perth CBD')
        calendar_dict[2017].date_list[2][5].append(event2)
        write_to_file(event2)

        event3 = cal_event(dt.date(2017,3,5), 'go to work')
        calendar_dict[2017].date_list[2][4].append(event3)
        write_to_file(event3)

        event4 = cal_event(dt.date(2017,3,5), 'go to interview')
        event4.description('I like robots')
        calendar_dict[2017].date_list[2][4].append(event3)
        write_to_file(event4)

if __name__ == '__main__':
    debug_methods = debug()
    debug_methods.basic_front()
