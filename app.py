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



st.title('Month long Stock time slice')






d = st.date_input(
     "Start Date",
     datetime.date(2019, 7, 6))
st.write('Start Date is ', d)
Ticker = st.text_input('Stock Ticker', 'IBM')
st.write('The current Stock Ticker is ', Ticker)


#Ticker="IBM"


if 1:
    if 0:
        load_dotenv('.env')
        APIkey=os.getenv('api_token')
    print(APIkey)
    #APIkey="GJKSUSWKNT7GMC1N"

    #r = requests.get('https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY_EXTENDED&symbol=IBM&interval=15min&slice=year1month1&apikey='+APIkey+'')
    r = requests.get("https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol="+Ticker+"&outputsize=full&apikey="+APIkey)

    #r = requests.get(
    #    "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=IBM&outputsize=full&apikey=demo")

    #print(r)
    #print(r.status_code)

    #print(r.headers['content-type'])

    #print(r.encoding)

    #print(r.text)

    gty=r.json()
    #print(gty)
    r2=pd.DataFrame.from_dict(gty['Time Series (Daily)'])
    #print(r2)
    #print(r2.columns)

    #print(datetime.date(int(r2.columns[0].split("-")[0]),int(r2.columns[0].split("-")[1]),int(r2.columns[0].split("-")[2])))
    StockDate=[]
    ClosePrice=[]

    thirtydays=datetime.timedelta(days=+30)

    for price in r2.columns:
        priceTime=datetime.date(int(price.split("-")[0]),int(price.split("-")[1]),int(price.split("-")[2]))

        if priceTime>=d and priceTime<d+thirtydays:
                #StockDate.append(datetime.date(int(price.split("-")[0]),int(price.split("-")[1]),int(price.split("-")[2])))
                StockDate.append(price)
                ClosePrice.append(r2[price]['4. close'])
                #print(r2[price]['4. close'])



    StockDate=np.array(StockDate)
    ClosePrice=np.array(ClosePrice)

    pdDict={}
    pdDict["StockDate"]=StockDate
    pdDict["ClosePrice"]=ClosePrice
    Rpd=pd.DataFrame.from_dict(pdDict)


    if 1:

        cc=alt.Chart(Rpd).mark_line().encode(
            x='StockDate',
            y='ClosePrice'
        )

        c=alt.Chart(Rpd).mark_line().encode(
#            alt.X('StockDate', axis=alt.Axis(format='$.2f')),
            alt.X('StockDate'),
            alt.Y('ClosePrice', axis=alt.Axis(format='$.2f'))

        )


        st.write(c)