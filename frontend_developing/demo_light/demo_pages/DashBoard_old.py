import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu
from utility.visualization_utli import *
from utility.db_util import (
    DataManagerContext,
    conference_stat_df,
    aggregate_stat_df,
    orgnization_stat_df,
)


class SessionState:
    """Manages dashboard state and selections."""

    @staticmethod
    def clear_selections(exclusive_keys: list[str] = None):
        """Clear all filter selections from session state except for those specified in exclusive_keys."""
        # Define the keys that are candidates for removal.
        keys_to_clear = [
            "selected_year",
            "selected_conference",
            "selected_organization",
            "selected_keyword",
        ]
        # If no exclusive keys are provided, default to an empty list.
        if exclusive_keys is None:
            exclusive_keys = []
        # Loop through each candidate key and delete it unless it's in the exclusive list.
        for key in keys_to_clear:
            if key not in exclusive_keys and key in st.session_state:
                del st.session_state[key]

    @staticmethod
    def get_current_selections():
        """Get current filter selections."""
        return {
            "year": st.session_state.get("selected_year"),
            "conference": st.session_state.get("selected_conference"),
            "organization": st.session_state.get("selected_organization"),
            "keyword": st.session_state.get("selected_keyword"),
        }


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


class FilterHandlers:
    """Handles different filter types and their logic."""

    @staticmethod
    def handle_year_filter():
        with DataManagerContext() as managers:
            # Get all available years from the database
            available_years = managers["conference"].get_all_years()
            selected_year = FilterDisplay.show_year_filter(available_years)
            # Update year selection if changed
            if st.session_state.get("selected_year") != selected_year:
                st.session_state.selected_year = selected_year
                st.session_state.selected_conference = None
            # Show conferences for selected year
            if selected_year:
                st.subheader(f"Conferences in {selected_year}")
                conferences = managers["conference"].get_conferences_by_year(selected_year)
                FilterDisplay.show_item_filter(
                    conferences,
                    f"year_{selected_year}",
                    StateCallbacks.on_conf_click,
                    st.session_state,
                    "selected_conference",
                )

    @staticmethod
    def handle_conference_filter():
        SessionState.clear_selections(["selected_conference"])
        with DataManagerContext() as managers:
            conferences = managers["conference"].get_all_conferences()
            FilterDisplay.show_item_filter(
                conferences,
                "all years",
                StateCallbacks.on_conf_click,
                st.session_state,
                "selected_conference",
            )

    @staticmethod
    def handle_organization_filter():
        SessionState.clear_selections(["selected_orgnization"])
        with DataManagerContext() as managers:
            # Get all organizations from database that are in our tracked list
            orgs = managers["org"].get_tracked_organizations()

            if orgs:
                FilterDisplay.show_item_filter(
                    orgs,
                    "all_years",
                    StateCallbacks.on_org_click,
                    st.session_state,
                    "selected_orgnization",
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


class ContentRenderers:
    """Handles rendering of different types of content."""

    @staticmethod
    def render_home_content():
        # Create two-column layout
        middle_col, right_col = st.columns([6, 4], gap="medium")
        
        # Middle column with scrollable content
        with middle_col.container(height=800):
            report_col, podcast_col = st.columns(2)
            
            with report_col:
                st.subheader("Top Reports")
                for i in range(10):
                    st.markdown(
                        """
                        <div style='border:1px solid #ddd; border-radius:5px; padding:10px; margin:5px;'>
                            <h4>Report Title {}</h4>
                            <p>Brief description of the report content and key findings...</p>
                        </div>
                        """.format(i+1),
                        unsafe_allow_html=True
                    )
            
            with podcast_col:
                st.subheader("Top Podcasts")
                for i in range(10):
                    st.markdown(
                        """
                        <div style='border:1px solid #ddd; border-radius:5px; padding:10px; margin:5px;'>
                            <h4>Podcast Title {}</h4>
                            <p>Brief description of the podcast episode and topics covered...</p>
                        </div>
                        """.format(i+1),
                        unsafe_allow_html=True
                    )
        
        # Right column with fixed content
        with right_col.container(height=800):
            # Happening Now Section
            st.subheader("Happening Now")
            left, middle, right = st.columns([1, 1, 1], gap="small")
            with left:
                st.button("ICSE 2024", key="conf_1")
            with middle:
                st.button("FSE 2024", key="conf_2")
            with right:
                st.button("ISSTA 2024", key="conf_3")
            # Top CS Schools Chart
            st.subheader("Top 10 CS Schools")
            fig_schools = ChartDisplay.create_cs_schools_chart()
            st.plotly_chart(fig_schools, use_container_width=True)
            
            # Top Companies Chart
            st.subheader("Top 5 Tech Companies")
            fig_companies = ChartDisplay.create_tech_companies_chart()
            st.plotly_chart(fig_companies, use_container_width=True)
        

    @staticmethod
    def render_aggregate(conference: str):
        """Render aggregate data for conferences through all years."""
        with DataManagerContext() as managers:
            stats = managers["conference"].get_conference_stats(conference, "All Years")
            df = aggregate_stat_df(stats, include_keywords=True)
            DashboardLayout.show_aggregate_layout(df, conference)

    @staticmethod
    def render_conference(year: int, conference: str = None):
        """Render conference-specific data."""
        with DataManagerContext() as managers:
            if not conference:
                stats = managers["conference"].get_yearly_conference_stats(year)
                df = conference_stat_df(stats, include_keywords=False)
                DashboardLayout.show_conference_layout(df, f"All Conferences in {year}")
            else:
                stats = managers["conference"].get_conference_stats(conference, year)
                df = conference_stat_df(stats, include_keywords=False)
                DashboardLayout.show_conference_layout(df, f"{conference} - {year}")

    @staticmethod
    def render_organization(organization: str):
        """Render organization-specific data."""
        with DataManagerContext() as managers:
            stats = managers["org"].get_organization_stats(organization)
            df = orgnization_stat_df(stats)
            DashboardLayout.show_orgnization_layout(df, f"Research by {organization}")


    @staticmethod
    def render_keyword(keyword: str):
        """Render keyword-specific data."""
        with DataManagerContext() as managers:
            papers = managers["paper"].get_papers_by_keyword(keyword)
            related_keywords = managers["keyword"].get_related_keywords(keyword)
            if not papers:
                st.info(f"No papers found for keyword: {keyword}")
                return
            DashboardLayout.show_keyword_layout(papers, keyword, related_keywords)


class DashboardUI:
    """Main dashboard UI handler."""

    @staticmethod
    def render_sidebar():
        """Render sidebar with filters."""
        with st.sidebar:
            st.title("Conference Navigator")
            filter_mode = option_menu(
                menu_title=None,  # Explicitly set no title for the menu
                options=["Home", "Year", "Conference", "Organization", "Keyword"],
                icons=[
                    "house",  # Added home icon
                    "calendar",
                    "journal-text",
                    "building",
                    "tag",
                ],  # Optional icons
                menu_icon="cast",
                default_index=0,  # Set Home as default
                styles={
                    "container": {
                        "padding": "0.2rem 0",
                        "background-color": "#22222200",
                    },
                    # Style for unselected menu items
                    "nav-link": {
                        "font-family": "monospace",
                        "font-size": "15px",
                    },
                    # Style for the selected menu item
                    "nav-link-selected": {
                        "font-family": "monospace",
                        "font-size": "16px",
                    },
                },
                key="filter_mode_menu",
            )

            if filter_mode == "Home":
                SessionState.clear_selections()  # Clear all filters when home is selected
            elif filter_mode == "Year":
                FilterHandlers.handle_year_filter()
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
        if not any(selections.values()):
            # Show home page when no filters are selected
            ContentRenderers.render_home_content()
        elif selections["year"]:
            if not selections["conference"]:
                ContentRenderers.render_conference(selections["year"])
            else:
                ContentRenderers.render_conference(
                    selections["year"], selections["conference"]
                )
        elif selections["conference"]:
            ContentRenderers.render_aggregate(selections["conference"])
        elif selections["organization"]:
            ContentRenderers.render_organization(selections["organization"])
        elif selections["keyword"]:
            ContentRenderers.render_keyword(selections["keyword"])


def dashboard_page():
    """Main dashboard page entry point."""
    # SessionState.clear_all_selections()
    DashboardUI.render_sidebar()
    DashboardUI.render_main_content()


if __name__ == "__main__":
    dashboard_page()
