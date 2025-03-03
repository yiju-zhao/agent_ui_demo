import streamlit as st
from utility.db_util import DataManagerContext
import plotly.graph_objects as go
import networkx as nx
import pandas as pd

class Organization:
    """Handles rendering of organization-related content."""

    @staticmethod
    def render(organization: str):
        """Render organization-specific data."""
        # Updated fake data for specific organization
        org_stats = {
            'name': organization,
            'total_papers': 150,
            'total_citations': 2500,
            'top_authors': [
                {'name': 'John Smith', 'papers': 20, 'citations': 300},
                {'name': 'Jane Doe', 'papers': 15, 'citations': 250},
                {'name': 'Bob Johnson', 'papers': 12, 'citations': 200}
            ],
            'recent_papers': [
                {
                    'title': f'Research Paper {i}',
                    'authors': ['Author A', 'Author B'],
                    'year': 2024 - (i % 3),
                    'conference': ['ICSE', 'FSE', 'ASE'][i % 3],
                    'citations': 50 - (i * 2)
                } for i in range(10)
            ],
            'yearly_papers': {
                'years': [2019, 2020, 2021, 2022, 2023],
                'counts': [30, 35, 40, 45, 50],
                'areas': ['AI', 'ML', 'SE', 'DevOps', 'Security']
            },
            'keywords': [
                {'keyword': 'AI', 'count': 100},
                {'keyword': 'ML', 'count': 80},
                {'keyword': 'DevOps', 'count': 60}
            ],
            'authors_by_year': {
                'years': [2019, 2020, 2021, 2022, 2023],
                'chinese': [5, 6, 7, 8, 9],
                'non_chinese': [10, 12, 14, 16, 18]
            },
            'research_trends': {
                'years': [2019, 2020, 2021, 2022, 2023],
                'topics': {
                    'AI': [20, 25, 35, 45, 55],
                    'ML': [15, 20, 30, 40, 45],
                    'SE': [25, 28, 30, 32, 35],
                    'DevOps': [10, 15, 18, 20, 22],
                    'Security': [8, 12, 15, 18, 20]
                }
            },
            'buzzword_trends': {
                'years': [2019, 2020, 2021, 2022, 2023],
                'keywords': {
                    'LLM': [0, 5, 15, 35, 60],
                    'Neural Networks': [20, 25, 30, 35, 40],
                    'Cloud Computing': [15, 18, 20, 22, 25],
                    'DevOps': [10, 15, 20, 25, 30],
                    'Blockchain': [5, 8, 10, 12, 15]
                }
            }
            
        }

        st.header(f"Research Profile: {organization}")

        # ---------------------------------------------------------------------------- #
        #                         Key metrics and report cards                         #
        # ---------------------------------------------------------------------------- #
        # Key metrics and report cards
        col1, col2, col3 = st.columns([1, 1, 2])
        with col1:
            st.metric("Total Publications", org_stats['total_papers'])
        with col2:
            st.metric("Total Citations", org_stats['total_citations'])
        with col3:
            report_col1, report_col2 = st.columns(2)
            with report_col1:
                show_tech_report = st.button(
                    "隐藏技术线索",
                    key="tech_report",
                    use_container_width=True,
                    type="primary",
                )
                
                if show_tech_report:
                    with st.container():
                        st.subheader("Technical Report")
                        if st.button("Close", key="close_tech"):
                            st.empty()
                        else:
                            st.divider()
                            st.subheader("Key Findings")
                            st.markdown("""
                            1. Technology trend analysis
                            2. Core technology stack
                            3. Technical advantages
                            4. Development trajectory
                            """)
                            st.subheader("Detailed Analysis")
                            st.write("Your detailed report content here...")

            with report_col2:
                show_comp_analysis = st.button(
                    "技术竞争力分析",
                    key="comp_analysis",
                    use_container_width=True,
                    type="primary",
                )
                
                if show_comp_analysis:
                    with st.container():
                        st.subheader("Competitive Analysis")
                        if st.button("Close", key="close_comp"):
                            st.empty()
                        else:
                            st.divider()
                            st.subheader("Market Position")
                            st.markdown("""
                            1. Industry ranking
                            2. Technical advantages
                            3. Innovation capacity
                            4. Future potential
                            """)
                            st.subheader("Detailed Comparison")
                            st.write("Your detailed analysis content here...")

        # ---------------------------------------------------------------------------- #
        #                       Left column with tabs for charts                       #
        # ---------------------------------------------------------------------------- #
        left_col, right_col = st.columns([2, 1])
        with left_col:
            tab1, tab2, tab3, tab4 = st.tabs(["Paper Count by Year", "Author by Year", "Trend in Research Topic", "Trend in Buzzword"])
            
            with tab1:
                # ------------- Stacked bar chart showing research areas by year ------------- #
                fig = go.Figure()
                years = org_stats['yearly_papers']['years']
                areas = org_stats['yearly_papers']['areas']
                
                # Generate fake data for each area per year
                area_data = {
                    'AI': [10, 12, 15, 18, 20],
                    'ML': [8, 10, 12, 14, 15],
                    'SE': [5, 6, 7, 8, 9],
                    'DevOps': [4, 4, 3, 3, 4],
                    'Security': [3, 3, 3, 2, 2]
                }
                
                colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']
                for area, color in zip(areas, colors):
                    fig.add_trace(go.Bar(
                        name=area,
                        x=years,
                        y=area_data[area],
                        marker_color=color
                    ))
                
                fig.update_layout(
                    barmode='stack',
                    title="Paper Count by Year and Research Area",
                    xaxis_title="Year",
                    yaxis_title="Number of Papers",
                    legend_title="Research Areas"
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with tab2:
                # ------------------ Authors by year chart ------------------ #
                fig = go.Figure()
                fig.add_trace(go.Bar(
                    x=org_stats['authors_by_year']['years'],
                    y=org_stats['authors_by_year']['chinese'],
                    name='Chinese',
                    marker_color='red'
                ))
                fig.add_trace(go.Bar(
                    x=org_stats['authors_by_year']['years'],
                    y=org_stats['authors_by_year']['non_chinese'],
                    name='Non-Chinese',
                    marker_color='orange'
                ))
                fig.update_layout(
                    barmode='stack',
                    title="Authors by Year",
                    xaxis_title="Year",
                    yaxis_title="Number of Authors"
                )
                st.plotly_chart(fig, use_container_width=True)

            with tab3:
                # ------------------- Line chart for research topic trends ------------------- #
                fig = go.Figure()
                for topic, values in org_stats['research_trends']['topics'].items():
                    fig.add_trace(go.Scatter(
                        x=org_stats['research_trends']['years'],
                        y=values,
                        name=topic,
                        mode='lines+markers'
                    ))
                
                fig.update_layout(
                    title="Research Topic Trends",
                    xaxis_title="Year",
                    yaxis_title="Number of Papers",
                    hovermode='x unified',
                    legend=dict(
                        orientation="h",
                        yanchor="bottom",
                        y=1.02,
                        xanchor="right",
                        x=1
                    )
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with tab4:
                # ---------------------- Line chart for buzzword trends ---------------------- #
                fig = go.Figure()
                for keyword, values in org_stats['buzzword_trends']['keywords'].items():
                    fig.add_trace(go.Scatter(
                        x=org_stats['buzzword_trends']['years'],
                        y=values,
                        name=keyword,
                        mode='lines+markers'
                    ))
                
                fig.update_layout(
                    title="Buzzword Trends",
                    xaxis_title="Year",
                    yaxis_title="Number of Papers",
                    hovermode='x unified',
                    legend=dict(
                        orientation="h",
                        yanchor="bottom",
                        y=1.02,
                        xanchor="right",
                        x=1
                    )
                )
                st.plotly_chart(fig, use_container_width=True)
                

        # ---------------------------------------------------------------------------- #
        #         Right column with expandable sections for authors and papers         #
        # ---------------------------------------------------------------------------- #
        with right_col:
            tab1, tab2 = st.tabs(["Top Papers (recent 5 years)", "Top Authors (recent 5 years)"])
            with tab1:
                top_papers = sorted(org_stats['recent_papers'], key=lambda x: x['citations'], reverse=True)[:5]
                for paper in top_papers:
                    with st.expander(f"**{paper['title']}**"):
                        st.markdown(f"""
                            <div style='
                                padding: 10px;
                                background-color: #f8f9fa;
                                border-radius: 5px;
                            '>
                                <div style='margin-bottom: 8px;'>
                                    <span style='font-weight: bold; color: #666;'>Year:</span>
                                    <span style='color: #1f77b4;'> {paper['year']}</span>
                                </div>
                                <div style='margin-bottom: 8px;'>
                                    <span style='font-weight: bold; color: #666;'>Conference:</span>
                                    <span style='color: #1f77b4;'> {paper['conference']}</span>
                                </div>
                                <div style='margin-bottom: 8px;'>
                                    <span style='font-weight: bold; color: #666;'>Citations:</span>
                                    <span style='color: #1f77b4;'> {paper['citations']}</span>
                                </div>
                                <div>
                                    <span style='font-weight: bold; color: #666;'>Authors:</span>
                                    <span style='color: #1f77b4;'> {', '.join(paper['authors'])}</span>
                                </div>
                            </div>
                        """, unsafe_allow_html=True)
            with tab2:
                for author in org_stats['top_authors']:
                    with st.expander(f"**{author['name']}**"):
                        st.markdown(f"""
                            <div style='
                                padding: 10px;
                                background-color: #f8f9fa;
                                border-radius: 5px;
                            '>
                                <div style='display: flex; justify-content: space-between; margin-bottom: 10px;'>
                                    <span style='font-weight: bold; color: #666;'>Total Papers</span>
                                    <span style='color: #1f77b4;'>{author['papers']}</span>
                                </div>
                                <div style='display: flex; justify-content: space-between;'>
                                    <span style='font-weight: bold; color: #666;'>Citations</span>
                                    <span style='color: #1f77b4;'>{author['citations']}</span>
                                </div>
                            </div>
                        """, unsafe_allow_html=True)
            

    @staticmethod
    def render_overview():
        """Render overview of all organizations."""
        # Fake data for organization overview
        org_stats = {
            'total_orgs': 50,
            'total_publications': 5000,
            'most_active_org': 'Stanford University',
            'avg_papers_per_org': 100,
            'collaborations': {
                'nodes': [
                    {'id': 'Stanford University', 'papers': 500},
                    {'id': 'MIT', 'papers': 450},
                    {'id': 'Berkeley', 'papers': 400},
                    {'id': 'Carnegie Mellon', 'papers': 350},
                    {'id': 'Harvard', 'papers': 300}
                ],
                'edges': [
                    {'source': 'Stanford University', 'target': 'MIT', 'weight': 45},
                    {'source': 'MIT', 'target': 'Berkeley', 'weight': 30},
                    {'source': 'Berkeley', 'target': 'Carnegie Mellon', 'weight': 25},
                    {'source': 'Harvard', 'target': 'MIT', 'weight': 20}
                ]
            },
            'yearly_pubs': {
                'years': [2019, 2020, 2021, 2022, 2023],
                'publications': [800, 900, 1000, 1200, 1100],
                'citations': [1500, 1800, 2000, 2200, 2400]
            },
            'top_orgs': [
                {'name': 'Stanford University', 'papers': 500, 'citations': 8000},
                {'name': 'MIT', 'papers': 450, 'citations': 7500},
                {'name': 'Berkeley', 'papers': 400, 'citations': 7000},
                {'name': 'Carnegie Mellon', 'papers': 350, 'citations': 6500},
                {'name': 'Harvard', 'papers': 300, 'citations': 6000}
            ],
            'focus_areas': [
                {
                    'area': 'Software Engineering',
                    'papers': 2000,
                    'subareas': [
                        {'name': 'Testing', 'papers': 800},
                        {'name': 'DevOps', 'papers': 700},
                        {'name': 'Security', 'papers': 500}
                    ]
                },
                {
                    'area': 'AI/ML',
                    'papers': 1500,
                    'subareas': [
                        {'name': 'Deep Learning', 'papers': 600},
                        {'name': 'NLP', 'papers': 500},
                        {'name': 'Computer Vision', 'papers': 400}
                    ]
                }
            ]
        }

        # st.header("Research Organizations Overview")
        
        # Top metrics
        st.subheader("快速统计")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Organizations", org_stats['total_orgs'])
        with col2:
            st.metric("Total Publications", org_stats['total_publications'])
        with col3:
            st.metric("Avg Papers/Org", org_stats['avg_papers_per_org'])
        with col4:
            st.metric("Most Active Org", org_stats['most_active_org'])
            

        st.markdown("""---""")
        # Main content in two columns
        # st.subheader("Research Activity")
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
        left_col, right_col = st.columns([1,1])
        with left_col:
            # Organization collaboration network
            st.subheader("Collaboration Network")
            network_fig = Organization._create_collaboration_network(org_stats['collaborations'])
            st.plotly_chart(network_fig, use_container_width=True)
            
            # Publication trends
            st.subheader("Publication Trends")
            trend_fig = Organization._create_publication_trend(org_stats['yearly_pubs'])
            st.plotly_chart(trend_fig, use_container_width=True)
        
        with right_col:
            # Top 10 organizations
            st.subheader("Top Organizations")
            top_fig = Organization._create_top_orgs_chart(org_stats['top_orgs'])
            st.plotly_chart(top_fig, use_container_width=True)
            
            # Research focus areas
            st.subheader("Research Focus Areas")
            focus_fig = Organization._create_focus_areas_chart(org_stats['focus_areas'])
            st.plotly_chart(focus_fig, use_container_width=True)

    def _create_collaboration_network(collab_data):
        """Create organization collaboration network visualization."""
        G = nx.Graph()
        
        # Add nodes
        for node in collab_data['nodes']:
            G.add_node(node['id'], size=node['papers'])
        
        # Add edges
        for edge in collab_data['edges']:
            G.add_edge(edge['source'], edge['target'], weight=edge['weight'])
        
        # Calculate layout
        pos = nx.spring_layout(G, k=1, iterations=50)
        
        # Create edge traces
        edge_traces = []
        for edge in G.edges():
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            weight = G.edges[edge]['weight']
            
            edge_traces.append(
                go.Scatter(
                    x=[x0, x1, None],
                    y=[y0, y1, None],
                    mode='lines',
                    line=dict(width=weight/5, color='rgba(169, 169, 169, 0.5)'),
                    hoverinfo='none',
                    showlegend=False
                )
            )
        
        # Create node trace
        node_sizes = [G.nodes[node]['size'] for node in G.nodes()]
        max_size = max(node_sizes)
        
        node_trace = go.Scatter(
            x=[pos[node][0] for node in G.nodes()],
            y=[pos[node][1] for node in G.nodes()],
            mode='markers+text',
            text=list(G.nodes()),
            textposition='bottom center',
            hovertext=[f"{node}<br>Papers: {G.nodes[node]['size']}" for node in G.nodes()],
            marker=dict(
                size=[size/max_size * 50 + 20 for size in node_sizes],
                color='lightblue',
                line=dict(width=1, color='darkblue'),
                opacity=0.8
            ),
            textfont=dict(size=10),
            name='Organizations'
        )
        
        # Create figure
        fig = go.Figure(data=edge_traces + [node_trace])
        
        fig.update_layout(
            # title='Organization Collaboration Network',
            showlegend=False,
            hovermode='closest',
            margin=dict(b=20, l=5, r=5, t=40),
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            plot_bgcolor='white'
        )
        
        return fig

    def _create_publication_trend(trend_data):
        """Create publication trend chart."""
        fig = go.Figure()
        
        # Add publication trace
        fig.add_trace(
            go.Scatter(
                x=trend_data['years'],
                y=trend_data['publications'],
                name='Publications',
                mode='lines+markers',
                line=dict(color='blue', width=2),
                marker=dict(size=8)
            )
        )
        
        # Add citation trace on secondary y-axis
        fig.add_trace(
            go.Scatter(
                x=trend_data['years'],
                y=trend_data['citations'],
                name='Citations',
                mode='lines+markers',
                line=dict(color='red', width=2),
                marker=dict(size=8),
                yaxis='y2'
            )
        )
        
        # Update layout with correct property names
        fig.update_layout(
            # title={
            #     'text': 'Publication and Citation Trends',
            #     'x': 0.5,
            #     'xanchor': 'center'
            # },
            xaxis={
                'title': 'Year',
                'gridcolor': 'lightgray'
            },
            yaxis={
                'title': 'Number of Publications',
                'title_font': {'color': 'blue'},  # Changed from titlefont
                'tickfont': {'color': 'blue'},
                'gridcolor': 'lightgray'
            },
            yaxis2={
                'title': 'Number of Citations',
                'title_font': {'color': 'red'},  # Changed from titlefont
                'tickfont': {'color': 'red'},
                'overlaying': 'y',
                'side': 'right',
                'gridcolor': 'lightgray'
            },
            hovermode='x unified',
            legend={
                'orientation': 'h',
                'yanchor': 'bottom',
                'y': 1.02,
                'xanchor': 'right',
                'x': 1
            },
            plot_bgcolor='white',
            showlegend=True,
            margin={'t': 50, 'l': 50, 'r': 50, 'b': 50}
        )
        
        return fig

    def _create_top_orgs_chart(top_orgs_data):
        """Create top organizations bar chart."""
        fig = go.Figure()
        
        # Sort organizations by papers
        sorted_data = sorted(top_orgs_data, key=lambda x: x['papers'], reverse=True)[:10]
        
        fig.add_trace(
            go.Bar(
                x=[org['name'] for org in sorted_data],
                y=[org['papers'] for org in sorted_data],
                name='Papers',
                marker_color='lightblue',
                text=[org['papers'] for org in sorted_data],
                textposition='auto'
            )
        )
        
        fig.update_layout(
            # title='Top Organizations by Publications',
            xaxis=dict(
                title='Organization',
                tickangle=45,
                tickmode='linear'
            ),
            yaxis=dict(title='Number of Papers'),
            margin=dict(b=100),
            showlegend=False
        )
        
        return fig

    def _create_focus_areas_chart(focus_areas_data):
        """Create research focus areas treemap."""
        labels = []
        parents = []
        values = []
        
        for area in focus_areas_data:
            labels.append(area['area'])
            parents.append('')
            values.append(area['papers'])
            
            for subarea in area['subareas']:
                labels.append(subarea['name'])
                parents.append(area['area'])
                values.append(subarea['papers'])
        
        fig = go.Figure(
            go.Treemap(
                labels=labels,
                parents=parents,
                values=values,
                textinfo='label+value',
                marker=dict(
                    colors=['lightblue', 'skyblue', 'royalblue'] * len(focus_areas_data)
                )
            )
        )
        
        fig.update_layout(
            # title='Research Focus Areas',
            margin=dict(t=50, l=25, r=25, b=25)
        )
        
        return fig