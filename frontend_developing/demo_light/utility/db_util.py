import sys
from pathlib import Path

# Add the parent directory to sys.path to access db_manager.py
sys.path.append(str(Path(__file__).parents[2]))

import pandas as pd
from db_manager import DBManager  # This will now find the root db_manager.py
from models import ConferenceInstance
from repositories import (
    ConferenceInstanceRepository,
    PaperRepository,
    KeywordRepository,
    AffiliationRepository,
)


class DataManagerContext:
    """Context manager for database sessions."""

    def __init__(self):
        self.data_manager = DBManager()
        self.session = None

    def __enter__(self):
        self.session = self.data_manager.get_session()
        return {
            "conference": ConferenceInstanceRepository(self.session),
            "paper": PaperRepository(self.session),
            "keyword": KeywordRepository(self.session),
            "org": AffiliationRepository(self.session),
        }

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            self.session.close()


def aggregate_stat_df(data: list[any], include_keywords: bool = True) -> pd.DataFrame:
    """Create a DataFrame from conference statistics."""
    if not data:
        return pd.DataFrame(columns=["Year", "conference", "paper_count"])

    df_data = []
    for item in data:
        try:
            # Assuming item[0] contains conference instance with year information
            year = None
            if isinstance(item[0], ConferenceInstance):
                year = item[0].year
            elif isinstance(item[0], str) and item[0].isdigit():
                year = int(item[0])

            row = {
                "Year": year,
                "conference": (
                    item[0].conference_name
                    if isinstance(item[0], ConferenceInstance)
                    else str(item[0])
                ),
                "paper_count": item[1] if item[1] is not None else 0,
            }

            if include_keywords and isinstance(item[0], ConferenceInstance):
                with DataManagerContext() as managers:
                    keywords = managers["keyword"].get_top_keywords_for_instance(
                        item[0].instance_id
                    )
                    row["Keywords"] = ", ".join(keywords) if keywords else ""

            df_data.append(row)
        except Exception as e:
            print(f"Error processing conference statistics row: {str(e)}")
            continue

    df = pd.DataFrame(df_data)

    # Ensure Year column exists and is numeric
    if "Year" in df.columns:
        df["Year"] = pd.to_numeric(df["Year"], errors="coerce")
        df = df.sort_values("Year")

    return df


def conference_stat_df(data: list[any], include_keywords: bool = True) -> pd.DataFrame:
    """Create a DataFrame from conference statistics."""
    if not data:
        return pd.DataFrame(columns=["Year", "conference", "paper_count"])

    df_data = []
    for item in data:
        try:
            # Assuming item[0] contains conference instance with year information
            year = None
            if isinstance(item[0], ConferenceInstance):
                year = item[0].year
            elif isinstance(item[0], str) and item[0].isdigit():
                year = int(item[0])

            row = {
                "Year": year,
                "conference": (
                    item[0].conference_name
                    if isinstance(item[0], ConferenceInstance)
                    else str(item[0])
                ),
                "paper_count": item[1] if item[1] is not None else 0,
            }

            if include_keywords and isinstance(item[0], ConferenceInstance):
                with DataManagerContext() as managers:
                    keywords = managers["keyword"].get_top_keywords_for_instance(
                        item[0].instance_id
                    )
                    row["Keywords"] = ", ".join(keywords) if keywords else ""

            df_data.append(row)
        except Exception as e:
            print(f"Error processing conference statistics row: {str(e)}")
            continue

    df = pd.DataFrame(df_data)

    # Ensure Year column exists and is numeric
    if "Year" in df.columns:
        df["Year"] = pd.to_numeric(df["Year"], errors="coerce")
        df = df.sort_values("Year")

    return df


def orgnization_stat_df(data: list[any], include_keywords: bool = True) -> pd.DataFrame:
    """Create a DataFrame from conference statistics."""
    if not data:
        return pd.DataFrame(columns=["conference", "total_papers"])

    df_data = []
    for item in data:
        try:
            conference_name, paper_count = item

            row = {
                "conference": conference_name,
                "total_papers": paper_count if paper_count is not None else 0,
            }

            df_data.append(row)
        except Exception as e:
            print(f"Error processing organization statistics row: {str(e)}")
            continue

    df = pd.DataFrame(df_data)

    # Sort by total papers in descending order
    if not df.empty:
        df = df.sort_values("total_papers", ascending=False)

    return df
