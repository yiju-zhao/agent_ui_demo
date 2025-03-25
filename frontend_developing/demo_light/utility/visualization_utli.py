import streamlit as st
import pandas as pd
from typing import List, Any, Tuple, List, Callable
import plotly.express as px
import plotly.graph_objects as go
import altair as alt

label_font_size = 16
title_font_size = 18
legend_font_size = 17

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

    @staticmethod
    def get_topic_color(topic):
        """Generate a color based on the topic name using HSL color space for better distribution."""
        # Use a hash of the topic name to generate a hue value
        topic_hash = hash(topic) % 360  # Hue values are 0-359

        # Fixed saturation and lightness for consistent, readable colors
        saturation = 80  # Higher value = more vibrant colors
        lightness = 45  # Slightly darker for better contrast

        # Convert HSL to a CSS color string
        return f"hsl({topic_hash}, {saturation}%, {lightness}%)"


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

class ConferenceVisualization:
    """Handles visualization of conference data."""
    
    @staticmethod
    def render_conference_header(instance, theme_color="#1f77b4"):
        """Render a styled conference header."""
        st.markdown(
            f"""
            <div style='padding: 10px; margin-bottom: 15px; background-color: #f8f9fa; 
                border-radius: 5px; border-left: 5px solid {theme_color};'>
                <div style='display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;'>
                    <h3 style='margin: 0; color: {theme_color};'>{instance.conference_name} {instance.year}</h3>
                    <div style='font-size: 0.9em;'>
                        <span style='margin-right: 15px;'><strong>Date:</strong> {instance.start_date.strftime('%b %d')} - 
                        {instance.end_date.strftime('%b %d, %Y')}</span>
                        <span><strong>Location:</strong> {instance.location or "N/A"}</span>
                    </div>
                </div>
                {f'<div style="font-size: 0.85em; margin-top: 5px;"><strong>Website:</strong> <a href="{instance.website}" target="_blank">{instance.website}</a></div>' 
                if instance.website else ''}
            </div>
            """,
            unsafe_allow_html=True,
        )
    
    @staticmethod
    def apply_session_styles(theme_color="#1f77b4"):
        """Apply CSS styles for session display."""
        st.markdown(f"""
            <style>
            /* More compact session cards */
            .session-card {{
                padding: 8px;
                margin-bottom: 8px;
                border: 1px solid #e6e6e6;
                border-radius: 5px;
                background-color: #f8f9fa;
            }}
            .session-time {{
                color: #666666;
                font-size: 0.8em;
            }}
            .session-title {{
                color: {theme_color};
                font-weight: bold;
                font-size: 0.95em;
                margin: 3px 0;
                white-space: nowrap;
                overflow: hidden;
                text-overflow: ellipsis;
            }}
            .session-track {{
                display: inline-block;
                padding: 1px 6px;
                background-color: {theme_color}20;
                color: {theme_color};
                border-radius: 10px;
                font-size: 0.75em;
            }}
            </style>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def render_session_card(session):
        """Render a session card with consistent styling."""
        st.markdown(f"""
            <div class="session-card">
                <div class="session-time">{session['session_code']}</div>
                <div class="session-title" title="{session['title']}">{session['title']}</div>
                <div class="session-track">{session['track']}</div>
            </div>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def render_session_details(session, theme_color="#1f77b4"):
        """Render detailed session information."""
        st.markdown(f"""
            <div style="padding: 12px; border: 1px solid #e6e6e6; border-radius: 5px; background-color: #f8f9fa;">
                <h4 style="color: {theme_color}; margin: 0 0 10px 0; font-size: 1.1em;">{session['title']}</h4>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 8px; margin-bottom: 10px; font-size: 0.9em;">
                    <div><strong>Time:</strong> {session['time']}</div>
                    <div><strong>Location:</strong> {session['location']}</div>
                    <div><strong>Track:</strong> {session['track']}</div>
                    <div><strong>Code:</strong> {session.get('session_code', 'N/A')}</div>
                </div>
                <div style="display: flex; justify-content: space-between; font-size: 0.9em;">
                    <div style="flex: 1;"><strong>Level:</strong> {session.get('technical_level', 'N/A')}</div>
                </div>
                <div style="margin-top: 8px; font-size: 0.9em;">
                    <strong>Speaker(s):</strong> {session['speaker']}
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def render_trend_charts(data, title="Trend Analysis"):
        """Render trend charts for conference data."""
        yearly_fig = go.Figure()
        
        # Add papers trend
        yearly_fig.add_trace(
            go.Scatter(
                x=data["years"],
                y=data["paper_counts"],
                name="Papers",
                mode="lines+markers",
                line=dict(color="blue", width=2),
            )
        )
        
        # Add conferences trend on secondary y-axis if available
        if "conference_counts" in data:
            yearly_fig.add_trace(
                go.Scatter(
                    x=data["years"],
                    y=data["conference_counts"],
                    name="Conferences",
                    mode="lines+markers",
                    line=dict(color="red", width=2),
                    yaxis="y2",
                )
            )
            
            yearly_fig.update_layout(
                yaxis2=dict(title="Number of Conferences", overlaying="y", side="right"),
            )

        yearly_fig.update_layout(
            title=title,
            xaxis=dict(title="Year"),
            yaxis=dict(title="Number of Papers"),
            hovermode="x unified",
            showlegend=True,
            legend=dict(
                orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1
            ),
        )
        
        st.plotly_chart(yearly_fig, use_container_width=True)

class CompanyVisualization:
    """Handles visualization of company data."""
    
    @staticmethod
    def create_company_involvement_chart(company_topic_data, company_list, title_prefix, instance_name, instance_year, horizontal=False, label_threshold=2):
        """
        Create a simplified stacked bar chart showing company involvement by topic with count labels on each segment.
        For a horizontal chart, a total session label is displayed at the end of each bar.
        
        Args:
            company_topic_data: List of dictionaries with company, topic, and count information.
            company_list: List of standardized company names to include.
            title_prefix: Prefix for the chart title.
            instance_name: Name of the conference instance.
            instance_year: Year of the conference instance.
            horizontal: Whether to create a horizontal bar chart (default: False).
            label_threshold: Minimum Count value required to display a label on a segment.
            
        Returns:
            Altair chart object.
        """
        if not company_topic_data:
            return None

        # Convert to DataFrame and compute unique session counts per Company/Topic
        df = pd.DataFrame(company_topic_data)
        counts = (df.drop_duplicates(subset=["Company", "Topic", "Session_ID"])
                    .groupby(["Company", "Topic"])
                    .size()
                    .reset_index(name="Count"))
        
        # Determine the top 10 topics by total count
        top_topics = counts.groupby("Topic")["Count"].sum().nlargest(10).index.tolist()
        counts = counts[counts["Topic"].isin(top_topics)]
        
        # Pivot the data so that rows are Companies and columns are topics
        pivot_df = counts.pivot_table(index="Company", columns="Topic", values="Count", fill_value=0)
        
        # Reindex to include all companies and reset the index
        pivot_df = pivot_df.reindex(company_list, fill_value=0).reset_index()
        
        # Compute total sessions per company
        pivot_df["total_sessions"] = pivot_df[top_topics].sum(axis=1)
        pivot_df = pivot_df[pivot_df["total_sessions"] > 0]  # filter out companies with zero sessions
        
        # Melt the pivot table (include total_sessions for later aggregation)
        melted_df = pd.melt(pivot_df, id_vars=["Company", "total_sessions"], value_vars=top_topics,
                            var_name="Topic", value_name="Count")
        
        # Base chart with window transform for cumulative sums and midpoints
        base = alt.Chart(melted_df).transform_window(
            cumulative_sum='sum(Count)',
            sort=[{'field': 'Count', 'order': 'descending'},
                {'field': 'Topic', 'order': 'ascending'}],
            groupby=['Company']
        ).transform_calculate(
            mid='datum.cumulative_sum - datum.Count/2',
            label=f"(datum.Count >= {label_threshold}) ? datum.Count : ''"
        )
        
        if horizontal:
            bar = base.mark_bar().encode(
                y=alt.Y('Company:N', title='', sort=company_list, axis=alt.Axis(labelLimit=120)),
                x=alt.X('sum(Count):Q', title='Number of Sessions', axis=alt.Axis(labels=False)),
                color=alt.Color('Topic:N', scale=alt.Scale(scheme='tableau10'),
                                legend=alt.Legend(title="", orient="right")),
                order=alt.Order('Count:Q', sort='descending'),
                tooltip=['Company', 'Topic', alt.Tooltip('Count:Q', format='.0f')]
            )
            
            text = base.mark_text(align='center', baseline='middle', color='white', fontSize=14).encode(
                y=alt.Y('Company:N', sort=company_list),
                x=alt.X('mid:Q'),
                text=alt.Text('label:N')
            )
            
            # Aggregate total sessions per company using the melted data
            total_text = alt.Chart(melted_df).transform_aggregate(
                total='max(total_sessions)',
                groupby=['Company']
            ).mark_text(align='left', baseline='middle', dx=3, fontSize=16).encode(
                y=alt.Y('Company:N', sort=company_list),
                x=alt.X('total:Q'),
                text=alt.Text('total:Q', format='.0f')
            )
            
            chart = (bar + text + total_text).properties(
                title=f"{title_prefix} Companies' Involvement by Topic at {instance_name} {instance_year}",
                height=400
            )
        else:
            # Vertical chart version (if needed)
            bar = base.mark_bar().encode(
                x=alt.X('Company:N', sort=company_list, axis=alt.Axis(labelAngle=0, labelLimit=120)),
                y=alt.Y('sum(Count):Q', title='Number of Sessions', axis=alt.Axis(labels=False)),
                color=alt.Color('Topic:N', scale=alt.Scale(scheme='tableau10'),
                                legend=alt.Legend(title="", orient="right")),
                order=alt.Order('Count:Q', sort='descending'),
                tooltip=['Company', 'Topic', alt.Tooltip('Count:Q', format='.0f')]
            )
            
            text = base.mark_text(align='center', baseline='middle', color='white', fontSize=14).encode(
                x=alt.X('Company:N', sort=company_list),
                y=alt.Y('mid:Q'),
                text=alt.Text('label:N')
            )
            
            total_text = alt.Chart(melted_df).transform_aggregate(
                total='max(total_sessions)',
                groupby=['Company']
            ).mark_text(align='center', baseline='bottom', dy=-3, fontSize=16).encode(
                x=alt.X('Company:N', sort=company_list),
                y=alt.Y('total:Q'),
                text=alt.Text('total:Q', format='.0f')
            )
            
            chart = (bar + text + total_text).properties(
                title=f"{title_prefix} Companies' Involvement by Topic at {instance_name} {instance_year}",
                height=500
            )
        
        return chart.configure_view(stroke=None)\
                    .configure_axis(labelFontSize=16, titleFontSize=18, grid=False)\
                    .configure_legend(labelFontSize=18, titleFontSize=18, padding=10, cornerRadius=5,
                                    orient='right', labelLimit=300, titleLimit=200)\
                    .configure_title(fontSize=18, font='Arial', anchor='start', color='black')




class TopicVisualization:
    """Handles visualization of topic data."""
    
    @staticmethod
    def create_topic_bar_chart(topic_data, conference_name, year, limit=20):
        """
        Create a bar chart showing topic counts.
        
        Args:
            topic_data: Dictionary mapping topics to their counts
            conference_name: Name of the conference
            year: Year of the conference
            limit: Maximum number of topics to display
            
        Returns:
            Altair chart object
        """
        if not topic_data:
            return None
            
        # Sort topics by count
        sorted_topics = sorted(topic_data.items(), key=lambda x: x[1], reverse=True)
        
        # Create dataframe for visualization
        topic_df = pd.DataFrame(sorted_topics, columns=["Topic", "Count"])
        
        # Limit to top N topics for better visualization
        if len(topic_df) > limit:
            display_df = topic_df.head(limit)
        else:
            display_df = topic_df
        
        # For the topic count bar chart
        base = alt.Chart(display_df).encode(
            y=alt.Y('Topic:N', sort='-x', title='', axis=alt.Axis(labelLimit=300)),
            x=alt.X('Count:Q', title='Number of Sessions', axis=alt.Axis(labels=False))
        )

        # Create the bars
        bars = base.mark_bar().encode(
            color=alt.Color('Count:Q', 
                        scale=alt.Scale(scheme='blues'),
                        legend=None),
            tooltip=['Topic', 'Count']
        )

        # Create the text labels at the end of the bars
        text = base.mark_text(
            align='left',     # Align text to the left (start of text is at the end of the bar)
            baseline='middle', # Center text vertically
            dx=3,              # Small horizontal offset from the end of the bar
            fontSize=16 
        ).encode(
            text='Count:Q'    # Use the Count field for the text
        )

        # Combine the bars and text
        chart = (bars + text).properties(
            title=f"Top Topics at {conference_name} {year}",
            height=600
        ).configure_axis(
            labelFontSize=16,
            titleFontSize=18
        ).configure_title(
            fontSize=18,
            font='Arial',
            anchor='start',
            color='black'
        )
        
        return chart
