# Program author: u/shitilostagain
# Date: 3/14/2021
# Note: This program requires the stockFunctions.py file along with the txt file 'buyStocksCramerFormattedHeaderless.txt', 
#       which can be found in the GitHub Repo below. To create the txt file 'buyStocksCramerFormattedHeaderless.txt',
#       simply process the file 'rawStocksCramer.txt' with the cleanTXT.py script, then delete the first 9 lines of the file 
#       'buyStocksCramerFormatted.txt' and replace the 9 lines with the line: 
#       
#       Ticker:,Date Recomended:,Segment:,Company Name:
#       
#       After the replacement, rename the file to 'buyStocksCramerFormattedHeaderless.txt'. All the neccessary files are
#       in the GitHub repo below:
#
# GitHub Repo: https://github.com/shitilostagain/JimmyChill
#
# This program will take the formatted text file 'buyStocksCramerFormattedHeaderless.txt' and then create
# a new text file that will take the original formatted text file and add data columns for 1 Day increase,
# 1 week increase, 1 month increase(if data is available), 1 year increase(if data is available), 1 week runup, and
# 1 month runup. The company name column will also be removed for the new dataset. The new dataset will be labeled
# 'buyAnalysis.txt' and will be in CSV format for easy analysis

out = open("buyAnalysis.txt","w")

from stockFunctions import *
import pandas as pd
import datetime

#variables
ticker = ''
date = ''
segment = ''


# putting original data into pandas dataframe for easy readibility:
data = pd.read_csv("buyStocksCramerFormattedHeaderless.txt")


#header,
out.write('Ticker:,Buy Date:,Seg:,1D inc:,1W inc:,1M inc:,1Y inc:,1W runup:,1M runup:\n')


#fill csv file with the information in the header
for x in range(data.shape[0]):
    ticker = data.iloc[x, 0][1:]
    date = ''.join(data.iloc[x,1].split())
    segment = ''.join(data.iloc[x,2].split())

    #file output
    out.write('$')
    out.write(ticker)
    out.write(',        ')
    out.write(date)
    out.write(',        ')
    out.write(segment)
    out.write(',        ')


    #one day increase
    out.write(str(percent_increase(ticker, date, futureClosure(date, 1))))
    out.write('%,       ')


    #one week increase
    out.write(str(percent_increase(ticker, date, futureClosure(date, 7))))
    out.write('%,       ')


    #one month increase, one month is defined as 30 days
    if (date_to_datetime(date) + datetime.timedelta(days = futureClosure(date, 30))) < date_to_datetime('03/14/2021'): #verify that data exists
        out.write(str(percent_increase(ticker, date, futureClosure(date, 30))))
        out.write('%,       ')
    else:
        out.write('NaN,        ')


    #one year increase
    if (date_to_datetime(date) + datetime.timedelta(days = futureClosure(date, 365))) < date_to_datetime('03/14/2021'): #verify that data exists
        out.write(str(percent_increase(ticker, date, futureClosure(date, 365))))
        out.write('%,       ')
    else:
        out.write('NaN,        ')


    #one week runup
    out.write(str(runup_percent(ticker, date, pastClosure(date, 7))))
    out.write('%')


    #one month runup
    out.write(str(runup_percent(ticker, date, pastClosure(date, 30))))
    out.write('%')

    #newline
    out.write('\n')

out.close()

#testing:
#print(futureClosure('12/07/2020', 5)) ##should return 7
#print(futureClosure('12/07/2020', 6)) ##should return 7

#print(pastClosure('02/12/21', 5)) #should return 4
#print(pastClosure('02/12/21', 6)) #should return 4