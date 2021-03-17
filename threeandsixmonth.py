
# Program author: u/shitilostagain
# Date: 3/16/2021
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
# a new text file that will take the original formatted text file and add data columns for 1M increase
# and 3M increase. The company name column will also be removed for the new dataset. The new dataset will be labeled
# 'data_3M6M.txt' and will be in CSV format for easy analysis. This is a seperate dataset to add new data for 3 month
# and 6 month periods of increase

out = open("data_3M6M.txt","w")

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
out.write('Ticker:,Buy Date:,Seg:,3M inc:,6M inc:\n')


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


    # three month increase, one month is defined as 30 days
    if (date_to_datetime(date) + datetime.timedelta(days = futureClosure(date, 90))) < date_to_datetime('03/14/2021'): #verify that data exists
        out.write(str(percent_increase(ticker, date, futureClosure(date, 90))))
        out.write('%,       ')
    else:
        out.write('NaN,        ')


    # six month increase, one month is defined as 30 days
    if (date_to_datetime(date) + datetime.timedelta(days = futureClosure(date, 180))) < date_to_datetime('03/14/2021'): #verify that data exists
        out.write(str(percent_increase(ticker, date, futureClosure(date, 180))))
        out.write('%')
    else:
        out.write('NaN')


    #newline
    out.write('\n')

out.close()