import streamlit as st
from streamlit_option_menu import option_menu
from demo_pages import DashBoard, DataSet, DeepDive


def main():
    st.set_page_config(layout="wide")

    # initialize session_state
    if "selected_article_index" not in st.session_state:
        st.session_state["selected_article_index"] = 0
    if "selected_page" not in st.session_state:
        st.session_state["selected_page"] = 0
    if st.session_state.get("rerun_requested", False):
        st.session_state["rerun_requested"] = False
        st.rerun()

    menu_container = st.container()
    with menu_container:
        pages = ["DashBoard", "DataSet", "DeepDive"]
        styles = {
            "container": {"padding": "0.2rem 0", "background-color": "#22222200"},
            # Style for unselected menu items
            "nav-link": {
                "font-family": "monospace",
                "font-size": "16px",
            },
            # Style for the selected menu item
            "nav-link-selected": {
                "font-family": "monospace",
                "font-size": "18px",
            },
        }
        menu_selection = option_menu(
            None,  # menu title (None means no title)
            pages,  # list of menu items
            icons=["house", "search", "graph-up"],  # Bootstrap icons for each menu item
            menu_icon="cast",  # icon for the menu itself
            orientation="horizontal",  # horizontal or vertical menu
            manual_select=st.session_state.selected_page,  # allows manual selection control
            styles=styles,  # custom CSS styles
            key="menu_selection",  # unique key for the component
        )

    if menu_selection == "DashBoard":
        DashBoard.dashboard_page()
    elif menu_selection == "DataSet":
        DataSet.dataset_page()
    elif menu_selection == "DeepDive":
        DeepDive.deepdive_page()


if __name__ == "__main__":
    main()
