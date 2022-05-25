'''
여기 아래는 Yahoo Finance로부터 원하는 주식 데이터를 읽어오는 코드이다.

from pandas_datareader import data as pdr
import yfinance as yf
yf.pdr_override()

data = pdr.get_data_yahoo('AAPL',start='2020-01-01', end='2022-03-02') #'AAPL'은 애플의 티커이다. 안타깝게도 미국 주식만 가능
print(data)
'''


import pandas as pd
import yfinance as yf
import statsmodels.api as sm
import getFamaFrenchFactors as gff

#1. Acquisition of Data
ticker = 'msft'
start = '2016-8-31'
end = '2022-2-3'

stock_data = yf.download(ticker, start, end, adjusted=True)

ff3_monthly = gff.famaFrench3Factor(frequency='m')
ff3_monthly.rename(columns={"date_ff_factors": 'Date'}, inplace=True)
ff3_monthly.set_index('Date', inplace=True)


print(stock_data)
print(ff3_monthly)
'''

#2. Calculation of the stock’s historical monthly returns
stock_returns = stock_data['Adj Close'].resample('M').last().pct_change().dropna()
stock_returns.name = "Month_Rtn"
ff_data = ff3_monthly.merge(stock_returns,on='Date')

#3. Calculation of Beta
X = ff_data[['Mkt-RF', 'SMB', 'HML']]
y = ff_data['Month_Rtn'] - ff_data['RF']
X = sm.add_constant(X)
ff_model = sm.OLS(y, X).fit()
print(ff_model.summary())
intercept, b1, b2, b3 = ff_model.params

#4. Estimation of Expected Returns of Stock
rf = ff_data['RF'].mean()
market_premium = ff3_monthly['Mkt-RF'].mean()
size_premium = ff3_monthly['SMB'].mean()
value_premium = ff3_monthly['HML'].mean()

expected_monthly_return = rf + b1 * market_premium + b2 * size_premium + b3 * value_premium
expected_yearly_return = expected_monthly_return * 12
print("Expected yearly return: " + str(expected_yearly_return))
'''

