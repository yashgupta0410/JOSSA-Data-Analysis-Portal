import streamlit as st

def load_developers():

    st.title("Meet the Developers")
    st.markdown("---")

    # FIX 1: Create 4 columns and assign to 4 variables
    col1, col2 = st.columns(4)

    with col1:
        # BEST PRACTICE: Use the assets folder and st.image's caption
        st.image("assets/sanskar.jpg", caption="Sanskar")

    with col2:
        # FIX 2: Use a different image file for each person
        st.image("assets/vanshita.jpg", caption="Vanshita")
        
