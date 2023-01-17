from claydates import MultiTickerProcessor
from itertools import chain
import pandas as pd
import numpy as np
import uuid
import warnings
warnings.simplefilter(action = 'ignore', category = UserWarning)


class BacktestDriver:
    
    '''
    Class used to see where trades would have occured given a strategy and a time series of price data. The class is also used for housing methods that organize data.
    This is the base class for all of the other classes.

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
        
        self._assetObject = MultiTickerProcessor(self._tickerSymbols,
                                                 self._tickInterval,
                                                 self._numberOfUnits)
        
        self._assetTimeSeries = self._assetObject.missingUnitsExcluded(dataType = 'numpy')[0]
        self._holdingPeriods = []
        self._openingAndClosingOrders = []
        self._profitLossForTrades = self.computeReturnSeries()
        self._tradesPercentageChangeSeries = (self.percentageChangeSeries(seriesType = 1))
        self._underlyingPercentageChangeSeries = (self.percentageChangeSeries(seriesType = 2))
        self._backtestID = str(uuid.uuid4())


    def batcher(self,
                subframeLength: int, 
                gapToNextFrame: int) -> list[list[float]]:

        '''
        Used to walk through the time series, so that the trading logic can be computed at each time step.
        For more information on the function, visit where I wrote about it in a separate project at: https://github.com/ClaytonDuffin/Complex-Plane-Analysis#batcher
                                                                                                             
        Parameters 
        ---------- 
        subframeLength: int
            Determines how long each subframe should be.
        gapToNextFrame: int
            Determines the spacing between the start of one subframe and the next. 
        '''
    
        if (len(self._assetTimeSeries.shape) == 1):
            originalData = list(zip(self._assetTimeSeries))
        elif (len(self._assetTimeSeries.shape) == 2):
            originalData = list(zip(self._assetTimeSeries[:, 4]))
        
        fullSeries = []
        for t, j in enumerate(originalData):
            subSeries = [] 
            for i in range(0, subframeLength, gapToNextFrame):
                try:
                    subSeries.append(originalData[t-i])
                except IndexError:
                    continue
                
            fullSeries.append(list(chain(*[list(row) for row in subSeries[::-1]])))
            
        return fullSeries[subframeLength : len(fullSeries)]

    
    def positionStates(self) -> list[tuple[bool, bool, bool, bool]]:
        
        '''
        Trading logic defined here. This method returns a list of tuples that represent the status of a trade, or lack thereof.
        So long as you keep the structure of the output the same, the content of this method is all that you have to change 
        to use this software to perform backtests using your own strategy. 
        
        (True, False, False, False) indicates that a trade was opened at this index position in the series.
        (False, True, False, False) indicates that an open trade is being held at this index position in the series.
        (False, False, True, False) indicates that an open trade was closed at this index position in the series.
        (False, False, False, True) indicates that nothing should be done and that no trades are currently open at this index position in the series.
        '''
        
        lastFives = self.batcher(5, 1)
        
        minimumSubframeValues = []
        for i in lastFives:
            minimumSubframeValues.append(min(i))
        
        entryCount = 0
        positionIsOpen = False
        currentState = (False, False, False, True)
        states = []
        for i, j in enumerate(lastFives):
                            
            if (j[0] == minimumSubframeValues[i]):
                entryCount += 1
            else:
                entryCount = 0
                
            if (entryCount == 3):
                currentState = (True, False, False, False)
                positionIsOpen = True
            if (positionIsOpen == True) and (entryCount != 3): 
                currentState = (False, True, False, False)
            if (positionIsOpen == True) and (j[2] == minimumSubframeValues[i]):
                currentState = (False, False, True, False)
                positionIsOpen = False
            if (positionIsOpen == False) and (currentState != (False, False, True, False)):
                currentState = (False, False, False, True)
            try:
                if (states[-1] == (False, True, False, False)) and (currentState == (True, False, False, False)):
                    currentState = (False, True, False, True)
                if (positionIsOpen == False) and (states[-1] == (False, False, True, False)):
                    currentState = (False, False, False, True)
            except IndexError:
                pass
    
            states.append(currentState)
            
        return (states)
    

    def priceAndStatesConstructor(self) -> pd.DataFrame:

        '''Combines the results from the positionStates() method with the underlying time series prices, and stores them in a dataframe.'''
        
        tempStates = pd.DataFrame(self.positionStates())
        tempStates.index = tempStates.index + 5 # Note the + 5 here, since batcher() was called with a subframeLength of 5 in positionStates()
        
        pricesAndStates = pd.DataFrame(self._assetTimeSeries[:, 4], columns = ['Price'])
        pricesAndStates['PositionOpen'] = tempStates[0] + tempStates[1] + tempStates[2]
        pricesAndStates.fillna(False,  inplace = True)
        
        return (pricesAndStates)
    

    def computeReturnSeries(self) -> list[float]:

        '''Computes the returns from the trade series. Returns the series as a list.'''
        
        openingAndClosingOrders = []
        for i, j in enumerate(self.positionStates()):
            if (j[0] == True):
                openingAndClosingOrders.append((i + 5, self._assetTimeSeries[:, 4][i + 5])) # Note the + 5 here, since batcher() was called with a subframeLength of 5 in positionStates()
            if (j[2] == True):
                openingAndClosingOrders.append((i + 5, self._assetTimeSeries[:, 4][i + 5])) # Note the + 5 here, since batcher() was called with a subframeLength of 5 in positionStates()
        if ((len(openingAndClosingOrders) % 2) == 1):
            openingAndClosingOrders.pop(-1)
        
        self._openingAndClosingOrders = openingAndClosingOrders
        
        profitLossForTrades = []
        holdingPeriods = []
        for i, j in enumerate(openingAndClosingOrders):
            if ((i % 2) == 1):
                profitLossForTrades.append(((j[1] - openingAndClosingOrders[i - 1][1]) / openingAndClosingOrders[i - 1][1]))
                holdingPeriods.append((j[0] - openingAndClosingOrders[i - 1][0]))
        
        self._holdingPeriods = holdingPeriods
        
        return (profitLossForTrades)
    
    
    def percentageChangeSeries(self,
                               seriesType: int) -> np.array:
        
        '''Computes the returns from the trade series as a percentage change series. Returns the series as a numpy array.'''

        if (seriesType == 1):
            return (np.array(self._profitLossForTrades, dtype = np.float64))
        if (seriesType == 2):
            return (np.array((np.diff(self._assetTimeSeries[:, 4]) / self._assetTimeSeries[:, 4][:-1]), dtype = np.float64))


    def tradeSeriesWithPositionIndices(self) -> pd.DataFrame:
        
        '''Aligns the trade series with the indices where the trades were generated at. Returns the series as a pandas DataFrame.'''
        
        indicesToBeCast = []
        for i, j in enumerate(self._openingAndClosingOrders[1::2]):
            indicesToBeCast.append(j[0])

        tradeSeries = pd.DataFrame(self.percentageChangeSeries(seriesType = 1))
        tradeSeries.index = indicesToBeCast
        
        return (tradeSeries)
    

#backtest = BacktestDriver(['SPY'], '45min', 390)
