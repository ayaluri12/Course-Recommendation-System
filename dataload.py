from typing import Collection
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import pandas as pd
import streamlit as st
import os



def initiliaze(collectionName):
    if not firebase_admin._apps:
        cred = credentials.Certificate(r"./serviceAccountKey.json")
        firebase_admin.initialize_app(cred)
    db = firestore.client()
    collection = db.collection(collectionName)
    return collection
@st.experimental_memo
def getCollections(collectionName):
    docs = []
    collection = initiliaze(collectionName)
    streamList = collection.stream()
    for doc in streamList:
        #print(doc)
        docs.append(doc.id)
    return docs

@st.experimental_memo
def uploadData(collectionName, fileName, dataframe):
    collection = initiliaze(collectionName)
    doc = collection.document(fileName)
    #print(dataframe.columns)
    res = dataframe.to_dict(orient = "list")
    doc.set(res)
    st.info("Upload Successful")
@st.experimental_memo
def downloadData(collectionName, stockName):
    collection = initiliaze(collectionName)
    docs = collection.stream()
    for doc in docs:    
        if doc.id == stockName:
            print("Last updated {} on {}".format(stockName,doc.update_time))
            #print(console.log(doc.data()))
            out = doc.to_dict()
    outDF = pd.DataFrame.from_dict(out)

    return outDF

if __name__=='__main__':
    pass