import bokeh
import streamlit as st
import requests
import altair as alt
import plotly
import pandas as pd
import numpy as np
import os
from bokeh.plotting import figure, output_file, show
import datetime
from bokeh.models import Label, Title, NumeralTickFormatter
from dotenv import load_dotenv

st.title('Month long Stock time slice \nby Parrish Brady')


d = st.date_input(
     "Start Date",
     datetime.date(2019, 7, 6))
st.write('Start Date is ', d)
Ticker = st.text_input('Stock Ticker', 'IBM')
st.write('The current Stock Ticker is ', Ticker)

if 1:
    if 0:
        load_dotenv('.env')
        APIkey=os.getenv('api_token')
    if 1:

        APIkey = os.environ['APIkey']

    r = requests.get("https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol="+Ticker+"&outputsize=full&apikey="+APIkey)



    gty=r.json()
    r2=pd.DataFrame.from_dict(gty['Time Series (Daily)'])
    StockDate=[]
    ClosePrice=[]

    thirtydays=datetime.timedelta(days=+30)

    for price in r2.columns:
        priceTime=datetime.date(int(price.split("-")[0]),int(price.split("-")[1]),int(price.split("-")[2]))

        if priceTime>=d and priceTime<d+thirtydays:
                StockDate.append(price)
                ClosePrice.append(r2[price]['4. close'])



    StockDate=np.array(StockDate)
    ClosePrice=np.array(ClosePrice)

    pdDict={}
    pdDict["StockDate"]=StockDate
    pdDict["ClosePrice"]=ClosePrice
    Rpd=pd.DataFrame.from_dict(pdDict)


    if 1:


        c=alt.Chart(Rpd).mark_line().encode(
            alt.X('StockDate'),
            alt.Y('ClosePrice', axis=alt.Axis(format='$.2f'))

        )


        st.write(c)