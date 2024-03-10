import fitz
from textblob import TextBlob
import numpy as np
import requests
import pandas as pd
import nltk
import streamlit as st
# demo = 'f4a42c38c25654431217221895b8c1df'
# company = 'AAPL'


def app():
  st.markdown("### Upload an earnings call transcript (.pdf) for analysis") 
  st.write("\n")

  uploaded_pdf = st.file_uploader("Choose a file", type = ['pdf'], accept_multiple_files=False)
  if uploaded_pdf is not None:
    with fitz.open(stream=uploaded_pdf.read(), filetype="pdf") as doc:
      text = ""
      for page in doc:
        text += page.get_text()

      negative = 0
      positive = 0
      neutral = 0
      all_sentences = []
      sentiment_call = TextBlob(text)

      for sentence in sentiment_call.sentences:
        #print(sentence.sentiment.polarity)
        if sentence.sentiment.polarity < 0:
          negative +=1
        if sentence.sentiment.polarity > 0:
          positive += 1
        else:
          neutral += 1
      
        all_sentences.append(sentence.sentiment.polarity) 

      st.header('General Info')
      met_dict = doc.metadata

      col1, col2, col3= st.columns(3)
      col1.metric("Lenght of Text", f"{len(text)}")
      col2.metric("Number of Pages ", f"{doc.page_count}")
      col3.metric("Number of Sentences ", f"{negative+positive+neutral}")

      st.header('Sentiment Analysis Results')
      # sentiment_call = TextBlob(text)
      st.subheader('Polarity')
      st.write("Polarity is a score between -1 and 1. The closer polarity number is to 1, the more positive the document.")

      col1, col2= st.columns(2)
      col1.metric("Polarity Score: ", f"{sentiment_call.sentiment.polarity}")
      col2.metric("Subjectivity Score", f"{sentiment_call.sentiment.subjectivity}")
      #st.write(f"Polarity score for your whole document is {sentiment_call.sentiment.polarity}")

      st.subheader('Polarity Score Calculation for Individual Sentences')


      col1, col2, col3= st.columns(3)
      col1.metric("Number of Positive Sentences", f"{str(positive)}")
      col2.metric("Number of Negative Sentences", f"{str(negative)}")
      col3.metric("Number of Neutral Sentences", f"{str(neutral)}")

      st.write(f"Your document has {str(positive)} positive sentences. {str(negative)} negative sentences, and {str(neutral)} neutral sentences.")

      # st.subheader('Sentences with Polarity Score of 0.8 or Higher')
      # for sentence in sentiment_call.sentences:
      #   if sentence.sentiment.polarity > 0.8:
      #     st.write(f"~~~{sentence}")




