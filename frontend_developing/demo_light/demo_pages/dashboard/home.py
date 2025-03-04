import streamlit as st
from utility.visualization_utli import ChartDisplay
import plotly.graph_objects as go


class Home:
    """Handles rendering of home page content."""

    def render_home():
        # Fake data for reports and podcasts

        if "show_report_details" not in st.session_state:
            st.session_state.show_report_details = None

        fake_reports = [
            {
                "type": "Code Transformation",
                "title": "Don't Transform the Code, Code the Transforms",
                "abstract": """The key innovation is the chain-of-thought process, where the model generates natural language descriptions, performs iterative refinement, and synthesizes transformations through a feedback loop.""",
                "methodology": [
                    "Generates a Natural Language Description",
                    "Performs Iterative Refinement",
                    "Synthesizes the Transform",
                    "Executes and Provides Feedback",
                ],
                "results": "The approach shows significant improvements in code transformation accuracy...",
                "image_path": "demo_pages/test_markdown_diagram.png",  # Add image path if available
            },
            {
                "type": "Test-time Computing",
                "title": "Impact of AI on Software Development Practices",
                "abstract": "This study explores how artificial intelligence is reshaping modern software development practices and methodologies.",
                "methodology": [
                    "Data Collection from Industry",
                    "Analysis of Development Patterns",
                    "Impact Assessment",
                    "Future Trends Prediction",
                ],
                "results": "Significant improvements in development efficiency and code quality...",
            },
            {
                "type": "DeepSeek, DeepEP",
                "title": "State of DevOps 2024",
                "abstract": "A comprehensive analysis of DevOps practices and their evolution in 2024.",
                "methodology": [
                    "Industry Survey",
                    "Performance Metrics Analysis",
                    "Best Practices Compilation",
                ],
                "results": "DevOps adoption continues to grow with emerging AI integration...",
            },
        ]
        fake_podcasts = [
            {
                "type": "Paper Discussion",
                "title": "Don't Transform the Code, Code the Transforms",
                "audio_path": "demo_pages/Don't Transform the Code, Code the Transforms.mp3",
            },
            {"type": "Interview Series", "title": "Conversations with AI Researchers"},
            {"type": "Panel Discussion", "title": "Software Testing in the AI Era"},
        ]

        middle_col, right_col = st.columns([7, 3], gap="small")

        with middle_col:
            report_col, podcast_col = st.columns([5, 4])

            with report_col:
                st.subheader("Top Reports")

                for i, report in enumerate(fake_reports):
                    # Report preview with expander
                    with st.expander(f"**{report['title']}**", expanded=False):
                        # Report header
                        st.markdown(
                            f"""
                            <div style="
                                margin-bottom: 15px;
                                padding-bottom: 10px;
                                border-bottom: 1px solid #eee;
                            ">
                                <div style="font-size: 0.9em; color: #1f77b4; font-weight: bold; margin-bottom: 5px;">
                                    {report['type']}
                                </div>
                                <div style="font-size: 0.95em; color: #666;">
                                    {report['abstract']}
                                </div>
                            </div>
                        """,
                            unsafe_allow_html=True,
                        )

                        # Methodology section
                        st.markdown("#### Methodology")
                        for step in report["methodology"]:
                            st.markdown(f"- {step}")

                        # Results section
                        st.markdown("#### Results")
                        st.markdown(report["results"])

                        # Image if available
                        if "image_path" in report:
                            try:
                                st.image(
                                    report["image_path"], caption="Methodology Diagram"
                                )
                            except:
                                st.warning("Image not available")

                        # Share button at the bottom
                        st.markdown(
                            """
                            <div style="display: flex; justify-content: flex-end; margin-top: 15px;">
                                <button style="
                                    padding: 5px 15px;
                                    border-radius: 5px;
                                    border: 1px solid #ddd;
                                    cursor: pointer;
                                    background-color: #f8f9fa;
                                    color: #1f77b4;
                                ">
                                    Share
                                </button>
                            </div>
                        """,
                            unsafe_allow_html=True,
                        )

            with podcast_col:
                st.subheader("Top Podcasts")
                for podcast in fake_podcasts:
                    with st.expander(podcast["title"]):
                        st.markdown(f"**Type:** {podcast['type']}")
                        if "audio_path" in podcast:
                            try:
                                audio_file = open(podcast["audio_path"], "rb")
                                audio_bytes = audio_file.read()
                                st.audio(audio_bytes, format="audio/mp3")
                            except Exception as e:
                                st.error(f"Audio file not found: {e}")

        # Right column content remains unchanged
        with right_col.container(height=820):
            st.subheader("Recent Conferences")

            # Fake data for conferences timeline
            conference_timeline = [
                {
                    "name": "ICSE 2024",
                    "date": "Apr 14-20, 2024",
                    "location": "Lisbon, Portugal",
                    "status": "Happening Now",  # or None if not current
                },
                {
                    "name": "FSE 2024",
                    "date": "Jul 15-19, 2024",
                    "location": "Porto, Portugal",
                    "status": None,
                },
                {
                    "name": "ASE 2024",
                    "date": "Sep 23-27, 2024",
                    "location": "Singapore",
                    "status": None,
                },
                {
                    "name": "ISSTA 2024",
                    "date": "Jul 15-19, 2024",
                    "location": "Vienna, Austria",
                    "status": None,
                },
            ]

            for conf in conference_timeline:
                status_html = ""
                if conf["status"] == "Happening Now":
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

                st.markdown(
                    f"""
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
                """,
                    unsafe_allow_html=True,
                )

            # -------------------------- Research Trend Analysis ------------------------- #
            st.subheader("Hot Research Topics")
            trending_topics = {
                "Topic": ["LLMs", "Testing", "Security", "DevOps", "ML Systems"],
                "Growth": [85, 45, 30, 25, 20],
            }

            trend_fig = go.Figure()
            trend_fig.add_trace(
                go.Bar(
                    x=trending_topics["Topic"],
                    y=trending_topics["Growth"],
                    marker_color="#1f77b4",
                    text=[f"+{x}%" for x in trending_topics["Growth"]],
                    textposition="outside",
                )
            )
            trend_fig.update_layout(
                height=385,
                margin=dict(l=20, r=20, t=20, b=10),
                yaxis_title="Growth Rate (%)",
                plot_bgcolor="white",
                showlegend=False,
            )
            st.plotly_chart(trend_fig, use_container_width=True)

            # ---------------------- Research Collaboration Network ---------------------- #
            st.subheader("Research Collaboration")

            # Fake data for collaboration metrics
            collab_data = {
                "metrics": [
                    {
                        "name": "Cross-Institution Papers",
                        "value": "45%",
                        "trend": "+5%",
                    },
                    {"name": "Industry-Academia", "value": "38%", "trend": "+8%"},
                    {
                        "name": "International Collaboration",
                        "value": "52%",
                        "trend": "+12%",
                    },
                ]
            }

            for metric in collab_data["metrics"]:
                st.markdown(
                    f"""
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
                """,
                    unsafe_allow_html=True,
                )
