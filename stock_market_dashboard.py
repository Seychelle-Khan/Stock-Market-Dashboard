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

#Current date
today_date = datetime.today().strftime('%Y-%m-%d')
year_first_day = date(date.today().year, 1, 1)

#streamlit dashboard base features
st.title("Stock Market Trends Dashboard")
st.sidebar.header("Filters")

st.header("Ticker Legend")
acronyms = ['KOS','HL','ALTM','AG','RIG','LAC','AAPL','MSFT','JNJ','MP']
names = ['Kosmos Energy Limited','Hecla Mining Company','Arcadium Lithium plc',
         'First Majestic Silver Corp.','Transocean Ltd.','Lithium Americas Corp.', 
         'Apple Inc.', 'Microsoft Corporation','Johnson & Johnson','MP Materials Corp.']
tickers = pd.DataFrame({'Ticker':acronyms,'Company':names})
st.table(tickers)

#DATA TRANSFORMATION
#Kosmos Energy Limited KOS
#Hecla Mining Company HL
#Arcadium Lithium plc ALTM
#First Majestic Silver Corp. AG
#Transocean Ltd. RIG
#Lithium Americas Corp. LAC
#Apple Inc. AAPL
#Microsoft Corporation MSFT
#Johnson & Johnson JNJ
#MP Materials Corp. MP
data = yf.download("KOS HL ALTM AG RIG LAC AAPL MSFT JNJ MP", 
                   start=year_first_day, 
                   end=today_date, 
                   group_by="Ticker")

data_kos = data['KOS']
data_kos.reset_index(inplace=True)
data_kos['Date'] = pd.to_datetime(data_kos['Date'])
data_kos['Ticker'] = 'KOS'

data_hl = data['HL']
data_hl.reset_index(inplace=True)
data_hl['Date'] = pd.to_datetime(data_hl['Date'])
data_hl['Ticker'] = 'HL'

data_altm = data['ALTM']
data_altm.reset_index(inplace=True)
data_altm['Date'] = pd.to_datetime(data_altm['Date'])
data_altm['Ticker'] = 'ALTM'

data_ag = data['AG']
data_ag.reset_index(inplace=True)
data_ag['Date'] = pd.to_datetime(data_ag['Date'])
data_ag['Ticker'] = 'AG'

data_rig = data['RIG']
data_rig.reset_index(inplace=True)
data_rig['Date'] = pd.to_datetime(data_rig['Date'])
data_rig['Ticker'] = 'RIG'

data_lac = data['LAC']
data_lac.reset_index(inplace=True)
data_lac['Date'] = pd.to_datetime(data_lac['Date'])
data_lac['Ticker'] = 'LAC'

data_aapl = data['AAPL']
data_aapl.reset_index(inplace=True)
data_aapl['Date'] = pd.to_datetime(data_aapl['Date'])
data_aapl['Ticker'] = 'AAPL'

data_msft = data['MSFT']
data_msft.reset_index(inplace=True)
data_msft['Date'] = pd.to_datetime(data_msft['Date'])
data_msft['Ticker'] = 'MSFT'

data_jnj = data['JNJ']
data_jnj.reset_index(inplace=True)
data_jnj['Date'] = pd.to_datetime(data_jnj['Date'])
data_jnj['Ticker'] = 'JNJ'

data_mp = data['MP']
data_mp.reset_index(inplace=True)
data_mp['Date'] = pd.to_datetime(data_mp['Date'])
data_mp['Ticker'] = 'MP'


dfs = [data_kos,data_hl,data_altm,data_ag,data_rig,data_lac,data_aapl,
       data_msft,data_jnj,data_mp]
data_all = pd.concat(dfs)
data_all['Average'] = data_all.loc[:, ["High","Low"]].mean(axis = 1)


#Filters
Ticker_filter = st.sidebar.multiselect("Ticker", options=data_all["Ticker"].unique())
start_date = st.sidebar.date_input("Start Date", data_all["Date"].min())
end_date = st.sidebar.date_input("End Date", data_all["Date"].max())

if Ticker_filter:
    data_all = data_all[data_all["Ticker"].isin(Ticker_filter)]
    data_display = data_display[data_display["Ticker"].isin(Ticker_filter)]
if start_date:
    start_date = pd.to_datetime(start_date)
    data_all = data_all[data_all["Date"]>start_date]
if end_date:
    end_date = pd.to_datetime(end_date)
    data_all = data_all[data_all["Date"]<end_date]



#Organizing table for display
data_avg = data_all[['Date','Ticker','Average']]
data_avg['Difference in Average'] = data_avg.groupby('Ticker')['Average'].diff()
data_avg['% Change in Average Price'] = data_avg.groupby('Ticker')['Average'].pct_change()
data_avg['% Change in Average Price'] = data_avg['% Change in Average Price']*100
data_avg['% Change in Average Price'] = data_avg['% Change in Average Price'].round(decimals=2)
data_avg['% Change in Average Price'] = data_avg['% Change in Average Price'].astype(str) + '%'
data_avg['% Change in Average Price'] = data_avg['% Change in Average Price'].str.replace('nan%', 'nan')

data_display = data_all.merge(data_avg,how='inner',on=['Date','Ticker'])
data_display = data_display.drop(columns=['Difference in Average','Average_x']).rename(columns={'Average_y':'Average'})

#Re-order dataframe for display on dashboard
#data_display = data_display[['Date', 'Ticker', 'Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume', 'Average', '% Change in Average Price']]
data_display = data_display.sort_values(by='Date', ascending=False)
st.header("Stock Market Trends Overview")
st.subheader("Today's Prices")
st.table(data_display.head(7))



#Dashboard charts
st.subheader("Open Price over Time")
open_prices_over_time = data_all[["Date","Ticker","Open"]]
fig=plt.figure(figsize=(10, 6))
sns.lineplot(x='Date', y='Open', data=open_prices_over_time, hue='Ticker')
plt.ylabel("Open Price")
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.xticks(rotation=90)
plt.show()
st.pyplot(fig)

st.subheader("Close Price over Time")
close_prices_over_time = data_all[["Date","Ticker","Close"]]
fig=plt.figure(figsize=(10, 6))
sns.lineplot(x='Date', y='Close', data=close_prices_over_time, hue='Ticker')
plt.ylabel("Close Price")
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.xticks(rotation=90)
plt.show()
st.pyplot(fig)

st.subheader("Average Price over Time")
avg_prices_over_time = data_all[["Date","Ticker","Average"]]
fig=plt.figure(figsize=(10, 6))
sns.lineplot(x='Date', y='Average', data=avg_prices_over_time, hue='Ticker')
plt.ylabel("Average Price")
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.xticks(rotation=90)
plt.show()
st.pyplot(fig)

st.subheader("Volume over Time")
vol_over_time = data_all[["Date","Ticker","Volume"]]
fig=plt.figure(figsize=(10, 6))
sns.lineplot(x='Date', y='Volume', data=vol_over_time, hue='Ticker')
plt.ylabel("Volume")
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.xticks(rotation=90)
plt.show()
st.pyplot(fig)
