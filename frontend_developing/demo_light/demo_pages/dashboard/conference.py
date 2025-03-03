import streamlit as st
from utility.db_util import (
    DataManagerContext,
    conference_stat_df,
    aggregate_stat_df,
)
from utility.visualization_utli import DashboardLayout
import plotly.graph_objects as go
import pandas as pd
import circlify

class Conference:
    """Handles rendering of conference-related content."""
    @staticmethod
    def render_overview():
        """Render overview of all conferences across years."""
        # Fake data for conference overview
        fake_data = {
            'summary_stats': {
                'total_conferences': 25,
                'total_papers': 45000,
                'total_years': 10,
                'avg_papers_per_year': 4500,
            },
            'yearly_stats': {
                'years': [2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023],
                'paper_counts': [3000, 3200, 3500, 3800, 4000, 4200, 4500, 4800, 5000, 5200],
                'conference_counts': [20, 20, 21, 22, 22, 23, 24, 24, 25, 25]
            },
            'research_focus': {
                'Software Testing & Verification': {
                    'description': 'Focus on testing methodologies, verification techniques, and quality assurance',
                    'conferences': ['ISSTA', 'ICSE', 'ASE', 'ISSRE']
                },
                'Program Analysis & Generation': {
                    'description': 'Research on code analysis, synthesis, and automated programming',
                    'conferences': ['FSE', 'ICSE', 'ASE', 'PLDI']
                },
                'Software Maintenance': {
                    'description': 'Studies on software evolution, maintenance, and legacy system modernization',
                    'conferences': ['ICSME', 'ICSE', 'SANER', 'MSR']
                },
                'Empirical Studies': {
                    'description': 'Evidence-based research and empirical methods in software engineering',
                    'conferences': ['ESEM', 'ICSE', 'FSE', 'MSR']
                },
                'AI/ML in Software Engineering': {
                    'description': 'Applications of AI and machine learning in software development',
                    'conferences': ['ICSE', 'FSE', 'ASE', 'MSR']
                }
            },
            'top_conferences': [
                {
                    'name': 'ICSE',
                    'full_name': 'International Conference on Software Engineering',
                    'intro': 'The premier software engineering conference, covering a wide range of topics from software development to maintenance and evolution.',
                    'total_papers': 5000,
                    'avg_citations': 25.5
                },
                {
                    'name': 'FSE',
                    'full_name': 'Foundations of Software Engineering',
                    'intro': 'A leading conference focusing on theoretical and practical aspects of software development, emphasizing innovative solutions to software engineering challenges.',
                    'total_papers': 4200,
                    'avg_citations': 23.8
                },
                {
                    'name': 'ASE',
                    'full_name': 'Automated Software Engineering',
                    'intro': 'Focuses on automated approaches to software development, testing, analysis, and maintenance, with emphasis on AI and machine learning applications.',
                    'total_papers': 3800,
                    'avg_citations': 22.1
                },
                {
                    'name': 'ISSTA',
                    'full_name': 'International Symposium on Software Testing and Analysis',
                    'intro': 'The primary conference for research in software testing and analysis, covering topics from test generation to program verification.',
                    'total_papers': 3500,
                    'avg_citations': 21.5
                },
                {
                    'name': 'ICSME',
                    'full_name': 'International Conference on Software Maintenance and Evolution',
                    'intro': 'Dedicated to advancing the state of the art in software maintenance, evolution, and reengineering of legacy systems.',
                    'total_papers': 3200,
                    'avg_citations': 20.2
                }
            ]
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
            st.metric("Total Conferences", fake_data['summary_stats']['total_conferences'])
        with col2:
            st.metric("Total Papers", f"{fake_data['summary_stats']['total_papers']:,}")
        with col3:
            st.metric("Years Covered", fake_data['summary_stats']['total_years'])
        with col4:
            st.metric("Avg Papers/Year", f"{fake_data['summary_stats']['avg_papers_per_year']:,}")

        # Create two columns for charts
        col_left, col_right = st.columns([1, 1])

        with col_left:
            # ------------------------- Top conferences overview ------------------------- #
            st.subheader("Top Conferences Overview")
            for conf in fake_data['top_conferences']:
                with st.expander(f"**{conf['name']} - {conf['full_name']}**"):
                    st.markdown(f"""
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
                    """, unsafe_allow_html=True)


        with col_right:
            # ------------------------- Conference research focus ------------------------ #
            st.subheader("Research Focus Areas")
            for focus, details in fake_data['research_focus'].items():
                with st.expander(f"**{focus}**"):
                    st.markdown(f"""
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
                    """, unsafe_allow_html=True)

        # st.subheader("Conference and Paper Trends")
        # ---------------------------- Yearly trends chart --------------------------- #
        yearly_fig = go.Figure()
        
        # Add papers trend
        yearly_fig.add_trace(
            go.Scatter(
                x=fake_data['yearly_stats']['years'],
                y=fake_data['yearly_stats']['paper_counts'],
                name='Papers',
                mode='lines+markers',
                line=dict(color='blue', width=2)
            )
        )
        
        # Add conferences trend on secondary y-axis
        yearly_fig.add_trace(
            go.Scatter(
                x=fake_data['yearly_stats']['years'],
                y=fake_data['yearly_stats']['conference_counts'],
                name='Conferences',
                mode='lines+markers',
                line=dict(color='red', width=2),
                yaxis='y2'
            )
        )
        
        yearly_fig.update_layout(
            title='Conference and Paper Trends',
            xaxis=dict(title='Year'),
            yaxis=dict(title='Number of Papers'),
            yaxis2=dict(
                title='Number of Conferences',
                overlaying='y',
                side='right'
            ),
            hovermode='x unified',
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )
        st.plotly_chart(yearly_fig, use_container_width=True)

        # Additional information or notes
        st.markdown("""
        > **Note:** This overview represents conference data across all tracked years. 
        Select a specific year from the sidebar for detailed annual statistics.
        """)

    @staticmethod
    def render_conference_overview(conference: str):
        """Render overview of all conferences."""
        # Fake data for conference trends
        fake_data = {
            'years': [2019, 2020, 2021, 2022, 2023],
            'keywords_trend': {
                'Large Language Models': [0, 5, 15, 45, 80],
                'Neural Networks': [50, 45, 40, 35, 30],
                'Transformer': [10, 20, 35, 50, 60],
                'Reinforcement Learning': [30, 35, 25, 20, 15],
                'AutoML': [40, 35, 30, 20, 10],
                'Prompt Engineering': [0, 0, 10, 30, 50],
                'Few-shot Learning': [5, 15, 25, 35, 40]
            },
            'companies_trend': {
                'Google Research': [20, 25, 30, 35, 40],
                'Microsoft Research': [18, 22, 25, 30, 35],
                'Meta AI': [0, 15, 20, 25, 30],
                'DeepMind': [15, 18, 20, 25, 28],
                'OpenAI': [0, 5, 15, 25, 35],
                'IBM Research': [25, 22, 20, 18, 15],
                'NVIDIA Research': [10, 15, 18, 20, 25]
            },
            'academic_trend': {
                'Stanford': [30, 35, 38, 40, 45],
                'MIT': [28, 32, 35, 38, 42],
                'Berkeley': [25, 28, 32, 35, 38],
                'CMU': [22, 25, 28, 32, 35],
                'Tsinghua': [20, 25, 30, 35, 40],
                'ETH Zurich': [18, 20, 25, 28, 30],
                'Oxford': [15, 18, 22, 25, 28]
            },
            'paper_counts': [350, 380, 420, 450, 500]
        }

        st.header(f"{conference} Overview")

        # Create two rows with two columns each
        row1_col1, row1_col2 = st.columns(2)
        row2_col1, row2_col2 = st.columns(2)

        common_layout = dict(
            height=550,
            margin=dict(l=50, r=50, t=50, b=20),  # Adjust margins
            plot_bgcolor='white',
            legend=dict(
                orientation="h",     # Horizontal legend
                yanchor="bottom",   # Place at bottom
                y=-0.4,            # Move below plot
                xanchor="center",   # Center horizontally
                x=0.5,
                bgcolor='rgba(255, 255, 255, 0.8)',  # Semi-transparent background
                bordercolor='rgba(0, 0, 0, 0.1)',    # Light border
                borderwidth=1
            ),
            xaxis=dict(
                showgrid=True,
                gridcolor='rgba(0, 0, 0, 0.1)'
            ),
            yaxis=dict(
                showgrid=True,
                gridcolor='rgba(0, 0, 0, 0.1)'
            )
        )

        with row1_col1:
            keywords_fig = go.Figure()
            for keyword, counts in fake_data['keywords_trend'].items():
                keywords_fig.add_trace(
                    go.Scatter(
                        x=fake_data['years'],
                        y=counts,
                        name=keyword,
                        mode='lines+markers'
                    )
                )
            keywords_fig.update_layout(
                title=dict(
                    text='Top Keywords Trend',
                    y=0.95
                ),
                xaxis_title='Year',
                yaxis_title='Number of Papers',
                **common_layout
            )
            st.plotly_chart(keywords_fig, use_container_width=True)

        # ------------------------------ Companies Trend ----------------------------- #
        with row1_col2:
            companies_fig = go.Figure()
            for company, counts in fake_data['companies_trend'].items():
                companies_fig.add_trace(
                    go.Scatter(
                        x=fake_data['years'],
                        y=counts,
                        name=company,
                        mode='lines+markers'
                    )
                )
            companies_fig.update_layout(
                title=dict(
                    text='Top Companies Contribution Trend',
                    y=0.95
                ),
                xaxis_title='Year',
                yaxis_title='Number of Papers',
                **common_layout
            )
            st.plotly_chart(companies_fig, use_container_width=True)

        # ------------------------ Academic Institutions Trend ----------------------- #
        with row2_col1:
            academic_fig = go.Figure()
            for inst, counts in fake_data['academic_trend'].items():
                academic_fig.add_trace(
                    go.Scatter(
                        x=fake_data['years'],
                        y=counts,
                        name=inst,
                        mode='lines+markers'
                    )
                )
            academic_fig.update_layout(
                title=dict(
                    text='Top Academic Institutions Trend',
                    y=0.95
                ),
                xaxis_title='Year',
                yaxis_title='Number of Papers',
                **common_layout
            )
            st.plotly_chart(academic_fig, use_container_width=True)

        # ----------------------------- Paper Count Trend ---------------------------- #
        with row2_col2:
            papers_fig = go.Figure()
            papers_fig.add_trace(
                go.Bar(
                    x=fake_data['years'],
                    y=fake_data['paper_counts'],
                    marker_color='rgb(55, 83, 109)'
                )
            )
            papers_fig.update_layout(
                title=dict(
                    text='Total Papers Published',
                    y=0.95
                ),
                xaxis_title='Year',
                yaxis_title='Number of Papers',
                height=400,
                margin=dict(l=50, r=50, t=50, b=50),
                plot_bgcolor='white',
                showlegend=False,
                xaxis=dict(
                    showgrid=True,
                    gridcolor='rgba(0, 0, 0, 0.1)'
                ),
                yaxis=dict(
                    showgrid=True,
                    gridcolor='rgba(0, 0, 0, 0.1)'
                )
            )
            st.plotly_chart(papers_fig, use_container_width=True)

        # Add spacing between rows
        st.markdown("<br>", unsafe_allow_html=True)

        # Additional conference information
        st.markdown(f"""
        > **Note:** This overview shows trends for {conference} over the past 5 years. 
        """)

    @staticmethod
    def render_year_overview(year: int):
        # Fake data
        fake_data = {
            'trending_keywords': [
                {'keyword': 'Large Language Models', 'count': 150, 'trend': '↑'},
                {'keyword': 'Prompt Engineering', 'count': 120, 'trend': '↑'},
                {'keyword': 'Neural Architecture', 'count': 100, 'trend': '→'},
                {'keyword': 'Transformer Models', 'count': 95, 'trend': '↑'},
                {'keyword': 'Federated Learning', 'count': 85, 'trend': '↑'},
                {'keyword': 'Edge Computing', 'count': 80, 'trend': '→'},
                {'keyword': 'Zero-shot Learning', 'count': 75, 'trend': '↑'},
                {'keyword': 'AutoML', 'count': 70, 'trend': '↓'},
                {'keyword': 'Knowledge Graphs', 'count': 65, 'trend': '→'},
                {'keyword': 'Quantum ML', 'count': 60, 'trend': '↑'}
            ],
            'academic_institutes': [
                {'name': 'Stanford University', 'papers': 120},
                {'name': 'MIT', 'papers': 110},
                {'name': 'UC Berkeley', 'papers': 95},
                {'name': 'Carnegie Mellon', 'papers': 90},
                {'name': 'ETH Zurich', 'papers': 85},
                {'name': 'Tsinghua University', 'papers': 80},
                {'name': 'University of Oxford', 'papers': 75},
                {'name': 'University of Cambridge', 'papers': 70},
                {'name': 'University of Toronto', 'papers': 65},
                {'name': 'TU Munich', 'papers': 60},
                {'name': 'Others', 'papers': 150}
            ],
            'companies': [
                {'name': 'Google Research', 'papers': 100},
                {'name': 'Microsoft Research', 'papers': 90},
                {'name': 'Meta AI', 'papers': 85},
                {'name': 'DeepMind', 'papers': 80},
                {'name': 'IBM Research', 'papers': 70},
                {'name': 'OpenAI', 'papers': 65},
                {'name': 'NVIDIA Research', 'papers': 60},
                {'name': 'Amazon Science', 'papers': 55},
                {'name': 'Anthropic', 'papers': 50},
                {'name': 'Huawei Research', 'papers': 45},
                {'name': 'Others', 'papers': 200}
            ],
            'conferences': [
                {'name': 'ICML 2024', 'date': 'Jul 21-27', 'papers': 1200},
                {'name': 'NeurIPS 2024', 'date': 'Dec 8-14', 'papers': 1150},
                {'name': 'ICLR 2024', 'date': 'May 7-11', 'papers': 1100},
                {'name': 'AAAI 2024', 'date': 'Feb 20-27', 'papers': 1000},
                {'name': 'ACL 2024', 'date': 'Aug 12-17', 'papers': 950},
                {'name': 'CVPR 2024', 'date': 'Jun 17-21', 'papers': 900},
                {'name': 'IJCAI 2024', 'date': 'Aug 3-9', 'papers': 850},
                {'name': 'ECCV 2024', 'date': 'Sep 29-Oct 4', 'papers': 800}
            ]
        }

        st.header("Conference Years Overview")

        # Create two columns for the layout
        left_col, right_col = st.columns([2,1])

        with left_col:
            # Trending Keywords (Top Left)
            st.subheader("Trending Research Topics")
            for keyword in fake_data['trending_keywords']:
                trend_color = {
                    '↑': 'green',
                    '↓': 'red',
                    '→': 'gray'
                }[keyword['trend']]
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
                    unsafe_allow_html=True
                )

            # Companies (Bottom Right)
            st.markdown("<br>", unsafe_allow_html=True)
            st.subheader("Top Industry Contributors")
            
            companies_fig = go.Figure(data=[go.Pie(
                labels=[company['name'] for company in fake_data['companies']],
                values=[company['papers'] for company in fake_data['companies']],
                hole=.3,
                textinfo='label+percent',
                textposition='outside',
                pull=[0.1 if company['name'] == 'Others' else 0 for company in fake_data['companies']]
            )])
            
            companies_fig.update_layout(
                showlegend=False,
                height=500,
                margin=dict(t=0, b=0, l=0, r=0)
            )
            
            st.plotly_chart(companies_fig, use_container_width=True)

            # Academic Institutes (Bottom Left)
            st.markdown("<br>", unsafe_allow_html=True)
            st.subheader("Top Academic Contributors")
            
            academic_fig = go.Figure(data=[go.Pie(
                labels=[inst['name'] for inst in fake_data['academic_institutes']],
                values=[inst['papers'] for inst in fake_data['academic_institutes']],
                hole=.3,
                textinfo='label+percent',
                textposition='outside',
                pull=[0.1 if inst['name'] == 'Others' else 0 for inst in fake_data['academic_institutes']]
            )])
            
            academic_fig.update_layout(
                title="Academic Institutions",
                showlegend=False,
                height=500,
                margin=dict(t=0, b=0, l=0, r=0)
            )
            
            st.plotly_chart(academic_fig, use_container_width=True)

        with right_col:
            # Conferences (Top Right)
            st.subheader(f"Conference in {year}")
            from datetime import datetime
            sorted_conferences = sorted(
                fake_data['conferences'],
                key=lambda x: datetime.strptime(x['date'].split('-')[0], '%b %d'),
                reverse=True
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
                    unsafe_allow_html=True
                )

    @staticmethod
    def render_instance(year: int, conference: str):
        """Render specific conference for a given year."""
        # Fake data for demonstration
        fake_data = {
            'keywords': [
                {'keyword': 'Large Language Models', 'count': 150},
                {'keyword': 'Transformer', 'count': 120},
                {'keyword': 'Neural Networks', 'count': 100},
                {'keyword': 'Reinforcement Learning', 'count': 85},
                {'keyword': 'Few-shot Learning', 'count': 75},
                {'keyword': 'Prompt Engineering', 'count': 70},
                {'keyword': 'Computer Vision', 'count': 65},
                {'keyword': 'NLP', 'count': 60},
                {'keyword': 'Graph Neural Networks', 'count': 55},
                {'keyword': 'Federated Learning', 'count': 50}
            ],
            'organizations': [
                {'name': 'Google AI', 'papers': 45, 'citations': 1200},
                {'name': 'Microsoft Research', 'papers': 40, 'citations': 1100},
                {'name': 'Stanford', 'papers': 35, 'citations': 950},
                {'name': 'MIT', 'papers': 32, 'citations': 900},
                {'name': 'Berkeley', 'papers': 30, 'citations': 850},
                {'name': 'OpenAI', 'papers': 28, 'citations': 800},
                {'name': 'DeepMind', 'papers': 25, 'citations': 750},
                {'name': 'CMU', 'papers': 22, 'citations': 700},
                {'name': 'Meta AI', 'papers': 20, 'citations': 650},
                {'name': 'Tsinghua', 'papers': 18, 'citations': 600}
            ],
            'paper_types': {
                'Oral': 150,
                'Spotlight': 300,
                'Poster': 750
            },
            'research_areas': {
                'Machine Learning': 400,
                'Computer Vision': 250,
                'Natural Language Processing': 200,
                'Robotics': 150,
                'Systems': 100,
                'Theory': 100
            },
            'award_papers': [
                {
                    'title': 'Advancing Large Language Models through Neural Architecture Search',
                    'authors': 'John Smith, Jane Doe, et al.',
                    'award': 'Best Paper Award',
                    'institution': 'Google Research'
                },
                {
                    'title': 'Novel Approaches to Few-shot Learning in Vision Transformers',
                    'authors': 'Alice Johnson, Bob Wilson, et al.',
                    'award': 'Best Paper Runner-up',
                    'institution': 'Stanford University'
                },
                {
                    'title': 'Efficient Training of Large Neural Networks',
                    'authors': 'David Brown, Sarah Miller, et al.',
                    'award': 'Outstanding Paper Award',
                    'institution': 'MIT'
                }
            ],
            'top_research': [
                {
                    'title': 'Breakthrough in Self-Supervised Learning',
                    'authors': 'Research Team A',
                    'institution': 'DeepMind',
                    'impact': 'Revolutionary approach to unsupervised learning'
                },
                {
                    'title': 'Novel Transformer Architecture for Vision Tasks',
                    'authors': 'Research Team B',
                    'institution': 'Microsoft Research',
                    'impact': 'Significant improvement in vision tasks'
                },
                {
                    'title': 'Efficient Large Language Model Training',
                    'authors': 'Research Team C',
                    'institution': 'OpenAI',
                    'impact': '10x reduction in training time'
                }
            ]
        }

        st.header(f"{conference} {year} Analysis")

        # Create main columns
        left_col, right_col = st.columns([2, 1])

        with left_col:
            # ----------------------- Keywords Horizontal Bar Chart ---------------------- #
            st.subheader("Top Keywords")
            keywords_fig = go.Figure()
            sorted_keywords = sorted(fake_data['keywords'], key=lambda x: x['count'], reverse=True)
            keywords_fig.add_trace(go.Bar(
                x=[k['count'] for k in sorted_keywords],
                y=[k['keyword'] for k in sorted_keywords],
                orientation='h',
                marker_color='rgb(55, 83, 109)'
            ))
            keywords_fig.update_layout(
                height=400,
                margin=dict(l=20, r=20, t=20, b=20),
                xaxis_title="Number of Papers",
                plot_bgcolor='white',
                yaxis=dict(autorange="reversed")
            )
            st.plotly_chart(keywords_fig, use_container_width=True)

            # ------------------------- Paper Types Distribution ------------------------- #
            col1, col2 = st.columns([2,3])
            with col1:
                st.subheader("Venue Types Distribution")
                types_fig = go.Figure(data=[go.Pie(
                    labels=list(fake_data['paper_types'].keys()),
                    values=list(fake_data['paper_types'].values()),
                    hole=.3
                )])
                types_fig.update_layout(height=300, margin=dict(l=20, r=20, t=20, b=20))
                st.plotly_chart(types_fig, use_container_width=True)

            # ------------------------ Research Areas Distribution ----------------------- #
            with col2:
                st.subheader("Research Areas")
                areas_fig = go.Figure(data=[go.Pie(
                    labels=list(fake_data['research_areas'].keys()),
                    values=list(fake_data['research_areas'].values()),
                    hole=.3
                )])
                areas_fig.update_layout(height=300, margin=dict(l=20, r=20, t=20, b=20))
                st.plotly_chart(areas_fig, use_container_width=True)

            # ------------------------ Organizations Bubble Chart ------------------------ #
            values = [org['papers'] for org in fake_data['organizations']]
            circles = circlify.circlify(
                values, 
                show_enclosure=False, 
                target_enclosure=circlify.Circle(x=0, y=0, r=1)
            )

            # Prepare lists for plotting.
            x_values, y_values, sizes, texts = [], [], [], []
            colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']

            # Map the circle packing positions to our plot.
            for org, circle in zip(fake_data['organizations'], circles):
                x_values.append(circle.x)
                y_values.append(circle.y)
                # Marker size is derived from the circle radius. Adjust the scale factor as needed.
                sizes.append(circle.r * 200)
                texts.append(org['name'])

            # Create the compact (packed) bubble chart.
            bubble_fig = go.Figure()

            bubble_fig.add_trace(go.Scatter(
                x=x_values,
                y=y_values,
                mode='markers+text',
                marker=dict(
                    size=sizes,
                    sizemode='diameter',
                    color=colors[:len(x_values)]
                ),
                text=texts,
                textposition="middle center"
            ))

            # Remove axis clutter for a cleaner look.
            bubble_fig.update_layout(
                height=400,
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                plot_bgcolor='white',
                margin=dict(l=20, r=20, t=20, b=20)
            )

            st.subheader("Top Organizations Contribution")
            st.plotly_chart(bubble_fig, use_container_width=True)

        with right_col:
            # -------------------------- Top Research Highlights ------------------------- #
            st.subheader("Top Research Highlights")
            for research in fake_data['top_research']:
                st.markdown(f"""
                    <div style='
                        padding: 15px;
                        margin: 10px 0;
                        border: 1px solid #ddd;
                        border-radius: 5px;
                        background-color: #ffffff;
                    '>
                        <div style='font-weight: bold;'>{research['title']}</div>
                        <div style='color: #666;'>{research['authors']}</div>
                        <div style='color: #888;'>{research['institution']}</div>
                        <div style='
                            margin-top: 8px;
                            padding: 8px;
                            background-color: #f8f9fa;
                            border-radius: 3px;
                            font-style: italic;
                        '>{research['impact']}</div>
                    </div>
                """, unsafe_allow_html=True)
            
            # ------------------------------- Award Papers ------------------------------- #
            st.subheader("Award Winning Papers")
            for paper in fake_data['award_papers']:
                st.markdown(f"""
                    <div style='
                        padding: 10px;
                        margin: 5px 0;
                        border: 1px solid #ddd;
                        border-radius: 5px;
                        background-color: #f8f9fa;
                    '>
                        <div style='color: #1f77b4; font-weight: bold;'>{paper['award']}</div>
                        <div style='font-weight: bold;'>{paper['title']}</div>
                        <div style='color: #666;'>{paper['authors']}</div>
                        <div style='color: #888; font-style: italic;'>{paper['institution']}</div>
                    </div>
                """, unsafe_allow_html=True)
