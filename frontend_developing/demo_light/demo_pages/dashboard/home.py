import streamlit as st
from utility.visualization_utli import ChartDisplay
import plotly.graph_objects as go

class Home:
    """Handles rendering of home page content."""

    def render_home():
        # Fake data for reports and podcasts
        fake_reports = [
            {
                'type': 'OpenAI',
                'title': 'The Rise of Large Language Models in Software Engineering'
            },
            {
                'type': 'Test-time Computing',
                'title': 'Impact of AI on Software Development Practices'
            },
            {
                'type': 'DeepSeek, DeepEP',
                'title': 'State of DevOps 2024'
            }
        ]

        fake_podcasts = [
            {
                'type': 'Tech Talk',
                'title': 'Future of Code Generation'
            },
            {
                'type': 'Interview Series',
                'title': 'Conversations with AI Researchers'
            },
            {
                'type': 'Panel Discussion',
                'title': 'Software Testing in the AI Era'
            }
        ]

        # Create two-column layout
        middle_col, right_col = st.columns([6, 3], gap="small")
        
        # Middle column with scrollable content
        with middle_col.container(height=820):
            report_col, podcast_col = st.columns([5,4])
            
            with report_col:
                st.subheader("Top Reports")
                for report in fake_reports:
                    st.markdown(f"""
                        <div style='
                            padding: 10px;
                            height: 100px;
                            margin: 5px 0;
                            border: 1px solid #ddd;
                            border-radius: 5px;
                            background-color: #f8f9fa;
                        '>
                            <div style='font-size: 0.9em; color: #1f77b4; font-weight: bold;'>{report['type']}</div>
                            <div style='font-size: 1.1em; font-weight: bold;'>{report['title']}</div>
                        </div>
                    """, unsafe_allow_html=True)
            
            with podcast_col:
                st.subheader("Top Podcasts")
                for podcast in fake_podcasts:
                    st.markdown(f"""
                        <div style='
                            padding: 10px;
                            height: 100px;
                            margin: 5px 0;
                            border: 1px solid #ddd;
                            border-radius: 5px;
                            background-color: #f8f9fa;
                        '>
                            <div style='font-size: 0.9em; color: #1f77b4; font-weight: bold;'>{podcast['type']}</div>
                            <div style='font-size: 1.1em; font-weight: bold;'>{podcast['title']}</div>
                        </div>
                    """, unsafe_allow_html=True)

        # Right column content remains unchanged
        with right_col.container(height=820):
            st.subheader("Recent Conferences")
            
            # Fake data for conferences timeline
            conference_timeline = [
                {
                    'name': 'ICSE 2024',
                    'date': 'Apr 14-20, 2024',
                    'location': 'Lisbon, Portugal',
                    'status': 'Happening Now'  # or None if not current
                },
                {
                    'name': 'FSE 2024',
                    'date': 'Jul 15-19, 2024',
                    'location': 'Porto, Portugal',
                    'status': None
                },
                {
                    'name': 'ASE 2024',
                    'date': 'Sep 23-27, 2024',
                    'location': 'Singapore',
                    'status': None
                },
                {
                    'name': 'ISSTA 2024',
                    'date': 'Jul 15-19, 2024',
                    'location': 'Vienna, Austria',
                    'status': None
                }
            ]

            for conf in conference_timeline:
                status_html = ""
                if conf['status'] == 'Happening Now':
                    status_html = """
                        <span style='
                            background-color: #2fb344;
                            color: white;
                            padding: 2px 8px;
                            border-radius: 12px;
                            font-size: 0.8em;
                            margin-left: 8px;
                        '>Happening Now</span>
                    """
                
                st.markdown(f"""
                    <div style='
                        padding: 8px;
                        margin: 5px 0;
                        border: 1px solid #ddd;
                        border-radius: 5px;
                        background-color: #f8f9fa;
                    '>
                        <div style='display: flex; justify-content: space-between;'>
                            <span style='font-weight: bold; color: #1f77b4;'>{conf['name']}{status_html}</span>
                            <span style='color: #666;'>{conf['date']}</span>
                        </div>
                        <div style='color: #888; font-size: 0.9em;'>{conf['location']}</div>
                    </div>
                """, unsafe_allow_html=True)

            # -------------------------- Research Trend Analysis ------------------------- #
            st.subheader("Hot Research Topics")
            trending_topics = {
                'Topic': ['LLMs', 'Testing', 'Security', 'DevOps', 'ML Systems'],
                'Growth': [85, 45, 30, 25, 20]
            }
            
            trend_fig = go.Figure()
            trend_fig.add_trace(go.Bar(
                x=trending_topics['Topic'],
                y=trending_topics['Growth'],
                marker_color='#1f77b4',
                text=[f'+{x}%' for x in trending_topics['Growth']],
                textposition='outside'
            ))
            trend_fig.update_layout(
                height=385,
                margin=dict(l=20, r=20, t=20, b=10),
                yaxis_title="Growth Rate (%)",
                plot_bgcolor='white',
                showlegend=False
            )
            st.plotly_chart(trend_fig, use_container_width=True)

            # ---------------------- Research Collaboration Network ---------------------- #
            st.subheader("Research Collaboration")
            
            # Fake data for collaboration metrics
            collab_data = {
                'metrics': [
                    {'name': 'Cross-Institution Papers', 'value': '45%', 'trend': '+5%'},
                    {'name': 'Industry-Academia', 'value': '38%', 'trend': '+8%'},
                    {'name': 'International Collaboration', 'value': '52%', 'trend': '+12%'}
                ]
            }

            for metric in collab_data['metrics']:
                st.markdown(f"""
                    <div style='
                        padding: 10px;
                        margin: 5px 0;
                        border: 1px solid #ddd;
                        border-radius: 5px;
                        background-color: #f8f9fa;
                    '>
                        <div style='display: flex; justify-content: space-between; align-items: center;'>
                            <span style='color: #444;'>{metric['name']}</span>
                            <div>
                                <span style='font-size: 1.2em; font-weight: bold; color: #1f77b4;'>{metric['value']}</span>
                                <span style='color: #2fb344; margin-left: 8px;'>{metric['trend']}</span>
                            </div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)