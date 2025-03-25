import re
import pandas as pd
from models import Speaker, Affiliation
from sqlalchemy import or_


class SpeakerRepository:
    def __init__(self, session):
        self.session = session

    def _clean_name(self, name: str) -> str:
        """Clean name by removing special characters and standardizing format"""
        if not name:
            return name

        # Convert to uppercase for standardization
        name = name.upper()

        # Remove special characters and extra whitespace
        name = re.sub(r"[^\w\s]", "", name)
        name = re.sub(r"\s+", " ", name).strip()

        # Common abbreviation standardization
        replacements = {
            "MASSACHUSETTS INSTITUTE OF TECHNOLOGY": "MIT",
            "MASS INST OF TECH": "MIT",
            "MASS INSTITUTE OF TECHNOLOGY": "MIT",
            # Add more common variations as needed
        }
        return replacements.get(name, name)

    def _get_affiliation(self, name: str) -> Affiliation:
        affiliation = self.session.query(Affiliation).filter_by(name=name).first()
        if not affiliation:
            cleaned_name = self._clean_name(name)
            affiliation = (
                self.session.query(Affiliation)
                .filter(
                    or_(
                        Affiliation.aliases.contains(
                            [cleaned_name]
                        ),  # Check if cleaned_name is in aliases
                        Affiliation.name == cleaned_name,
                    )
                )
                .first()
            )
        if not affiliation:
            affiliation = Affiliation(name=cleaned_name)
            self.session.add(affiliation)
            self.session.commit()
        return affiliation

    def get_speaker(self, name: str, affil_id: int) -> Speaker:
        return self.session.query(Speaker).filter_by(name=name, affiliation_id=affil_id).first()

    def upsert(self, name: str, affiliation: str, position: str) -> Speaker:
        affil_obj = self._get_affiliation(name=affiliation)
        speaker = self.get_speaker(name, affil_obj.affiliation_id)
        if speaker:
            speaker.position = position
        else:
            speaker = Speaker(name=name, affiliation_id=affil_obj.affiliation_id, position=position)
            self.session.add(speaker)

        self.session.commit()
        return speaker
    
    def get_company_topic_data(self, instance_id):
        """
        Get company and topic data for sessions in a conference instance.
        
        Args:
            instance_id: The ID of the conference instance
            
        Returns:
            A list of dictionaries with company, topic, and count information
        """
        # Query to get sessions with their speakers and affiliations
        query = """
        SELECT 
            s.session_id, 
            s.topic, 
            sp.name as speaker_name, 
            a.name as company_name
        FROM 
            session s
        JOIN 
            session_speaker ss ON s.session_id = ss.session_id
        JOIN 
            speaker sp ON ss.speaker_id = sp.speaker_id
        LEFT JOIN 
            affiliation a ON sp.affiliation_id = a.affiliation_id
        WHERE 
            s.instance_id = :instance_id
        """
        
        result = self.session.execute(query, {"instance_id": instance_id})
        
        # Process the results
        company_topic_data = []
        for row in result:
            # Skip if no topic or company
            if not row.topic or pd.isna(row.topic) or not row.company_name or pd.isna(row.company_name):
                continue
                
            # Extract the high-level topic (before the first " - ")
            parts = row.topic.split(" - ")
            high_level_topic = parts[0].strip()
            
            # Skip empty or N/A values
            if (not high_level_topic or pd.isna(high_level_topic) or 
                high_level_topic.lower() in ['n/a', 'nan', ''] or
                not row.company_name or pd.isna(row.company_name) or
                row.company_name.lower() in ['n/a', 'nan', '']):
                continue
                
            company_topic_data.append({
                "Company": row.company_name,
                "Topic": high_level_topic,
                "Count": 1
            })
        
        return company_topic_data
