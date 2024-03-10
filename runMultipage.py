import os
import streamlit as st

from multipage import MultiPage
import data,updateMetaData,readPDF,spark, live_data


app = MultiPage()

app.add_page('Upload Data', data.app)
app.add_page('Update Meta Data', updateMetaData.app)
app.add_page('Upload Earnings Call', readPDF.app)
app.add_page('Spark Analysis', spark.app)
app.add_page('Live Data Streaming', live_data.app)

app.run()