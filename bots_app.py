import streamlit as st
from multiapp import MultiApp
from apps import home,snail,market,scalper

st.set_page_config(page_title='JimBot BVT Bot', page_icon='\xe2\x9c\x85', layout='wide')

app = MultiApp()

# Add all your application here
app.add_app("Home", home.app)
app.add_app("Snail", snail.app)
app.add_app("Scalper", scalper.app)
app.add_app("Market", market.app)

# The main app
app.run()

