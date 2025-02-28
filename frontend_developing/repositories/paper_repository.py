from models import (
    Paper,
    ConferenceInstance,
    Author,
    Reference,
    Keyword,
    Conference,
    Affiliation,
    paper_author,
    AuthorAffiliation,
    PaperKeyword,
)

from config import TRACKED_ORGANIZATIONS


class PaperRepository:
    def __init__(self, session):
        self.session = session

    def _get_author(self, author_id: str) -> Author:
        author = self.session.query(Author).filter_by(author_id=author_id).first()
        if not author:
            raise ValueError(f"Author {author_id} not found.")
        return author

    def _get_reference(self, title: str) -> Reference:
        reference = self.session.query(Reference).filter_by(title=title).first()
        if not reference:
            raise ValueError(f"Reference {title} not found.")
        return reference

    def _get_keyword(self, keyword: str) -> Keyword:
        keyword = self.session.query(Keyword).filter_by(keyword=keyword).first()
        if not keyword:
            raise ValueError(f"Keyword {keyword} not found.")
        return keyword

    def upsert(
        self,
        title: str,
        year: int,
        instance_id: str,
        author_ids: list = None,
        references: list = None,
        keywords: list = None,
        **kwargs,
    ) -> Paper:
        paper = (
            self.session.query(Paper)
            .filter_by(instance_id=instance_id, title=title)
            .first()
        )
        if paper:
            for key, value in kwargs.items():
                setattr(paper, key, value)
        else:
            paper = Paper(instance_id=instance_id, title=title, year=year, **kwargs)
            self.session.add(paper)

        if author_ids:
            paper.author_to_paper = []
            for authorid in author_ids:
                author_obj = self._get_author(author_id=authorid)
                paper.author_to_paper.append(author_obj)
        if references:
            paper.reference_to_paper = []
            for reference in references:
                reference_obj = self._get_reference(title=reference["title"])
                paper.reference_to_paper.append(reference_obj)
        if keywords:
            paper.keyword_to_paper = []
            for kw in keywords:
                keyword_obj = self._get_keyword(keyword=kw)
                paper.keyword_to_paper.append(keyword_obj)

        self.session.commit()
        return paper

    def get_papers_by_conference(self, conference: str, year: int) -> list[Paper]:
        """Get papers for a specific conference and year."""
        return (
            self.session.query(Paper)
            .join(ConferenceInstance)
            .join(Conference)
            .filter(Conference.name == conference)
            .filter(ConferenceInstance.year == year)
            .all()
        )

    def get_papers_by_organization(self, organization: str) -> list[Paper]:
        if organization not in TRACKED_ORGANIZATIONS:
            raise ValueError(f"Organization {organization} is not in the tracked list")

        return (
            self.session.query(Paper)
            .join(paper_author)
            .join(Author)
            .join(AuthorAffiliation)
            .join(Affiliation)
            .filter(Affiliation.name == organization)
            .all()
        )

    def get_papers_by_keyword(self, keyword: str) -> list[Paper]:
        """Get papers with a specific keyword."""
        return (
            self.session.query(Paper)
            .join(PaperKeyword)
            .join(Keyword)
            .filter(Keyword.keyword == keyword)
            .all()
        )

    def get_paper_details(self, paper_id: int) -> dict[str, any]:
        """Get detailed information about a paper."""
        paper = self.session.query(Paper).get(paper_id)
        if not paper:
            return None

        return {
            "title": paper.title,
            "authors": [author.name for author in paper.author_to_paper],
            "conference": paper.instance_to_paper.conference_name,
            "year": paper.year,
            "citations": paper.citation_count,
            "keywords": [kw.keyword for kw in paper.keyword_to_paper],
            "abstract": paper.abstract,
            "pdf_url": paper.pdf_url,
        }
