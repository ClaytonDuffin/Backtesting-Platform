from datetime import datetime
from bs4 import BeautifulSoup
from urllib.request import urlopen
from backtestDriver import BacktestDriver


class BacktestMetrics(BacktestDriver):

    '''
    Class used for computing and organizing any information that you wish to compute and log from the backtest.

    Parameters
    ---------- 
    tickerSymbol : list[str]
        the ticker symbol of the asset or currency pair to be processed.
    tickInterval : str
        the interval of time between each data point. Options are: '1min', '5min', '15min', '30min', '45min', '1h', '2h', '4h', '8h', '1day', '1week', and '1month'
    numberOfUnits : int
        the number of units of data to request from the API.
    '''

    def __init__(self, 
                 tickerSymbols: list[str],
                 tickInterval: int,
                 numberOfUnits: int) -> None:
    
        self._tickerSymbols = tickerSymbols
        self._tickInterval = tickInterval
        self._numberOfUnits = numberOfUnits

        super().__init__(tickerSymbols, tickInterval, numberOfUnits)
        

    def yieldCurveParser(self) -> float:

        '''Fetches the ten year from the web. Page updates once a day.'''
        
        URL = ["https://home.treasury.gov/resource-center/data-chart-center/interest-rates/TextView?type=daily_treasury_yield_curve&field_tdr_date_value_month=" + str(datetime.today().strftime('%Y%m'))]
        webpageTableAsList = []
        
        for webPage in URL:
     
            stew = BeautifulSoup(urlopen(webPage).read())
            attributes = stew.find('table').find_all('tr')
            
            for parYieldCurveRate in attributes:
                
                maturityDate = parYieldCurveRate.find_all('td')
                maturityDate = [i.text.strip() for i in maturityDate]
                webpageTableAsList.append(maturityDate)
            
        tenYearRate = float(webpageTableAsList[-1][17])
        
        return (tenYearRate)

    
    def yieldCurveStandardization(self) -> float:

        '''Reduces the rate to match the period of time that the backtest was ran over. This is done so that the ratios/KPIs will compute properly.'''
        pass


    def someMetric(self): # Type hinting to be determined
        pass


    def someOtherMetric(self): # Type hinting to be determined
        pass


    def someRatio(self): # Type hinting to be determined
        pass


    def composeLog(self): # Type hinting to be determined

        '''Puts together all the metrics so that they can either be stored or viewed in the console.'''

        log = [
              ('backtestID', self._backtestID),
              ('someMetric', self.someMetric()),
              ('someOtherMetric', self.someOtherMetric()),
              ('someRatio', self.someRatio())
              ]

        return (log)
    
    
#backtest = BacktestMetrics(['VIX'], '45min', 390)
#backtest.composeLog()
    