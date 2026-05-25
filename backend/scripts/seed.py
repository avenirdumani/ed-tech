"""
Seed script for development. Populates the database with representative data
covering all models.

    python -m scripts.seed
"""

from datetime import date, timedelta
from typing import NamedTuple

from src.core.constants import (
    ChecklistItemStatus,
    DegreeType,
    EvidenceType,
    RequirementType,
    TimelineEventStatus,
)
from src.core.db import LocalSessionMaker, engine
from src.core.db.mixins import Base
from src.core.models import (
    ChecklistItem,
    Program,
    ProgramRequirement,
)

TODAY = date.today()

# ---------------------------------------------------------------------------
# Requirement specs
# ---------------------------------------------------------------------------
ReqSpec = tuple[str, RequirementType, str, EvidenceType, int]

_TRANSCRIPT: ReqSpec = (
    "Transcript",
    RequirementType.TRANSCRIPT,
    "Official transcripts from all prior institutions attended.",
    EvidenceType.DOCUMENT,
    0,
)
_RESUME: ReqSpec = (
    "Resume / CV",
    RequirementType.RESUME,
    "Current resume or curriculum vitae.",
    EvidenceType.DOCUMENT,
    0,
)
_SOP: ReqSpec = (
    "Statement of Purpose",
    RequirementType.ESSAY,
    "1–2 page statement of academic and professional goals.",
    EvidenceType.TEXT,
    0,
)
_LOR_1: ReqSpec = (
    "Letter of Recommendation 1",
    RequirementType.RECOMMENDATION_LETTER,
    "Academic or professional recommendation.",
    EvidenceType.DOCUMENT,
    14,
)
_LOR_2: ReqSpec = (
    "Letter of Recommendation 2",
    RequirementType.RECOMMENDATION_LETTER,
    "Second academic or professional recommendation.",
    EvidenceType.DOCUMENT,
    14,
)
_LOR_3: ReqSpec = (
    "Letter of Recommendation 3",
    RequirementType.RECOMMENDATION_LETTER,
    "Third academic or professional recommendation.",
    EvidenceType.DOCUMENT,
    14,
)
_GRE: ReqSpec = (
    "GRE General Test",
    RequirementType.TEST_SCORE,
    "GRE scores (verbal, quantitative, and analytical writing).",
    EvidenceType.SCORE,
    0,
)
_GMAT: ReqSpec = (
    "GMAT or GRE",
    RequirementType.TEST_SCORE,
    "GMAT or GRE scores.",
    EvidenceType.SCORE,
    0,
)
_RESEARCH_PROPOSAL: ReqSpec = (
    "Research Proposal",
    RequirementType.ESSAY,
    "3–5 page proposal outlining your intended dissertation focus.",
    EvidenceType.TEXT,
    0,
)
_WRITING_SAMPLE: ReqSpec = (
    "Writing Sample",
    RequirementType.ESSAY,
    "Scholarly writing sample (15–25 pages).",
    EvidenceType.DOCUMENT,
    0,
)
_PORTFOLIO: ReqSpec = (
    "Portfolio",
    RequirementType.PORTFOLIO,
    "Link to a portfolio of past work or creative projects.",
    EvidenceType.URL,
    0,
)
_INTERVIEW: ReqSpec = (
    "Interview",
    RequirementType.INTERVIEW,
    "Panel or one-on-one interview with faculty or admissions staff.",
    EvidenceType.DOCUMENT,
    0,
)

# Requirement set templates
_MS_BASE = [_TRANSCRIPT, _RESUME, _SOP, _LOR_1, _LOR_2]
_MS_STEM = [_TRANSCRIPT, _RESUME, _SOP, _LOR_1, _LOR_2, _GRE]
_MS_RES = [_TRANSCRIPT, _RESUME, _SOP, _LOR_1, _LOR_2, _WRITING_SAMPLE]
_MBA = [_TRANSCRIPT, _RESUME, _SOP, _LOR_1, _LOR_2, _GMAT, _INTERVIEW]
_PHD_STEM = [
    _TRANSCRIPT,
    _RESUME,
    _SOP,
    _LOR_1,
    _LOR_2,
    _LOR_3,
    _GRE,
    _RESEARCH_PROPOSAL,
]
_PHD_SOC = [
    _TRANSCRIPT,
    _RESUME,
    _SOP,
    _LOR_1,
    _LOR_2,
    _LOR_3,
    _WRITING_SAMPLE,
    _RESEARCH_PROPOSAL,
]
_MFA = [_TRANSCRIPT, _RESUME, _SOP, _LOR_1, _LOR_2, _PORTFOLIO]


# ---------------------------------------------------------------------------
# Program catalogue
# ---------------------------------------------------------------------------
class ProgramDef(NamedTuple):
    name: str
    degree_type: DegreeType
    deadline_offset: int  # days from today
    req_template: list[ReqSpec]


CATALOG: list[ProgramDef] = [
    # Computer Science & Technology
    ProgramDef("Computer Science", DegreeType.MS, 120, _MS_STEM),
    ProgramDef("Artificial Intelligence", DegreeType.MS, 110, _MS_STEM),
    ProgramDef("Cybersecurity", DegreeType.MS, 100, _MS_STEM),
    ProgramDef("Human-Computer Interaction", DegreeType.MS, 130, _MS_STEM),
    ProgramDef("Software Engineering", DegreeType.MS, 115, _MS_BASE),
    ProgramDef("Computer Engineering", DegreeType.MS, 105, _MS_STEM),
    ProgramDef("Data Science", DegreeType.PHD, 90, _PHD_STEM),
    ProgramDef("Computer Science", DegreeType.PHD, 85, _PHD_STEM),
    # Business
    ProgramDef("Business Administration", DegreeType.MBA, 80, _MBA),
    ProgramDef("Business Analytics", DegreeType.MS, 95, _MS_STEM),
    ProgramDef("Finance", DegreeType.MS, 85, _MS_BASE),
    ProgramDef("Accounting", DegreeType.MS, 75, _MS_BASE),
    ProgramDef("Marketing", DegreeType.MS, 70, _MS_BASE),
    ProgramDef("Supply Chain Management", DegreeType.MS, 65, _MS_BASE),
    ProgramDef("Information Systems", DegreeType.MS, 60, _MS_STEM),
    # Mathematics & Statistics
    ProgramDef("Statistics", DegreeType.MS, 100, _MS_STEM),  # 15 ← Alice applies
    ProgramDef("Applied Mathematics", DegreeType.MS, 110, _MS_STEM),
    ProgramDef("Operations Research", DegreeType.MS, 90, _MS_STEM),
    ProgramDef("Biostatistics", DegreeType.PHD, 85, _PHD_STEM),
    # Engineering
    ProgramDef("Electrical Engineering", DegreeType.MS, 100, _MS_STEM),
    ProgramDef("Mechanical Engineering", DegreeType.MS, 95, _MS_STEM),
    ProgramDef("Civil Engineering", DegreeType.MS, 90, _MS_STEM),
    ProgramDef("Chemical Engineering", DegreeType.PHD, 80, _PHD_STEM),
    ProgramDef("Biomedical Engineering", DegreeType.MS, 75, _MS_STEM),
    ProgramDef("Environmental Engineering", DegreeType.MS, 70, _MS_STEM),
    # Natural Sciences
    ProgramDef("Biology", DegreeType.PHD, 65, _PHD_STEM),
    ProgramDef("Chemistry", DegreeType.MS, 70, _MS_STEM),
    ProgramDef("Physics", DegreeType.PHD, 60, _PHD_STEM),
    ProgramDef("Neuroscience", DegreeType.PHD, 75, _PHD_STEM),
    ProgramDef("Environmental Science", DegreeType.MS, 90, _MS_STEM),
    # Social Sciences & Humanities
    ProgramDef("Psychology", DegreeType.PHD, 80, _PHD_SOC),
    ProgramDef("Economics", DegreeType.PHD, 85, _PHD_SOC),
    ProgramDef("Public Administration", DegreeType.MS, 100, _MS_RES),
    ProgramDef("International Relations", DegreeType.MS, 95, _MS_RES),
    # Health & Social Services
    ProgramDef("Public Health", DegreeType.MS, 75, _MS_BASE),
    ProgramDef("Healthcare Administration", DegreeType.MS, 70, _MS_BASE),
    ProgramDef("Social Work", DegreeType.MS, 65, _MS_BASE),
    # Arts & Design
    ProgramDef("Fine Arts", DegreeType.MFA, 60, _MFA),
    ProgramDef("Graphic Design", DegreeType.MFA, 55, _MFA),
]

# Indices into CATALOG for Alice's applications
ALICE_APPLIES_TO = [0, 1, 7, 9, 15]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def _checklist_status(due: date) -> ChecklistItemStatus:
    if due < TODAY:
        return ChecklistItemStatus.COMPLETE
    if due <= TODAY + timedelta(days=14):
        return ChecklistItemStatus.IN_PROGRESS
    return ChecklistItemStatus.NOT_STARTED


def _timeline_status(item: ChecklistItem) -> TimelineEventStatus:
    if item.status == ChecklistItemStatus.COMPLETE:
        return TimelineEventStatus.COMPLETED
    if item.due_date and item.due_date < TODAY:
        return TimelineEventStatus.OVERDUE
    if item.due_date and item.due_date <= TODAY + timedelta(days=14):
        return TimelineEventStatus.DUE_SOON
    return TimelineEventStatus.UPCOMING


# ---------------------------------------------------------------------------
# Seed
# ---------------------------------------------------------------------------
def seed() -> None:
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    with LocalSessionMaker() as session:

        for idx, defn in enumerate(CATALOG):
            prog = Program(
                name=defn.name,
                degree_type=defn.degree_type,
                application_deadline=TODAY + timedelta(days=defn.deadline_offset),
            )
            session.add(prog)
            session.flush()

            reqs = [
                ProgramRequirement(
                    title=title,
                    type=req_type,
                    description=desc,
                    evidence_type=ev_type,
                    due_offset_days=offset,
                    program_id=prog.id,
                )
                for title, req_type, desc, ev_type, offset in defn.req_template
            ]
            session.add_all(reqs)
            session.flush()
            session.commit()


if __name__ == "__main__":
    seed()
