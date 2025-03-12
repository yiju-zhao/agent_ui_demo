import os

import streamlit as st
import pandas as pd
import json
from datetime import datetime


class Conference:
    """Handles rendering of conference-related content."""

    # Function to sanitize description to prevent HTML rendering issues
    @staticmethod
    def sanitize_description(text):
        """Basic sanitization to escape HTML tags but preserve basic formatting"""
        if not text:
            return ""

        # Replace < and > with their HTML entities to prevent rendering as HTML
        text = text.replace("<", "<").replace(">", ">")

        # Add line breaks for readability
        text = text.replace("\n", "<br>")

        return text

    def _transform_json_to_gtc_format(json_data):
        transformed_data = []

        for session_day in json_data:
            # Transform date format from "2025-03-16" to "March 16, 2025"
            date_obj = datetime.strptime(session_day["date"], "%Y-%m-%d")
            formatted_date = date_obj.strftime("%B %d, %Y")

            transformed_sessions = []
            for session in session_day["sessions"]:
                # Skip sessions with missing required fields if needed
                if not session.get("badges") or not session.get("topic"):
                    continue

                # Basic fields needed for display
                transformed_session = {
                    "time": session.get("time", ""),
                    "title": session.get("title", ""),
                    "speaker": session.get("speakers", ""),
                    "location": session.get("badges", ""),
                    "track": session.get("topic", "").split(" - ")[0] if " - " in session.get("topic",
                                                                                              "") else session.get(
                        "topic", ""),
                    "description": session.get("description", ""),

                    # Additional fields for enhanced display
                    "session_code": session.get("session code", ""),
                    "technical_level": session.get("technical level", ""),
                    "full_topic": session.get("topic", ""),
                    "points": session.get("points", ""),
                    "start_time": session.get("start_time", ""),
                    "end_time": session.get("end_time", ""),
                    "expert_input": session.get("expert input", "")
                }
                transformed_sessions.append(transformed_session)

            transformed_day = {
                "date": formatted_date,
                "day": session_day["day"],
                "sessions": transformed_sessions
            }
            transformed_data.append(transformed_day)

        return transformed_data

    @staticmethod
    def load_conference_data():
        try:
            # Get the directory of the current file (conference.py)
            current_dir = os.path.dirname(os.path.abspath(__file__))
            # Construct the full path to the JSON file
            json_file_path = os.path.join(current_dir,  "conference_sessions.json")

            with open(json_file_path, "r", encoding="utf-8") as f:
                json_data = json.load(f)

            transformed_data = Conference._transform_json_to_gtc_format(json_data)

            # Print debug info to verify data is loaded and path
            print(f"Successfully loaded {len(transformed_data)} days of conference data from {json_file_path}")

            if not transformed_data:
                raise ValueError("Transformed data is empty")

            return transformed_data

        except Exception as e:
            print(f"Error loading conference_sessions.json: {e}")

            # Return fallback data similar to the original structure
            return [
                {
                    "date": "March 16, 2025",
                    "day": "Sunday",
                    "sessions": [
                        {
                            "time": "9:00 AM - 5:00 PM",
                            "title": "Building AI Agents With Multimodal Models",
                            "speaker": "Mark Moyou (Sr. Data Scientist, NVIDIA)",
                            "location": "In-Person; Full-Day Workshop",
                            "track": "Generative AI",
                            "description": "Just like how humans have multiple senses to perceive the world around them, more and more computer sensors are being developed to capture a wide variety of data. In the health industry, computed tomography (CT) scans..."
                        },
                        {
                            "time": "9:00 AM - 5:00 PM",
                            "title": "Build LLM Applications With Prompt Engineering",
                            "speaker": "Mohammad Raza (Solutions Architect, NVIDIA)",
                            "location": "In-Person; Full-Day Workshop",
                            "track": "AI Infrastructure",
                            "description": "With the incredible capabilities of large language models (LLMs), enterprises are eager to integrate them into their products and internal applications for a wide variety of use cases. These include text generation,..."
                        }
                    ]
                },
                {
                    "date": "March 17, 2025",
                    "day": "Monday",
                    "sessions": [
                        {
                            "time": "12:00 AM - 12:40 AM",
                            "title": "Application of Large Language Models in Smart Cockpits",
                            "speaker": "Jie Gao (Sr. Director, Digital Cockpit Department; NIO Head of AI Development for Digital Cockpit, NIO)",
                            "location": "Virtual; Talks & Panels",
                            "track": "Robotics & Autonomous Systems",
                            "description": "This session discusses NVIDIA technologies and their applications in advanced computing, AI, and GPU acceleration."
                        }
                    ]
                }
            ]

    # Load conference data
    gtc_sessions = None  # Initialize gtc_sessions as None initially

    @staticmethod
    def render_overview():
        """Render overview of all conferences across years."""
        # Keeping the basic conference information but removing graphs

        # Fake data for conference overview
        fake_data = {
            "summary_stats": {
                "total_conferences": 25,
                "total_papers": 45000,
                "total_years": 10,
                "avg_papers_per_year": 4500,
            },
            "top_conferences": [
                {
                    "name": "ICSE",
                    "full_name": "International Conference on Software Engineering",
                    "intro": "The premier software engineering conference, covering a wide range of topics from software development to maintenance and evolution.",
                    "total_papers": 5000,
                    "avg_citations": 25.5,
                },
                {
                    "name": "FSE",
                    "full_name": "Foundations of Software Engineering",
                    "intro": "A leading conference focusing on theoretical and practical aspects of software development, emphasizing innovative solutions to software engineering challenges.",
                    "total_papers": 4200,
                    "avg_citations": 23.8,
                },
                {
                    "name": "Nvidia GTC 2025",
                    "full_name": "GPU Technology Conference",
                    "intro": "NVIDIA's premier conference for developers, researchers, and technologists exploring AI, graphics, HPC, and more.",
                    "total_sessions": 120,
                    "dates": "March 17-21, 2025",
                },
            ],
        }

        st.header("Conference Overview")

        # Summary Statistics
        metric_style = """
        <style>
        [data-testid="stMetricValue"] {
            font-size: 1.5rem;
        }
        [data-testid="stMetricLabel"] {
            font-size: 1.0rem;
        }
        </style>
        """
        st.markdown(metric_style, unsafe_allow_html=True)
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric(
                "Total Conferences", fake_data["summary_stats"]["total_conferences"]
            )
        with col2:
            st.metric("Total Papers", f"{fake_data['summary_stats']['total_papers']:,}")
        with col3:
            st.metric("Years Covered", fake_data["summary_stats"]["total_years"])
        with col4:
            st.metric(
                "Avg Papers/Year",
                f"{fake_data['summary_stats']['avg_papers_per_year']:,}",
            )

        # Create column for conferences list
        st.subheader("Top Conferences")

        for conf in fake_data["top_conferences"]:
            with st.expander(f"**{conf['name']} - {conf['full_name']}**"):
                # Determine which keys to display based on what's available in the conference data
                has_papers = 'total_papers' in conf
                has_citations = 'avg_citations' in conf

                # Create the appropriate display text
                first_metric_label = "Total Papers" if has_papers else "Total Sessions"
                first_metric_value = f"{conf['total_papers']:,}" if has_papers else f"{conf['total_sessions']}"

                second_metric_label = "Average Citations" if has_citations else "Dates"
                second_metric_value = f"{conf['avg_citations']}" if has_citations else f"{conf['dates']}"

                st.markdown(
                    f"""
                    <div style='padding: 10px;'>
                        <div style='
                            color: #666;
                            margin-bottom: 15px;
                            padding: 10px;
                            background-color: #f8f9fa;
                            border-radius: 5px;
                            font-style: italic;
                        '>{conf['intro']}</div>
                        <div style='display: flex; justify-content: space-between; margin-bottom: 10px;'>
                            <span style='font-weight: bold; color: #666;'>{first_metric_label}</span>
                            <span style='font-weight: bold; color: #1f77b4;'>{first_metric_value}</span>
                        </div>
                        <div style='display: flex; justify-content: space-between;'>
                            <span style='font-weight: bold; color: #666;'>{second_metric_label}</span>
                            <span style='font-weight: bold; color: #1f77b4;'>{second_metric_value}</span>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

    @staticmethod
    def render_conference_overview(conference: str):
        """Render overview of specific conference with session data and filtering options."""
        # Load the conference data if it hasn't been loaded yet
        if Conference.gtc_sessions is None:
            Conference.gtc_sessions = Conference.load_conference_data()

        st.header(f"{conference} Conference Details")

        # Conference information
        st.markdown(
            """
            <div style='
                padding: 15px;
                margin-bottom: 20px;
                background-color: #f8f9fa;
                border-radius: 5px;
                border-left: 5px solid #1f77b4;
            '>
                <h3 style='margin-top: 0; color: #1f77b4;'>Nvidia GTC 2025</h3>
                <p style='font-style: italic;'>NVIDIA's premier conference for developers, researchers, and technologists exploring AI, graphics, HPC, and more.</p>
                <p><strong>Date:</strong> March 17-21, 2025</p>
                <p><strong>Location:</strong> San Jose Convention Center, San Jose, CA</p>
                <p><strong>Total Sessions:</strong> 120+</p>
            </div>
            """,
            unsafe_allow_html=True
        )

        # Get available dates from the mock data
        available_dates = [day_data["date"] for day_data in Conference.gtc_sessions]
        days_of_week = [day_data["day"] for day_data in Conference.gtc_sessions]

        # Combine dates with days for display
        date_labels = [f"{day} ({date.split(', ')[0]})" for day, date in zip(days_of_week, available_dates)]

        # Initialize session state for selected date if not exists
        if "selected_date_index" not in st.session_state:
            st.session_state.selected_date_index = 0

        # Session state for tracking selected session
        if "selected_session" not in st.session_state:
            st.session_state.selected_session = None

        # Get the currently selected date
        selected_date = available_dates[st.session_state.selected_date_index]

        # Create browser-tab style date navigation
        st.markdown(
            """
            <style>
            /* Date tab styles */
            .date-tab-container {
                display: flex;
                overflow-x: auto;
                margin-bottom: 20px;
                border-bottom: 1px solid #ddd;
            }
            .date-tab {
                padding: 8px 16px;
                margin-right: 4px;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
                cursor: pointer;
                text-align: center;
                user-select: none;
                transition: background-color 0.3s;
            }
            .date-tab.active {
                background-color: #1f77b4;
                color: white;
                border: 1px solid #1f77b4;
                border-bottom: none;
                position: relative;
                top: 1px;
                font-weight: bold;
            }
            .date-tab:not(.active) {
                background-color: #f1f1f1;
                border: 1px solid #ddd;
                border-bottom: none;
            }
            .date-tab:hover:not(.active) {
                background-color: #e6e6e6;
            }

            /* Session list styles */
            .session-list-item {
                padding: 10px 15px;
                margin: 5px 0;
                border: 1px solid #ddd;
                border-radius: 5px;
                cursor: pointer;
                transition: all 0.2s ease;
            }
            .session-list-item:hover {
                background-color: #f5f5f5;
                transform: translateX(5px);
            }
            .session-list-item.selected {
                background-color: #e6f7ff;
                border-color: #1f77b4;
                border-left: 4px solid #1f77b4;
            }

            /* Topic tag styles */
            .topic-tag {
                display: inline-block;
                color: white;
                font-weight: bold;
                font-size: 0.8em;
                padding: 3px 10px;
                border-radius: 12px;
                margin-bottom: 8px;
            }

            /* Session detail styles */
            .session-detail-container {
                padding: 0;
                height: 0;
                overflow: hidden;
                transition: all 0.3s ease-out;
                opacity: 0;
            }
            .session-detail-container.active {
                padding: 15px;
                height: auto;
                opacity: 1;
                border: 1px solid #ddd;
                border-radius: 5px;
                background-color: white;
                border-left: 4px solid #1f77b4;
                margin-bottom: 15px;
                box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            }
            </style>
            """,
            unsafe_allow_html=True
        )

        # Create tabs container with columns (one for each date)
        tabs_cols = st.columns(len(available_dates))

        # Update the selected date when a tab is clicked
        for i, (col, date, label) in enumerate(zip(tabs_cols, available_dates, date_labels)):
            with col:
                # Create a button styled as a tab
                if st.button(
                        label,
                        key=f"date_tab_{i}",
                        use_container_width=True,
                        type="primary" if i == st.session_state.selected_date_index else "secondary"
                ):
                    st.session_state.selected_date_index = i
                    # Reset selected session when changing dates
                    st.session_state.selected_session = None
                    st.rerun()

        # Find the sessions for the selected date
        selected_day_data = next(
            (day for day in Conference.gtc_sessions if day["date"] == selected_date),
            None
        )

        # Helper function to sort times chronologically
        def time_key(time_str):
            """Convert time string to minutes for sorting."""
            # Handle both formats: "9:00 AM" and "9:00 AM - 10:30 AM"
            if " - " in time_str:
                time_str = time_str.split(" - ")[0]

            # Extract hours and minutes
            time_parts = time_str.split(":")
            hour = int(time_parts[0])
            minute_parts = time_parts[1].split(" ")
            minute = int(minute_parts[0])
            am_pm = minute_parts[1].upper()

            # Convert to 24-hour time for easier sorting
            if am_pm == "PM" and hour != 12:
                hour += 12
            elif am_pm == "AM" and hour == 12:
                hour = 0

            # Return minutes since midnight for sorting
            return hour * 60 + minute

        # Extract times and topics only for the selected date
        available_times_for_date = []
        available_topics_for_date = []

        if selected_day_data:
            for session in selected_day_data["sessions"]:
                # Extract the starting time from the time range
                start_time = session["time"].split(" - ")[0]
                available_times_for_date.append(start_time)
                available_topics_for_date.append(session["track"])

            # Remove duplicates and sort
            # Sort times chronologically using the time_key function
            available_times_for_date = sorted(list(set(available_times_for_date)), key=time_key)
            available_topics_for_date = sorted(list(set(available_topics_for_date)))

        # Create filters section
        st.subheader("Filter Sessions")

        # Create two columns for remaining filters
        filter_col1, filter_col2 = st.columns(2)

        # Topic/track filter in first column
        with filter_col1:
            selected_track = st.selectbox(
                "Filter by topic:",
                options=["All Topics"] + available_topics_for_date,
                index=0
            )

        # Time filter in second column - with date-specific times
        with filter_col2:
            selected_time = st.selectbox(
                "Filter by start time:",
                options=["All Hours"] + available_times_for_date,
                index=0  # Default to "All Hours"
            )

        # Check if we should reset to show all tracks when none are selected
        if not selected_track:
            st.warning("No topics selected. Showing all topics.")
            selected_track = available_topics_for_date

        if selected_day_data:
            # Apply combined filtering
            filtered_sessions = selected_day_data["sessions"]

            # Filter by topic
            if selected_track != "All Topics":
                filtered_sessions = [
                    session for session in filtered_sessions
                    if session["track"] == selected_track
                ]

            # Filter by start time if a specific time is selected
            if selected_time != "All Hours":
                filtered_sessions = [
                    session for session in filtered_sessions
                    if session["time"].startswith(selected_time)
                ]

            if not filtered_sessions:
                st.info(f"No sessions found for the selected filters on {selected_day_data['date']}.")
            else:
                st.markdown(f"### Sessions for {selected_day_data['date']} ({selected_day_data['day']})")
                st.markdown(f"Showing {len(filtered_sessions)} session(s) matching your filters")

                # Show filter summary
                filter_summary = []
                if selected_track != "All Topics":
                    filter_summary.append(f"**Topics:** {selected_track}")
                if selected_time != "All Hours":
                    filter_summary.append(f"**Starting at:** {selected_time}")

                if filter_summary:
                    st.markdown(" | ".join(filter_summary))

                # Dynamic color generation for topics - will work with any number of topics
                def get_topic_color(topic):
                    """Generate a color based on the topic name using HSL color space for better distribution."""
                    # Use a hash of the topic name to generate a hue value
                    topic_hash = hash(topic) % 360  # Hue values are 0-359

                    # Fixed saturation and lightness for consistent, readable colors
                    saturation = 80  # Higher value = more vibrant colors
                    lightness = 45  # Slightly darker for better contrast

                    # Convert HSL to a CSS color string
                    return f"hsl({topic_hash}, {saturation}%, {lightness}%)"

                # Create two-column layout for sessions
                main_col1, main_col2 = st.columns([1, 1.5])

                with main_col1:
                    st.markdown("### Session List")

                    # Display each session as a clickable item
                    for i, session in enumerate(filtered_sessions):
                        # Determine if this session is selected
                        is_selected = st.session_state.selected_session == i

                        # Get topic color
                        topic_color = get_topic_color(session['track'])

                        # Create session item container
                        session_container = st.container()
                        with session_container:
                            # First show the topic tag ABOVE the session title
                            st.markdown(
                                f"""
                                <div>
                                    <span class="topic-tag" style="background-color: {topic_color};">
                                        {session['track']}
                                    </span>
                                </div>
                                """,
                                unsafe_allow_html=True
                            )

                            # Then show the session button
                            if st.button(
                                    f"{session['time']} - {session['title']}",
                                    key=f"session_btn_{i}",
                                    use_container_width=True,
                                    type="primary" if is_selected else "secondary",
                                    help="Click to view details"
                            ):
                                # Toggle selection
                                if st.session_state.selected_session == i:
                                    st.session_state.selected_session = None
                                else:
                                    st.session_state.selected_session = i
                                st.rerun()

                            # Add a little spacing between sessions
                            st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

                with main_col2:
                    st.markdown("### Session Details")

                    # Display details of selected session with animation
                    if st.session_state.selected_session is not None and st.session_state.selected_session < len(
                            filtered_sessions):
                        selected_session = filtered_sessions[st.session_state.selected_session]
                        topic_color = get_topic_color(selected_session['track'])

                        # Create animated container for details with all fields
                        # Prepare additional details sections
                        additional_details = ""

                        # Session Code (if available)
                        if 'session_code' in selected_session and selected_session['session_code']:
                            additional_details += f"""
                            <div style="margin-bottom: 10px;">
                                <strong>Session Code:</strong> {selected_session['session_code']}
                            </div>
                            """

                        # Technical Level (if available)
                        if 'technical_level' in selected_session and selected_session['technical_level']:
                            additional_details += f"""
                            <div style="margin-bottom: 10px;">
                                <strong>Technical Level:</strong> {selected_session['technical_level']}
                            </div>
                            """

                        # Full Topic (if available and different from track)
                        if 'full_topic' in selected_session and selected_session['full_topic'] and selected_session[
                            'full_topic'] != selected_session['track']:
                            additional_details += f"""
                            <div style="margin-bottom: 10px;">
                                <strong>Full Topic:</strong> {selected_session['full_topic']}
                            </div>
                            """

                        # Key Points (if available)
                        points_html = ""
                        if 'points' in selected_session and selected_session['points']:
                            points = selected_session['points'].split('\n')
                            points_html = """
                            <div style="margin-top: 15px; margin-bottom: 15px;">
                                <strong>Key Points:</strong>
                                <ul style="margin-top: 5px;">
                            """
                            for point in points:
                                if point.strip():  # Skip empty lines
                                    points_html += f"<li>{point.strip()}</li>"

                            points_html += """
                                </ul>
                            </div>
                            """

                        # Expert Input (if available)
                        expert_html = ""
                        if 'expert_input' in selected_session and selected_session['expert_input']:
                            expert_html = f"""
                            <div style="margin-top: 15px; margin-bottom: 15px;">
                                <strong>Expert Input:</strong>
                                <div style="
                                    margin-top: 5px;
                                    padding: 10px;
                                    background-color: #f0f7ff;
                                    border-radius: 5px;
                                    border-left: 3px solid #1f77b4;
                                ">
                                    {selected_session['expert_input']}
                                </div>
                            </div>
                            """
                        # Description (if available) - Refactored for consistency
                        description_html = ""
                        if 'description' in selected_session and selected_session['description']:
                            description_html = f"""
                            <div style="margin-top: 15px; margin-bottom: 15px;">
                                <strong>Description:</strong>
                                <div style="
                                    margin-top: 5px;
                                    padding: 10px;
                                    background-color: #f8f9fa; /* Lighter gray */
                                    border-radius: 5px;
                                    border-left: 3px solid #1f77b4;
                                    font-style: italic; /* Optional: Italicize the description */
                                ">
                                    {Conference.sanitize_description(selected_session['description'])}
                                </div>
                            </div>
                            """

                        # Create animated container for details with all fields in a single HTML block
                        st.markdown(
                            f"""
                            <div class="session-detail-container active">
                                <div>
                                    <span class="topic-tag" style="background-color: {topic_color};">
                                        {selected_session['track']}
                                    </span>
                                </div>
                                <h3>{selected_session['title']}</h3>
                                <div style="margin-bottom: 10px;">
                                    <strong>Time:</strong> {selected_session['time']}
                                </div>
                                <div style="margin-bottom: 10px;">
                                    <strong>Speaker:</strong> {selected_session['speaker']}
                                </div>
                                <div style="margin-bottom: 10px;">
                                    <strong>Location:</strong> {selected_session['location']}
                                </div>

                                {additional_details}
                                {description_html}
                                {points_html}
                                {expert_html}

                            </div>
                            """,
                            unsafe_allow_html=True
                        )
                    else:
                        # Show a placeholder when no session is selected
                        st.markdown(
                            """
                            <div style="
                                text-align: center;
                                padding: 30px;
                                background-color: #f8f9fa;
                                color: #666;
                                border-radius: 5px;
                                border: 1px dashed #ddd;
                            ">
                                <p>Select a session from the list to view details</p>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )

        else:
            st.warning("No sessions found for the selected date.")

    @staticmethod
    def render_year_overview(year: int):
        """Simplified year overview - redirects to conference overview."""
        st.info(f"Please select a specific conference to view its details for {year}.")
        Conference.render_overview()

    @staticmethod
    def render_instance(year: int, conference: str):
        """Simplified instance view - redirects to conference overview."""
        Conference.render_conference_overview(conference)