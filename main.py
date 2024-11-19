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
    portfolio = Portfolio(cash_weights=0.1, data=data)
    portfolio.weights = pd.Series({
        "FTSE All Cap": 0.22,
        "US Treasury": 0.36,
        "Corporate": 0.12,
        "High Yield": 0.05,
        "EM Bond": 0.15,
    })
    sum_weights = portfolio.weights.sum()
    print(f"Sum of weights: {sum_weights}")

    # # optimize portfolio
    # optimizer = MeanVarianceOptimizer(portfolio)  
    # # add constraints
    # optimizer.add_constraint_sum_one()
    # lower_bound = pd.Series(0.1, index=portfolio.assets)
    # optimizer.add_constraint_lower_bound(lower_bound)
    #
    # new_portfolio = optimizer.optimize()  
    # portfolio_data = new_portfolio.get_portfolio_data()

    # Without optimization
    portfolio_data = portfolio.get_portfolio_data()

    # equal weight benchmark, using varibale data
    equal_weight_benchmark = data / data.iloc[0]
    equal_weight_benchmark = equal_weight_benchmark.mean(axis=1)
    combined_data = pd.concat([portfolio_data, equal_weight_benchmark], axis=1)
    combined_data.columns = ["Portfolio", "Equal Weight Benchmark"]

    # plots
    accumulate_return = fig_accumulate_return(portfolio_data)
    accumulate_return.show()

    # accumulate_return = fig_accumulate_return(combined_data)
    # accumulate_return.show()
    
    # drawdown = fig_drawdown(portfolio_data)
    # drawdown.show()

    # drawdown = fig_drawdown(combined_data)
    # drawdown.show()

    # save figure
    # drawdown.savefig("drawdown.png")
    
    plt.show()

    print(portfolio)
   

if __name__ == "__main__":
    main()

