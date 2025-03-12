import os

import streamlit as st
from streamlit_option_menu import option_menu

from demo_pages import DataSet, DeepDive, DashBoard
from demo_pages.dashboard.conference import Conference  # Import Conference


def load_css():
    # Get the directory where the current script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Create relative path to style.css from the script location
    css_path = os.path.join(script_dir, "style.css")

    with open(css_path) as css:
        st.markdown(f"<style>{css.read()}</style>", unsafe_allow_html=True)

def main():
    st.set_page_config(layout="wide")
    load_css()
    st.title("DeepSight UI Demo")

    # initialize session_state
    if "selected_article_index" not in st.session_state:
        st.session_state["selected_article_index"] = 0
    if "selected_page" not in st.session_state:
        st.session_state["selected_page"] = 0
    if "previous_menu_selection" not in st.session_state:
        st.session_state["previous_menu_selection"] = None
    if "page_change_requested" not in st.session_state:
        st.session_state["page_change_requested"] = False
    # Add session state variables for conference navigation
    if "view_conference" not in st.session_state:
        st.session_state.view_conference = False
    if "selected_conference" not in st.session_state:
        st.session_state.selected_conference = None

    # If we're viewing a conference, show it and skip the main navigation
    if st.session_state.view_conference and st.session_state.selected_conference:
        # edit for session state
        Conference.render_conference_overview(st.session_state.selected_conference)
        # Add a back button
        if st.button("← Back to Dashboard"):
            st.session_state.view_conference = False
            st.rerun()
        return

    menu_container = st.container()
    with menu_container:
        pages = ["DashBoard", "DataSet", "DeepDive"]
        # Only update manual_select if no page change was requested
        current_page = (
            st.session_state.selected_page
            if st.session_state.page_change_requested
            else None
        )
        menu_selection = option_menu(
            None,
            pages,
            icons=["speedometer2", "search", "graph-up"],
            menu_icon="cast",
            orientation="horizontal",
            manual_select=current_page,
            key="menu_selection",
        )

    # Handle page changes from menu
    if not st.session_state.page_change_requested:
        if menu_selection != st.session_state.previous_menu_selection:
            st.session_state.previous_menu_selection = menu_selection
            st.session_state.selected_page = pages.index(menu_selection)
            if menu_selection == "DataSet":
                # Reset Dataset-specific states
                st.session_state.has_searched = False
                st.session_state.cart = []
                st.session_state.selected_row = None
    else:
        # Reset the page change request flag
        st.session_state.page_change_requested = False

    if menu_selection == "DashBoard":
        DashBoard.dashboard_page()
    elif menu_selection == "DataSet":
        DataSet.dataset_page()
    elif menu_selection == "DeepDive":
        DeepDive.deepdive_page()


if __name__ == "__main__":
    main()