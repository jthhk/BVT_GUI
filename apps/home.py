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

    profile_summary_file = '/home/pi/bots/' + key \
        + '/test_bot_stats.json'
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
        
def app():
    st.title('DashBoard')

    # Per Algo
    my_expander = st.expander('Snail', expanded=True)
    with my_expander:
        clicked = my_widget('Snail')


    my_expander = st.expander('Scalper', expanded=True)
    with my_expander:
        clicked = my_widget('Scalper')



