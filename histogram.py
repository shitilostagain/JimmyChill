# Program author: u/shitilostagain
# Date: 3/16/2021
# Description: This file will take the compiled data in the files 'SPY_QQQ.txt', 'buyAnalysis.txt', and
#              'data_3M6M.txt' and create probability density estimates for 1, 3, and 6 month periods, both for
#              pre and post pandemic comparing Jim Cramer's stock picks to $QQQ and $SPY. 
#
# GitHub Repo: https://github.com/shitilostagain/JimmyChill

from stockFunctions import *
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import yfinance as yf
import datetime
from statistics import mean 



SQ = pd.read_csv("SPY_QQQ.txt")


#variables
date = ''
cramerPicks = []
setSPY = []
setQQQ = []
temp = []


# Creates a histogram comparing Cramer's picks agains the QQQ and the SPY
# Note: we will be ignoring data from between Jan 20 - March 20 2020 to account for the pandemic black crash due to it being a black swan event
# Variables
#   - pre_post: str, 'PRE' for prepandemic, 'POST' for postpandemic
#   - period: 1 for 1M, 3 for 3M, 6 for 6M
# return type: none
def createHistogram(pre_post, period):
    #local variables
    start = 0
    end = 0
    col = -1
    dataset = pd.DataFrame()
    index = -1

    #set proper start and end range
    if pre_post == 'PRE':
        end = 6087
        if period == 1:
            start = 2928
        elif period == 3:
            start = 3397
        elif period == 6:
            start = 3968

    elif pre_post == 'POST':
        start = 0
        end = 2411
    else:
        print("select either pre or post pandemic using function header")
        return

    #set proper columns, date increases, and pick proper dataset:
    if period == 1:
        col = 5
        index = 1
        dataset = pd.read_csv("buyAnalysis.txt")
    elif period == 3:
        col = 3
        index = 2
        dataset = pd.read_csv("data_3M6M.txt")
    elif period == 6:
        col = 4
        index = 3
        dataset = pd.read_csv("data_3M6M.txt")
    else:
        print("select proper period from range in function header")
        return


    #######################################################################################################

    #compile data in date range
    for x in range(end - start):
        x += start #account for offset

        date = str(''.join(dataset.iloc[x,1].split())) #date in string form

        #string representation of data in column col @ index x + start
        percent = str(''.join(dataset.iloc[x,col].split())) #string representation of percent figure

        if percent != 'NaN' and percent != '--%': #verify that percent representation exists
            #add valid percent representations to dataset cramerPicks
            cramerPicks.append(float(percent[:-1])) #remove percent symbol and convert to floating point number

            #add percent representations to datasets setSPY and setQQQ , index & index+3 respectively
            SPYRAW = SQ[SQ['Date:'] == str(date_to_datetime(date))].iloc[0,index]
            QQQRAW = SQ[SQ['Date:'] == str(date_to_datetime(date))].iloc[0,index+3]

            SPYRAW =  str(''.join(SPYRAW.split()))
            QQQRAW =  str(''.join(QQQRAW.split()))

            setSPY.append(float(SPYRAW[:-1]))
            setQQQ.append(float(QQQRAW[:-1]))

    #testing:
    #print(cramerPicks)
    #print(setSPY)
    #print(setQQQ)
    #if len(cramerPicks) == len(setQQQ) and len(cramerPicks) == len(setSPY):
    #    print("LENTGHS MATCH")
    #print('length: ', end = '')
    #print(len(cramerPicks))
    print(str(period), end=' month averages, ')
    print(pre_post)
    print('SPY Average: ',end='')
    print(mean(setSPY),end='%\n')
    print('QQQ Average: ',end='')
    print(mean(setQQQ),end='%\n')
    print('Cramer Average: ',end='')
    print(mean(cramerPicks),end='%\n')


    #display plot, TODO: format chart
    sns.set_palette("muted")
    sns.set_style('darkgrid')

    sns.kdeplot(setSPY)
    sns.kdeplot(setQQQ)
    sns.kdeplot(cramerPicks)
    plt.legend(labels=['SPY', 'QQQ', 'Cramer'])
    plt.xlabel('Price % Increase Over ' + str(period) + ' Months, ' + pre_post + ' pandemic')

    plt.show()


#selectively comment out to get data
#prepandemic:
#createHistogram('PRE', 1)
#createHistogram('PRE', 3)
#createHistogram('PRE', 6)


#postpandemic:
#createHistogram('POST', 1)
#createHistogram('POST', 3)
createHistogram('POST', 6)
