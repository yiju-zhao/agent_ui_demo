import streamlit as st
from streamlit_option_menu import option_menu
from utility.db_util import DataManagerContext
from utility.visualization_utli import FilterDisplay

from .dashboard import Home, Conference, Organization, Keyword


class StateCallbacks:
    """Manages state-related callback functions for different filters."""

    @staticmethod
    def on_conf_click(conf: str) -> None:
        """Handle conference selection/deselection."""
        st.session_state.selected_conference = (
            None if st.session_state.get("selected_conference") == conf else conf
        )
        st.rerun()

    @staticmethod
    def on_org_click(org: str) -> None:
        """Handle organization selection/deselection."""
        st.session_state.selected_organization = (
            None if st.session_state.get("selected_organization") == org else org
        )
        st.rerun()


class SessionState:
    """Manages dashboard state and selections."""

    @staticmethod
    def clear_selections(exclusive_keys: list[str] = None):
        keys_to_clear = [
            "selected_year",
            "selected_conference",
            "selected_organization",
            "selected_keyword",
        ]
        if exclusive_keys is None:
            exclusive_keys = []
        for key in keys_to_clear:
            if key not in exclusive_keys and key in st.session_state:
                del st.session_state[key]

    @staticmethod
    def get_current_selections():
        return {
            "year": st.session_state.get("selected_year"),
            "conference": st.session_state.get("selected_conference"),
            "organization": st.session_state.get("selected_organization"),
            "keyword": st.session_state.get("selected_keyword"),
        }


class FilterHandlers:

    @staticmethod
    def handle_conference_filter():
        with DataManagerContext() as managers:
            # Get available years and conferences
            available_years = managers["conference"].get_all_years()
            available_conferences = managers["conference"].get_all_conferences()

            current_year = st.session_state.get("selected_year")
            current_conf = st.session_state.get("selected_conference")

            # Calculate the correct index for year selectbox
            year_index = 0  # default to first option (None)
            if current_year in available_years:
                year_index = available_years.index(current_year) + 1  # +1 because None is first

            selected_year = st.selectbox(
                "Select Year",
                options=[None] + available_years,
                format_func=lambda x: "All Years" if x is None else str(x),
                index=year_index,
                key="year_selectbox"  # Add a unique key
            )

            # Calculate the correct index for conference selectbox
            conf_index = 0  # default to first option (None)
            if current_conf in available_conferences:
                conf_index = available_conferences.index(current_conf) + 1  # +1 because None is first

            selected_conf = st.selectbox(
                "Select Conference",
                options=[None] + available_conferences,
                format_func=lambda x: "All Conferences" if x is None else str(x),
                index=conf_index,
                key="conf_selectbox"  # Add a unique key
            )

            # Update session state and force rerun if changed
            if selected_year != current_year:
                st.session_state.selected_year = selected_year
                st.rerun()  # Force rerun on change

            if selected_conf != current_conf:
                st.session_state.selected_conference = selected_conf
                st.rerun()  # Force rerun on change

    @staticmethod
    def handle_organization_filter():
        SessionState.clear_selections(["selected_organization"])
        with DataManagerContext() as managers:
            orgs = managers["org"].get_tracked_organizations()
            if orgs:
                FilterDisplay.show_item_filter(
                    orgs,
                    "all_years",
                    StateCallbacks.on_org_click,
                    st.session_state,
                    "selected_organization",
                )

    @staticmethod
    def handle_keyword_filter():
        SessionState.clear_selections(["selected_keyword"])
        with DataManagerContext() as managers:
            keywords = managers["keyword"].get_all_keywords()
            search_keyword = FilterDisplay.show_keyword_search(keywords)

            if search_keyword:
                filtered_keywords = [
                    k for k in keywords if search_keyword.lower() in k.lower()
                ]
                for kw in filtered_keywords:
                    if st.button(kw, key=f"button_{kw.replace(' ', '_')}_kw"):
                        st.session_state.selected_keyword = kw


class DashboardUI:
    """Main dashboard UI handler."""

    @staticmethod
    def render_sidebar():
        # Check if we need to switch to conference view
        if "nav_target" in st.session_state:
            # Force a reset of the option_menu widget by using a different key
            if "option_menu_key" in st.session_state:
                st.session_state.option_menu_key += 1
            else:
                st.session_state.option_menu_key = 1
                
            st.session_state.filter_mode_menu = st.session_state.nav_target
            del st.session_state.nav_target  # Clean up after use

        if "filter_mode_menu" not in st.session_state:
            st.session_state.filter_mode_menu = "Home"
            
        if "option_menu_key" not in st.session_state:
            st.session_state.option_menu_key = 0

        with st.sidebar:
            st.title("Conference Navigator")
            # Store the current mode before creating the widget
            current_mode = st.session_state.filter_mode_menu
            
            selected_mode = option_menu(
                menu_title=None,
                options=["Home", "Conference", "Organization", "Keyword"],
                icons=["house", "calendar-event", "building", "tag"],
                menu_icon="cast",
                default_index=["Home", "Conference", "Organization", "Keyword"].index(current_mode),
                key=f"filter_mode_menu_{st.session_state.option_menu_key}"
            )
            
            # If the selected mode changed, update the session state
            if selected_mode != current_mode:
                st.session_state.filter_mode_menu = selected_mode
                # Clear selections when switching to home
                if selected_mode == "Home":
                    SessionState.clear_selections()
                st.rerun()

            if selected_mode == "Home":
                SessionState.clear_selections()
            elif selected_mode == "Conference":
                FilterHandlers.handle_conference_filter()
            elif selected_mode == "Organization":
                FilterHandlers.handle_organization_filter()
            elif selected_mode == "Keyword":
                FilterHandlers.handle_keyword_filter()

    @staticmethod
    def render_main_content():
        """Render main content based on current selections."""
        selections = SessionState.get_current_selections()
        filter_mode = st.session_state.get("filter_mode_menu")

        if filter_mode == "Home":
            Home.render_home()
        elif filter_mode == "Conference":
            year = selections["year"]
            conf = selections["conference"]

            if not year and not conf:
                Conference.render_overview()
            elif year and conf:
                Conference.render_instance(year, conf)
            elif year:
                Conference.render_year_overview(year)
            else:
                Conference.render_conference_overview(conf)
        elif filter_mode == "Organization":
            if selections["organization"]:
                Organization.render(selections["organization"])
            else:
                Organization.render_overview()
        elif filter_mode == "Keyword":
            if selections["keyword"]:
                Keyword.render(selections["keyword"])
            else:
                Keyword.render_overview()


def dashboard_page():
    # 添加CSS来减少页面顶部的空白
    st.markdown(
        """
        <style>
        .block-container {
            padding-top: 1rem;
            padding-bottom: 0rem;
        }
        header {
            visibility: hidden;
        }
        #MainMenu {
            visibility: hidden;
        }
        footer {
            visibility: hidden;
        }
        </style>
    """,
        unsafe_allow_html=True,
    )
    """Main dashboard page entry point."""
    DashboardUI.render_sidebar()
    DashboardUI.render_main_content()


if __name__ == "__main__":
    dashboard_page()
