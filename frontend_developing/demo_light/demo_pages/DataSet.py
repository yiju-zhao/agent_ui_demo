import streamlit as st
import pandas as pd
from datetime import datetime

def initialize_filters():
    """Initialize filter selections and shopping cart in sidebar."""
    with st.sidebar:
        st.sidebar.title("Filters")
        year = st.sidebar.multiselect(
            "Year",
            options=list(range(2024, 2019, -1)),
            default=None,
            placeholder="Select years..."
        )
        
        conference = st.sidebar.multiselect(
            "Conference",
            options=["NeurIPS", "ICML", "ICLR", "ACL", "EMNLP", "AAAI"],
            default=None,
            placeholder="Select conferences..."
        )
        
        organization = st.sidebar.multiselect(
            "Organization",
            options=["Stanford", "MIT", "Berkeley", "Google", "Meta", "OpenAI"],
            default=None,
            placeholder="Select organizations..."
        )
        
        keywords = st.sidebar.multiselect(
            "Keywords",
            options=["Machine Learning", "NLP", "Computer Vision", "Reinforcement Learning", "Robotics"],
            default=None,
            placeholder="Select keywords..."
        )
        
        search_button = st.sidebar.button("Apply Filters", type="primary")
        
        # Shopping Cart Section
        st.sidebar.markdown(f"### Shopping Cart ({len(st.session_state.cart)}/3)")
        for paper in st.session_state.cart:
            if st.sidebar.button(paper, key=f"cart_{paper}"):
                st.session_state.cart.remove(paper)
                st.rerun()
        
        if len(st.session_state.cart) < 3:
            st.sidebar.markdown(f"You can add up to {3 - len(st.session_state.cart)} more paper(s).")
        else:
            st.sidebar.markdown("Cart is full (3 papers).")
        
        if st.sidebar.button("DeepDive", key="deepdive_button"):
            st.write("Jumping to DeepDive page...")  # Placeholder
        
        return year, conference, organization, keywords, search_button

def render_initial_search():
    """Render the initial search page with centered search box and embedded button."""
    st.markdown(
        """
        <style>
        .center-container {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 50vh;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown('<div class="center-container">', unsafe_allow_html=True)
        input_col, button_col = st.columns([5, 1])
        with input_col:
            search_query = st.text_input(
                label="Search Query",
                placeholder="Enter your search query...",
                key="main_search",
                label_visibility="collapsed"
            )
        with button_col:
            search_button = st.button("Search", type="primary", key="main_search_button")
        st.markdown('</div>', unsafe_allow_html=True)
        
        return search_query, search_button

def render_search_results(query, filters=None):
    """Render search results as a table with 'Paper Title' as a clickable button."""
    input_col, button_col = st.columns([5, 1])
    with input_col:
        new_query = st.text_input(
            label="Search Results Query",
            value=query,
            key="top_search_bar",
            label_visibility="collapsed"
        )
    with button_col:
        new_search = st.button("Search", key="top_search_button")
    
    # Example results data
    results_data = {
        "Paper Title": [
            "Large Language Models in Scientific Discovery",
            "Neural Network Architecture Search",
            "Reinforcement Learning in Robotics"
        ],
        "Conference": ["NeurIPS", "ICML", "ICLR"],
        "Published Year": [2024, 2023, 2023],  # Rename "Year" to "Published Year"
        "PDF Link": [
            "[PDF](#)",  # Update to PDF Link
            "[PDF](#)",
            "[PDF](#)"
        ],
        "Authors": [
            "Smith, J., Johnson, A.",
            "Williams, R., Brown, M.",
            "Davis, K., Miller, L."
        ],
        "Citations": [45, 89, 67]
    }
    
    results_df = pd.DataFrame(results_data)
    
    # Two-column layout: table on left, details on right
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### Search Results")
        # Create a container for each row with a table-like layout
        selected_index = st.session_state.get("selected_row", None)
        for idx, row in results_df.iterrows():
            with st.container():
                col_title, col_conf, col_year, col_pdf = st.columns([2, 1, 1, 2])
                with col_title:
                    if st.button(row["Paper Title"], key=f"title_button_{idx}"):
                        st.session_state.selected_row = idx
                        st.rerun()
                with col_conf:
                    st.write(row["Conference"])
                with col_year:
                    st.write(row["Published Year"])
                with col_pdf:
                    st.write(row["PDF Link"])
    
    with col2:
        if "selected_row" in st.session_state and st.session_state.selected_row is not None:
            selected_index = st.session_state.selected_row
            st.markdown("### Detailed Information")
            selected_paper = results_df.iloc[selected_index]
            st.markdown(f"**{selected_paper['Paper Title']}**")
            st.markdown(f"**Authors:** {selected_paper['Authors']}")
            st.markdown(f"**Conference:** {selected_paper['Conference']} {selected_paper['Published Year']}")
            st.markdown(f"**Citations:** {selected_paper['Citations']}")
            st.markdown("### Abstract")
            st.write("This is a sample abstract for the selected paper.")
            st.markdown("### Keywords")
            st.write("Machine Learning, Neural Networks, AI")
            st.markdown("### Links")
            st.markdown(f"- {selected_paper['PDF Link']}")  # Use PDF Link instead of Project Page
            st.markdown("- [Code Repository](#)")
            
            if st.button("Add to Cart", key=f"add_to_cart_{selected_index}"):
                if len(st.session_state.cart) < 3 and selected_paper['Paper Title'] not in st.session_state.cart:
                    st.session_state.cart.append(selected_paper['Paper Title'])
                    st.rerun()

    if new_search and new_query:
        st.session_state.last_query = new_query
        if "selected_row" in st.session_state:
            del st.session_state.selected_row  # Reset selection on new search
        st.rerun()

def dataset_page():
    """Main dataset page function."""
    if "has_searched" not in st.session_state:
        st.session_state.has_searched = False
    if "cart" not in st.session_state:
        st.session_state.cart = []
    if "selected_row" not in st.session_state:
        st.session_state.selected_row = None
    
    try:
        year, conference, organization, keywords, filter_search = initialize_filters()
    except Exception as e:
        st.error(f"Error initializing filters: {str(e)}")
        return
    
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
        render_search_results(st.session_state.last_query)

if __name__ == "__main__":
    dataset_page()