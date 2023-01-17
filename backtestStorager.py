from backtestMetrics import BacktestMetrics


class BacktestStorager(BacktestMetrics):

    '''
    Class used to store data either in the form of logs, plots, or both.

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

        self.createFolderForBacktest()
        #put something here to let the next few method calls in the initializer (next few lines) know where the folder that was just created is.
        self.storeTradeSeries()
        self.storeUnderlyingSeries()
        self.storeMetrics()
        self.storePlots()

    def createFolderForBacktest(self) -> None:

        '''Creates a directory or subdirectory somewhere so that data can be stored there. Uses self._backtestID for the name of the folder.'''
        pass


    def storeTradeSeries(self) -> None:

        '''Stores the trade series that was generated when the backtest ran.'''
        pass


    def storeUnderlyingSeries(self) -> None:

        '''Stores the series of data that was used to generate the backtest.'''
        pass


    def storeMetrics(self) -> None:

        '''Fetches the output from self.composeLog() and stores it.'''
        pass


    def storePlots(self) -> None:
        
        '''Stores any plots that you might want to store.'''
        pass


#backtest = BacktestStorager(['SPY'], '45min', 390)
