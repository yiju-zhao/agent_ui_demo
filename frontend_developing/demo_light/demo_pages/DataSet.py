import streamlit as st
import pandas as pd
from datetime import datetime
from streamlit_option_menu import option_menu


paper_data = [
    {
        "title": "Large Language Models in Scientific Discovery",
        "authors": "John Smith, Mary Brown",
        "affiliation": "Stanford University",
        "conference": "NeurIPS",
        "year": 2024,
        "citations": 45,
        "abstract": "This paper explores the application of large language models in scientific research...",
        "keywords": ["LLM", "Scientific Discovery", "AI"],
        "pdf_link": "[PDF](#)",
        "code_link": "https://github.com/example/llm-science",
        "methodology": [
            "Data collection from scientific papers",
            "Fine-tuning LLMs on scientific corpus",
            "Evaluation on discovery tasks"
        ],
        "results": "Achieved 85% accuracy in predicting scientific outcomes..."
    },
    {
        "title": "Neural Network Architecture Search",
        "authors": "Rachel Williams",
        "affiliation": "MIT",
        "conference": "ICML",
        "year": 2023,
        "citations": 89,
        "abstract": "A novel approach to automated neural architecture search...",
        "keywords": ["Neural Architecture", "AutoML", "Optimization"],
        "pdf_link": "[PDF](#)",
        "code_link": "https://github.com/example/neural-arch"
    },
    {
        "title": "Reinforcement Learning in Robotics",
        "authors": "Kevin Davis",
        "affiliation": "Stanford Robotics",
        "conference": "ICLR",
        "year": 2023,
        "citations": 67,
        "abstract": "Implementing advanced RL algorithms in robotic systems...",
        "keywords": ["Robotics", "Reinforcement Learning", "Control"],
        "pdf_link": "[PDF](#)",
        "code_link": "https://github.com/example/robot-rl"
    }
]
author_data = [
    {
        "name": "John Smith",
        "title": "Professor",
        "email": "john.smith@stanford.edu",
        "affiliation": "Stanford University",
        "research_interests": ["Machine Learning", "Scientific AI", "NLP"],
        "h_index": 45,
        "total_citations": 15000,
        "recent_papers": ["Large Language Models in Scientific Discovery", "AI in Healthcare"],
        "website": "https://scholar.example.com/smith_j",
        "bio": "Leading researcher in AI applications for scientific discovery..."
    },
    {
        "name": "Rachel Williams",
        "title": "Research Scientist",
        "email": "r.williams@mit.edu",
        "affiliation": "MIT",
        "research_interests": ["Neural Architecture", "AutoML"],
        "h_index": 28,
        "total_citations": 8500,
        "recent_papers": ["Neural Network Architecture Search", "AutoML Systems"],
        "website": "https://scholar.example.com/williams_r",
        "bio": "Specializes in automated machine learning systems..."
    },
    {
        "name": "Kevin Davis",
        "title": "Assistant Professor",
        "email": "kdavis@stanford.edu",
        "affiliation": "Stanford Robotics",
        "research_interests": ["Robotics", "Reinforcement Learning"],
        "h_index": 25,
        "total_citations": 5000,
        "recent_papers": ["Reinforcement Learning in Robotics", "Robot Control"],
        "website": "https://scholar.example.com/davis_k",
        "bio": "Focuses on robotic learning and control..."
    }
]
affiliation_data = [
    {
        "name": "Stanford University",
        "department": "Computer Science",
        "location": "Stanford, CA, USA",
        "research_areas": ["AI", "Systems", "Theory"],
        "faculty_count": 65,
        "student_count": 800,
        "ranking": 1,
        "website": "https://cs.stanford.edu",
        "notable_projects": [
            "AI for Science Initiative",
            "Human-Centered AI"
        ],
        "research_funding": "$100M annually"
    },
    {
        "name": "MIT",
        "department": "CSAIL",
        "location": "Cambridge, MA, USA",
        "research_areas": ["AI", "Robotics", "Security"],
        "faculty_count": 120,
        "student_count": 1000,
        "ranking": 1,
        "website": "https://csail.mit.edu",
        "notable_projects": [
            "SuperUROP",
            "AI2 Initiative"
        ],
        "research_funding": "$150M annually"
    },
    {
        "name": "Stanford Robotics",
        "department": "Mechanical Engineering",
        "location": "Stanford, CA, USA",
        "research_areas": ["Robotics", "Control", "AI"],
        "faculty_count": 15,
        "student_count": 150,
        "ranking": 2,
        "website": "https://robotics.stanford.edu",
        "notable_projects": [
            "Robotic Manipulation",
            "Human-Robot Interaction"
        ],
        "research_funding": "$40M annually"
    }
]

def render_paper_container(idx, paper):
    """Return a clickable HTML container for a paper row."""
    return f"""
    <div class="paper-container" onclick="document.getElementById('hidden_button_{idx}').click()" style="
        padding: 10px;
        border: 1px solid #ddd;
        border-radius: 5px;
        background-color: #f8f9fa;
        cursor: pointer;
        transition: all 0.2s ease;
        margin-bottom: 10px;
    ">
        <div style="font-size: 0.9em; color: #1f77b4;">
            {paper['conference']} {paper['year']} | {paper['authors']} | {paper['affiliation']}
        </div>
        <div style="font-size: 1.1em; font-weight: bold; margin-top: 5px;">
            {paper['title']}
        </div>
    </div>
    """


def render_details_panel(selected_paper):
    """Return HTML for the details panel for a selected paper."""
    return f"""
    <div style="
        padding: 15px;
        border: 1px solid #ddd;
        border-radius: 5px;
        background-color: white;
    ">
        <h3>Detailed Information</h3>
        <div style="font-size: 1.2em; font-weight: bold; margin-bottom: 10px;">
            {selected_paper['Paper Title']}
        </div>
        <div style="margin-bottom: 5px;">
            <strong>Authors:</strong> {selected_paper['Authors']}
        </div>
        <div style="margin-bottom: 5px;">
            <strong>Affiliation:</strong> {selected_paper['Affiliation']}
        </div>
        <div style="margin-bottom: 5px;">
            <strong>Conference:</strong> {selected_paper['Conference']} {selected_paper['Published Year']}
        </div>
        <div style="margin-bottom: 15px;">
            <strong>Citations:</strong> {selected_paper['Citations']}
        </div>
        <h4>Abstract</h4>
        <p>This is a sample abstract for the selected paper.</p>
        <h4>Keywords</h4>
        <p>Machine Learning, Neural Networks, AI</p>
        <h4>Links</h4>
        <p>{selected_paper['PDF Link']}<br>
        <a href="#">Code Repository</a></p>
    </div>
    """


def initialize_filters():
    """Initialize filter selections and shopping cart in sidebar."""
    with st.sidebar:
        st.sidebar.title("Filters")
        # Initialize filters based on search mode
        year = st.sidebar.multiselect(
            "Year",
            options=list(range(2024, 2019, -1)),
            default=st.session_state.get("year", None),
            placeholder="Select years...",
        )

        conference = st.sidebar.multiselect(
            "Conference",
            options=["NeurIPS", "ICML", "ICLR", "ACL", "EMNLP", "AAAI"],
            default=st.session_state.get("conference", None),
            placeholder="Select conferences...",
        )

        # Show organization filter for Paper and Author
        organization = None
        if st.session_state.search_mode in ["Paper", "Author"]:
            organization = st.sidebar.multiselect(
                "Organization",
                options=["Stanford", "MIT", "Berkeley", "Google", "Meta", "OpenAI"],
                default=st.session_state.get("organization", None),
                placeholder="Select organizations...",
            )

        # Show keywords filter only for Paper
        keywords = None
        if st.session_state.search_mode == "Paper":
            keywords = st.sidebar.multiselect(
                "Keywords",
                options=[
                    "Machine Learning",
                    "NLP",
                    "Computer Vision",
                    "Reinforcement Learning",
                    "Robotics",
                ],
                default=st.session_state.get("keywords", None),
                placeholder="Select keywords...",
            )

        search_button = st.sidebar.button("Apply Filters", type="primary")

        # Shopping Cart Section
        st.sidebar.markdown(f"### Shopping Cart ({len(st.session_state.cart)}/3)")
        for paper in st.session_state.cart:
            if st.sidebar.button(paper, key=f"cart_{paper}"):
                st.session_state.cart.remove(paper)
                st.rerun()

        if len(st.session_state.cart) < 3:
            st.sidebar.markdown(
                f"You can add up to {3 - len(st.session_state.cart)} more paper(s)."
            )
        else:
            st.sidebar.markdown("Cart is full (3 papers).")

        if st.sidebar.button("DeepDive", key="deepdive_button"):
            st.session_state.has_searched = False
            st.session_state.selected_row = None
            st.session_state.selected_page = 2
            st.session_state.page_change_requested = True
            st.rerun()

        return year, conference, organization, keywords, search_button


def render_initial_search():
    """Render the initial search page with centered search box and embedded button."""
    st.markdown(
        """
        <style>
        .center-container {
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            height: 50vh;
        }
        
        /* Style for option menu */
        .nav-link {
            margin: 0 10px !important;
            padding: 10px 20px !important;
            border-radius: 5px !important;
        }
        
        .nav-link.active {
            background-color: #1f77b4 !important;
            color: white !important;
        }
        
        /* Container width for search components */
        .search-components {
            width: 100%;
            max-width: 800px;
            margin: 0 auto;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown('<div class="center-container">', unsafe_allow_html=True)
        st.markdown('<div class="search-components">', unsafe_allow_html=True)

        # Get current mode from session state
        current_mode = st.session_state.get("search_mode", "Paper")

        selected_mode = option_menu(
            menu_title=None,
            options=["Paper", "Author", "Organization"],
            icons=["file-text", "person", "building"],
            orientation="horizontal",
            default_index=["Paper", "Author", "Organization"].index(current_mode),
            styles={
                "container": {"padding": "0!important", "margin-bottom": "20px"},
                "icon": {"font-size": "14px"},
                "nav-link": {
                    "font-size": "14px",
                    "text-align": "center",
                    "margin": "0px",
                    "--hover-color": "#eee",
                },
            },
        )

        # Check if mode has changed
        if selected_mode != current_mode:
            st.session_state.search_mode = selected_mode
            st.session_state.has_searched = False
            if "last_query" in st.session_state:
                del st.session_state.last_query
            if "selected_row" in st.session_state:
                del st.session_state.selected_row
            if "main_search" in st.session_state:
                st.session_state.main_search = ""
            st.rerun()

        # Search bar and button
        input_col, button_col = st.columns([5, 1])
        with input_col:
            search_query = st.text_input(
                label="Search Query",
                placeholder=f"Enter your {selected_mode.lower()} search query...",
                key="main_search",
                label_visibility="collapsed",
            )
        with button_col:
            search_button = st.button(
                "Search", type="primary", key="main_search_button"
            )

        st.markdown("</div></div>", unsafe_allow_html=True)

        return search_query, search_button


def render_search_results(query, filters=None):
    """Render search results with 'Paper Title' on a separate row, followed by other details."""
    # Add search mode selection above search bar
    left, mid, right = st.columns([2, 2, 1])
    with left:
        current_mode = st.session_state.get("search_mode", "Paper")
        selected_mode = option_menu(
            menu_title=None,
            options=["Paper", "Author", "Organization"],
            icons=["file-text", "person", "building"],
            orientation="horizontal",
            default_index=["Paper", "Author", "Organization"].index(current_mode),
            styles={
                "container": {"padding": "0!important", "margin-bottom": "20px"},
                "icon": {"font-size": "14px"},
                "nav-link": {
                    "font-size": "14px",
                    "text-align": "center",
                    "margin": "0px",
                    "--hover-color": "#eee",
                },
            },
        )

        # Update session state if mode changed
        if selected_mode != current_mode:
            st.session_state.search_mode = selected_mode
            st.session_state.last_query = ""  # Clear the query
            if "selected_row" in st.session_state:
                del st.session_state.selected_row
            if "top_search_bar" in st.session_state:
                st.session_state.top_search_bar = ""
            # Clear filters
            if "filters" in st.session_state:
                st.session_state.filters = None
            st.session_state.year = None
            st.session_state.conference = None
            st.session_state.organization = None
            st.session_state.keywords = None
            st.rerun()

    # Search bar
    input_col, button_col = st.columns([5, 1])
    with input_col:
        new_query = st.text_input(
            label="Search Results Query",
            value=st.session_state.get("last_query", ""),
            key="top_search_bar",
            label_visibility="collapsed",
        )
    with button_col:
        new_search = st.button("Search", key="top_search_button")

    if new_search and new_query:
        st.session_state.last_query = new_query
        if "selected_row" in st.session_state:
            del st.session_state.selected_row
        st.rerun()

    if st.session_state.get("last_query"):
        # Example results data

        # Two-column layout: table on left, details on right
        st.markdown(
            """
            <style>
            .detail-button {
                background-color: transparent !important;
                border: 1px solid #ddd !important;
                border-radius: 4px !important;
                color: #666 !important;
                padding: 0px 10px !important;
                height: 35px !important;
                line-height: 35px !important;
                transition: all 0.2s ease !important;
            }
            .detail-button:hover {
                background-color: #f0f0f0 !important;
                border-color: #999 !important;
                color: #333 !important;
            }
            .stButton {
                text-align: center;
            }
            </style>
        """,
            unsafe_allow_html=True,
        )

        col1, col2 = st.columns([2, 1])

        with col1:
            # st.markdown("### Search Results")
            
            if st.session_state.search_mode == "Author":
                # Author search results
                for idx, author in enumerate(author_data):
                    if st.button(author["name"], key=f"author_button_{idx}", use_container_width=True):
                        st.session_state.selected_row = ("author", idx)
                        st.rerun()
            
            elif st.session_state.search_mode == "Organization":
                # Organization search results
                for idx, org in enumerate(affiliation_data):
                    if st.button(org["name"], key=f"org_button_{idx}", use_container_width=True):
                        st.session_state.selected_row = ("organization", idx)
                        st.rerun()
            
            else:  # Paper search results
                for idx, paper in enumerate(paper_data):
                    paper_col, button_col = st.columns([0.92, 0.08])
                    with paper_col:
                        st.markdown(render_paper_container(idx, paper), unsafe_allow_html=True)
                    with button_col:
                        if st.button("→", key=f"button_{idx}", help="Click to view details"):
                            st.session_state.selected_row = ("paper", idx)
                            st.rerun()
        
        with col2:
            if "selected_row" in st.session_state and st.session_state.selected_row is not None:
                item_type, idx = st.session_state.selected_row
                
                if item_type == "author":
                    selected_item = author_data[idx]
                    st.markdown("### Author Details")
                    st.markdown(f"**Name:** {selected_item['name']}")
                    st.markdown(f"**Title:** {selected_item['title']}")
                    st.markdown(f"**Email:** {selected_item['email']}")
                    st.markdown(f"**Affiliation:** {selected_item['affiliation']}")
                    st.markdown(f"**H-index:** {selected_item['h_index']}")
                    st.markdown(f"**Citations:** {selected_item['total_citations']}")
                    st.markdown("**Research Interests:**")
                    st.markdown(", ".join(selected_item['research_interests']))
                    st.markdown("**Recent Papers:**")
                    st.markdown("\n".join([f"- {paper}" for paper in selected_item['recent_papers']]))
                
                elif item_type == "organization":
                    selected_item = affiliation_data[idx]
                    st.markdown("### Institution Details")
                    st.markdown(f"**Name:** {selected_item['name']}")
                    st.markdown(f"**Department:** {selected_item['department']}")
                    st.markdown(f"**Location:** {selected_item['location']}")
                    st.markdown(f"**Faculty:** {selected_item['faculty_count']}")
                    st.markdown(f"**Students:** {selected_item['student_count']}")
                    st.markdown("**Research Areas:**")
                    st.markdown(", ".join(selected_item['research_areas']))
                    st.markdown("**Notable Projects:**")
                    st.markdown("\n".join([f"- {project}" for project in selected_item['notable_projects']]))
                
                else:  # paper details
                    selected_item = paper_data[idx]
                    st.markdown("### Paper Details")
                    st.markdown(f"**Title:** {selected_item['title']}")
                    st.markdown(f"**Authors:** {selected_item['authors']}")
                    st.markdown(f"**Affiliation:** {selected_item['affiliation']}")
                    st.markdown(f"**Conference:** {selected_item['conference']} {selected_item['year']}")
                    st.markdown(f"**Citations:** {selected_item['citations']}")
                    st.markdown("**Abstract:**")
                    st.markdown(selected_item['abstract'])
                    st.markdown("**Keywords:**")
                    st.markdown(", ".join(selected_item['keywords']))
                    
                    if st.button("Add to Cart"):
                        if len(st.session_state.cart) < 3 and selected_item['title'] not in st.session_state.cart:
                            st.session_state.cart.append(selected_item['title'])
                            st.rerun()
    else:
        st.markdown("### ")


def dataset_page():
    """Main dataset page function."""
    # 添加CSS来减少页面顶部的空白
    st.markdown(
        """
        <style>
        .block-container {
            padding-top: 1rem;
            padding-bottom: 0rem;
        }
        header {
            visibility: hidden;
        }
        #MainMenu {
            visibility: hidden;
        }
        footer {
            visibility: hidden;
        }
        </style>
    """,
        unsafe_allow_html=True,
    )
    
    # Initialize session state variables if they don't exist
    if "has_searched" not in st.session_state:
        st.session_state.has_searched = False
    if "cart" not in st.session_state:
        st.session_state.cart = []
    if "selected_row" not in st.session_state:
        st.session_state.selected_row = None
    if "search_mode" not in st.session_state:
        st.session_state.search_mode = "Paper"

    try:
        year, conference, organization, keywords, filter_search = initialize_filters()

        if not st.session_state.has_searched:
            query, main_search = render_initial_search()
            if main_search and query:
                st.session_state.has_searched = True
                st.session_state.last_query = query
                st.rerun()
            elif filter_search and any([year, conference, organization, keywords]):
                st.session_state.has_searched = True
                st.session_state.last_query = f"Filters: {', '.join(filter(None, [str(year), str(conference), str(organization), str(keywords)]))}"
                st.rerun()
        else:
            render_search_results(st.session_state.get("last_query", ""))

    except Exception as e:
        st.error(f"Error initializing filters: {str(e)}")
        return


if __name__ == "__main__":
    dataset_page()
