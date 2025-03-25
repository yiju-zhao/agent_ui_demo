from typing import Optional
from sqlalchemy import text
from sqlalchemy.orm import Session
from models import Session as SessionModel, Speaker
from datetime import datetime, time


class SessionRepository:
    def __init__(self, db_session: Session):
        self.session = db_session

    def _get_speaker(self, speaker_id: str) -> Speaker:
        speaker = self.session.query(Speaker).filter_by(speaker_id=speaker_id).first()
        if not speaker:
            raise ValueError(f"Speaker {speaker_id} not found.")
        return speaker

    def get_session(self, instance_id: int, session_id: int) -> Optional[SessionModel]:
        return (
            self.session.query(SessionModel)
            .filter_by(instance_id=instance_id, session_id=session_id)
            .first()
        )

    def upsert(
        self,
        instance_id: int,
        title: str,
        session_code: str,
        date: datetime,
        start_time: time,
        end_time: time,
        speaker_ids: list = None,
        **kwargs,
    ) -> SessionModel:

        # Check if session already exists
        existing_session = (
            self.session.query(SessionModel)
            .filter(
                SessionModel.instance_id == instance_id,
                SessionModel.session_code == session_code,
                SessionModel.date == date,
            )
            .first()
        )

        if existing_session:
            existing_session.title = title
            existing_session.start_time = start_time
            existing_session.end_time = end_time
            for key, value in kwargs.items():
                setattr(existing_session, key, value)

            session_obj = existing_session
        else:
            # Create new session
            session_obj = SessionModel(
                instance_id=instance_id,
                title=title,
                session_code=session_code,
                date=date,
                start_time=start_time,
                end_time=end_time,
                **kwargs,
            )
            self.session.add(session_obj)
            self.session.flush()

        if speaker_ids:
            # self.session.execute(
            #     text(f"DELETE FROM session_speaker WHERE session_id = {session_obj.session_id}")
            # )
            session_obj.speaker_to_session = []
            for speaker_id in speaker_ids:
                speaker_obj = self._get_speaker(speaker_id=speaker_id)
                session_obj.speaker_to_session.append(speaker_obj)

        self.session.commit()
        return session_obj

    def get_sessions_by_instance(self, instance_id: int) -> list:
        """
        Get all sessions for a specific conference instance.
        
        Args:
            instance_id (int): The conference instance ID
            
        Returns:
            list: List of Session objects
        """
        return self.session.query(SessionModel).filter_by(instance_id=instance_id).all()

    def get_sessions_by_date(self, instance_id: int, date: datetime.date) -> list:
        """
        Get sessions for a specific conference instance and date.
        
        Args:
            instance_id (int): The conference instance ID
            date (datetime.date): The date to filter by
            
        Returns:
            list: List of Session objects
        """
        return self.session.query(SessionModel).filter_by(
            instance_id=instance_id, 
            date=date
        ).all()

    def get_session_dates(self, instance_id: int) -> list:
        """
        Get all unique dates for sessions in a conference instance.
        
        Args:
            instance_id (int): The conference instance ID
            
        Returns:
            list: List of dates
        """
        from sqlalchemy import func
        result = self.session.query(
            func.distinct(SessionModel.date)
        ).filter_by(
            instance_id=instance_id
        ).order_by(
            SessionModel.date
        ).all()
        
        return [date[0] for date in result]

    def get_session_tracks(self, instance_id: int) -> list:
        """
        Get all unique tracks/topics for sessions in a conference instance.
        
        Args:
            instance_id (int): The conference instance ID
            
        Returns:
            list: List of track names
        """
        from sqlalchemy import func
        result = self.session.query(
            func.distinct(SessionModel.topic)
        ).filter_by(
            instance_id=instance_id
        ).order_by(
            SessionModel.topic
        ).all()
        
        return [track[0] for track in result if track[0]]

    def get_session_venues(self, instance_id: int) -> list:
        """
        Get all unique venues for sessions in a conference instance.
        
        Args:
            instance_id (int): The conference instance ID
            
        Returns:
            list: List of venue names
        """
        from sqlalchemy import func
        result = self.session.query(
            func.distinct(SessionModel.venue)
        ).filter_by(
            instance_id=instance_id
        ).order_by(
            SessionModel.venue
        ).all()
        
        return [venue[0] for venue in result if venue[0]]

    def get_session_speakers(self, instance_id: int) -> list:
        """
        Get all speakers for sessions in a conference instance.
        
        Args:
            instance_id (int): The conference instance ID
            
        Returns:
            list: List of Speaker objects
        """
        return self.session.query(Speaker).join(
            SessionModel.speaker_to_session
        ).filter(
            SessionModel.instance_id == instance_id
        ).distinct().all()

    def get_session_companies(self, instance_id: int) -> list:
        """
        Get all unique companies (affiliations) for speakers in a conference instance.
        
        Args:
            instance_id (int): The conference instance ID
            
        Returns:
            list: List of company names
        """
        from sqlalchemy import func
        from models import Affiliation
        
        result = self.session.query(
            func.distinct(Affiliation.name)
        ).join(
            Speaker, Speaker.affiliation_id == Affiliation.affiliation_id
        ).join(
            SessionModel.speaker_to_session
        ).filter(
            SessionModel.instance_id == instance_id
        ).order_by(
            Affiliation.name
        ).all()
        
        return [company[0] for company in result if company[0]]

    def count_sessions_by_instance(self, instance_id: int) -> int:
        """
        Count the number of sessions for a specific conference instance.
        
        Args:
            instance_id (int): The conference instance ID
            
        Returns:
            int: The number of sessions
        """
        return self.session.query(SessionModel).filter_by(instance_id=instance_id).count()

    def count_speakers_by_instance(self, instance_id: int) -> int:
        """
        Count the number of unique speakers for a specific conference instance.
        
        Args:
            instance_id (int): The conference instance ID
            
        Returns:
            int: The number of speakers
        """
        return self.session.query(Speaker).join(
            SessionModel.speaker_to_session
        ).filter(
            SessionModel.instance_id == instance_id
        ).distinct().count()

    def get_top_tracks_by_session_count(self, instance_id: int, limit: int = 10) -> list:
        """
        Get the top tracks/topics by session count for a specific conference instance.
        
        Args:
            instance_id (int): The conference instance ID
            limit (int, optional): The maximum number of tracks to return
            
        Returns:
            list: List of (track, count) tuples
        """
        from sqlalchemy import func
        
        result = self.session.query(
            SessionModel.topic, func.count(SessionModel.session_id).label('session_count')
        ).filter_by(
            instance_id=instance_id
        ).group_by(
            SessionModel.topic
        ).order_by(
            func.count(SessionModel.session_id).desc()
        ).limit(limit).all()
        
        return result
