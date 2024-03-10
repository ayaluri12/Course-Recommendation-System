import streamlit as st
import pandas as pd
from datetime import datetime
from dataload import uploadData,downloadData,getCollections

# def adjustVals(originalDataFrame, appendData):
#     # cols = list(df.columns)
#     # actualIndex = cols.index('date')
#     # poppedDate = rwNew.pop(pos)
#     # rwNew.insert(actualIndex,poppedDate)
#     for col in originalDataFrame.columns:
#         actualIndex = 

def app():

    st.markdown('''
    # Stock IT App
    ''')
    st.write('---')

    st.write("\n")
    ##  st.markdown("## Data Upload")
    #st.markdown("### Meta Data Update") 
    #st.write("\n")

    #ticker_list = getCollections('StockData')
    ticker_list.insert(0, 'None')
    tickerSymbol = st.sidebar.selectbox('Stock ticker', ticker_list)

    if tickerSymbol == 'None':
        st.info("Select a Stock ticker to proceed with")
    else:
        df = downloadData('StockData',tickerSymbol)
        #df = df[['Date','OPEN','HIGH','LOW','VOLUME','CLOSE']]
        st.header(f"**{tickerSymbol} data**")
        st.dataframe(df.head())

        with st.expander("Change Column Name"):
            #### Change information about columns"
            col1, col2 = st.columns(2)

            #Design thecolumn names
                

            name = col1.radio("Select column", df.columns)          
            newName = col2.text_input("Enter new column name here","Input")         

            if col2.button(label = "Submit") and newName != "Input":
                df.rename(columns = {name:newName}, inplace= True)

                st.markdown("#### Updated dataframe")
                st.dataframe(df.head(5))
                amendColButton = st.button("Press here to update data in database")
                if amendColButton:
                    uploadData('StockData',tickerSymbol, df)

        

        ###Adding new rows to the data
        newRowVal = ""
        with st.expander("Add rows"):
                        
            if newRowVal == "":
                st.info("Please enter data in the order: "+ ', '.join(df.columns))
                
            newRowVal = st.text_input("Enter Rows")
            rwNew = []
            if newRowVal:
                pos = 0
                #posNew={}
                for rows in newRowVal.split("/n"):
                    row = [x.strip() for x in rows.split(",")]
                    #zipped = zip(row,list(df.columns))
                    if len(row) == len(df.columns):
                        #st.write(row)
                        #testcols = df.columns
                        for i,val in enumerate(row):
                            #print(col)
                            if '-' not in val:
                                rwNew.append(float(val))
                                #posNew[testcols[i]]
                            else:
                                #rwNew.append(datetime.strptime(val,"%Y-%m-%d"))
                                rwNew.append(val) #Date stored in firebase as string
                                #Find the position of date object to append it accordingly
                                pos = i

                        #Adjusting the changes in the position accordingly
                        #adjustVals(df,rwNew)
                        cols = list(df.columns)
                        actualIndex = cols.index('date')
                        poppedDate = rwNew.pop(pos)
                        rwNew.insert(actualIndex,poppedDate)

                        df = df[cols]
                        df2 = pd.DataFrame([rwNew],columns = cols)
                        
                        df = df.append(df2, ignore_index=True)

                        st.info("Insert Successful")
                        st.dataframe(df.tail(5))

                        appendRowButton = st.button("Press here to update data in database")
                        if appendRowButton:
                            uploadData('StockData',tickerSymbol, df)
                            #st.info("File upload successful")

                    else:
                        print(len(row),len(df.columns))
                        st.error("Number of values less than columns")
0