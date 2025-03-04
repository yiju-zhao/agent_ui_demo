import streamlit as st
import pandas as pd
from typing import List, Dict, Any, Tuple, List, Callable
import plotly.express as px
import plotly.graph_objects as go


class MetricsDisplay:
    """Handles display of metrics in a consistent format."""

    @staticmethod
    def show_basic_metrics(total_papers: int):
        """Display basic metrics in three columns."""
        st.metric("Total Papers", f"{total_papers:,}")
        # col1, col2, col3 = st.columns(3)
        # with col1:
        #     st.metric("Total Papers", f"{total_papers:,}")
        # with col2:
        #     st.metric("Average Citations", f"{avg_citations:.1f}")
        # with col3:
        #     st.metric("Highest Citation", f"{max_citations:,}")

    @staticmethod
    def show_conference_metrics(df: pd.DataFrame):
        """Display conference-specific metrics."""
        try:
            # Calculate basic metrics
            total_papers = df["paper_count"].sum() if "paper_count" in df.columns else 0
            total_org = df["affil_count"].sum() if "affil_count" in df.columns else 0

            st.metric(label="Total Papers", value=f"{int(total_papers):,}")
            st.metric(label="Total Organizations", value=f"{int(total_org):,}")

        except Exception as e:
            st.warning("Unable to display some metrics due to missing data")
            print(f"Metrics display error: {str(e)}")  # For debugging


class DataFrameDisplay:
    """Handles DataFrame display with consistent formatting."""

    @staticmethod
    def show_paper_table(papers_df: pd.DataFrame, use_container_width: bool = True):
        """Display paper information in a formatted table."""
        st.dataframe(
            papers_df.style.format(
                {"Citations": "{:,.0f}", "Avg Citations": "{:,.1f}"}
            ),
            use_container_width=use_container_width,
        )

    @staticmethod
    def show_conference_stats(df: pd.DataFrame):
        """Display conference statistics with formatting."""
        st.subheader("Detailed Statistics")
        DataFrameDisplay.show_paper_table(df)


class ChartDisplay:
    """Handles creation and display of various charts."""

    @staticmethod
    def create_cs_schools_chart():
        """Create a radar chart for top CS schools metrics."""
        # Sample data - replace with real data
        schools_data = {
            "School": ["MIT", "Stanford", "Berkeley", "CMU", "ETH Zurich"],
            "Research Impact": [95, 92, 90, 88, 87],
            "Citations": [98, 95, 92, 90, 89],
            "Industry Collab": [90, 92, 88, 94, 85],
            "Funding": [96, 94, 92, 90, 88],
        }

        fig = go.Figure()
        categories = ["Research Impact", "Citations", "Industry Collab", "Funding"]

        for i, school in enumerate(schools_data["School"]):
            fig.add_trace(
                go.Scatterpolar(
                    r=[schools_data[cat][i] for cat in categories],
                    theta=categories,
                    fill="toself",
                    name=school,
                )
            )

        fig.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
            showlegend=True,
            height=300,
        )
        return fig

    @staticmethod
    def create_tech_companies_chart():
        """Create a bubble chart for tech companies metrics."""
        # Sample data - replace with real data
        companies_data = {
            "Company": ["Google", "Microsoft", "Meta", "Apple", "Amazon"],
            "Research Papers": [150, 120, 90, 70, 80],
            "Patents": [200, 180, 120, 150, 130],
            "Market Cap": [2000, 1800, 800, 2500, 1500],
        }

        fig = go.Figure()

        fig.add_trace(
            go.Scatter(
                x=companies_data["Research Papers"],
                y=companies_data["Patents"],
                mode="markers",
                marker=dict(
                    size=[cap / 50 for cap in companies_data["Market Cap"]],
                    sizemode="area",
                    sizeref=2.0 * max(companies_data["Market Cap"]) / (40.0**2),
                    sizemin=4,
                ),
                text=companies_data["Company"],
                name="Companies",
            )
        )

        fig.update_layout(
            height=300, xaxis_title="Research Papers", yaxis_title="Patents"
        )
        return fig

    @staticmethod
    def show_trend_analysis(df: pd.DataFrame, x_col: str = "Year"):
        """Display trend analysis tabs with multiple charts."""
        # Verify we have required columns and handle column case sensitivity
        df = df.copy()  # Create a copy to avoid modifying original

        # Check if x_col exists (case-insensitive)
        available_columns = df.columns.str.lower()
        if x_col.lower() not in available_columns:
            st.warning(
                f"Missing {x_col} column. Please ensure time series data is available."
            )
            return

        # Get the actual column name with correct case
        x_col = df.columns[available_columns == x_col.lower()][0]

        required_columns = ["paper_count"]
        if not all(col in df.columns for col in required_columns):
            st.warning("Missing required data columns for trend analysis")
            return

        tab1, tab2 = st.tabs(["Papers Over Time", "Combined Analysis"])

        with tab1:
            try:
                # Sort by year to ensure proper trend line
                df = df.sort_values(by=x_col)

                fig = px.line(
                    df,
                    x=x_col,
                    y="paper_count",
                    title="Papers Published Over Time",
                    markers=True,  # Add markers for better visibility
                )
                fig.update_layout(xaxis_title=x_col, yaxis_title="Number of Papers")
                st.plotly_chart(fig, use_container_width=True)
            except Exception as e:
                st.error(f"Error creating papers over time chart: {str(e)}")
                st.write("DataFrame columns:", df.columns.tolist())  # Debug info

        with tab2:
            try:
                normalized = df.copy()
                cols_to_normalize = ["paper_count"]

                for col in cols_to_normalize:
                    if col in df.columns:
                        max_val = df[col].max()
                        min_val = df[col].min()
                        if max_val != min_val:
                            normalized[f"{col} (normalized)"] = (df[col] - min_val) / (
                                max_val - min_val
                            )
                        else:
                            normalized[f"{col} (normalized)"] = (
                                1  # All values are the same
                            )

                fig = px.line(
                    normalized,
                    x=x_col,
                    y=[
                        f"{col} (normalized)"
                        for col in cols_to_normalize
                        if col in df.columns
                    ],
                    title="Normalized Trends",
                    markers=True,
                )
                fig.update_layout(xaxis_title=x_col, yaxis_title="Normalized Value")
                st.plotly_chart(fig, use_container_width=True)
            except Exception as e:
                st.error(f"Error creating normalized trends chart: {str(e)}")

    @staticmethod
    def show_conference_distribution(df: pd.DataFrame):
        """Display conference distribution charts."""
        if "conference" not in df.columns or "paper_count" not in df.columns:
            st.warning("Missing required columns for conference distribution")
            return

        st.subheader("Conference Distribution")
        try:
            fig = px.bar(
                df, x="conference", y="paper_count", title="Papers by Conference"
            )
            st.plotly_chart(fig, use_container_width=True)
        except Exception as e:
            st.error(f"Error creating conference distribution chart: {str(e)}")

    @staticmethod
    def show_keyword_network(keywords: List[Tuple[str, int]], central_keyword: str):
        """Display keyword relationship network."""
        nodes = [central_keyword] + [k[0] for k in keywords]
        edges = [(central_keyword, k[0]) for k in keywords]
        weights = [k[1] for k in keywords]

        # Create network visualization using plotly
        fig = go.Figure()
        # Add nodes and edges with appropriate styling
        # (Network visualization implementation details)
        st.plotly_chart(fig, use_container_width=True)


class DashboardLayout:
    """Handles consistent layout of dashboard components."""

    @staticmethod
    def show_conference_layout(df: pd.DataFrame, conference: str):
        """Display standard conference dashboard layout."""
        if df is None or df.empty:
            st.warning(f"No data available for {conference}")
            return
        try:
            st.header(conference)
            # If Year column is missing, try to use conference column as x-axis
            x_col = "Year" if "Year" in df.columns else "conference"

            MetricsDisplay.show_conference_metrics(df)
            ChartDisplay.show_trend_analysis(df, x_col=x_col)
            DataFrameDisplay.show_conference_stats(df)
        except Exception as e:
            st.error(f"Error displaying conference layout: {str(e)}")
            st.write("Available columns:", df.columns.tolist())  # Debug info

    @staticmethod
    def show_aggregate_layout(df: pd.DataFrame, conference: str):
        """Display standard conference dashboard layout."""
        if df is None or df.empty:
            st.warning(f"No data available for {conference}")
            return
        try:
            st.header(conference)
            # If Year column is missing, try to use conference column as x-axis
            x_col = "Year" if "Year" in df.columns else "conference"

            MetricsDisplay.show_conference_metrics(df)
            ChartDisplay.show_trend_analysis(df, x_col=x_col)
            DataFrameDisplay.show_conference_stats(df)
        except Exception as e:
            st.error(f"Error displaying conference layout: {str(e)}")
            st.write("Available columns:", df.columns.tolist())  # Debug info

    @staticmethod
    def show_keyword_layout(
        papers: List[Any], keyword: str, related_keywords: List[Tuple[str, int]]
    ):
        """Display standard keyword dashboard layout."""
        papers_df = pd.DataFrame(
            [
                {
                    "Title": p.title,
                    "Authors": ", ".join([a.name for a in p.author_to_paper]),
                    "Year": p.year,
                    "Citations": p.citation_count,
                }
                for p in papers
            ]
        )

        MetricsDisplay.show_basic_metrics(
            len(papers), papers_df["Citations"].mean(), papers_df["Citations"].max()
        )

        st.subheader("Paper Distribution")
        ChartDisplay.show_trend_analysis(
            papers_df.groupby("Year")
            .agg({"Title": "count", "Citations": ["mean", "max"]})
            .reset_index()
        )

        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Related Keywords")
            ChartDisplay.show_keyword_network(related_keywords, keyword)
        with col2:
            st.subheader("Top Papers")
            DataFrameDisplay.show_paper_table(papers_df.nlargest(5, "Citations"))


class FilterDisplay:
    """Handles display of filter components."""

    @staticmethod
    def show_year_filter(available_years: List[int]) -> int:
        """Display year selection filter."""
        return st.selectbox(
            "Select Year",
            options=available_years,
            index=None,
            placeholder="Choose a year...",
        )

    @staticmethod
    def show_item_filter(
        items: List[str],
        key_suffix: str,
        callback: Callable[[str], None],
        session_state: dict,
        selected_key: str,
        num_columns: int = 2,
    ) -> str:
        """Display conference selection filter."""

        columns = st.columns(num_columns)
        chunk_size = (len(items) + num_columns - 1) // num_columns

        for i, col in enumerate(columns):
            with col:
                start = i * chunk_size
                end = (i + 1) * chunk_size
                for item in items[start:end]:
                    is_selected = session_state.get(selected_key) == item
                    if st.button(
                        item,
                        key=f"{item}_{key_suffix}",
                        use_container_width=True,
                        type="primary" if is_selected else "secondary",
                    ):
                        # Let the callback handle the toggle logic
                        callback(item)

        # return st.session_state.get("selected_conference")

    @staticmethod
    def show_keyword_search(keywords: List[str]) -> str:
        """Display keyword search/filter."""
        return st.text_input("Search Keywords", placeholder="Type to search...")
