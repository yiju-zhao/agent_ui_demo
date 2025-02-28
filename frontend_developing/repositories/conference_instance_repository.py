from models import Conference, ConferenceInstance, Paper
from typing import Optional
from sqlalchemy import func


class ConferenceInstanceRepository:
    def __init__(self, session):
        self.session = session

    def upsert(
        self, conference_id: str, name: str, year: int, **kwargs
    ) -> ConferenceInstance:
        conference = (
            self.session.query(Conference)
            .filter_by(conference_id=conference_id)
            .first()
        )
        if not conference:
            raise ValueError("Conference not found")

        instance = (
            self.session.query(ConferenceInstance)
            .filter_by(conference_id=conference_id, year=year)
            .first()
        )
        if instance:
            for key, value in kwargs.items():
                setattr(instance, key, value)
        else:
            instance = ConferenceInstance(
                conference_id=conference_id, conference_name=name, year=year, **kwargs
            )
            self.session.add(instance)

        self.session.commit()
        return instance

    def get_all_conferences(self) -> list[str]:
        """Get list of all conference names."""
        conferences = self.session.query(Conference.name).distinct().all()
        return sorted([conf[0] for conf in conferences])

    def get_all_years(self) -> list[int]:
        """Get all available years from the database, sorted in descending order."""
        years = (
            self.session.query(ConferenceInstance.year)
            .distinct()
            .order_by(ConferenceInstance.year.desc())
            .all()
        )
        return [year[0] for year in years]

    def get_conferences_by_year(self, year: int) -> list[str]:
        """Get all conferences that have papers in a specific year."""
        conferences = (
            self.session.query(Conference.name)
            .join(ConferenceInstance)
            .filter(ConferenceInstance.year == year)
            .distinct()
            .order_by(Conference.name)
            .all()
        )
        return [conf[0] for conf in conferences]

    def get_conference_years(self, conference: str) -> list[int]:
        """Get available years for a specific conference."""
        years = (
            self.session.query(ConferenceInstance.year)
            .join(Conference)
            .filter(Conference.name == conference)
            .distinct()
            .order_by(ConferenceInstance.year.desc())
            .all()
        )
        return [year[0] for year in years]

    def get_conference_stats(
        self, conference: str, year: Optional[int] = None
    ) -> list[tuple]:
        try:
            query = (
                self.session.query(
                    ConferenceInstance, func.count(Paper.paper_id).label("paper_count")
                )
                .select_from(Conference)
                .join(
                    ConferenceInstance,
                    Conference.conference_id == ConferenceInstance.conference_id,
                )
                .outerjoin(Paper, ConferenceInstance.instance_id == Paper.instance_id)
                .filter(Conference.name == conference)
            )

            if year and year != "All Years":
                query = query.filter(ConferenceInstance.year == year)

            query = query.group_by(ConferenceInstance).order_by(
                ConferenceInstance.year.desc()
            )
            return query.all()

        except Exception as e:
            print(f"Error in get_conference_stats: {str(e)}")
            return []

    def get_yearly_conference_stats(self, year: int) -> list[tuple]:
        """Get statistics for all conferences in a specific year."""
        return (
            self.session.query(
                Conference.name,
                func.count(Paper.paper_id),
            )
            .select_from(Conference)
            .join(
                ConferenceInstance,
                Conference.conference_id == ConferenceInstance.conference_id,
            )
            .outerjoin(Paper, ConferenceInstance.instance_id == Paper.instance_id)
            .filter(ConferenceInstance.year == year)
            .group_by(Conference.name)
            .all()
        )
