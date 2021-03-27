import streamlit as st
import requests
import altair as alt
import pandas as pd
import numpy as np
import os
import datetime
from dotenv import load_dotenv


#Title of the heroku page
st.title('Month long Stock time slice \nby Parrish Brady')

#Selection of the date
d = st.date_input(
     "Start Date",
     datetime.date(2019, 7, 6))
st.write('Start Date is ', d)

#Manual imput of the ticker
Ticker = st.text_input('Stock Ticker', 'IBM')
st.write('The current Stock Ticker is ', Ticker)

if 1:
    if 0:#for working locally
        load_dotenv('.env')
        APIkey=os.getenv('api_token')
    if 1:
        #for loading to Heroku
        APIkey = os.environ['APIkey']

    #The API for alphavantage using requests
    r = requests.get("https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol="+Ticker+"&outputsize=full&apikey="+APIkey)


    #converting the Json to pandas
    gty=r.json()
    r2=pd.DataFrame.from_dict(gty['Time Series (Daily)'])

    #extracting a months amount of data
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

    #recompiling a dataframe for plotting
    pdDict={}
    pdDict["StockDate"]=StockDate
    pdDict["ClosePrice"]=ClosePrice
    Rpd=pd.DataFrame.from_dict(pdDict)


    #Plotting with altair, bokeh did not work for this example
    if 1:
        c=alt.Chart(Rpd).mark_line().encode(
            alt.X('StockDate'),
            alt.Y('ClosePrice', axis=alt.Axis(format='$.2f'))
        )
        st.write(c)