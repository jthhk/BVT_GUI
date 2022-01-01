# BVT_GUI

For my personal use but happy for people to reference 

* install Streamlit
* each bots folder you need to manually  

## (0) Copy to same folder as your BVT Bots 



- **UI**  <- where I copy to
- snail
- Scalper
- JimBotreinvest


## (1) bots_app.py 
To add a new page/bot update:

1a. import 
from apps import home,snail,market,scalper,reinvest, **YOURPAGE**

1.b add your new page
app.add_app("**YOURPAGE**", **YOURPAGE**.app)

_You can also remove any bots you don't need from this file_

## (2) new file under apps - copy snail an update def app()

**YOURPAGE**.py

(2a) def app():
    st.title('**YOURFOLDER**')

    # Per Algo
    my_expander = st.expander('**YOURFOLDER**', expanded=True)
    with my_expander:
        clicked = my_widget('**YOURFOLDER**')

    getclosedtrades('**YOURFOLDER**')


(2b) update "/home/pi/bots/" to your directory structure via **BotsHomeDir**

## (3) other things

(3a) may have to change Open position times - got stuck and added +8hr in the end 

df['timestamp'] = df['timestamp'] + **28800000**

(3b) missing fields - reports need a few extra fields passed out of the bot - reports will flag warnings
![MissingFields](https://user-images.githubusercontent.com/31700188/147178420-abb9fb65-26a1-45b7-b9bc-b824a61c3676.PNG)

**Fields:**

unrealised_session_profit_incfees_total, unrealised_session_profit_incfees_perc, session_profit_incfees_perc,session_profit_incfees_total

**update_bot_stats():**

copy whole function into your fork:- 
https://github.com/jthhk/Binance-volatility-trading-bot/blob/main/Binance_Detect_Mooningsv1.py#L1081

**def balance_report(last_price):**

copy the global line into your fork:-
https://github.com/jthhk/Binance-volatility-trading-bot/blob/main/Binance_Detect_Mooningsv1.py#L413


## Notes

* reads from the output files from BVT
* I add the Realised and unrealised to give me the position - otherwise i end up down when i think I'm up
* include fees - again for the above reason
* Pause is only done when the "siginal/Pause" file exists - not when manual
* expect can be slow if large open position due to the 3rd party request for current price 
* runs on a raspberry pi (you need to install the 64bit OS tp get streamlit installed)
* start streamlit you have to reference bots_app.py eg 'streamlit run ../UI/bots_app.py' 
* If you want to add more info - 2 places add global in balance_report and then output in update_bot_stats (ref 3b above) 

## Backlog

* Copy files after exiting bot to a log folder so i can ref/look at later 

## Screens

![Dashboard](https://user-images.githubusercontent.com/31700188/147178401-85af0387-2625-466d-af3f-684f0f5dba74.PNG)
![PerBot](https://user-images.githubusercontent.com/31700188/147178412-c9b735a7-4508-4294-8a55-568f65cd9fbf.PNG)
![Market](https://user-images.githubusercontent.com/31700188/147178435-d762ce9e-3472-4364-8f21-63c3b649e0b1.PNG)
