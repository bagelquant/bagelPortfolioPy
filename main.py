# McGill Portfolio Competition 2024
import pandas as pd
import matplotlib.pyplot as plt

from datahandler import DataHandler
from portfolio import Portfolio 
from optimizer import MeanVarianceOptimizer
from plot import fig_accumulate_return, fig_return_hist, fig_drawdown, fig_rolling_volatility


def main():
    # data input
    datahandler = DataHandler()

    # create portfolio
    data = datahandler.get_all_data()
    # drop us mbs
    data = data.drop(columns=["US MBS"])
    portfolio = Portfolio(cash_weights=0.1, data=data)
    # portfolio.weights = pd.Series({
    #     "FTSE All Cap": 0.32,
    #     "US Treasury": 0.24,
    #     "US MBS": 0.12,
    #     "Corporate": 0.12,
    #     "High Yield": 0.05,
    #     "EM Bond": 0.15,
    # })

    # optimize portfolio
    optimizer = MeanVarianceOptimizer(portfolio)  
    # add constraints
    optimizer.add_constraint_sum_one_inc_cash()
    lower_bound = pd.Series(0.1, index=portfolio.assets)
    optimizer.add_constraint_lower_bound(lower_bound)

    new_portfolio = optimizer.optimize()  
    portfolio_data = new_portfolio.get_portfolio_data()
    
    combined_data = pd.concat([portfolio_data, data], axis=1)
    # remove US MBS

    # plots
    accumulate_return = fig_accumulate_return(combined_data.loc["2020":])
    accumulate_return.show()
    
    # return_hist = fig_return_hist(portfolio_data)
    # return_hist.show()
    
    drawdown = fig_drawdown(combined_data.loc["2018":])
    drawdown.show()
    
    # rolling_volatility = fig_rolling_volatility(portfolio_data)
    # rolling_volatility.show()
    print(portfolio)
    print(new_portfolio)
    plt.show()
   

if __name__ == "__main__":
    main()

