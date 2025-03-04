import streamlit as st
import pandas as pd
from datetime import datetime


def initialize_filters():
    """Initialize filter selections in sidebar."""
    with st.sidebar:
        st.sidebar.title("Filters")
        year = st.sidebar.multiselect(
            "Year",
            options=list(range(2024, 2019, -1)),
            default=None,
            placeholder="Select years...",
        )

        conference = st.sidebar.multiselect(
            "Conference",
            options=["NeurIPS", "ICML", "ICLR", "ACL", "EMNLP", "AAAI"],
            default=None,
            placeholder="Select conferences...",
        )

        organization = st.sidebar.multiselect(
            "Organization",
            options=["Stanford", "MIT", "Berkeley", "Google", "Meta", "OpenAI"],
            default=None,
            placeholder="Select organizations...",
        )

        keywords = st.sidebar.multiselect(
            "Keywords",
            options=[
                "Machine Learning",
                "NLP",
                "Computer Vision",
                "Reinforcement Learning",
                "Robotics",
            ],
            default=None,
            placeholder="Select keywords...",
        )

        search_button = st.sidebar.button("Apply Filters", type="primary")

        return year, conference, organization, keywords, search_button


def render_initial_search():
    """Render the initial search page with centered search box."""
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
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown('<div class="center-container">', unsafe_allow_html=True)
        search_query = st.text_input(
            "", placeholder="Enter your search query...", key="main_search"
        )
        search_button = st.button("Search", type="primary", key="main_search_button")
        st.markdown("</div>", unsafe_allow_html=True)

        return search_query, search_button


def render_search_results(query, filters=None):
    """Render search results with top search bar and results table."""
    # Top search bar
    col1, col2 = st.columns([3, 1])
    with col1:
        new_query = st.text_input("", value=query, key="top_search_bar")
    with col2:
        new_search = st.button("Search", key="top_search_button")

    # Example results data
    results_data = {
        "Title": [
            "Large Language Models in Scientific Discovery",
            "Neural Network Architecture Search",
            "Reinforcement Learning in Robotics",
        ],
        "Authors": [
            "Smith, J., Johnson, A.",
            "Williams, R., Brown, M.",
            "Davis, K., Miller, L.",
        ],
        "Year": [2024, 2023, 2023],
        "Conference": ["NeurIPS", "ICML", "ICLR"],
        "Citations": [45, 89, 67],
    }

    # Create results DataFrame
    results_df = pd.DataFrame(results_data)

    # Display results in two columns
    col1, col2 = st.columns([2, 1])

    with col1:
        # Make the DataFrame rows clickable
        selected_index = None
        for idx, row in results_df.iterrows():
            with st.container():
                if st.button(
                    f"{row['Title']}\n\n"
                    f"Authors: {row['Authors']} | {row['Conference']} {row['Year']} | Citations: {row['Citations']}",
                    key=f"result_{idx}",
                    use_container_width=True,
                ):
                    selected_index = idx

    with col2:
        if selected_index is not None:
            st.markdown("### Detailed Information")
            selected_paper = results_df.iloc[selected_index]
            st.markdown(f"**{selected_paper['Title']}**")
            st.markdown(f"**Authors:** {selected_paper['Authors']}")
            st.markdown(
                f"**Conference:** {selected_paper['Conference']} {selected_paper['Year']}"
            )
            st.markdown(f"**Citations:** {selected_paper['Citations']}")
            st.markdown("### Abstract")
            st.write(
                "This is a sample abstract for the selected paper. It would contain a brief summary of the research work, methodology, and findings."
            )
            st.markdown("### Keywords")
            st.write("Machine Learning, Neural Networks, AI")
            st.markdown("### Links")
            st.markdown("- [PDF Link](#)")
            st.markdown("- [Code Repository](#)")
            st.markdown("- [Project Page](#)")


def dataset_page():
    """Main dataset page function."""
    # Initialize session state
    if "has_searched" not in st.session_state:
        st.session_state.has_searched = False

    # Always show filters in sidebar
    year, conference, organization, keywords, filter_search = initialize_filters()

    # Main content
    if not st.session_state.has_searched:
        # Initial search page
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
        # Results page
        render_search_results(st.session_state.last_query)


if __name__ == "__main__":
    dataset_page()
