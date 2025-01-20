# -*- coding: utf-8 -*-
"""
Created on Tue Dec 17 17:43:03 2024

@author: seych
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import yfinance as yf
from datetime import datetime
from datetime import date
import mplfinance as mpf

#Current date
today_date = datetime.today()#.strftime('%Y-%m-%d')
#year_first_day = date(date.today().year, 1, 1)
previous_year = datetime.today().year -1
today_last_year = today_date.replace(year = previous_year)

#streamlit dashboard base features + Page Configurations
#st.title("Stock Market Trends Dashboard")
st.set_page_config(
    page_title="Stock Market Trends Dashboard",
    layout="wide",
    initial_sidebar_state="expanded")
st.sidebar.header("Filters")

#Tickers
acronyms = ['KOS','HL','ALTM','AG','RIG','LAC','AAPL','MSFT','JNJ','MP']
names = ['Kosmos Energy Limited','Hecla Mining Company','Arcadium Lithium plc',
         'First Majestic Silver Corp.','Transocean Ltd.','Lithium Americas Corp.', 
         'Apple Inc.', 'Microsoft Corporation','Johnson & Johnson','MP Materials Corp.']
tickers = pd.DataFrame({'Ticker':acronyms,'Company':names})

#Pull stock data
def get_stock_data(ticker):
    data = yf.download(ticker, 
                       start=today_last_year, 
                       end=today_date, 
                       group_by="Ticker")
    data = data[ticker]
    data['Date pulled'] = data.index
    data['Date pulled'] = pd.to_datetime(data['Date pulled'])
    data = data.sort_values(by='Date pulled',ascending=False)
    return data

def get_chart_title(ticker):
    candlestick_chart_title="Candlestick Chart for "+ticker
    return candlestick_chart_title
    

# data = yf.download("MSFT", 
#                    start=today_last_year, 
#                    end=today_date, 
#                    group_by="Ticker")
# data = data['MSFT']
# data['Date pulled'] = data.index
# data['Date pulled'] = pd.to_datetime(data['Date pulled'])
# data = data.sort_values(by='Date pulled',ascending=False)

#Sidebar Filters & get ticker & get chart title
ticker = st.sidebar.selectbox("Select a ticker:", acronyms, index=2)
company = tickers['Company'].loc[tickers['Ticker']==ticker].iloc[0]
#Getting stock data
if ticker:
        data = get_stock_data(ticker)
        candlestick_chart_title = get_chart_title(ticker)

#Sidebar filters
start_date = st.sidebar.date_input("Start Date", data["Date pulled"].min())
end_date = st.sidebar.date_input("End Date", data["Date pulled"].max())

if start_date:
    start_date = pd.to_datetime(start_date)
    data = data[data["Date pulled"]>start_date]
if end_date:
    end_date = pd.to_datetime(end_date)
    data = data[data["Date pulled"]<end_date]
    
#Sidebar Ticker legend
st.sidebar.header("Ticker Legend")
st.sidebar.table(tickers)


#Cards
col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    st.metric("Open", "${:.2f}".format(data['Open'][0]))
with col2:
    st.metric("Close", "${:.2f}".format(data['Close'][0]))
with col3:
    st.metric("High", "${:.2f}".format(data['High'][0]))
with col4:
    st.metric("Low", "${:.2f}".format(data['Low'][0]))
with col5:
    st.download_button("Download Stock Data for "+company, data.to_csv(index=True), file_name=f"{ticker}_stock_data.csv", mime="text/csv")

#Chart
st.subheader("Prices over Time")
fig2, ax = mpf.plot(data,type="candle",title=candlestick_chart_title,ylabel="Price", style="mike",volume=True,figratio=(6,3),figscale=0.5,returnfig=True)
st.pyplot(fig2,use_container_width=True)
