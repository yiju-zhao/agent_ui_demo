import os
import streamlit as st
import pandas as pd
import json
from datetime import datetime
from models import ConferenceInstance, Session
from utility.db_util import (
    DataManagerContext,
    conference_stat_df,
    aggregate_stat_df,
)
from utility.visualization_utli import DashboardLayout
import plotly.graph_objects as go
import circlify


class Conference:
    """Handles rendering of conference-related content."""

    @staticmethod
    def sanitize_description(text):
        """Basic sanitization to escape HTML tags but preserve basic formatting"""
        if not text:
            return ""
        text = text.replace("<", "&lt;").replace(">", "&gt;")
        text = text.replace("\n", "<br>")
        return text
    
    @staticmethod
    def load_session_data(instance_id=None):
        """Load session data from database"""
        try:
            with DataManagerContext() as managers:
                if instance_id:
                    # Get sessions through conference repository
                    sessions = managers["conference"].get_sessions_by_instance(
                        instance_id
                    )
                    if not sessions:
                        return []

                    # Group sessions by date
                    session_by_date = {}
                    for session in sessions:
                        date_str = session.date.strftime("%Y-%m-%d")
                        if date_str not in session_by_date:
                            session_by_date[date_str] = []

                        # Find related speakers
                        speaker_list = []
                        speaker_companies = []
                        
                        for speaker in session.speaker_to_session:
                            # Get affiliation name using affiliation_id
                            affiliation_name = ""
                            if speaker.affiliation_id:
                                affiliation = managers["org"].get_affiliation_by_id(
                                    speaker.affiliation_id
                                )
                                if affiliation:
                                    affiliation_name = affiliation.name
                                    speaker_companies.append(affiliation_name)

                            # Format speaker string
                            if speaker.position:
                                speaker_str = f"{speaker.name} ({speaker.position} | {affiliation_name})"
                            else:
                                speaker_str = f"{speaker.name} ({affiliation_name})" if affiliation_name else speaker.name
                            
                            speaker_list.append(speaker_str)

                        formatted_session = {
                            "time": f"{session.start_time.strftime('%I:%M %p')} - {session.end_time.strftime('%I:%M %p')}",
                            "title": session.title,
                            "speaker": ", ".join(speaker_list),
                            "location": (
                                f"{session.venue}, {session.room}"
                                if session.room
                                else session.venue
                            ),
                            "venue": session.venue,  # Add venue separately for filtering
                            "speaker_companies": speaker_companies,  # Add companies for filtering
                            "track": session.topic,
                            "description": session.description if session.description and session.description != 'nan' else "",
                            "session_code": session.session_code,
                            "technical_level": session.technical_level,
                            "full_topic": session.topic,
                            "points": session.points if session.points and session.points != 'nan' else "",
                        }
                        session_by_date[date_str].append(formatted_session)

                    # Convert to list and sort chronologically
                    session_data = [
                        {
                            "date": date_str,
                            "day": datetime.strptime(date_str, "%Y-%m-%d").strftime(
                                "%A"
                            ),
                            "sessions": sorted(
                                sessions_list,
                                key=lambda x: datetime.strptime(
                                    x["time"].split(" - ")[0], "%I:%M %p"
                                ),
                            ),
                        }
                        for date_str, sessions_list in session_by_date.items()
                    ]

                    # Sort days chronologically
                    session_data.sort(key=lambda x: x["date"])

                    return session_data

                return []
        except Exception as e:
            st.error(f"Error loading session data: {e}")
            return []

    # ---------------------------------------------------------------------------- #
    #                                   overview                                   #
    # ---------------------------------------------------------------------------- #
    @staticmethod
    def render_overview():
        """Render overview of all conferences across years."""
        # Fake data for conference overview
        fake_data = {
            "summary_stats": {
                "total_conferences": 25,
                "total_papers": 45000,
                "total_years": 10,
                "avg_papers_per_year": 4500,
            },
            "yearly_stats": {
                "years": [2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023],
                "paper_counts": [
                    3000,
                    3200,
                    3500,
                    3800,
                    4000,
                    4200,
                    4500,
                    4800,
                    5000,
                    5200,
                ],
                "conference_counts": [20, 20, 21, 22, 22, 23, 24, 24, 25, 25],
            },
            "research_focus": {
                "Software Testing & Verification": {
                    "description": "Focus on testing methodologies, verification techniques, and quality assurance",
                    "conferences": ["ISSTA", "ICSE", "ASE", "ISSRE"],
                },
                "Program Analysis & Generation": {
                    "description": "Research on code analysis, synthesis, and automated programming",
                    "conferences": ["FSE", "ICSE", "ASE", "PLDI"],
                },
                "Software Maintenance": {
                    "description": "Studies on software evolution, maintenance, and legacy system modernization",
                    "conferences": ["ICSME", "ICSE", "SANER", "MSR"],
                },
                "Empirical Studies": {
                    "description": "Evidence-based research and empirical methods in software engineering",
                    "conferences": ["ESEM", "ICSE", "FSE", "MSR"],
                },
                "AI/ML in Software Engineering": {
                    "description": "Applications of AI and machine learning in software development",
                    "conferences": ["ICSE", "FSE", "ASE", "MSR"],
                },
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
                    "name": "ASE",
                    "full_name": "Automated Software Engineering",
                    "intro": "Focuses on automated approaches to software development, testing, analysis, and maintenance, with emphasis on AI and machine learning applications.",
                    "total_papers": 3800,
                    "avg_citations": 22.1,
                },
                {
                    "name": "ISSTA",
                    "full_name": "International Symposium on Software Testing and Analysis",
                    "intro": "The primary conference for research in software testing and analysis, covering topics from test generation to program verification.",
                    "total_papers": 3500,
                    "avg_citations": 21.5,
                },
                {
                    "name": "ICSME",
                    "full_name": "International Conference on Software Maintenance and Evolution",
                    "intro": "Dedicated to advancing the state of the art in software maintenance, evolution, and reengineering of legacy systems.",
                    "total_papers": 3200,
                    "avg_citations": 20.2,
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

        # Create two columns for charts
        col_left, col_right = st.columns([1, 1])

        with col_left:
            # ------------------------- Top conferences overview ------------------------- #
            st.subheader("Top Conferences Overview")
            for conf in fake_data["top_conferences"]:
                with st.expander(f"**{conf['name']} - {conf['full_name']}**"):
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
                                <span style='font-weight: bold; color: #666;'>Total Papers</span>
                                <span style='font-weight: bold; color: #1f77b4;'>{conf['total_papers']:,}</span>
                            </div>
                            <div style='display: flex; justify-content: space-between;'>
                                <span style='font-weight: bold; color: #666;'>Average Citations</span>
                                <span style='font-weight: bold; color: #1f77b4;'>{conf['avg_citations']:.1f}</span>
                            </div>
                        </div>
                    """,
                        unsafe_allow_html=True,
                    )

        with col_right:
            # ------------------------- Conference research focus ------------------------ #
            st.subheader("Research Focus Areas")
            for focus, details in fake_data["research_focus"].items():
                with st.expander(f"**{focus}**"):
                    st.markdown(
                        f"""
                        <div style='
                            padding: 10px;
                            background-color: #f8f9fa;
                            border-radius: 5px;
                        '>
                            <div style='color: #666; margin-bottom: 8px;'>{details['description']}</div>
                            <div style='margin-top: 10px;'>
                                <div style='color: #666; font-weight: bold;'>Related Conferences:</div>
                                <div style='color: #1f77b4; padding: 5px 0;'>
                                    {', '.join(details['conferences'])}
                                </div>
                            </div>
                        </div>
                    """,
                        unsafe_allow_html=True,
                    )

        # st.subheader("Conference and Paper Trends")
        # ---------------------------- Yearly trends chart --------------------------- #
        yearly_fig = go.Figure()

        # Add papers trend
        yearly_fig.add_trace(
            go.Scatter(
                x=fake_data["yearly_stats"]["years"],
                y=fake_data["yearly_stats"]["paper_counts"],
                name="Papers",
                mode="lines+markers",
                line=dict(color="blue", width=2),
            )
        )

        # Add conferences trend on secondary y-axis
        yearly_fig.add_trace(
            go.Scatter(
                x=fake_data["yearly_stats"]["years"],
                y=fake_data["yearly_stats"]["conference_counts"],
                name="Conferences",
                mode="lines+markers",
                line=dict(color="red", width=2),
                yaxis="y2",
            )
        )

        yearly_fig.update_layout(
            title="Conference and Paper Trends",
            xaxis=dict(title="Year"),
            yaxis=dict(title="Number of Papers"),
            yaxis2=dict(title="Number of Conferences", overlaying="y", side="right"),
            hovermode="x unified",
            showlegend=True,
            legend=dict(
                orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1
            ),
        )
        st.plotly_chart(yearly_fig, use_container_width=True)

        # Additional information or notes
        st.markdown(
            """
        > **Note:** This overview represents conference data across all tracked years. 
        Select a specific year from the sidebar for detailed annual statistics.
        """
        )

    # ---------------------------------------------------------------------------- #
    #                                  conference                                  #
    # ---------------------------------------------------------------------------- #
    @staticmethod
    def render_conference_overview(conference: str):
        """Render overview of specific conference with session data and filtering options."""
        """Render overview of all conferences."""
        # Fake data for conference trends
        fake_data = {
            "years": [2019, 2020, 2021, 2022, 2023],
            "keywords_trend": {
                "Large Language Models": [0, 5, 15, 45, 80],
                "Neural Networks": [50, 45, 40, 35, 30],
                "Transformer": [10, 20, 35, 50, 60],
                "Reinforcement Learning": [30, 35, 25, 20, 15],
                "AutoML": [40, 35, 30, 20, 10],
                "Prompt Engineering": [0, 0, 10, 30, 50],
                "Few-shot Learning": [5, 15, 25, 35, 40],
            },
            "companies_trend": {
                "Google Research": [20, 25, 30, 35, 40],
                "Microsoft Research": [18, 22, 25, 30, 35],
                "Meta AI": [0, 15, 20, 25, 30],
                "DeepMind": [15, 18, 20, 25, 28],
                "OpenAI": [0, 5, 15, 25, 35],
                "IBM Research": [25, 22, 20, 18, 15],
                "NVIDIA Research": [10, 15, 18, 20, 25],
            },
            "academic_trend": {
                "Stanford": [30, 35, 38, 40, 45],
                "MIT": [28, 32, 35, 38, 42],
                "Berkeley": [25, 28, 32, 35, 38],
                "CMU": [22, 25, 28, 32, 35],
                "Tsinghua": [20, 25, 30, 35, 40],
                "ETH Zurich": [18, 20, 25, 28, 30],
                "Oxford": [15, 18, 22, 25, 28],
            },
            "paper_counts": [350, 380, 420, 450, 500],
        }

        st.header(f"{conference} Overview")

        # Create two rows with two columns each
        row1_col1, row1_col2 = st.columns(2)
        row2_col1, row2_col2 = st.columns(2)

        common_layout = dict(
            height=550,
            margin=dict(l=50, r=50, t=50, b=20),  # Adjust margins
            plot_bgcolor="white",
            legend=dict(
                orientation="h",  # Horizontal legend
                yanchor="bottom",  # Place at bottom
                y=-0.4,  # Move below plot
                xanchor="center",  # Center horizontally
                x=0.5,
                bgcolor="rgba(255, 255, 255, 0.8)",  # Semi-transparent background
                bordercolor="rgba(0, 0, 0, 0.1)",  # Light border
                borderwidth=1,
            ),
            xaxis=dict(showgrid=True, gridcolor="rgba(0, 0, 0, 0.1)"),
            yaxis=dict(showgrid=True, gridcolor="rgba(0, 0, 0, 0.1)"),
        )

        with row1_col1:
            keywords_fig = go.Figure()
            for keyword, counts in fake_data["keywords_trend"].items():
                keywords_fig.add_trace(
                    go.Scatter(
                        x=fake_data["years"],
                        y=counts,
                        name=keyword,
                        mode="lines+markers",
                    )
                )
            keywords_fig.update_layout(
                title=dict(text="Top Keywords Trend", y=0.95),
                xaxis_title="Year",
                yaxis_title="Number of Papers",
                **common_layout,
            )
            st.plotly_chart(keywords_fig, use_container_width=True)

        # ------------------------------ Companies Trend ----------------------------- #
        with row1_col2:
            companies_fig = go.Figure()
            for company, counts in fake_data["companies_trend"].items():
                companies_fig.add_trace(
                    go.Scatter(
                        x=fake_data["years"],
                        y=counts,
                        name=company,
                        mode="lines+markers",
                    )
                )
            companies_fig.update_layout(
                title=dict(text="Top Companies Contribution Trend", y=0.95),
                xaxis_title="Year",
                yaxis_title="Number of Papers",
                **common_layout,
            )
            st.plotly_chart(companies_fig, use_container_width=True)

        # ------------------------ Academic Institutions Trend ----------------------- #
        with row2_col1:
            academic_fig = go.Figure()
            for inst, counts in fake_data["academic_trend"].items():
                academic_fig.add_trace(
                    go.Scatter(
                        x=fake_data["years"], y=counts, name=inst, mode="lines+markers"
                    )
                )
            academic_fig.update_layout(
                title=dict(text="Top Academic Institutions Trend", y=0.95),
                xaxis_title="Year",
                yaxis_title="Number of Papers",
                **common_layout,
            )
            st.plotly_chart(academic_fig, use_container_width=True)

        # ----------------------------- Paper Count Trend ---------------------------- #
        with row2_col2:
            papers_fig = go.Figure()
            papers_fig.add_trace(
                go.Bar(
                    x=fake_data["years"],
                    y=fake_data["paper_counts"],
                    marker_color="rgb(55, 83, 109)",
                )
            )
            papers_fig.update_layout(
                title=dict(text="Total Papers Published", y=0.95),
                xaxis_title="Year",
                yaxis_title="Number of Papers",
                height=400,
                margin=dict(l=50, r=50, t=50, b=50),
                plot_bgcolor="white",
                showlegend=False,
                xaxis=dict(showgrid=True, gridcolor="rgba(0, 0, 0, 0.1)"),
                yaxis=dict(showgrid=True, gridcolor="rgba(0, 0, 0, 0.1)"),
            )
            st.plotly_chart(papers_fig, use_container_width=True)

        # Add spacing between rows
        st.markdown("<br>", unsafe_allow_html=True)

        # Additional conference information
        st.markdown(
            f"""
        > **Note:** This overview shows trends for {conference} over the past 5 years. 
        """
        )

    # ---------------------------------------------------------------------------- #
    #                                     year                                     #
    # ---------------------------------------------------------------------------- #
    @staticmethod
    def render_year_overview(year: int):
        # Fake data
        fake_data = {
            "trending_keywords": [
                {"keyword": "Large Language Models", "count": 150, "trend": "↑"},
                {"keyword": "Prompt Engineering", "count": 120, "trend": "↑"},
                {"keyword": "Neural Architecture", "count": 100, "trend": "→"},
                {"keyword": "Transformer Models", "count": 95, "trend": "↑"},
                {"keyword": "Federated Learning", "count": 85, "trend": "↑"},
                {"keyword": "Edge Computing", "count": 80, "trend": "→"},
                {"keyword": "Zero-shot Learning", "count": 75, "trend": "↑"},
                {"keyword": "AutoML", "count": 70, "trend": "↓"},
                {"keyword": "Knowledge Graphs", "count": 65, "trend": "→"},
                {"keyword": "Quantum ML", "count": 60, "trend": "↑"},
            ],
            "academic_institutes": [
                {"name": "Stanford University", "papers": 120},
                {"name": "MIT", "papers": 110},
                {"name": "UC Berkeley", "papers": 95},
                {"name": "Carnegie Mellon", "papers": 90},
                {"name": "ETH Zurich", "papers": 85},
                {"name": "Tsinghua University", "papers": 80},
                {"name": "University of Oxford", "papers": 75},
                {"name": "University of Cambridge", "papers": 70},
                {"name": "University of Toronto", "papers": 65},
                {"name": "TU Munich", "papers": 60},
                {"name": "Others", "papers": 150},
            ],
            "companies": [
                {"name": "Google Research", "papers": 100},
                {"name": "Microsoft Research", "papers": 90},
                {"name": "Meta AI", "papers": 85},
                {"name": "DeepMind", "papers": 80},
                {"name": "IBM Research", "papers": 70},
                {"name": "OpenAI", "papers": 65},
                {"name": "NVIDIA Research", "papers": 60},
                {"name": "Amazon Science", "papers": 55},
                {"name": "Anthropic", "papers": 50},
                {"name": "Huawei Research", "papers": 45},
                {"name": "Others", "papers": 200},
            ],
            "conferences": [
                {"name": "ICML 2024", "date": "Jul 21-27", "papers": 1200},
                {"name": "NeurIPS 2024", "date": "Dec 8-14", "papers": 1150},
                {"name": "ICLR 2024", "date": "May 7-11", "papers": 1100},
                {"name": "AAAI 2024", "date": "Feb 20-27", "papers": 1000},
                {"name": "ACL 2024", "date": "Aug 12-17", "papers": 950},
                {"name": "CVPR 2024", "date": "Jun 17-21", "papers": 900},
                {"name": "IJCAI 2024", "date": "Aug 3-9", "papers": 850},
                {"name": "ECCV 2024", "date": "Sep 29-Oct 4", "papers": 800},
            ],
        }

        st.header("Conference Years Overview")

        # Create two columns for the layout
        left_col, right_col = st.columns([2, 1])

        with left_col:
            # Trending Keywords (Top Left)
            st.subheader("Trending Research Topics")
            for keyword in fake_data["trending_keywords"]:
                trend_color = {"↑": "green", "↓": "red", "→": "gray"}[keyword["trend"]]
                st.markdown(
                    f"""
                    <div style='
                        display: flex;
                        justify-content: space-between;
                        padding: 5px;
                        border-bottom: 1px solid #eee;
                    '>
                        <span>{keyword['keyword']}</span>
                        <span style='color: {trend_color}'>{keyword['count']} {keyword['trend']}</span>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            # Companies (Bottom Right)
            st.markdown("<br>", unsafe_allow_html=True)
            st.subheader("Top Industry Contributors")

            companies_fig = go.Figure(
                data=[
                    go.Pie(
                        labels=[company["name"] for company in fake_data["companies"]],
                        values=[
                            company["papers"] for company in fake_data["companies"]
                        ],
                        hole=0.3,
                        textinfo="label+percent",
                        textposition="outside",
                        pull=[
                            0.1 if company["name"] == "Others" else 0
                            for company in fake_data["companies"]
                        ],
                    )
                ]
            )

            companies_fig.update_layout(
                showlegend=False, height=500, margin=dict(t=0, b=0, l=0, r=0)
            )

            st.plotly_chart(companies_fig, use_container_width=True)

            # Academic Institutes (Bottom Left)
            st.markdown("<br>", unsafe_allow_html=True)
            st.subheader("Top Academic Contributors")

            academic_fig = go.Figure(
                data=[
                    go.Pie(
                        labels=[
                            inst["name"] for inst in fake_data["academic_institutes"]
                        ],
                        values=[
                            inst["papers"] for inst in fake_data["academic_institutes"]
                        ],
                        hole=0.3,
                        textinfo="label+percent",
                        textposition="outside",
                        pull=[
                            0.1 if inst["name"] == "Others" else 0
                            for inst in fake_data["academic_institutes"]
                        ],
                    )
                ]
            )

            academic_fig.update_layout(
                title="Academic Institutions",
                showlegend=False,
                height=500,
                margin=dict(t=0, b=0, l=0, r=0),
            )

            st.plotly_chart(academic_fig, use_container_width=True)

        with right_col:
            # Conferences (Top Right)
            st.subheader(f"Conference in {year}")
            from datetime import datetime

            sorted_conferences = sorted(
                fake_data["conferences"],
                key=lambda x: datetime.strptime(x["date"].split("-")[0], "%b %d"),
                reverse=True,
            )

            for conf in sorted_conferences:
                st.markdown(
                    f"""
                    <div style='
                        padding: 10px;
                        margin: 5px 0;
                        border: 1px solid #ddd;
                        border-radius: 5px;
                    '>
                        <div style='
                            display: flex;
                            justify-content: space-between;
                        '>
                            <strong>{conf['name']}</strong>
                            <span>{conf['papers']} papers</span>
                        </div>
                        <div style='color: gray; font-size: 0.9em;'>{conf['date']}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

    # ---------------------------------------------------------------------------- #
    #                                   instance                                   #
    # ---------------------------------------------------------------------------- #
    @staticmethod
    def render_instance(year: int, conference: str):
        # Ensure we preserve the current view
        st.session_state.filter_mode_menu = "Conference"
        st.session_state.selected_year = year
        st.session_state.selected_conference = conference
        
        # Initialize session states if not exists
        if "active_tab" not in st.session_state:
            st.session_state.active_tab = 0
        if "selected_session" not in st.session_state:
            st.session_state.selected_session = None
        if "filtered_sessions" not in st.session_state:
            st.session_state.filtered_sessions = None
            
        # Callback functions for state updates
        def on_date_select(idx):
            st.session_state.active_tab = idx
            st.session_state.selected_session = None
            
        def on_session_select(idx):
            st.session_state.selected_session = idx

        try:
            with DataManagerContext() as managers:
                # Get conference instance through repository
                instance = managers["conference"].get_instance_by_year_and_name(
                    year, conference
                )

                if not instance:
                    st.error(f"No conference instance found for {conference} {year}")
                    return

                # Load session data
                session_data = Conference.load_session_data(instance.instance_id)
                if not session_data:
                    st.warning("No sessions found for this conference instance.")
                    return

                # Conference information header
                st.markdown(
                    f"""
                    <div style='padding: 15px; margin-bottom: 20px; background-color: #f8f9fa; 
                        border-radius: 5px; border-left: 5px solid #1f77b4;'>
                        <h3 style='margin-top: 0; color: #1f77b4;'>{instance.conference_name} {instance.year}</h3>
                        <p><strong>Date:</strong> {instance.start_date.strftime('%B %d')} - 
                        {instance.end_date.strftime('%B %d, %Y')}</p>
                        <p><strong>Location:</strong> {instance.location or "Location not specified"}</p>
                        {f'<p><strong>Website:</strong> <a href="{instance.website}" target="_blank">{instance.website}</a></p>' 
                        if instance.website else ''}
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                # Get available dates
                available_dates = [day_data["date"] for day_data in session_data]
                days_of_week = [day_data["day"] for day_data in session_data]
                date_labels = [
                    f"{day} ({datetime.strptime(date, '%Y-%m-%d').strftime('%B %d')})"
                    for day, date in zip(days_of_week, available_dates)
                ]

                # Date selection buttons with callbacks
                st.markdown("### Select Date")
                date_cols = st.columns(len(date_labels))
                for i, (label, col) in enumerate(zip(date_labels, date_cols)):
                    with col:
                        st.button(
                            label,
                            key=f"date_btn_{i}",
                            on_click=on_date_select,
                            args=(i,),
                            use_container_width=True,
                            type="primary" if st.session_state.active_tab == i else "secondary"
                        )

                # Get current day's data
                tab_idx = st.session_state.active_tab
                day_data = session_data[tab_idx]

                # Cache and get filter options
                filter_key = f"filter_options_{tab_idx}"
                if filter_key not in st.session_state:
                    st.session_state[filter_key] = {
                        "topics": sorted(list(set(s["track"] for s in day_data["sessions"]))),
                        "times": sorted(list(set(
                            s["time"].split(" - ")[0] for s in day_data["sessions"]
                        )), key=lambda x: datetime.strptime(x, "%I:%M %p")),
                        "venues": sorted(list(set(s["venue"] for s in day_data["sessions"]))),
                        "companies": sorted(list(set(
                            company for s in day_data["sessions"]
                            for company in s["speaker_companies"]
                        )))
                    }

                # Filter UI
                st.subheader("Filter Sessions")
                filter_cols = st.columns(4)
                
                with filter_cols[0]:
                    selected_track = st.selectbox(
                        "Filter by topic:",
                        options=["All Topics"] + st.session_state[filter_key]["topics"],
                        key=f"topic_filter_{tab_idx}"
                    )
                
                with filter_cols[1]:
                    selected_time = st.selectbox(
                        "Filter by start time:",
                        options=["All Hours"] + st.session_state[filter_key]["times"],
                        key=f"time_filter_{tab_idx}"
                    )
                
                with filter_cols[2]:
                    selected_venue = st.selectbox(
                        "Filter by venue:",
                        options=["All Venues"] + st.session_state[filter_key]["venues"],
                        key=f"venue_filter_{tab_idx}"
                    )
                
                with filter_cols[3]:
                    selected_company = st.selectbox(
                        "Filter by company:",
                        options=["All Companies"] + st.session_state[filter_key]["companies"],
                        key=f"company_filter_{tab_idx}"
                    )

                # Apply filters
                filtered_sessions = day_data["sessions"]
                if selected_track != "All Topics":
                    filtered_sessions = [s for s in filtered_sessions if s["track"] == selected_track]
                if selected_time != "All Hours":
                    filtered_sessions = [s for s in filtered_sessions if s["time"].startswith(selected_time)]
                if selected_venue != "All Venues":
                    filtered_sessions = [s for s in filtered_sessions if s["venue"] == selected_venue]
                if selected_company != "All Companies":
                    filtered_sessions = [s for s in filtered_sessions if selected_company in s["speaker_companies"]]

                # Session list and details
                list_col, details_col = st.columns([1, 1.5])
                
                with list_col:
                    st.markdown("### Sessions")
                    if not filtered_sessions:
                        st.info("No sessions found for the selected filters.")
                    else:
                        st.markdown(f"Showing {len(filtered_sessions)} session(s)")
                        
                        for i, session in enumerate(filtered_sessions):
                            st.markdown(
                                f"""<div style='color: #666666; font-size: 0.9em; 
                                margin-bottom: 2px;'>{session['time']}</div>""",
                                unsafe_allow_html=True
                            )
                            
                            st.button(
                                session['title'],
                                key=f"session_btn_{tab_idx}_{i}",
                                on_click=on_session_select,
                                args=(i,),
                                use_container_width=True,
                                type="primary" if st.session_state.selected_session == i else "secondary"
                            )

                # Rest of the details column code remains the same
                with details_col:
                    st.markdown("### Session Details")
                    if st.session_state.selected_session is not None and st.session_state.selected_session < len(filtered_sessions):
                        selected_session = filtered_sessions[st.session_state.selected_session]
                        
                        # Title first
                        st.markdown(f"#### {selected_session['title']}")
                        
                        # Create two columns for the first row
                        col1, col2 = st.columns(2)
                        with col1:
                            st.markdown(f"**Time:** {selected_session['time']}")
                            st.markdown(f"**Track:** {selected_session['track']}")
                        with col2:
                            st.markdown(f"**Location:** {selected_session['location']}")
                            if selected_session.get('session_code'):
                                st.markdown(f"**Session Code:** {selected_session['session_code']}")

                        # Technical level
                        if selected_session.get('technical_level'):
                            st.markdown(f"**Technical Level:** {selected_session['technical_level']}")

                        # Speakers
                        st.markdown(f"**Speaker(s):** {selected_session['speaker']}")


                        # In the display section:
                        # Description
                        if selected_session.get('description') and selected_session['description'] != 'nan':
                            description = selected_session['description']
                            if isinstance(description, str) and description.strip():
                                st.markdown('<div class="description-expander">', unsafe_allow_html=True)
                                with st.expander("📝 Description"):
                                    st.markdown(description)
                                st.markdown('</div>', unsafe_allow_html=True)
                                
                        # Key Points
                        if selected_session.get('points'):
                            points = selected_session['points']
                            if isinstance(points, str) and points.strip() and points.lower() != 'nan':
                                points_list = [p.strip() for p in points.split('\n') if p.strip() and p.lower() != 'nan']
                                if points_list:
                                    st.markdown('<div class="key-points-expander">', unsafe_allow_html=True)
                                    with st.expander("🎯 Key Points"):
                                        for point in points_list:
                                            st.markdown(point)
                                    st.markdown('</div>', unsafe_allow_html=True)

                        # Expert Opinion
                        if selected_session.get('expert_opinion') and selected_session['expert_opinion'] != 'nan':
                            expert_opinion = selected_session['expert_opinion']
                            if isinstance(expert_opinion, str) and expert_opinion.strip():
                                st.markdown('<div class="expert-opinion-expander">', unsafe_allow_html=True)
                                with st.expander("👨‍🏫 专家观点"):
                                    opinion_list = [p.strip() for p in expert_opinion.split('\n') if p.strip()]
                                    for opinion in opinion_list:
                                        st.markdown(opinion)
                                st.markdown('</div>', unsafe_allow_html=True)

                        # AI Interpretation
                        if selected_session.get('ai_interpretation') and selected_session['ai_interpretation'] != 'nan':
                            ai_interpretation = selected_session['ai_interpretation']
                            if isinstance(ai_interpretation, str) and ai_interpretation.strip():
                                st.markdown('<div class="ai-interpretation-expander">', unsafe_allow_html=True)
                                with st.expander("🤖 AI解读"):
                                    interpretation_list = [p.strip() for p in ai_interpretation.split('\n') if p.strip()]
                                    for interpretation in interpretation_list:
                                        st.markdown(interpretation)
                                st.markdown('</div>', unsafe_allow_html=True)

        except Exception as e:
            st.error(f"Error rendering conference instance: {e}")
            import traceback
            st.error(traceback.format_exc())
