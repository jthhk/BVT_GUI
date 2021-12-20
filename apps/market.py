#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
from types import SimpleNamespace

import datetime
from datetime import datetime

import streamlit as st
import os
import streamlit.components.v1 as components

#st.set_page_config(page_title='JimBot BVT Bot', page_icon='\xe2\x9c\x85', layout='wide')

def ShowPrices():
    #<img src="https://alternative.me/crypto/fear-and-greed-index.png" alt="Latest Crypto Fear & Greed Index"/> 
    components.html(
    """
    <!-- TradingView Widget BEGIN -->
    <div class="tradingview-widget-container">
      <div class="tradingview-widget-container__widget"></div>
      <div class="tradingview-widget-copyright"><a href="https://www.tradingview.com/markets/cryptocurrencies/prices-all/" rel="noopener" target="_blank"><span class="blue-text">Cryptocurrency Markets</span></a> by TradingView</div>
      <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-screener.js" async>
      {
      "width": "100%",
      "height": "400",
      "defaultColumn": "moving_averages",
      "screener_type": "crypto_mkt",
      "displayCurrency": "USD",
      "colorTheme": "light",
      "locale": "en",
      "isTransparent": false
    }
      </script>
    </div>
    <!-- TradingView Widget END -->
    """,
    height=400,)

def ShowGorF():
    components.html(
    """
    <img src="https://alternative.me/crypto/fear-and-greed-index.png" width="80%" alt="Latest Crypto Fear & Greed Index"/>
    """,
    height=1000,)

def left(s, amount):
    return s[:amount]

def right(s, amount):
    return s[amount:]

def modification_date(filename):
    t = os.path.getmtime(filename)
    return datetime.fromtimestamp(t).strftime('%Y-%m-%d %H:%M')



        
def app():
    st.title('Prices')

    my_expander = st.expander("Prices", expanded=True)
    with my_expander:
        clicked = ShowPrices()

    my_expander = st.expander("Index", expanded=True)
    with my_expander:
        clicked = ShowGorF()


