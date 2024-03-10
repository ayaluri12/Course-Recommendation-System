import numpy as np
import requests
import pandas as pd
import streamlit as st




def app():

	st.markdown('''LIVE DATA''')
	st.write('---')
	st.write("\n")

	company = st.selectbox('Select one of the top S&p 500 companies for live data!',('AAPL', 'MSFT', 'AMZN', 'FB', 'TSLA'))
	name = company+'_NEW.csv'
	feat = ["Open", "High", "Low Close", "Adj Close", "Volume", "name"]
	df = pd.read_csv(f'./{name}', names = feat)
	df = df.drop('name', axis=1)
	df = df.reset_index(drop=True)
	st.dataframe(df)
	