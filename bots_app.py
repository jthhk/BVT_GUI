import streamlit as st
from multiapp import MultiApp
#more info:- https://github.com/jthhk/BVT_GUI/blob/main/README.md'
#Adding a new Page needs to be done in 4 places
#(1)below in the import below
#(2)then a new line for your page "app.add_app("YOURPAGE", YOURPAGE.app)"
#(3)copy existing snail.py in apps and rename it to YOURPAGE.py
#(4)Update YOURPAGE.py to reference your bot folder
from apps import home,snail,market,scalper,reinvest,Binance-volatility-trading-bot

st.set_page_config(page_title='JimBot BVT Bots', page_icon='\xe2\x9c\x85', layout='wide')

app = MultiApp()

# Add all your application here
app.add_app("Home", home.app)
#app.add_app("Snail", snail.app)
#app.add_app("Scalper", scalper.app)
#app.add_app("Market", market.app)
#app.add_app("Reinvest", reinvest.app)
app.add_app("Market", Binance-volatility-trading-bot.app)



# The main app
app.run()

