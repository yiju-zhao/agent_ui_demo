import os

script_dir = os.path.dirname(os.path.abspath(__file__))
wiki_root_dir = os.path.dirname(os.path.dirname(script_dir))

import streamlit as st
from streamlit_option_menu import option_menu


def deepdive_page():
    st.title("DeepDive")
