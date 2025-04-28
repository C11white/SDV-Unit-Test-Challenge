import json, requests, time, json
from datetime import datetime
#import matplotlib.pyplot as plt
#import mplfinance as mpf
#import pandas as pd
import pygal
import numpy as np


def main():
    #variables
    apiKey = "WZYK9TQ3C96A9WXT"

    #Ask the user to enter the stock symbol for the company they want data for.
    while True:
        stockSymbol = input("\nPlease enter the stock symbol for the company you want data for: ").upper()

        if (ValidSymbolUnit(stockSymbol) == False):
            print("Please enter a valid stock symbol.")
            continue
        else:
            break

    #Ask the user for the chart type they would like.
    #validChartTypes = ["LINE", "BAR"] #Just take this lol
    #validChartTypes = ["LINE", "BAR", "CANDLESTICK"]
    chartType = input("\nWould you like a Line Chart (1) or Bar Chart (2) Please Enter a Number: ").upper()
    #chartType = input("\nPlease enter the chart type you would like (LINE, BAR, CANDLESTICK): ").upper()

    while ChartTypeUnit(chartType) == False:
        print("Invalid chart type. Please enter a valid option.")
        chartType = input("\nWould you like a Line Chart (1) or Bar Chart (2)? Please Enter a Number: ")
            
    #while chartType not in validChartTypes:
    
        #chartType = input("\nPlease enter the chart type you would like (LINE, BAR): ").upper()
        #chartType = input("\nPlease enter the chart type you would like (LINE, BAR, CANDLESTICK): ").upper()
    
    #Ask the user for the time series function they want the api to use.
    #validTimeSeries = ["INTRADAY", "DAILY", "DAILY_ADJUSTED", "WEEKLY", "WEEKLY_ADJUSTED", "MONTHLY", "MONTHLY_ADJUSTED"]
    timeSeriesNum = input("\nPlease enter the number for the time series function you would like the api to use (1. INTRADAY, 2. DAILY, 3. WEEKLY, 4. MONTHLY): ")

    while TimeSeriesUnit(timeSeriesNum) == False:
        print("Invalid chart type. Please enter a valid option.")
        timeSeriesNum = input("\nPlease enter the number for the time series function you would like the api to use (1. INTRADAY, 2. DAILY, 3. WEEKLY, 4. MONTHLY): ")   
    
    timeSeries = TimeSeriesConvert(timeSeriesNum)


    beginningDate = input("\nPlease enter the beginning date in YYYY-MM-DD format: ")
    while DateUnit(beginningDate) == False:
        print("Invalid chart type. Please enter a valid option.")
        beginningDate = input("\nPlease enter the beginning date in YYYY-MM-DD format: ")   

    endDate = input("\nPlease enter the end date in YYYY-MM-DD format: ")
    while DateUnit(endDate) == False:
        print("Invalid chart type. Please enter a valid option.")
        endDate = input("\nPlease enter the end date in YYYY-MM-DD format: ") 
    

    #NEED TO SEE IF THIS IS EVEN NEEDED (the whole rows thing below), COULD JSUT CALC THE DAYS INBETWEEN START AND END BC THIS IS JUST GONNA DO THAT ANYWAYS
    # u ask for 5 days in start and end date but then choose 3 for rows then it does the last 3 days not the 5 soo

    # asking user how many rows of data they want, how many days of data they want to see
    #while True:
     #   try:
      #      chosenRows = int(input("\nHow many rows of data would you like to see? (1-100): "))
       #     if (chosenRows < 1 or chosenRows > 100):
        #        print("Please enter a number between 1 and 100.")
         #       continue
          #  else:
           #     break
        #except ValueError:
         #   print("Please enter a valid number.")
          #  continue
        #except Exception as e:
         #   print("An error occurred: ", e)

    #Ask the user for the beginning date in YYYY-MM-DD format.
    #convertedBeginDate, convertedEndDate = ChoosingDates()

    #generating chart
    GetData(stockSymbol, apiKey, timeSeries, beginningDate, endDate, chartType)


#getting the api data
def GetData(stockSymbol, apiKey, timeSeries, convertedBeginningDate, convertedEndDate, chartType):
    
    convertedBeginningDate = datetime.strptime(convertedBeginningDate, "%Y-%m-%d")
    convertedEndDate = datetime.strptime(convertedEndDate, "%Y-%m-%d")
    
    #getting the data from the API
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_{timeSeries}&symbol={stockSymbol}&outputsize=compact&apikey={apiKey}&datatype=json"
    
    response = requests.get(url)
    data = response.json()

    if response.status_code != 200:
        print(f"Error: Received status code {response.status_code} from the API")
        return
    
    time_series_key = None
    for key in data.keys():
        if 'Time Series' in key:
            time_series_key = key
            break
    
    if not time_series_key:
        print("Error: Could not find time series data in the API response")
        print("Available keys:", data.keys())
        return
    
    filtered_data = {}
    for date, values in data[time_series_key].items():
        date_obj = datetime.strptime(date, "%Y-%m-%d")
        if convertedBeginningDate <= date_obj <= convertedEndDate:
            filtered_data[date] = values

    limited_data = dict(list(filtered_data.items()))

    dates = list(limited_data.keys())[::-1]

    if not dates:
        print("There is no data for the selected dates")
        return
    
    
    print("")
    time.sleep(2)
    for i in range(3, 0, -1):
        time.sleep(1)
        print("Generating chart" + "." * i) #to look cool
    
    time.sleep(2)
    print("\n", json.dumps(limited_data, indent=4))
    with open("data.json", "w") as file:
        json.dump(data, file)

    
    #print("Data received from API:", limited_data)
    GenerateChart(chartType, limited_data, convertedBeginningDate, convertedEndDate, stockSymbol)
    
    return

#generate the chart
def GenerateChart(chartType, data, startDate, EndDate, stockSymbol):
    dates = list(data.keys())[::-1]
    opens, highs, lows, closes = [], [], [], []


    for date in dates:
        values = data[date]  
    
        if all(key in values for key in ['1. open', '2. high', '3. low', '4. close']):
            opens.append(float(values['1. open']))
            highs.append(float(values['2. high']))
            lows.append(float(values['3. low']))
            closes.append(float(values['4. close'])) 

    if chartType == "1":
        line_chart = pygal.Line()
        line_chart.title = '%s %s Chart from %s to %s' % (stockSymbol, chartType, startDate, EndDate)
        line_chart.x_labels = dates
        line_chart.add('Open', opens)
        line_chart.add('High', highs)
        line_chart.add('Low',  lows)
        line_chart.add('Close', closes)
        line_chart.render_in_browser()
    elif chartType == "2":
        bar_chart = pygal.Bar()
        bar_chart.title = '%s %s Chart from %s to %s' % (stockSymbol, chartType, startDate, EndDate)
        bar_chart.x_labels = dates
        bar_chart.add('Open', opens)
        bar_chart.add('High', highs)
        bar_chart.add('Low',  lows)
        bar_chart.add('Close', closes)
        bar_chart.render_in_browser()

    #elif chartType == "CANDLESTICK":
        

        #ohlc_data = [(datetime.datetime.strptime(date, "%Y-%m-%d"), float(values['1. open']), float(values['2. high']), float(values['3. low']), float(values['4. close'])) for date, values in data.items()]
        #mpf.plot(pd.DataFrame(ohlc_data, columns=['Date', 'Open', 'High', 'Low', 'Close']).set_index('Date'), type='candle', style='charles')
    return
    
    
#getting user dates
def ChoosingDates():

    try:
        beginningDate = input("\nPlease enter the beginning date in M-D-YY or MM-DD-YY format: ")
        convertedBeginDate = datetime.datetime.strptime(beginningDate, "%m-%d-%y")

        #beginning date cant be past the present
        if (convertedBeginDate > datetime.datetime.now()):
            print("The beginning date should not be in the future.")
            return ChoosingDates()
    except ValueError:
        print("Please enter the date in the correct format.")
        return ChoosingDates()
    except Exception as e:
        print("An error occurred: ", e)
        return ChoosingDates()

    #end date should not be before the begin date
    while True:
        try:
            endDate = input("\nPlease enter the end date in M-D-YY or MM-DD-YY format: ")
            convertedEndDate = datetime.datetime.strptime(endDate, "%m-%d-%y")
        except ValueError:
            print("Please enter the date in the correct format.")
            continue
        except Exception as e:
            print("An error occurred: ", e)
            continue

        if (convertedEndDate < convertedBeginDate):
            print("The end date should not be before the begin date.")
            
            changeDates = input("Would you like to restart the dates portion? (y/n): ").lower()
            if (changeDates == 'y'):
                return ChoosingDates()
            else:
                continue
        else:
            return convertedBeginDate, convertedEndDate

def ValidSymbolUnit(symbol):
    return symbol.isalpha() and symbol.isupper() and 1 <= len(symbol) <= 7

def ChartTypeUnit(chart_type):
    return chart_type in ['1', '2']

def TimeSeriesUnit(time_series):
    return time_series in ['1', '2', '3', '4']

def TimeSeriesConvert(time_series_num):
    options = {
        '1': "INTRADAY",
        '2': "DAILY",
        '3': "WEEKLY",
        '4': "MONTHLY"
    }
    return options.get(time_series_num)

def DateUnit(date):
    try:
        datetime.strptime(date, "%Y-%m-%d")
        return True
    except ValueError:
        return False


main()