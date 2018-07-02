'''
<<< calendar 0.3 >>>
Text based frontend for the calendar
'''
from __future__ import print_function
import backend as backend
import datetime as dt
import sys

#arbitrary years because this makes me less scared
START_YEAR = 1900
END_YEAR = 2100

calendar_dict = backend.generate_calendar(START_YEAR, END_YEAR)
backend.read_from_file(calendar_dict)

def look_for_response(usr_input, initial = True):
    if usr_input == 'quit' or usr_input == 'q':
        print('closing calendar app')
        sys.exit()
    if usr_input == 'main' or usr_input == 'menu':
        return main()
    if initial == True:
        if usr_input == 'd' or usr_input == 'day':
            return view_day()
        if usr_input == 'm' or usr_input == 'month':
            return view_month()
        if usr_input == 'c' or usr_input == 'create':
            return create_event()
        
def create_event():
    print('text based form to create a new event')
    print('Use current date? Y/N')
    while True:
        usr_input = str(raw_input('user >')).lower()
        look_for_response(usr_input)
        if usr_input == 'y' or usr_input == 'n':
            break
    if usr_input == 'y':
        date = dt.date.today()
        year = date.year
        month = date.month
        day = date.day
    else:
        print('Choose a date. Format: YYYY-MM-DD')
        while True:
            usr_date = str(raw_input('user >')).lower()
            if check_date(date, 'day') == True:
                year = int(usr_date[0:4])
                month = int(usr_date[5:7])-1
                day = int(usr_date[8:10])-1
                processed_date = dt.date(year, month, day)
                break
    print('Choose a title')   
    title = str(raw_input('user >')).lower()
    look_for_response(title)
    new_event = backend.cal_event(date,title)
    backend.write_to_file(new_event)
    calendar_dict[year].date_list[month][day].append(new_event)

def view_day():
    print('\nWhich day? Type: YEAR-MONTH-DAY (0000-00-00)')
    while True:
        usr_input = str(raw_input('>')).lower()
        look_for_response(usr_input)
        if check_date(usr_input, 'day') == True:
            break
    year = int(usr_input[0:4])
    month = int(usr_input[5:7])-1
    day = int(usr_input[8:10])-1
    view_day_pt2(year, month, day)

def view_day_pt2(year, month, day):
    show_day_cal(year, month, day, calendar_dict)
    while True:
        print('\nType \'next\' to view next day, or \'prev\' to view day before.\nType \'main\' or \'menu\' to return to main menu')
        usr_input = str(raw_input('>')).lower()
        look_for_response(usr_input)
        if usr_input == 'next':
            day += 1
            show_day_cal(year, month, day, calendar_dict)
        elif usr_input == 'prev':
            day -= 1
            show_day_cal(year, month, day, calendar_dict)

def view_week():
    pass

def view_month():
    print('\nWhich month? Type: YEAR-MONTH (0000-00)')
    while True:
        usr_input = str(raw_input('>')).lower()
        look_for_response(usr_input)
        if check_date(usr_input, 'month') == True:
            break
    year = int(usr_input[0:4])
    month = int(usr_input[5:7])-1
    view_month_pt2(year, month)

def view_month_pt2(year, month):
    print('showing month calendar for :', year, backend.MONTH_DICT[month])
    backend.print_a_month(year, month, calendar_dict)
    while True:
        print('Type \'d\' followed by a number to show an individual day (d00). Type \'next\' to show next month, or \'prev\' to show previous month')
        print('Type \'main\' or \'menu\' to return to main menu')
        usr_input = str(raw_input('>')).lower()
        look_for_response(usr_input, initial = False)
        if usr_input == 'next':
            month += 1
            print('showing month calendar for :', year, backend.MONTH_DICT[month])
            backend.print_a_month(year, month, calendar_dict)
        elif usr_input == 'prev':
            month -= 1
            print('showing month calendar for :', year, backend.MONTH_DICT[month])
            backend.print_a_month(year, month, calendar_dict)
        elif usr_input[0] == 'd':
            day = int(usr_input[1:])
            view_day_pt2(year, month, day-1)

def check_date(date, check_type):
    if check_type == 'day':
        year = int(date[0:4])
        month = int(date[5:7])-1
        day = int(date[8:10])-1
        if len(date) == 10:
            if (START_YEAR <= year <= END_YEAR):
                if (0 <= month <= 11):
                    if (0 <= day <= 31):
                        return True
                    else:
                        print('invalid day format')
                else:
                    print('invalid month format')
            else:
                print('invalid year format')
        else:
            print('incorrect date format, try again. Use: YEAR-MONTH-DAY (0000-00-00)')
        return False
    elif check_type == 'month':
        year = int(date[0:4])
        month = int(date[5:7])-1
        if len(date) == 7:
            if (START_YEAR <= year <= END_YEAR):
                if (0 <= month <= 11):
                    return True
                else:
                    print('invalid month format')
            else:
                print('invalid year format')
        else:
            print('incorrect date format, try again. Use: YEAR-MONTH-DAY (0000-00-00)')
        return False
    print('invalid check type for check_date')
    return False

def show_day_cal(year, month, day, calendar_dict):
    print('\nShowing day calendar for', calendar_dict[year].date_list[month][day][0])
    print('events on this day: \n')
    print(backend.print_events(calendar_dict[year].date_list[month][day]), end='')

def main():
    print('<<<<<---- MAIN MENU ---->>>>>')
    print('You can view [D]ay, [W]eek, or [M]onth calendars')
    print('Print \'quit\' to exit')
    usr_input = ''
    while usr_input == '':
        #take input from user
        usr_input = str(raw_input('user >')).lower()
        look_for_response(usr_input)

#start program
print('\nWelcome to Adam\'s First Calendar App!!')
while True:
    main()
