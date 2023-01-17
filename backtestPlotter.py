import pandas as pd
import numpy as np
import matplotlib.pyplot as plt; plt.rcdefaults()
import matplotlib.patches as mpatches
from backtestDriver import BacktestDriver 


class BacktestPlotter(BacktestDriver):

    '''
    Class used to plot the results of the backtest.

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
        

    def plotIndividualTrades(self) -> None:
        
        '''Plots the underlying data with the trades executed by the backtest, shaded in.'''

        pricesAndStates = self.priceAndStatesConstructor()
        
        fig, ax1 = plt.subplots(figsize = [14.275, 9.525])
        pricesAndStates['Price'].plot(color = 'black')
        ax1.fill_between(pricesAndStates.index, 0, 1, where = pricesAndStates['PositionOpen'], transform = ax1.get_xaxis_transform(), color = 'grey', alpha = 0.5)
        ax1.set_ylim(pricesAndStates['Price'].min(), pricesAndStates['Price'].max());
        ax1.title.set_text('Long System over ' + str(self._tickerSymbols[0]) + ' with Overnight Holding Periods Permitted, ' + str(backtest._assetTimeSeries[0][0]) + ' – ' + str(backtest._assetTimeSeries[-1][0]))
        ax1.tick_params(labelsize = 16, labelright = True)
        underlyingCurve = mpatches.Patch(color = 'black', label = 'Underlying Asset')
        individualTrades = mpatches.Patch(color = 'grey', alpha = .75, label = (str(len(self._holdingPeriods)) + ' Trade(s)'))
        plt.legend(handles = [underlyingCurve, individualTrades], loc = 'upper left')
        ax1.minorticks_on()
        ax1.grid(which = 'both', linestyle = '-', linewidth = '1', color = 'dimgrey')
        ax1.grid(which = 'minor', linestyle = ':', linewidth = '1', color = 'grey')
        plt.pause(0.01)


    def cumulativeSeriesPlot(self) -> None:
        
        '''Plots the underlying data with the trades executed by the backtest, shaded in.
           Also plots the equity curve in the same figure for the trade series generated.'''

        tradeSeries = self.tradeSeriesWithPositionIndices()
        compositeSeries = pd.DataFrame(self._underlyingPercentageChangeSeries, columns = ['underlyingSeries']).cumsum()
        compositeSeries['tradeSeries'] = tradeSeries.cumsum()
        compositeSeries['tradeSeries'].iloc[0] = 0.0
        compositeSeries['tradeSeries'].iloc[-1] = float(tradeSeries.sum())
        compositeSeries = compositeSeries.interpolate(method = 'linear')
        
        pricesAndStates = self.priceAndStatesConstructor()
        
        fig, ax1 = plt.subplots(figsize = [14.275, 9.525])
        compositeSeries['underlyingSeries'].plot(color = 'black', linewidth = 1.1)
        compositeSeries['tradeSeries'].plot(color = 'C0', linewidth = 1.5)
        ax1.axhline(0.0, linewidth = 0.5, color = 'firebrick')
        ax1.fill_between(pricesAndStates.index, 0, 1, where = pricesAndStates['PositionOpen'], transform = ax1.get_xaxis_transform(), color = 'grey', alpha = 0.25)
        
        if (compositeSeries['tradeSeries'].min() < compositeSeries['underlyingSeries'].min()):
            if (compositeSeries['tradeSeries'].max() < compositeSeries['underlyingSeries'].max()):
                ax1.set_ylim(compositeSeries['tradeSeries'].min() - 0.005, compositeSeries['underlyingSeries'].max() + 0.005);
            else:
                ax1.set_ylim(compositeSeries['tradeSeries'].min() - 0.005, compositeSeries['tradeSeries'].max() + 0.005);
        else:
            if (compositeSeries['tradeSeries'].max() < compositeSeries['underlyingSeries'].max()):
                ax1.set_ylim(compositeSeries['underlyingSeries'].min() - 0.005, compositeSeries['underlyingSeries'].max() + 0.005);
            else:
                ax1.set_ylim(compositeSeries['underlyingSeries'].min() - 0.005, compositeSeries['tradeSeries'].max() + 0.005);
        
        ax1.set_title('Long System over ' + str(self._tickerSymbols[0]) + ' with Overnight Holding Periods Permitted, ' + str(backtest._assetTimeSeries[0][0]) + ' – ' + str(backtest._assetTimeSeries[-1][0]))
        ax1.tick_params(labelsize = 14, labelright = True)
        yValues = ax1.get_yticks()
        ax1.set_yticklabels(['{:,.2%}'.format(y) for y in yValues])
        underlyingCurve = mpatches.Patch(color = 'black', label = 'Underlying Asset')
        tradeSeriesCurve = mpatches.Patch(color = 'C0', alpha = 0.8, label = 'Trade Series')
        individualTrades = mpatches.Patch(color = 'grey', alpha = 0.25, label = (str(len(self._holdingPeriods)) + ' Trade(s)'))
        plt.legend(handles = [underlyingCurve, tradeSeriesCurve, individualTrades], loc = 'upper left')
        ax1.minorticks_on()
        ax1.grid(which = 'both', linestyle = '-', linewidth = '1', color = 'dimgrey')
        ax1.grid(which = 'minor', linestyle = ':', linewidth = '1', color = 'grey')
        plt.pause(0.01)


    def drawdownPlot(self) -> None:
        
        '''Plots the drawdown for both the underlying series, and the trade series.'''
        
        tradeSeries = self.tradeSeriesWithPositionIndices()
        tradeSeriesDrawdown = (((1 + tradeSeries[0]).cumprod()) - ((1 + tradeSeries[0]).cumprod()).cummax()) / ((1 + tradeSeries[0]).cumprod()).cummax()

        underlyingSeries = pd.DataFrame(self._underlyingPercentageChangeSeries)
        underlyingDrawdown = (((1 + underlyingSeries[0]).cumprod()) - ((1 + underlyingSeries[0]).cumprod()).cummax()) / ((1 + underlyingSeries[0]).cumprod()).cummax()

        compositeDrawdown = pd.concat([underlyingDrawdown, tradeSeriesDrawdown], axis = 1)
        compositeDrawdown.columns = ['underlyingSeries','tradeSeries']
        compositeDrawdown['tradeSeries'].iloc[0] = 0.0
        compositeDrawdown['tradeSeries'].iloc[-1] = float(tradeSeriesDrawdown.iloc[-1])
        compositeDrawdown = compositeDrawdown.interpolate(method = 'linear')

        fig, ax1 = plt.subplots(figsize = [14.275, 9.525])
        compositeDrawdown['underlyingSeries'].plot(color = 'black', linewidth = 1.1)
        compositeDrawdown['tradeSeries'].plot(color = 'C0', linewidth = 1.5)
        ax1.axhline(0.0, linewidth = 0.5, color = 'firebrick')
        ax1.set_title('Drawdown for Long System over ' + str(self._tickerSymbols[0]) + ' with Overnight Holding Periods Permitted, ' + str(backtest._assetTimeSeries[0][0]) + ' – ' + str(backtest._assetTimeSeries[-1][0]))
        ax1.tick_params(labelsize = 14, labelright = True)
        yValues = ax1.get_yticks()
        ax1.set_yticklabels(['{:,.2%}'.format(y) for y in yValues])
        underlyingCurve = mpatches.Patch(color = 'black', label = 'Underlying Asset')
        tradeSeriesCurve = mpatches.Patch(color = 'C0', alpha = 0.8, label = 'Trade Series')
        plt.legend(handles = [underlyingCurve, tradeSeriesCurve], loc = 'lower left')
        ax1.minorticks_on()
        ax1.grid(which = 'both', linestyle = '-', linewidth = '1', color = 'dimgrey')
        ax1.grid(which = 'minor', linestyle = ':', linewidth = '1', color = 'grey')
        plt.pause(0.01)
          
        
#backtest = BacktestPlotter(['SPY'], '45min', 390)
#backtest.plotIndividualTrades()
#backtest.cumulativeSeriesPlot()
#backtest.drawdownPlot()
