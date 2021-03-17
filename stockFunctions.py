# Program author: u/shitilostagain
# Date: 3/14/2021
# basic stock analysis toolbox
# Functions Overview:
#   - date_to_datetime:     modifies a string date object into a datetime object
#   - ticker_close:         gets the closing price for a given ticker 
#   - runup_percent:        determines the percent increase in the runup period relative to the price at the beginning of the runup period
#   - percent_increase:     determines the percent increase after a certain number of days relative to the intitial price
#   - futureCloseure:       corrects for weekends and holidays when looking forwards for a certain number of days
#   - pastClosure:          corrects for weekends and holidays when looking backwards for a certain number of days

import pandas as pd
import datetime
import yfinance as yf




# date modification, takes in date in str format and spits back a datetime object
# will return NaN for invalid date
# variables:
#   - date:     date in either MM/DD/YYYY format or YYYY-MM-DD format (str)
#
# return types:
#   - date in datetime format (datetime)
def date_to_datetime(date):
    #modifies MM/DD/YYYY into datetime object
    if date[2:3] == '/':
        d = date[3:5]
        m = date[0:2]
        y = date[6:10]
        return datetime.date(int(y),int(m),int(d))

    #modifies YYYY-MM-DD into datetime object
    elif date[4:5] == '-':
        d = date[8:10]
        m = date[5:7]
        y = date[0:4]
        return datetime.date(int(y),int(m),int(d))
    
    else:
        print('error: wrong date format')
        return 'NaN'


#dates of closures in dataset
#dates the stock market has been closed over the past 3 years
stockClosure = ['01/01/2018','01/15/2018','02/19/2018','03/30/2018',
                '05/28/2018','07/04/2018','09/03/2018','11/22/2018',
                '12/05/2018','12/25/2018','01/01/2019','01/21/2019',
                '02/18/2019','04/19/2019','05/27/2019','07/04/2019',
                '09/02/2019','11/28/2019','12/25/2019','01/01/2020',
                '01/20/2020','02/17/2020','04/10/2020','05/25/2020',
                '07/03/2020','11/26/2020','12/25/2020','01/01/2021',
                '01/18/2021','02/15/2021','01/01/2030']

#converts the closure dates to datetime format
stockClosureDT = []
for x in range(30):
    stockClosureDT.append(date_to_datetime(stockClosure[x]))


# takes ticker w/ date as input, returns close price@date
# will catch invalid tickers and invalid dates and return NaN
# variables:
#   - ticker:   market ticker (str)
#   - date:     date in either MM/DD/YYYY format or YYYY-MM-DD format (str)
#
# return types:
#   - closing price for the provided ticker on the given date (double)
def ticker_close(ticker, date):
    #get datetime objects for dates we are looking at
    startDate = date_to_datetime(date)
    
    #verify startDate is valid
    if startDate == 'NaN':
        return 'NaN'
    
    endDate = startDate + datetime.timedelta(days = 1)

    #download ticker data
    data = yf.download(ticker, startDate, endDate)
    
    #catch invalid tickers:
    if data.empty:
      return 'NaN'
    
    #if ticker is valid, return it
    else:
        return data.iloc[0,3] #return close price on date




# runup increase in percent for a stock ticker for a given date and number of runup dates
# will catch invalid tickers and return '--'
# WARNING: runupDays IS NOT MARKET DAYS, IT IS CALANDER DAYS!!!! USER MUST ACCOUNT FOR MARKET DAYS
# note: percent increase is relative to the price at initial date-runupdays
# variables:
#   - ticker:       SINGLE index ticker, multiple index tickers will cause error (str)
#   - date:         date in either MM/DD/YYYY format or YYYY-MM-DD format (str)
#   - runupDays:    number of runup days to compare price change against (int)
# 
# return types:
#   - percent change relative to initial runup price, 2 decimal places (double)
def runup_percent(ticker, date, runupDays):
    currentDate = date_to_datetime(date)
    runupDate = currentDate - datetime.timedelta(days = runupDays)

    currentPrice = ticker_close(ticker, str(currentDate))
    runupPrice = ticker_close(ticker, str(runupDate))
      
    #catch invalid tickers
    if currentPrice == 'NaN' or runupPrice == 'NaN':
        return '--'

    else:
        return round((((currentPrice-runupPrice)/(runupPrice)) * 100.0),2)



# Increase in percent for a stock ticker for a given date and number of following days
# will catch invalid tickers and return '--'
# WARNING: forwardDays IS NOT MARKET DAYS, IT IS CALANDER DAYS!!!! USER MUST ACCOUNT FOR MARKET DAYS
# note: percent increase is relative to the price at initial date
# variables:
#   - ticker:           SINGLE index ticker, multiple tickers will cause error (str)
#   - date:             date in either MM/DD/YYYY format or YYYY-MM-DD format (str)
#   - forwardDays:      number of days to compare price change against (int)
# 
# return types:
#   - percent change relative to initial price, 2 decimal places (double)
def percent_increase(ticker, date, forwardDays):
    currentDate = date_to_datetime(date)
    futureDate = currentDate + datetime.timedelta(days = forwardDays)

    currentPrice = ticker_close(ticker, str(currentDate))
    futurePrice = ticker_close(ticker, str(futureDate))

    #catch invalid tickers
    if currentPrice == 'NaN' or futurePrice == 'NaN':
        return '--'
    
    else:
        return round((((futurePrice-currentPrice)/(currentPrice)) * 100.0),2)


# check for no holiday/weekend interference, will return updated numDays
# date is current days, numDays is how many days looking forwards
# used in conjunction with percent increase looking forward
# variables:
#   - date:         current day
#   - numDays:      days looking forwards
# 
# return types:
#   -corrected numDays to account for weekends and holidays
def futureClosure(date, numDays):
    # if increase falls on a holiday
    if (date_to_datetime(date) + datetime.timedelta(days = numDays)) in stockClosureDT:
        #if day after holiday is a saturday
        if (date_to_datetime(date) + datetime.timedelta(days = (numDays + 1))).strftime('%A') == 'Saturday':
            return numDays + 3
        else:
            return numDays + 1
    #if increase falls on a saturday
    elif (date_to_datetime(date) + datetime.timedelta(days = (numDays))).strftime('%A') == 'Saturday':
        #if day after weekend is a holiday:
        if (date_to_datetime(date) + datetime.timedelta(days = numDays+2)) in stockClosureDT:
            return numDays + 3
        else:
            return numDays + 2
    #if increase falls on a sunday
    elif (date_to_datetime(date) + datetime.timedelta(days = (numDays))).strftime('%A') == 'Sunday':
        #if day after weekend is a holiday:
        if (date_to_datetime(date) + datetime.timedelta(days = numDays+1)) in stockClosureDT:
            return numDays + 2
        else:
            return numDays + 1
    else:
        return numDays



# check for no holiday/weekend interference, will return updated numDays
# date is current days, numDays is how many days looking backwards
# used in conjuction with runup percents
# variables:
#   - date:         current day
#   - numDays:      days looking backwards
# 
# return types:
#   -corrected numDays to account for weekends and holidays
def pastClosure(date, numDays):
    # if decrease falls on a holiday
    if (date_to_datetime(date) - datetime.timedelta(days = numDays)) in stockClosureDT:
        #if day after holiday is a saturday
        if (date_to_datetime(date) - datetime.timedelta(days = (numDays + 1))).strftime('%A') == 'Sunday':
            return numDays + 3
        else:
            return numDays + 1
    #if decrease falls on a saturday
    elif (date_to_datetime(date) - datetime.timedelta(days = (numDays))).strftime('%A') == 'Saturday':
        #if day before weekend is a holiday:
        if (date_to_datetime(date) - datetime.timedelta(days = numDays + 1)) in stockClosureDT:
            return numDays + 2
        else:
            return numDays + 1
    #if decrease falls on a sunday
    elif (date_to_datetime(date) - datetime.timedelta(days = (numDays))).strftime('%A') == 'Sunday':
        #if day before weekend is a holiday:
        if (date_to_datetime(date) - datetime.timedelta(days = numDays + 2)) in stockClosureDT:
            return numDays + 3
        else:
            return numDays + 2
    else:
        return numDays



#testing, uncomment for code examples:
#print(ticker_close('SPY', '03/05/2021'))
#print(ticker_close('SPY', '2021-03-05'))
#print(ticker_close('SPY', str(datetime.date(2021,3,5))))
#print(runup_percent('SPY', '03/05/2021', 7), end='%\n')
#print(percent_increase('SPY', '02/26/2021', 7), end='%\n')

#print(ticker_close('INVALID','03/05/2021'))
#print(runup_percent('ABCDEFG', '03/05/2021', 7), end='%\n')
#print(percent_increase('NOT_A_TICKER', '02/26/2021', 7), end='%\n')