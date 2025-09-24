import streamlit as st
from streamlit_option_menu import option_menu

# Set the page configuration
st.set_page_config(page_title="Josaa Data Analysis", layout="wide")

# Create a horizontal navigation menu
selected = option_menu(
    menu_title=None,
    options=["Dashboard", "Developers"],
    icons=["house", "person"],
    menu_icon="cast",
    default_index=0,
    orientation="horizontal"
)

st.session_state.page = selected

if selected == "Dashboard":
    from dashboard import load_dashboard
    load_dashboard()
elif selected == "Developers":
    from Developers import load_developers
    load_developers()

# Hide Streamlit style elements
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility:hidden;}
            </style>
           """
st.markdown(hide_st_style, unsafe_allow_html=True)
