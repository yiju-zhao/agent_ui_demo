import streamlit as st
from utility.db_util import DataManagerContext
from utility.visualization_utli import DashboardLayout
import networkx as nx
import plotly.graph_objects as go


class Keyword:
    """Handles rendering of keyword-related content."""

    @staticmethod
    def render(keyword: str):
        """Render keyword-specific data."""
        # Fake data for demonstration
        fake_papers = [
            {
                "title": f"Paper about {keyword} #{i}",
                "authors": ["Author A", "Author B"],
                "year": 2023 - (i % 3),
                "conference": ["ICSE", "FSE", "ASE"][i % 3],
                "citations": 50 - (i * 2),
                "abstract": f"This is a research paper about {keyword} and its applications...",
            }
            for i in range(10)
        ]

        fake_related_keywords = [
            {"keyword": f"related_{keyword}_{i}", "papers": 20 - i} for i in range(5)
        ]

        DashboardLayout.show_keyword_layout(fake_papers, keyword, fake_related_keywords)

    @staticmethod
    def render_overview():
        """Render overview of all keywords and trends."""
        # st.header("Research Topics & Trends")

        # Fake keyword statistics
        keyword_stats = {
            "keywords": [
                "machine learning",
                "deep learning",
                "neural networks",
                "computer vision",
                "NLP",
                "software testing",
                "cloud computing",
                "agile development",
            ],
            "trending": ["machine learning", "deep learning", "computer vision"],
            "new_keywords": 5,
            "hottest_topic": "machine learning",
            "trends": {
                "machine learning": {
                    "years": [2021, 2022, 2023],
                    "counts": [80, 90, 100],
                },
                "deep learning": {"years": [2021, 2022, 2023], "counts": [60, 70, 80]},
                "neural networks": {
                    "years": [2021, 2022, 2023],
                    "counts": [55, 60, 60],
                },
            },
            "connections": {
                "nodes": [
                    {"id": "machine learning", "papers": 150},
                    {"id": "deep learning", "papers": 120},
                    {"id": "neural networks", "papers": 100},
                    {"id": "computer vision", "papers": 90},
                    {"id": "natural language processing", "papers": 85},
                ],
                "edges": [
                    {
                        "source": "machine learning",
                        "target": "deep learning",
                        "weight": 45,
                    },
                    {
                        "source": "deep learning",
                        "target": "neural networks",
                        "weight": 30,
                    },
                    {
                        "source": "computer vision",
                        "target": "deep learning",
                        "weight": 25,
                    },
                    {
                        "source": "natural language processing",
                        "target": "deep learning",
                        "weight": 20,
                    },
                ],
            },
            "yearly_top": {
                2023: [
                    {"keyword": "machine learning", "count": 100, "trend": "↑"},
                    {"keyword": "deep learning", "count": 80, "trend": "↑"},
                    {"keyword": "neural networks", "count": 60, "trend": "→"},
                    {"keyword": "computer vision", "count": 50, "trend": "↑"},
                    {"keyword": "NLP", "count": 45, "trend": "↑"},
                ],
                2022: [
                    {"keyword": "machine learning", "count": 90, "trend": "↑"},
                    {"keyword": "deep learning", "count": 70, "trend": "↑"},
                    {"keyword": "neural networks", "count": 60, "trend": "→"},
                    {"keyword": "software testing", "count": 40, "trend": "↓"},
                    {"keyword": "agile development", "count": 35, "trend": "→"},
                ],
                2021: [
                    {"keyword": "machine learning", "count": 80, "trend": "↑"},
                    {"keyword": "deep learning", "count": 60, "trend": "↑"},
                    {"keyword": "neural networks", "count": 55, "trend": "→"},
                    {"keyword": "software testing", "count": 45, "trend": "→"},
                    {"keyword": "cloud computing", "count": 40, "trend": "↓"},
                ],
            },
            "top_pairs": [
                ("machine learning", "deep learning"),
                ("deep learning", "neural networks"),
                ("computer vision", "deep learning"),
                ("NLP", "machine learning"),
                ("neural networks", "computer vision"),
            ],
            "growth_rates": [
                {"keyword": "machine learning", "growth_rate": 25},
                {"keyword": "deep learning", "growth_rate": 33},
                {"keyword": "computer vision", "growth_rate": 20},
                {"keyword": "NLP", "growth_rate": 15},
                {"keyword": "cloud computing", "growth_rate": 10},
            ],
            "emerging": [
                {"name": "Transformer Models", "growth_rate": 150, "first_seen": 2021},
                {"name": "Few-shot Learning", "growth_rate": 120, "first_seen": 2021},
                {
                    "name": "Graph Neural Networks",
                    "growth_rate": 90,
                    "first_seen": 2022,
                },
            ],
        }

        # Top metrics
        st.subheader("Quick Statistics")
        col1, col2, col3, col4 = st.columns(4)
        # Custom CSS for smaller metric font sizes
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
        with col1:
            st.metric("Total Keywords", len(keyword_stats["keywords"]))
        with col2:
            st.metric("Trending Topics", len(keyword_stats["trending"]))
        with col3:
            st.metric("New This Year", keyword_stats["new_keywords"])
        with col4:
            st.metric("Hot Topic", keyword_stats["hottest_topic"])

        # Main content in tabs
        tab1, tab2 = st.tabs(["Topic Trends", "Emerging Topics"])

        with tab1:
            st.subheader("Research Topic Trends")
            trend_fig = Keyword._create_trend_chart(keyword_stats["trends"])
            st.plotly_chart(trend_fig, use_container_width=True)

        with tab2:
            st.subheader("Emerging Research Topics")
            trend_col, detail_col = st.columns([2, 1])

            with trend_col:
                growth_fig = Keyword._create_growth_chart(keyword_stats["growth_rates"])
                st.plotly_chart(growth_fig, use_container_width=True)

            with detail_col:
                st.markdown("#### Fast-Growing Topics")
                for topic in keyword_stats["emerging"]:
                    st.markdown(
                        f"""
                        <div style='border:1px solid #ddd; 
                                border-radius:5px; 
                                padding:10px; 
                                margin:5px;'>
                            <h5>{topic['name']}</h5>
                            <p>Growth Rate: {topic['growth_rate']}%</p>
                            <p>First Appeared: {topic['first_seen']}</p>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

    @staticmethod
    def _create_trend_chart(trend_data):
        """Create line chart for keyword trends over time."""
        # Create figure
        fig = go.Figure()

        # Color palette for different lines
        colors = [
            "rgb(31, 119, 180)",
            "rgb(255, 127, 14)",
            "rgb(44, 160, 44)",
            "rgb(214, 39, 40)",
        ]

        # Add trace for each keyword
        for idx, (keyword, data) in enumerate(trend_data.items()):
            fig.add_trace(
                go.Scatter(
                    x=data["years"],
                    y=data["counts"],
                    name=keyword,
                    mode="lines+markers",
                    line=dict(color=colors[idx % len(colors)], width=2),
                    marker=dict(size=8, symbol="circle"),
                    hovertemplate=(
                        f"<b>{keyword}</b><br>"
                        + "Year: %{x}<br>"
                        + "Papers: %{y}<br>"
                        + "<extra></extra>"
                    ),
                )
            )

        # Update layout
        fig.update_layout(
            title=dict(text="Research Topic Trends Over Time", x=0.5, xanchor="center"),
            xaxis=dict(
                title="Year", tickmode="linear", gridcolor="rgba(211, 211, 211, 0.3)"
            ),
            yaxis=dict(title="Number of Papers", gridcolor="rgba(211, 211, 211, 0.3)"),
            hovermode="x unified",
            plot_bgcolor="white",
            showlegend=True,
            legend=dict(
                yanchor="top",
                y=0.99,
                xanchor="left",
                x=0.01,
                bgcolor="rgba(255, 255, 255, 0.8)",
            ),
            margin=dict(t=50, l=50, r=50, b=50),
        )

        return fig

    # @staticmethod
    # def _create_keyword_network(connection_data):
    #     """Create network visualization of keyword relationships."""
    #     # Create network graph
    #     G = nx.Graph()

    #     # Add nodes
    #     for node in connection_data['nodes']:
    #         G.add_node(node['id'], size=node['papers'])

    #     # Add edges
    #     for edge in connection_data['edges']:
    #         G.add_edge(edge['source'], edge['target'], weight=edge['weight'])

    #     # Calculate layout
    #     pos = nx.spring_layout(G, k=1, iterations=50)

    #     # Create edge traces
    #     edge_traces = []
    #     for edge in G.edges():
    #         x0, y0 = pos[edge[0]]
    #         x1, y1 = pos[edge[1]]
    #         weight = G.edges[edge]['weight']

    #         # Add edge trace
    #         edge_traces.append(
    #             go.Scatter(
    #                 x=[x0, x1, None],
    #                 y=[y0, y1, None],
    #                 mode='lines',
    #                 line=dict(
    #                     width=weight/5,  # Scale weight for visualization
    #                     color='rgba(169, 169, 169, 0.5)'
    #                 ),
    #                 hoverinfo='none',
    #                 showlegend=False
    #             )
    #         )

    #     # Create node trace
    #     node_sizes = [G.nodes[node]['size'] for node in G.nodes()]
    #     max_size = max(node_sizes)

    #     node_trace = go.Scatter(
    #         x=[pos[node][0] for node in G.nodes()],
    #         y=[pos[node][1] for node in G.nodes()],
    #         mode='markers+text',
    #         text=list(G.nodes()),
    #         textposition='bottom center',
    #         hovertext=[f"{node}<br>Papers: {G.nodes[node]['size']}" for node in G.nodes()],
    #         marker=dict(
    #             size=[size/max_size * 50 + 20 for size in node_sizes],  # Normalize sizes
    #             color='lightblue',
    #             line=dict(width=1, color='darkblue'),
    #             opacity=0.8
    #         ),
    #         textfont=dict(size=10),
    #         name='Keywords'
    #     )

    #     # Create figure
    #     fig = go.Figure(data=edge_traces + [node_trace])

    #     # Update layout
    #     fig.update_layout(
    #         title=dict(
    #             text='Keyword Co-occurrence Network',
    #             x=0.5,
    #             xanchor='center'
    #         ),
    #         showlegend=False,
    #         hovermode='closest',
    #         margin=dict(b=20, l=5, r=5, t=40),
    #         xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
    #         yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
    #         plot_bgcolor='white',
    #         width=800,
    #         height=600
    #     )

    #     return fig

    @staticmethod
    def _create_growth_chart(growth_data):
        """Create visualization for keyword growth rates."""
        # Sort data by growth rate
        sorted_data = sorted(growth_data, key=lambda x: x["growth_rate"], reverse=True)

        # Create figure
        fig = go.Figure()

        # Add bar trace
        fig.add_trace(
            go.Bar(
                x=[d["keyword"] for d in sorted_data],
                y=[d["growth_rate"] for d in sorted_data],
                text=[f"{d['growth_rate']}%" for d in sorted_data],
                textposition="auto",
                marker_color=[
                    (
                        "rgba(44, 160, 44, 0.7)"
                        if rate["growth_rate"] > 20
                        else "rgba(31, 119, 180, 0.7)"
                    )
                    for rate in sorted_data
                ],
                hovertemplate=(
                    "<b>%{x}</b><br>" + "Growth Rate: %{y}%<br>" + "<extra></extra>"
                ),
            )
        )

        # Update layout
        fig.update_layout(
            title=dict(text="Topic Growth Rates", x=0.5, xanchor="center"),
            xaxis=dict(title="Keywords", tickangle=45, tickmode="linear"),
            yaxis=dict(title="Growth Rate (%)", gridcolor="rgba(211, 211, 211, 0.3)"),
            plot_bgcolor="white",
            showlegend=False,
            margin=dict(
                t=50, l=50, r=50, b=100
            ),  # Increased bottom margin for rotated labels
        )

        return fig
