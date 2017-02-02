from datetime import date
import calendar

def obradadatuma(value):
    if value == None:
        value = raw_input("Unesite datum (format dd-mm-yyyy) >>  ")
    day = datum(value)
    return day

def datum(value):
    dan,mesec,godina = value.split('-')
    day = calendar.day_name[date(eval(godina), eval(mesec), eval(dan)).weekday()]

    if day == 'Monday':
        day = 'pon'
    elif day == 'Tuesday':
        day = 'uto'
    elif day == 'Wednesday':
        day = 'sre'
    elif day == 'Thursday':
        day = 'cet'
    elif day == 'Friday':
        day = 'pet'
    elif day == 'Saturday':
        day = 'sub'
    elif day == 'Sunday':
        day = 'ned'
    return day
