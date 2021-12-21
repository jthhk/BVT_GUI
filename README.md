# BVT_GUI

For my personal use but happy of people to reference 

* install Streamlit
* each folder you need to manually add to 

(0) Copy to same folder as your BVT Bots 


- UI
- snail
- Scalper



(1) bots_app.py 



app.add_app("Snail", snail.app)



(2) new file under apps - copy snail an update def app()

def app():
    st.title('YOURFOLDER')

    # Per Algo
    my_expander = st.expander('YOURFOLDER', expanded=True)
    with my_expander:
        clicked = my_widget('YOURFOLDER')

    getclosedtrades('YOURFOLDER')


