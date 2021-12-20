#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
from types import SimpleNamespace

import datetime
from datetime import datetime

import streamlit as st
import os
import streamlit.components.v1 as components

import pandas as pd
from IPython.display import HTML
import requests

#st.set_page_config(page_title='JimBot BVT Bot', page_icon='\xe2\x9c\x85', layout='wide')

def left(s, amount):
    return s[:amount]

def right(s, amount):
    return s[amount:]

def modification_date(filename):
    t = os.path.getmtime(filename)
    return datetime.fromtimestamp(t).strftime('%Y-%m-%d %H:%M')


def my_widget(key):

    # path to the saved transactions history
    trading_mode = "test"
    Bot_Is_Paused = False

    profile_summary_file = '/home/pi/bots/' + key + '/test_bot_stats.json'  
    (col1, col2) = st.columns([1, 3])

    #If Test does not exist, check for live
    if not os.path.isfile(profile_summary_file):
         profile_summary_file = '/home/pi/bots/' + key + '/live_bot_stats.json'
         trading_mode = "live"

    if os.path.isfile('/home/pi/bots/' + key + '/signals/pausebot.pause'):
         Bot_Is_Paused = True

    if os.path.isfile(profile_summary_file):
        with open(profile_summary_file) as f:
            profile_summary = json.load(f, object_hook=lambda d: \
                    SimpleNamespace(**d))

            last_updated = modification_date(profile_summary_file)
            try:
                win_ratio = round(profile_summary.tradeWins
                              / (profile_summary.tradeWins
                              + profile_summary.tradeLosses) * 100, 2)
            except:
                win_ratio = 0
    
            started = left(profile_summary.botstart_datetime, 16)
            start_date = datetime.fromisoformat(profile_summary.botstart_datetime)
            run_for = str(datetime.now() - start_date).split('.')[0]
            d2 = datetime.now().strftime('%Y-%m-%d %H:%M')
            a = datetime.strptime(last_updated, "%Y-%m-%d %H:%M")
            b = datetime.strptime(d2, "%Y-%m-%d %H:%M")
            last_refresh = str(b - a).split('.')[0]

            if (profile_summary.unrealised_session_profit_incfees_perc+profile_summary.session_profit_incfees_perc) < 0.0:
                col1.metric('Lose',
                            str(round((profile_summary.unrealised_session_profit_incfees_total+profile_summary.session_profit_incfees_total),4)),
                            str(round((profile_summary.unrealised_session_profit_incfees_perc+profile_summary.session_profit_incfees_perc),4)))
                col2.error('Win: ' + str(profile_summary.tradeWins)
                           + ' | Loss: '
                           + str(profile_summary.tradeLosses)
                           + ' | WL: ' + str(win_ratio) + '%')
            elif profile_summary.historicProfitIncFees_Percent > 0.0:
                col1.metric('Profit',
                            str(round((profile_summary.unrealised_session_profit_incfees_total+profile_summary.session_profit_incfees_total),4)),
                            str(round((profile_summary.unrealised_session_profit_incfees_perc+profile_summary.session_profit_incfees_perc),4)))
                col2.success('Win: ' + str(profile_summary.tradeWins)
                           + ' | Loss: '
                           + str(profile_summary.tradeLosses)
                           + ' | WL: ' + str(win_ratio) + '%')
            else:
                col1.metric('Flat',
                            str(round(0,2)),
                            str(round(0,1)))
                col2.success('Win: ' + str(0)
                             + ' | Loss: '
                             + str(0)
                             + ' | WL: ' + str(win_ratio) + '%')

            if int(last_refresh[2:4]) < 15 and int(last_refresh[0:1]) == 0:
                col2.write('Refreshed: ' + str(last_refresh) + ' | Last: ' + str(last_updated)
                       + ' |  Started:' + str(started) + ' | Running:'
                       + str(run_for) + " | mode:" + str(trading_mode) + " | Paused:"  + str(Bot_Is_Paused))
            else:
                col2.warning('Refreshed: ' + str(last_refresh) + ' | Last: ' + str(last_updated)
                       + ' |  Started:' + str(started) + ' | Running:'
                       + str(run_for) + " | mode:" + str(trading_mode) + " | Paused:"  + str(Bot_Is_Paused))

    else:

        col1.metric('N/A', '0', '0%')
        col2.info('Not started/no file')

# Function to convert file path into clickable form.
def make_clickable(link):
    # target _blank to open new window
    # extract clickable text to display for your link
    text = link
    return f'<a target="_blank" href="https://www.tradingview.com/symbols/{text}">{text}</a>'

# Function to convert file path into clickable form.
def get_px(link):
    # target _blank to open new window
    # extract clickable text to display for your link
    coin = left(link,len(link)-4)
    try:
        response = requests.get(f"https://api.binance.com/api/v3/ticker/price?symbol={coin}USDT")
        pxdata = response.json()
        price = pxdata["price"] 
    except ValueError:
        price = 0.0

    return price
    

def getclosedtrades(key):

      #If Test does not exist, check for live
    open_order_file = '/home/pi/bots/' + key + '/test_coins_bought.json'  
    if not os.path.isfile(open_order_file):
         closed_trades_file  = '/home/pi/bots/' + key + '/live_coins_bought.json'

    if os.path.isfile(open_order_file):
        #data = pd.read_json(open_order_file,orient='columns') #path folder of the data file
        #with open(open_order_file, 'r') as f:
        #   data = pd.read_json(f)
        data = json.load(open(open_order_file, "r"))
        df = pd.DataFrame.from_dict(data, orient="index")
        df['timestamp']= pd.to_datetime(df['timestamp'],unit='s')
        df['bought_at'] = df['bought_at'].astype(float)
        df['CurrentPx'] = df['symbol'] 
        df['CurrentPx'] = df['CurrentPx'].apply(get_px)
        df['CurrentPx'] = df['CurrentPx'].astype(float)
        #df['EstProfit'] = 
        #df['EstProfit'] = df.apply(lambda x: (t(df['CurrentPx'])) - float((df['bought_at'])))
        df['PriceDiff'] =  df['CurrentPx'] - df['bought_at']
        df = df.sort_values(by='timestamp', ascending=False)
        df = df[['timestamp', 'symbol', 'bought_at', 'CurrentPx', 'PriceDiff', 'stop_loss', 'take_profit']]
        st.header('Open Positions')
        #df['symbol'] = df['symbol'].apply(make_clickable)
        #df = df.to_html(escape=False)
        #st.write(df, unsafe_allow_html=True)
        st.dataframe(df.style.applymap(color_negative_red, subset=['PriceDiff']))

    #If Test does not exist, check for live
    closed_trades_file = '/home/pi/bots/' + key + '/test_trades.txt'  
    if not os.path.isfile(closed_trades_file):
         closed_trades_file  = '/home/pi/bots/' + key + '/live_trades.txt'

    if os.path.isfile(closed_trades_file):
        data = pd.read_csv(closed_trades_file, sep='\t') #path folder of the data file
        df = pd.DataFrame(data)
        df = df.sort_values(by='Datetime', ascending=False)
        df = df[['Datetime', 'Coin', 'Type', 'Buy Price', 'Sell Price', 'Profit $', 'Sell Reason']]
        st.header('Closed Positions')
        filtered = df[(df['Type'] == "Sell")]
        filtered.style.applymap(color_negative_red, subset=['Profit $'])
        st.dataframe(filtered.style.applymap(color_negative_red, subset=['Profit $']))
        #filtered = filtered.to_html(escape=False)
        #st.dataframe(filtered)
        
        

def bg_colour_col(col):
    colour = 'red'
    return [('background-color: %s' % colour if col.name == 'Profit $' or i == 4 else '') for (i, x) in col.iteritems()]  

def color_negative_red(value):
  """
  Colors elements in a dateframe
  green if positive and red if
  negative. Does not color NaN
  values.
  """
  color='black'
  if value=='<NA>':
    value=0
  else:
    value=float(value)

  if value< 0:
    color = 'red'
  elif value > 0:
    color = 'green'
  
  return 'color: %s' % color


def app():
    st.title('Snail')

    # Per Algo
    my_expander = st.expander('Snail', expanded=True)
    with my_expander:
        clicked = my_widget('Snail')

    getclosedtrades('Snail')
 