# Backtesting Platform

## Table of Contents
+ [General Description](#gendes)
+ [Example Outputs](#examou)		
+ [Suggestions for Continuation](#sugcon)

## General Description <a name = "gendes"></a>

Unregistered package for performing backtests.

**The package is comprised of four classes which serve the following purposes:**
```
    1.  BacktestDriver
            - Used to determine where trades would have occurred given a strategy and a time series of price data. 
            - Also used for housing various methods that organize and structure data.
            - Is the base class of all of the other classes.
    
    2.  BacktestPlotter
            - Class used to plot the results of the backtest.
            - Is the child class of BacktestDriver.

    3.  BacktestMetrics
            - Used for computing and organizing any information that you wish to compute and log from the backtest.
            - Is the child class of BacktestDriver.

    4.  BacktestStorager
            - Used to store data either in the form of logs, plots, or both.
            - Is the child class of BacktestMetrics, which is the child class of BacktestDriver.
```

The classes BacktestDriver and BacktestPlotter are fully functional, whereas BacktestMetrics and BacktestStorager are not. The skeletal structure is laid out for how things should be done, and there are empty or partially empty methods in the source code of these two classes that outline the recommended implementation and flow of data to and from the classes. I may fill out some more syntax at a later date, but for now, I’ll leave you to customize it how you please. You may not even need them, depending on what you want to do with the program. 

Class instantiation is shown in the source code at the bottom of each file.

The program obtains data from the claydates package, which calls upon the Twelve Data API. For more information, navigate to the claydates package's [Github](https://github.com/ClaytonDuffin/claydates), or [PyPi](https://pypi.org/project/claydates/).

## Example Outputs <a name = "examou"></a>

![exampleOutput1](https://user-images.githubusercontent.com/116965482/212800978-a8b970a9-2144-4202-98b3-c82e63878627.png)

![exampleOutput2](https://user-images.githubusercontent.com/116965482/212801012-886e33cf-02f5-4870-9fe0-9fac7ff69274.png)

![exampleOutput3](https://user-images.githubusercontent.com/116965482/212801051-3450d801-0dad-4a18-a624-a907adc10277.png)

![exampleOutput4](https://user-images.githubusercontent.com/116965482/212801079-22a5d57f-ee80-488a-add6-75fe40916dc8.png)

## Suggestions for Continuation <a name = "sugcon"></a>

1. Fill out more syntax in the source code of the classes. Efforts here would be best directed to the classes BacktestMetrics and BacktestStorager.

2. Be mindful of time complexity if you decide to build it out further. Consider using numba JIT to enhance the runtime of BacktestMetrics when/if you decide to build it out. Also, depending on what you decide to do with it, the program could benefit from multiprocessing. Also consider replacing the yieldCurveParser() method in the BacktestMetrics class with something that runs faster.
