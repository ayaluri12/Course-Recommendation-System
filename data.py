import streamlit as st
import numpy as np
import pandas as pd
from PIL import Image
import matplotlib.pyplot as plt
import seaborn as sns
import yfinance as yf
from prophet import Prophet
from dataload import uploadData,downloadData,getCollections

import warnings
warnings.filterwarnings("ignore")
## new_title = '<p style="font-family:sans-serif; color:Blue; font-size: 50px;">STOCK-IT</p>'
## st.markdown(new_title, unsafe_allow_html=True)
## st.title("STOCK-IT") 
## display = Image.open('/Users/sanjana/Desktop/Stock-it_-LOGO300.jpeg') 
## #display = np.array(display)
## st.image(display,width=200)
def app():
    
    
    st.markdown('''
        # Stock IT App''')
    st.write('---')
    st.write("\n")
    ##  st.markdown("## Data Upload")
    # st.markdown("### Upload a csv file for analysis or select a company from our sidebar!") 
    # st.write("\n")



    # uploaded_file = st.file_uploader("Choose a file", type = ['csv', 'xlsx'], accept_multiple_files=False)
    ## print(uploaded_file.name)

    ## sidebar
    
    ticker_list = getCollections('StockData')#['None','AAPL','GDX','IWM','QQQ','SPY','FB','MCD','WMT','IBM','AXP','DIS','BA','CAT','CSCO','CVX','KO','DD','XOM','GE','GS','HD','INTC','JNJ','JPM','MMM','MRK','MSFT','NKE','PFE','PG','TRV','UNH','UTX','V','VZ','DIA']
    ticker_list.insert(0, 'None')
    tickerSymbol = st.sidebar.selectbox('Stock ticker', ticker_list)

    @st.cache(suppress_st_warning=True, allow_output_mutation=True)
    def pred(ph_df):
        m = Prophet()

        # Drop the columns
        ph_df = df.drop(['open', 'high', 'low','volume', 'Daily Return'], axis=1)
        ph_df.rename(columns={'close': 'y', 'date': 'ds'}, inplace=True)

        # st.write(ph_df.head())

        m.fit(ph_df)

        future_prices = m.make_future_dataframe(periods=365)

        # Predict Prices
        forecast = m.predict(future_prices)
        #fig2 = m.plot_components(forecast)
        fig2 = m.plot(forecast, uncertainty=True)

        st.pyplot(plt)
        #forecast['ds'] =  pd.to_datetime(forecast['ds'], format='%Y-%m-%dT%H:%M:%S')
        forecast['ds']= forecast['ds'].dt.strftime("%Y-%m-%d")
        fc = forecast.copy()
        fc = fc.rename(columns={'yhat':'Predicted Closing Price', 'yhat_lower': 'Predicted Low Price', 'yhat_upper': 'Predicted High Price'})
        #st.write(forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail())
        #st.write(fc[['ds', 'Predicted Closing Price', 'Predicted Low Price', 'Predicted High Price']].head(10))
        return fc

    @st.cache(suppress_st_warning=True, allow_output_mutation=True)
    def plot_g(df):
        f, (ax1, ax2) = plt.subplots(1, 2, figsize=(14,5))
        ax1.plot(df["date"], df["close"])
        ax1.set_xlabel("Date", fontsize=12)
        ax1.set_ylabel("Stock Price")
        ax1.set_title("Close Price History")

        # Second Subplot
        ax2.plot(df["date"], df["high"], color="green")
        ax2.set_xlabel("Date", fontsize=12)
        ax2.set_ylabel("Stock Price")
        ax2.set_title("High Price History")

        # # Third Subplot
        # ax1.plot(amzn_df["date"], amzn_df["low"], color="red")
        # ax1.set_xlabel("Date", fontsize=12)
        # ax1.set_ylabel("Stock Price")
        # ax1.set_title("Amazon Low Price History")

        # # Fourth Subplot
        # ax2.plot(df["date"], df["volume"], color="orange")
        # ax2.set_xlabel("Date", fontsize=12)
        # ax2.set_ylabel("Stock Price")
        # ax2.set_title("Amazon's Volume History")
        st.pyplot(plt)



    if tickerSymbol != 'None':
        st.markdown('''        
        Shown are the stock price data for query companies!
        ''')

        # company's info
        tickerData = yf.Ticker(tickerSymbol)


        try:
            string_name = tickerData.info['longName']
            st.header('**%s**' % string_name)
            string_summary = tickerData.info['longBusinessSummary']
            st.info(string_summary)
        except:
            st.write("Company info not available.")
        ## end of company's info

        #df = pd.read_csv('./data/'+tickerSymbol+'.csv', sep = ',')
        df = downloadData('StockData',tickerSymbol)
        df.columns = map(str.lower, df.columns)


        st.header(f"**{tickerSymbol} data**")
        col1, col2= st.columns(2)
        col1.metric("Number of Rows", f"{len(df)}")
        col2.metric("Number of Features ", f"{df.shape[1]}")
        # col3.metric("Humidity", "86%", "4%")
        st.write(df.head())

        st.header(f"**Description for {tickerSymbol}**")
        st.write(df.describe())

        plot_g(df)


        st.header(f"**Daily Returns For {tickerSymbol} Company**")
        df['Daily Return'] = df['close'].pct_change()
        plt.figure(figsize=(12, 7))
        sns.distplot(df['Daily Return'].dropna(), bins=100, color='purple')
        plt.ylabel('Daily Return')
        plt.title(f'{tickerSymbol}')
        st.pyplot(plt)

        ### machine learning
        st.header(f"**Machine Learning**")

        # Drop the columns
        ph_df = df.drop(['open', 'high', 'low','volume', 'Daily Return'], axis=1)
        ph_df.rename(columns={'close': 'y', 'date': 'ds'}, inplace=True)

        fc = pred(ph_df)

        fc['ds2']= pd.to_datetime(fc['ds']).dt.date
        d = st.date_input("Pick a date to view prediction: ", value = fc['ds2'].iloc[np.ceil(len(fc)/2).astype('int')], min_value =fc['ds2'].iloc[0], max_value =fc['ds2'].iloc[len(fc)-1])

        st.write(fc[['ds', 'Predicted Closing Price', 'Predicted Low Price', 'Predicted High Price']].loc[fc['ds2']==d])
        
        num = st.number_input("Select the number of rows for prediction", 0, len(fc)-1, 10, 1)
        st.write(fc[['ds', 'Predicted Closing Price', 'Predicted Low Price', 'Predicted High Price']].tail(num))
        

    # User input file
    else:
        global data
        st.markdown("### Upload a csv file for analysis or select a company from our sidebar!") 
        st.write("\n")

        uploaded_file = st.file_uploader("Choose a file", type = ['csv', 'xlsx'], accept_multiple_files=False)
        if uploaded_file is not None:
            try:
                df = pd.read_csv(uploaded_file)
                df.columns = map(str.lower, df.columns)

                st.header(f"**Your Data Header**")
                col1, col2= st.columns(2)
                col1.metric("Number of Rows", f"{len(df)}")
                col2.metric("Number of Features ", f"{df.shape[1]}")
                # col3.metric("Humidity", "86%", "4%")
                st.write(df.head())

                st.header(f"**Description for your Data**")
                st.write(df.describe())


                st.header(f"**Daily Returns For Company**")
                df['Daily Return'] = df['close'].pct_change()
                plt.figure(figsize=(12, 7))
                sns.distplot(df['Daily Return'].dropna(), bins=100, color='purple')
                plt.ylabel('Daily Return')
                plt.title(f'{tickerSymbol}')
                st.pyplot(plt)

                #Create a button to upload data
                with st.expander("Upload Data"):
                    with st.form(key = "File_Upload"):
                        textInput = st.text_input(label= "Enter filename")
                        submitted = st.form_submit_button(label = "Upload")
                        
                        if submitted:
                            fileName = textInput
                            #st.write(fileName)
                            uploadData('StockData',fileName, df)

                    

                

                ### machine learning
                st.header(f"**Machine Learning**")
                # m = Prophet()

                # Drop the columns
                ph_df = df.drop(['open', 'high', 'low','volume', 'Daily Return'], axis=1)
                ph_df.rename(columns={'close': 'y', 'date': 'ds'}, inplace=True)
                fc = pred(ph_df)

                fc['ds2']= pd.to_datetime(fc['ds']).dt.date
                d = st.date_input("Pick a date to view prediction: ", value = fc['ds2'].iloc[np.ceil(len(fc)/2).astype('int')], min_value =fc['ds2'].iloc[0], max_value =fc['ds2'].iloc[len(fc)-1])
                st.write(fc[['ds', 'Predicted Closing Price', 'Predicted Low Price', 'Predicted High Price']].loc[fc['ds2']==d])

                num = st.number_input("Select the number of rows for prediction", 0, len(fc)-1, 10, 1)
                st.write(fc[['ds', 'Predicted Closing Price', 'Predicted Low Price', 'Predicted High Price']].tail(num))
            except Exception as e:
                print(e)


