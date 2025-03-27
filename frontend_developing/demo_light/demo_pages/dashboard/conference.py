import os
import streamlit as st
import pandas as pd
import json
from streamlit import cache_data
from datetime import datetime
from models import ConferenceInstance, Session
from utility.db_util import (
    DataManagerContext,
    conference_stat_df,
    aggregate_stat_df,
    DataLoader,
    CompanyMatcher,
    TopicAnalyzer,
)
from utility.visualization_utli import DashboardLayout, ConferenceVisualization, CompanyVisualization, TopicVisualization
from utility.conf_util import SessionFilterHandler
import plotly.graph_objects as go
import altair as alt
import circlify
import plotly.express as px  # Add this import for Plotly Express



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

        # Yearly trends chart
        ConferenceVisualization.render_trend_charts(fake_data["yearly_stats"], "Conference and Paper Trends")

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

        st.header(f"Conference Year Overview: {year}")

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
                showlegend=False,
                height=500,
                margin=dict(t=0, b=0, l=0, r=0),
            )

            st.plotly_chart(academic_fig, use_container_width=True)

        with right_col:
            # Conferences (Top Right)
            st.subheader(f"Conferences in {year}")
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
    @cache_data(ttl=3600)  # Cache for 1 hour
    def _prepare_instance_data(year: int, conference: str):
        """Cache all data preparation for the instance"""
        with DataManagerContext() as managers:
            # Get conference instance and session data
            instance = managers["conference"].get_instance_by_year_and_name(year, conference)
            if not instance:
                return None
            
            # Use the DataLoader utility to load session data
            session_data = DataLoader.load_session_data(instance.instance_id)
            if not session_data:
                return None
            
            # Prepare date information
            available_dates = [day_data["date"] for day_data in session_data]
            days_of_week = [day_data["day"] for day_data in session_data]
            date_labels = [
                f"{day} ({datetime.strptime(date, '%Y-%m-%d').strftime('%B %d')})"
                for day, date in zip(days_of_week, available_dates)
            ]
            
            # Prepare filter options for each day using the SessionFilterHandler
            filter_options = SessionFilterHandler.prepare_filter_options(session_data)
            
            return {
                "instance": instance,
                "session_data": session_data,
                "date_labels": date_labels,
                "filter_options": filter_options
            }
        
    @staticmethod
    @cache_data(ttl=3600)  # Cache for 1 hour
    def _get_topic_data_cached(instance_id):
        """Cache topic data retrieval to prevent redundant database queries."""
        with DataManagerContext() as managers:
            # Get all sessions for this instance
            sessions = managers["conference"].get_sessions_by_instance(instance_id)
            if not sessions:
                return None
            
            # Extract topic data using the TopicAnalyzer utility
            return TopicAnalyzer.extract_topic_data(sessions)
        
    @staticmethod
    @cache_data(ttl=3600)  # Cache for 1 hour
    def _get_company_data_cached(instance_id):
        """Cache company data retrieval to prevent redundant database queries."""
        with DataManagerContext() as managers:
            # Use the DataLoader utility to load session data
            session_data = DataLoader.load_session_data(instance_id)
            if not session_data:
                return None, None
            
            # Extract company data
            cloud_data = CompanyMatcher.extract_company_topic_data(
                session_data, 
                CompanyMatcher.CLOUD_COMPANIES, 
                CompanyMatcher.CLOUD_COMPANY_ALIASES
            )
            
            oem_data = CompanyMatcher.extract_company_topic_data(
                session_data, 
                CompanyMatcher.OEM_COMPANIES, 
                CompanyMatcher.OEM_COMPANY_ALIASES
            )
            
            return cloud_data, oem_data
    
    @staticmethod
    def _render_session_insights(instance):
        """Render insights for session-based conferences."""
        # Get cached data using only the instance_id (which is hashable)
        topic_data = Conference._get_topic_data_cached(instance.instance_id)
        cloud_data, oem_data = Conference._get_company_data_cached(instance.instance_id)
        
        # Render topic insights
        if topic_data:
            # Check if we have too many topics
            if len(topic_data) > 18:
                st.info(f"Showing top 18 topics out of {len(topic_data)} total topics")
            
            # Create and display the bar chart
            bar_chart = TopicVisualization.create_topic_bar_chart(
                topic_data, 
                instance.conference_name, 
                instance.year
            )
            
            if bar_chart:
                st.altair_chart(bar_chart, use_container_width=True)
            else:
                st.info("Could not create topic bar chart")
        else:
            st.info(f"No topic data available for {instance.conference_name} {instance.year}")
        
        # Render company insights
        if cloud_data:
            # Create a horizontal bar chart for cloud providers with companies on y-axis
            cloud_chart = CompanyVisualization.create_company_involvement_chart(
                cloud_data,
                CompanyMatcher.CLOUD_COMPANIES,
                "Cloud",
                instance.conference_name,
                instance.year,
                horizontal=True  # Use horizontal orientation with companies on y-axis
            )
            if cloud_chart:
                st.altair_chart(cloud_chart, use_container_width=True)
            else:
                st.info("No data available for cloud companies")
        else:
            st.info("No data available for cloud companies")
        
        if oem_data:
            oem_chart = CompanyVisualization.create_company_involvement_chart(
                oem_data,
                CompanyMatcher.OEM_COMPANIES,
                "OEM",
                instance.conference_name,
                instance.year,
                horizontal=False
            )
            if oem_chart:
                st.altair_chart(oem_chart, use_container_width=True)
            else:
                st.info("No data available for OEM companies")
        else:
            st.info("No data available for OEM companies")

    @staticmethod
    def _render_session_based_view(instance, session_data, date_labels, filter_options, 
                                on_date_select, on_session_select, theme_color):
        """Render the view for session-based conferences like GTC."""
        # Apply session styles
        ConferenceVisualization.apply_session_styles(theme_color)

        # Date selection buttons
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
        day_filter_options = filter_options[tab_idx]

        # Filter UI using the SessionFilterHandler
        selected_track, selected_time, selected_venue, selected_company, has_expert_opinion = SessionFilterHandler.render_filter_ui(
            day_filter_options, tab_idx
        )

        # Get filtered sessions
        filtered_sessions = SessionFilterHandler.apply_filters(
            day_data["sessions"],
            selected_track,
            selected_time,
            selected_venue,
            selected_company,
            has_expert_opinion
        )

        # Session list and details columns
        list_col, details_col = st.columns([1, 1.9])

        # Display session count or "No sessions" message outside the scrollable container
        with list_col:
            if not filtered_sessions:
                st.info("No sessions found for the selected filters.")
            else:
                st.markdown(f"{len(filtered_sessions)} session(s)", unsafe_allow_html=True)
            
            # Create a scrollable container for the session list only if we have sessions
            if filtered_sessions:
                with st.container(height=900):  # Increased height to show more sessions
                    # Add sessions to the container
                    for i, session in enumerate(filtered_sessions):
                        # Create a compact card for each session using the visualization utility
                        ConferenceVisualization.render_session_card(session)
                        
                        # Add a compact button
                        st.button(
                            "Details",  # Shorter button text
                            key=f"session_btn_{tab_idx}_{i}",
                            on_click=on_session_select,
                            args=(i,),
                            type="primary" if st.session_state.selected_session == i else "secondary",
                            use_container_width=True
                        )

        # Rest of the details column code
        with details_col:
            st.markdown("""
                <div style="height: 40px;"></div>
            """, unsafe_allow_html=True)
            if st.session_state.selected_session is not None and st.session_state.selected_session < len(filtered_sessions):
                selected_session = filtered_sessions[st.session_state.selected_session]
                
                # Render session details using the visualization utility
                ConferenceVisualization.render_session_details(selected_session, theme_color)

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
                if selected_session.get('ai_analysis') and selected_session['ai_analysis'] != 'nan':
                    ai_analysis = selected_session['ai_analysis']
                    if isinstance(ai_analysis, str) and ai_analysis.strip():
                        st.markdown('<div class="ai-interpretation-expander">', unsafe_allow_html=True)
                        with st.expander("🤖 AI解读"):
                            interpretation_list = [p.strip() for p in ai_analysis.split('\n') if p.strip()]
                            for interpretation in interpretation_list:
                                st.markdown(interpretation)
                        st.markdown('</div>', unsafe_allow_html=True)
    
    @staticmethod
    def render_instance(year: int, conference: str):
        """Render conference instance with session data and statistics."""
        # Ensure we preserve the current view
        st.session_state.filter_mode_menu = "Conference"
        st.session_state.selected_year = year
        st.session_state.selected_conference = conference
    
        # Initialize session states if not exists
        if "active_tab" not in st.session_state:
            st.session_state.active_tab = 0
        if "selected_session" not in st.session_state:
            st.session_state.selected_session = None

        # Define theme color
        theme_color = "#1f77b4"  # Default color

        # Callback functions for state updates
        def on_date_select(idx):
            st.session_state.active_tab = idx
            st.session_state.selected_session = None
            
        def on_session_select(idx):
            st.session_state.selected_session = idx
            
        # Get cached data
        data = Conference._prepare_instance_data(year, conference)
        if data is None:
            st.error(f"No conference instance found for {conference} {year}")
            return

        instance = data["instance"]
        session_data = data["session_data"]
        date_labels = data["date_labels"]
        filter_options = data["filter_options"]

        # Determine if this is a session-based conference (like GTC) or a paper-based academic conference
        is_session_based = Conference._is_session_based_conference(conference)
        
        # Create tabs for different views
        if is_session_based:
            tabs = st.tabs(["Session Catalog ", "Insights"])
        else:
            tabs = st.tabs(["Papers", "Statistics"])
        
        with tabs[0]:
            # Render conference header using the visualization utility
            ConferenceVisualization.render_conference_header(instance, theme_color)
            
            if is_session_based:
                # For session-based conferences like GTC
                Conference._render_session_based_view(
                    instance, session_data, date_labels, filter_options, 
                    on_date_select, on_session_select, theme_color
                )
            else:
                # For paper-based academic conferences
                Conference._render_paper_based_view(instance, year, conference)
        
        with tabs[1]:
            # Statistics or insights tab content
            if is_session_based:
                Conference._render_session_insights(instance)
            else:
                Conference._render_instance_statistics(year, conference, instance)

    @staticmethod
    def _is_session_based_conference(conference: str) -> bool:
        """Determine if a conference is session-based (like GTC) or paper-based."""
        # This could be based on a list of known session-based conferences
        # or by checking if there are sessions in the database
        session_based_conferences = ["GTC", "NVIDIA GTC", "GPU Technology Conference"]
        return conference in session_based_conferences


    @staticmethod
    def _render_paper_based_view(instance, year, conference):
        """Render the view for paper-based academic conferences."""
        # This would display paper information, authors, citations, etc.
        with DataManagerContext() as managers:
            papers = managers["paper"].get_papers_by_conference(conference, year)
            
            if not papers:
                st.info(f"No papers found for {conference} {year}")
                return
                
            # Display paper count
            st.metric("Total Papers", len(papers))
            
            # Create a dataframe with paper information
            papers_df = pd.DataFrame([
                {
                    "Title": paper.title,
                    "Authors": ", ".join([a.name for a in paper.author_to_paper]),
                    "Citations": paper.citation_count or 0,
                    "Year": paper.year
                }
                for paper in papers
            ])
            
            # Display the papers in a table
            st.dataframe(papers_df, use_container_width=True)
    