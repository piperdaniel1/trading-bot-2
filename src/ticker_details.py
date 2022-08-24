import pandas
from matplotlib import pyplot as plt
import yfinance as yf
import inquirer
import os
import colored as c
import talib

def print_basic_info(ticker: yf.Ticker):
    ACCENT_COLOR = c.fg('green')
    PRIMARY_COLOR = c.fg('white')
    ERR_COLOR = c.fg('red')

    res = c.attr('reset')
    info = ticker.info
    print(f"{ACCENT_COLOR}Sector:{res}", f"{ERR_COLOR}n/a{res}" if not 'sector' in info else f"{PRIMARY_COLOR}{info['sector']}{res}")
    print(f"{ACCENT_COLOR}Industry:{res}", f"{ERR_COLOR}n/a{res}" if not 'industry' in info else f"{PRIMARY_COLOR}{info['industry']}{res}")
    print(f"{ACCENT_COLOR}Full time employees:{res}", f"{ERR_COLOR}n/a{res}" if not 'fullTimeEmployees' in info else f"{PRIMARY_COLOR}{info['fullTimeEmployees']:,}{res}")
    print(f"{ACCENT_COLOR}Location:{res}", f"{ERR_COLOR}n/a{res}" if not 'city' in info or not 'state' in info or not 'country' in info else f"{PRIMARY_COLOR}{info['city']}, {info['state']}{res}, {info['country']}")
    print(f"{ACCENT_COLOR}Website:{res}", f"{ERR_COLOR}n/a{res}" if not 'website' in info else f"{PRIMARY_COLOR}{info['website']}{res}")
    print(f"{ACCENT_COLOR}Business Summary:{res}", f"{ERR_COLOR}n/a{res}" if not 'longBusinessSummary' in info else f"{PRIMARY_COLOR}{info['longBusinessSummary']}{res}")

def print_technical_analysis(ticker: yf.Ticker):
    pass

def execute_ticker_details():
    HEADER_COLOR = c.fg('yellow')
    questions = [
        inquirer.Text('ticker', message='What is the ticker of the stock?')
    ]
    answer = inquirer.prompt(questions)

    print("\nPlease wait, querying for data...")
    yf_ticker = yf.Ticker(answer['ticker'])
    os.system('clear')

    print(" === Basic Info ===")
    print_basic_info(yf_ticker)

    print(" === Technical Analysis ===")
    bars = yf_ticker.history()
    print(type(bars))
    print(bars)
    bars.plot()

