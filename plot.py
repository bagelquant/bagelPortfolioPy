"""
plotting functions

Using Rutgers color scheme with red and black
"""

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.figure import Figure


def fig_accumulate_return(price: pd.DataFrame) -> Figure:
    fig, ax = plt.subplots()
    price.to_excel("price.xlsx")
    price_new = price / price.iloc[0]
    price_new = price_new - 1
    price_new.plot(ax=ax)

    # show percentage on y-axis
    vals = ax.get_yticks()
    ax.set_yticklabels(['{:,.0%}'.format(x) for x in vals])

    # Highlight the first column and darken the rest
    for line in ax.get_lines()[1:]:
        # line.set_color("Grey")
        # set alpha to 0.5
        line.set_alpha(0.5)
        # set linewidth to 0.5
        line.set_linewidth(0.5)

    # title
    ax.set_title("Accumulated Return since 2011")
    return fig
    

def fig_return_hist(price: pd.DataFrame, bins: int = 50) -> Figure:
    fig, ax = plt.subplots()
    price.pct_change().hist(bins=bins, ax=ax)
    return fig


def fig_drawdown(price: pd.DataFrame) -> Figure:
    fig, ax = plt.subplots()
    price_new = price / price.iloc[0]
    max_drawdown_rate = (price_new - price_new.cummax()) / price_new.cummax()
    max_drawdown_rate.plot(ax=ax)

    # show percentage on y-axis
    vals = ax.get_yticks()
    ax.set_yticklabels(['{:,.0%}'.format(x) for x in vals])

    # Highlight the first column and darken the rest
    for line in ax.get_lines()[1:]:
        # line.set_color("Grey")
        # set alpha to 0.5
        line.set_alpha(0.5)
        # set linewidth to 0.5
        line.set_linewidth(0.5)

    # title
    ax.set_title("Max Drawdown since 2018")
    return fig


def fig_rolling_volatility(price: pd.DataFrame, window: int = 252) -> Figure:
    fig, ax = plt.subplots()
    price.pct_change().rolling(window=window).std().plot(ax=ax)
    return fig


if __name__ == "__main__":
    data = pd.DataFrame({
        "AAPL": [1, 2, 3],
        "GOOGL": [4, 5, 6],
        "MSFT": [7, 8, 9]
    })

    fig = fig_accumulate_return(data)
    fig.show()
    fig = fig_return_hist(data)
    fig.show()
    fig = fig_drawdown(data)
    fig.show()
    fig = fig_rolling_volatility(data)
    fig.show()

