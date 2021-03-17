# Program author: u/shitilostagain
# Date: 3/16/2021
# Compiles data for 1, 3 and 6 M price increases for dates in the text file 'dateMaster.txt' for
# $QQQ and $SPY

from stockFunctions import *
import pandas as pd
import datetime

out = open("SPY_QQQ.txt", "w")
with open("dateMaster.txt") as f:
    out.write("Date:, SPY1M:, SPY3M:, SPY6M:, QQQ1M:, QQQ3M:, QQQ6M:")
    line = f.readline()
    while line:
        date = str(line[15:25])
        
        #date
        out.write(date)
        out.write(',        ')


        #one month increase SPY, one month is defined as 30 days
        if (date_to_datetime(date) + datetime.timedelta(days = futureClosure(date, 30))) < date_to_datetime('03/14/2021'): #verify that data exists
            out.write(str(percent_increase('SPY', date, futureClosure(date, 30))))
            out.write('%,       ')
        else:
            out.write('NaN,        ')

        #three month increase SPY, one month is defined as 30 days
        if (date_to_datetime(date) + datetime.timedelta(days = futureClosure(date, 90))) < date_to_datetime('03/14/2021'): #verify that data exists
            out.write(str(percent_increase('SPY', date, futureClosure(date, 90))))
            out.write('%,       ')
        else:
            out.write('NaN,        ')

        #six month increase SPY, one month is defined as 30 days
        if (date_to_datetime(date) + datetime.timedelta(days = futureClosure(date, 180))) < date_to_datetime('03/14/2021'): #verify that data exists
            out.write(str(percent_increase('SPY', date, futureClosure(date, 180))))
            out.write('%,       ')
        else:
            out.write('NaN,        ')
        
        #one month increase QQQ, one month is defined as 30 days
        if (date_to_datetime(date) + datetime.timedelta(days = futureClosure(date, 30))) < date_to_datetime('03/14/2021'): #verify that data exists
            out.write(str(percent_increase('QQQ', date, futureClosure(date, 30))))
            out.write('%,       ')
        else:
            out.write('NaN,        ')

        #three month increase QQQ, one month is defined as 30 days
        if (date_to_datetime(date) + datetime.timedelta(days = futureClosure(date, 90))) < date_to_datetime('03/14/2021'): #verify that data exists
            out.write(str(percent_increase('QQQ', date, futureClosure(date, 90))))
            out.write('%,       ')
        else:
            out.write('NaN,        ')

        #six month increase QQQ, one month is defined as 30 days
        if (date_to_datetime(date) + datetime.timedelta(days = futureClosure(date, 180))) < date_to_datetime('03/14/2021'): #verify that data exists
            out.write(str(percent_increase('QQQ', date, futureClosure(date, 180))))
            out.write('%')
        else:
            out.write('NaN')

        out.write('\n')

        line = f.readline()

f.close()
out.close()
