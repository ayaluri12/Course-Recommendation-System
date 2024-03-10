import streamlit as st

class MultiPage:

    def __init__(self):
        self.pages = []
    
    def add_page(self, name, func):
        """
        Add multiple pages to the project
        """
        self.pages.append(
            {
                'title': name,
                'function': func
            }
        )
    
    def run(self):
        page = st.sidebar.selectbox(
            'App Navigation',
            self.pages,
            format_func= lambda page:page['title']
        )
        page['function']()