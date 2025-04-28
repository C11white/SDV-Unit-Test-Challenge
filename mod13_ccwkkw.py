import unittest
from datetime import datetime


def SymbolUnit(symbol):  # I originally had all this in a single line on return but it wasnt working so I expanded it
    if not symbol.isalpha():
        return False
    if not symbol.isupper():
        return False
    if not (0 < len(symbol) <= 7):
        return False
    return True

def ChartTypeUnit(chart_type):
    return chart_type in ['1', '2']

def TimeSeriesUnit(time_series): 
    return time_series in ['1', '2', '3', '4']

def DateUnit(date):
    try:
        datetime.strptime(date, "%Y-%m-%d")
        return True
    except ValueError:
        return False




class SDVTest(unittest.TestCase):

    # symbol: capitalized, 1-7 alpha characters
    def test_ValidSymbolUnit(self):
    # True
        self.assertTrue(SymbolUnit("A")) 
        self.assertTrue(SymbolUnit("GOOGL")) 
        self.assertTrue(SymbolUnit("APPLE")) 
        self.assertTrue(SymbolUnit("HI")) 
        self.assertTrue(SymbolUnit("WORLDS"))
    # False
        self.assertFalse(SymbolUnit("okay"))
        self.assertFalse(SymbolUnit("HELLOWORLD")) 
        self.assertFalse(SymbolUnit("2025")) 
        self.assertFalse(SymbolUnit("SICK--")) 

        
    # chart type: 1 numeric character, 1 or 2
    def test_ChartTypeUnit(self):
    # True
        self.assertTrue(ChartTypeUnit("1"))
        self.assertTrue(ChartTypeUnit("2"))    
    # False
        self.assertFalse(ChartTypeUnit("3")) 
        self.assertFalse(ChartTypeUnit("0")) 
        self.assertFalse(ChartTypeUnit("LINE")) 
        self.assertFalse(ChartTypeUnit("Bar")) 
       
    # time series: 1 numeric character, 1 - 4
    def test_TimeSeriesUnit(self): 
    # True
        self.assertTrue(TimeSeriesUnit("1")) 
        self.assertTrue(TimeSeriesUnit("2")) 
        self.assertTrue(TimeSeriesUnit("3")) 
        self.assertTrue(TimeSeriesUnit("4")) 
    # False
        self.assertFalse(TimeSeriesUnit("DAILY"))
        self.assertFalse(TimeSeriesUnit("Weekly"))
        self.assertFalse(TimeSeriesUnit("monthly"))
        self.assertFalse(TimeSeriesUnit("0"))
        self.assertFalse(TimeSeriesUnit("5"))
        self.assertFalse(TimeSeriesUnit("20"))
       
    # start date: date type YYYY-MM-DD ------ end date: date type YYYY-MM-DD
    def test_DateUnit(self): 
    # True
        self.assertTrue(DateUnit("2023-01-01"))
        self.assertTrue(DateUnit("2000-12-31"))  
    # False
        self.assertFalse(DateUnit("2023-02-30"))  
        self.assertFalse(DateUnit("2023-13-01"))  
        self.assertFalse(DateUnit("2023-01-01 12:00"))  
        self.assertFalse(DateUnit("01-01-2023"))
        self.assertFalse(DateUnit("April 23, 2025"))
        self.assertFalse(DateUnit("2023"))
        self.assertFalse(DateUnit("1"))


if __name__ == '__main__':
    unittest.main()
