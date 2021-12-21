# BVT_GUI

For my personal use but happy for people to reference 

* install Streamlit
* each folder you need to manually add to 

(0) Copy to same folder as your BVT Bots 


- UI
- snail
- Scalper



(1) bots_app.py 



app.add_app("YOURFOLDER", snail.app)



(2) new file under apps - copy snail an update def app()

(2a) def app():
    st.title('YOURFOLDER')

    # Per Algo
    my_expander = st.expander('YOURFOLDER', expanded=True)
    with my_expander:
        clicked = my_widget('YOURFOLDER')

    getclosedtrades('YOURFOLDER')


(2b) update "/home/pi/bots/" to your directory structure 


(3) other things

may have to change Open position times - got stuck and added +8hr in the end 

df['timestamp'] = df['timestamp'] + 28800000


