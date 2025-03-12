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

            selected_year = st.selectbox(
                "Select Year",
                options=[None] + available_years,
                format_func=lambda x: "All Years" if x is None else str(x),
            )

            selected_conf = st.selectbox(
                "Select Conference",
                options=[None] + available_conferences,
                format_func=lambda x: "All Conferences" if x is None else str(x),
            )

            # Update session state
            if st.session_state.get("selected_year") != selected_year:
                st.session_state.selected_year = selected_year

            if st.session_state.get("selected_conference") != selected_conf:
                st.session_state.selected_conference = selected_conf

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
        if "filter_mode_menu" not in st.session_state:
            st.session_state.filter_mode_menu = "Home"

        with st.sidebar:
            st.title("Conference Navigator")
            filter_mode = option_menu(
                menu_title=None,
                options=["Home", "Conference", "Organization", "Keyword"],
                icons=["house", "calendar-event", "building", "tag"],
                menu_icon="cast",
                default_index=0,
                key="filter_mode_menu",
            )

            if filter_mode == "Home":
                SessionState.clear_selections()
            elif filter_mode == "Conference":
                FilterHandlers.handle_conference_filter()
            elif filter_mode == "Organization":
                FilterHandlers.handle_organization_filter()
            elif filter_mode == "Keyword":
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
                # Conference.render_overview()
                Conference.render_conference_overview("Nvidia GTC 2025")

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
    """Main dashboard page entry point."""
    DashboardUI.render_sidebar()
    DashboardUI.render_main_content()


if __name__ == "__main__":
    dashboard_page()
