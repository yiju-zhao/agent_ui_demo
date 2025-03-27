import sys
from pathlib import Path
from datetime import datetime

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


class DataLoader:
    """Handles loading and processing of conference session data."""
    
    @staticmethod
    def load_session_data(instance_id=None):
        """Load session data from database"""
        try:
            with DataManagerContext() as managers:
                if instance_id:
                    # Get sessions through conference repository
                    sessions = managers["conference"].get_sessions_by_instance(
                        instance_id
                    )
                    if not sessions:
                        return []

                    # Group sessions by date
                    session_by_date = {}
                    for session in sessions:
                        date_str = session.date.strftime("%Y-%m-%d")
                        if date_str not in session_by_date:
                            session_by_date[date_str] = []

                        # Find related speakers
                        speaker_list = []
                        speaker_companies = []
                        
                        for speaker in session.speaker_to_session:
                            # Get affiliation name using affiliation_id
                            affiliation_name = ""
                            if speaker.affiliation_id:
                                affiliation = managers["org"].get_affiliation_by_id(
                                    speaker.affiliation_id
                                )
                                if affiliation:
                                    affiliation_name = affiliation.name
                                    speaker_companies.append(affiliation_name)

                            # Format speaker string
                            if speaker.position:
                                speaker_str = f"{speaker.name} ({speaker.position} | {affiliation_name})"
                            else:
                                speaker_str = f"{speaker.name} ({affiliation_name})" if affiliation_name else speaker.name
                            
                            speaker_list.append(speaker_str)

                        formatted_session = {
                            "time": f"{session.start_time.strftime('%I:%M %p')} - {session.end_time.strftime('%I:%M %p')}",
                            "title": session.title,
                            "speaker": ", ".join(speaker_list),
                            "location": (
                                f"{session.venue}, {session.room}"
                                if session.room
                                else session.venue
                            ),
                            "venue": session.venue,  # Add venue separately for filtering
                            "speaker_companies": speaker_companies,  # Add companies for filtering
                            "track": session.topic,
                            "description": session.description if session.description and session.description != 'nan' else "",
                            "session_code": session.session_code,
                            "technical_level": session.technical_level,
                            "full_topic": session.topic,
                            "points": session.points if session.points and session.points != 'nan' else "",
                            "expert_opinion": session.expert_view if session.expert_view and session.expert_view != 'nan' else "",
                            "ai_analysis": session.ai_analysis if session.ai_analysis and session.ai_analysis != 'nan' else "",
                        }
                        session_by_date[date_str].append(formatted_session)

                    # Convert to list and sort chronologically
                    session_data = [
                        {
                            "date": date_str,
                            "day": datetime.strptime(date_str, "%Y-%m-%d").strftime(
                                "%A"
                            ),
                            "sessions": sorted(
                                sessions_list,
                                key=lambda x: datetime.strptime(
                                    x["time"].split(" - ")[0], "%I:%M %p"
                                ),
                            ),
                        }
                        for date_str, sessions_list in session_by_date.items()
                    ]

                    # Sort days chronologically
                    session_data.sort(key=lambda x: x["date"])

                    return session_data

                return []
        except Exception as e:
            print(f"Error loading session data: {e}")
            return []
        
    
class CompanyMatcher:
    """Utility for matching company names to standardized company names."""
    
    # Cloud company aliases
    CLOUD_COMPANIES = ["Microsoft", "Google", "AWS", "Oracle"]
    CLOUD_COMPANY_ALIASES = {
        "Microsoft": ["Microsoft", "MSFT", "Microsoft Corporation", "Microsoft Corp", "MS"],
        "Google": ["Google", "Google Inc", "Google LLC", "Google Cloud", "Alphabet"],
        "AWS": ["AWS", "Amazon", "Amazon Web Services", "Amazon AWS", "Amazon.com"],
        "Oracle": ["Oracle", "Oracle Corporation", "Oracle Corp", "Oracle Cloud"]
    }
    
    # OEM company aliases
    OEM_COMPANIES = ["HP", "Dell", "Lenovo", "ASUS", "QTN", "Inventec", "MSI"]
    OEM_COMPANY_ALIASES = {
        "HP": ["HP", "Hewlett Packard", "Hewlett-Packard", "HP Inc", "HPE", "Hewlett Packard Enterprise"],
        "Dell": ["Dell", "Dell Technologies", "Dell Inc", "Dell EMC", "Dell Computer"],
        "Lenovo": ["Lenovo", "Lenovo Group", "Lenovo Inc"],
        "ASUS": ["ASUS", "ASUSTeK", "ASUSTeK Computer", "ASUS Computer"],
        "QTN": ["QTN", "Quanta", "Quanta Computer", "Quanta Inc"],
        "Inventec": ["Inventec", "Inventec Corporation", "Inventec Corp"],
        "MSI": ["MSI", "Micro-Star", "Micro-Star International", "Micro Star", "MSI Computer"]
    }
    
    @staticmethod
    def match_company(company_name, company_list, aliases_dict):
        """
        Match a company name to a standardized company name using aliases.
        
        Args:
            company_name: The company name to match
            company_list: List of standardized company names
            aliases_dict: Dictionary mapping standardized names to lists of aliases
            
        Returns:
            Matched standardized company name or None if no match
        """
        if not company_name:
            return None
            
        # Normalize the company name
        normalized_name = company_name.strip().upper()
        
        # Check against each target company and its aliases
        for target, aliases in aliases_dict.items():
            if any(alias.upper() in normalized_name or normalized_name in alias.upper() for alias in aliases):
                return target
                
        return None
    
    @staticmethod
    def extract_company_topic_data(session_data, company_list, aliases_dict):
        """
        Extract company and topic data from session data.
        
        Args:
            session_data: List of session data by day
            company_list: List of standardized company names to match
            aliases_dict: Dictionary mapping standardized names to lists of aliases
            
        Returns:
            List of dictionaries with company, topic, and count information
        """
        company_topic_data = []
        
        for day_data in session_data:
            for session in day_data["sessions"]:
                # Skip sessions with no topic
                if not session.get("track") or pd.isna(session["track"]):
                    continue
                
                # Extract the high-level topic (before the first " - ")
                topic = session["track"]
                parts = topic.split(" - ")
                high_level_topic = parts[0].strip()
                
                # Skip if no valid topic
                if not high_level_topic or pd.isna(high_level_topic) or high_level_topic.lower() in ['n/a', 'nan', '']:
                    continue
                
                # Get companies from speaker_companies field
                companies = session.get("speaker_companies", [])
                if not companies:
                    continue
                
                # Track unique matched companies for this session
                matched_companies = set()
                
                # Process each company
                for company in companies:
                    if not company or pd.isna(company) or company.lower() in ['n/a', 'nan', '']:
                        continue
                        
                    # Try to match to one of our target companies
                    matched_company = CompanyMatcher.match_company(company, company_list, aliases_dict)
                    if matched_company:
                        matched_companies.add(matched_company)
                
                # Add data for each matched company
                for company in matched_companies:
                    company_topic_data.append({
                        "Company": company,
                        "Topic": high_level_topic,
                        "Count": 1,
                        "Session_ID": session.get("session_code", "")
                    })
        
        return company_topic_data
    
class TopicAnalyzer:
    """Utility for analyzing topic data from sessions."""
    
    @staticmethod
    def extract_topic_data(sessions):
        """
        Extract high-level topics from session data and count occurrences.
        
        Args:
            sessions: List of Session objects
            
        Returns:
            Dictionary mapping topics to their counts
        """
        topic_data = {}
        
        for session in sessions:
            # Skip sessions with no topic or NaN/N/A topics
            if not session.topic or pd.isna(session.topic) or session.topic.lower() in ['n/a', 'nan', '']:
                continue
                
            # Extract the high-level topic (before the first " - ")
            parts = session.topic.split(" - ")
            high_level_topic = parts[0].strip()
            
            # Skip empty or N/A high-level topics
            if not high_level_topic or pd.isna(high_level_topic) or high_level_topic.lower() in ['n/a', 'nan', '']:
                continue
                
            if high_level_topic in topic_data:
                topic_data[high_level_topic] += 1
            else:
                topic_data[high_level_topic] = 1
        
        return topic_data
    
    @staticmethod
    def extract_hierarchical_topic_data(sessions):
        """
        Extract hierarchical topic data (high-level and sub-topics) from sessions.
        
        Args:
            sessions: List of Session objects
            
        Returns:
            List of dictionaries with high-level topic, sub-topic, and count information
        """
        treemap_data = []
        
        for session in sessions:
            if session.topic and not pd.isna(session.topic):
                parts = session.topic.split(" - ")
                high_level = parts[0].strip()
                sub_topic = parts[1].strip() if len(parts) > 1 else "General"
                
                # Skip if high-level topic is empty or N/A
                if not high_level or pd.isna(high_level) or high_level.lower() in ['n/a', 'nan', '']:
                    continue
                
                treemap_data.append({
                    "High-Level Topic": high_level,
                    "Sub-Topic": sub_topic,
                    "Count": 1
                })
        
        return treemap_data
