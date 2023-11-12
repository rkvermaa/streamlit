import yfinance as yf
import streamlit as st
import pandas as pd


st.write("""
         # simple stock price app
          Shown are the stock closing price and volume of google
         
         """)

# define the ticker symbol
tickerSymbol = "GOOGL"

# get data on this ticker
tickerData = yf.Ticker(tickerSymbol)

# Get the historical price for this ticker

tickerDf = tickerData.history(period='id', start = '2019-05-31', end='2020-05-31')

# open high low close volume dividend stock splits
st.write(""" ### Closing Price""")
st.line_chart(tickerDf.Close)

st.write(""" ### Volume""")
st.line_chart(tickerDf.Volume)

