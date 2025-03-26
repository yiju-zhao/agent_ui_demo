import streamlit as st
from datetime import datetime
from streamlit import cache_data

class SessionFilterHandler:
    """Handles filtering and processing of session data."""
    
    @staticmethod
    @cache_data(ttl=3600)  # Cache for 1 hour
    def apply_filters(sessions, track, time, venue, company, has_expert_opinion=False):
        """
        Filter sessions based on selected criteria.
        
        Args:
            sessions (list): List of session dictionaries
            track (str): Selected track/topic filter
            time (str): Selected time filter
            venue (str): Selected venue filter
            company (str): Selected company filter
            has_expert_opinion (bool): Filter for sessions with expert opinions
            
        Returns:
            list: Filtered list of sessions
        """
        filtered_sessions = sessions

        if track != "All Topics":
            filtered_sessions = [
                session for session in filtered_sessions
                if session["track"] == track
            ]

        if time != "All Hours":
            filtered_sessions = [
                session for session in filtered_sessions
                if session["time"].startswith(time)
            ]
            
        if venue != "All Venues":
            filtered_sessions = [
                session for session in filtered_sessions
                if session["venue"] == venue
            ]
            
        if company != "All Companies":
            filtered_sessions = [
                session for session in filtered_sessions
                if company in session["speaker_companies"]
            ]
            
        if has_expert_opinion:
            filtered_sessions = [
                session for session in filtered_sessions
                if session.get("expert_opinion") and 
                   isinstance(session["expert_opinion"], str) and 
                   session["expert_opinion"].strip() and 
                   session["expert_opinion"].lower() != "nan"
            ]
            
        return filtered_sessions
    
    @staticmethod
    def prepare_filter_options(session_data):
        """
        Prepare filter options from session data.
        
        Args:
            session_data (list): List of day data dictionaries
            
        Returns:
            list: List of filter option dictionaries for each day
        """
        filter_options = []
        for day_data in session_data:
            filter_options.append({
                "topics": sorted(list(set(s["track"] for s in day_data["sessions"]))),
                "times": sorted(list(set(
                    s["time"].split(" - ")[0] for s in day_data["sessions"]
                )), key=lambda x: datetime.strptime(x, "%I:%M %p")),
                "venues": sorted(list(set(s["venue"] for s in day_data["sessions"]))),
                "companies": sorted(list(set(
                    company for s in day_data["sessions"]
                    for company in s["speaker_companies"]
                )))
            })
        return filter_options
    
    @staticmethod
    def render_filter_ui(filter_options, tab_idx):
        """
        Render filter UI components.
        
        Args:
            filter_options (dict): Dictionary of filter options
            tab_idx (int): Current tab index
            
        Returns:
            tuple: Selected filter values (track, time, venue, company, has_expert_opinion)
        """
        with st.expander("Filter Sessions", expanded=False):
            filter_cols = st.columns(4)
            
            with filter_cols[0]:
                selected_track = st.selectbox(
                    "Topic:",
                    options=["All Topics"] + filter_options["topics"],
                    key=f"topic_filter_{tab_idx}"
                )
            
            with filter_cols[1]:
                selected_time = st.selectbox(
                    "Start time:",
                    options=["All Hours"] + filter_options["times"],
                    key=f"time_filter_{tab_idx}"
                )
            
            with filter_cols[2]:
                selected_venue = st.selectbox(
                    "Venue:",
                    options=["All Venues"] + filter_options["venues"],
                    key=f"venue_filter_{tab_idx}"
                )
            
            with filter_cols[3]:
                selected_company = st.selectbox(
                    "Company:",
                    options=["All Companies"] + filter_options["companies"],
                    key=f"company_filter_{tab_idx}"
                )
            
            # Add checkbox for expert opinion filter
            has_expert_opinion = st.checkbox(
                "Show only sessions with expert opinions",
                key=f"expert_opinion_filter_{tab_idx}"
            )
                
        return selected_track, selected_time, selected_venue, selected_company, has_expert_opinion
