from datetime import date

import pytest
from fastapi.testclient import TestClient

from src.app.main import app
from src.core.constants import DegreeType, EvidenceType, RequirementType
from src.core.db import LocalSessionMaker, engine
from src.core.db.mixins import Base
from src.core.models import Program, ProgramRequirement


@pytest.fixture(autouse=True, scope="function")
def clean_db() -> None:
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


@pytest.fixture(scope="function")
def api_client() -> TestClient:
    return TestClient(app=app)


@pytest.fixture(scope="function")
def programs() -> list[Program]:
    db = LocalSessionMaker()
    try:
        program_a = Program(
            name="Computer Science MS",
            degree_type=DegreeType.MS,
            application_deadline=date(2026, 12, 15),
            requirements=[
                ProgramRequirement(
                    title="Official Transcripts",
                    type=RequirementType.TRANSCRIPT,
                    description="Official transcripts from all post-secondary institutions attended.",
                    evidence_type=EvidenceType.DOCUMENT,
                    due_offset_days=0,
                    required=True,
                ),
                ProgramRequirement(
                    title="GRE Scores",
                    type=RequirementType.TEST_SCORE,
                    description="Official GRE general test scores sent directly from ETS.",
                    evidence_type=EvidenceType.SCORE,
                    due_offset_days=0,
                    required=True,
                ),
                ProgramRequirement(
                    title="Statement of Purpose",
                    type=RequirementType.ESSAY,
                    description="A 500–1000 word essay describing your research interests and goals.",
                    evidence_type=EvidenceType.TEXT,
                    due_offset_days=0,
                    required=True,
                ),
                ProgramRequirement(
                    title="Letters of Recommendation",
                    type=RequirementType.RECOMMENDATION_LETTER,
                    description="Three letters from academic or professional references.",
                    evidence_type=EvidenceType.DOCUMENT,
                    due_offset_days=7,
                    required=True,
                ),
                ProgramRequirement(
                    title="Resume / CV",
                    type=RequirementType.RESUME,
                    description="Current resume or curriculum vitae.",
                    evidence_type=EvidenceType.DOCUMENT,
                    due_offset_days=0,
                    required=True,
                ),
            ],
        )
        program_b = Program(
            name="Business Administration MBA",
            degree_type=DegreeType.MBA,
            application_deadline=date(2027, 1, 15),
            requirements=[
                ProgramRequirement(
                    title="Official Transcripts",
                    type=RequirementType.TRANSCRIPT,
                    description="Official transcripts from all post-secondary institutions attended.",
                    evidence_type=EvidenceType.DOCUMENT,
                    due_offset_days=0,
                    required=True,
                ),
                ProgramRequirement(
                    title="GMAT / GRE Scores",
                    type=RequirementType.TEST_SCORE,
                    description="Official GMAT or GRE scores no older than five years.",
                    evidence_type=EvidenceType.SCORE,
                    due_offset_days=0,
                    required=True,
                ),
                ProgramRequirement(
                    title="Personal Statement",
                    type=RequirementType.ESSAY,
                    description="A 750-word essay on your professional goals and how the MBA will help you achieve them.",
                    evidence_type=EvidenceType.TEXT,
                    due_offset_days=0,
                    required=True,
                ),
                ProgramRequirement(
                    title="Letters of Recommendation",
                    type=RequirementType.RECOMMENDATION_LETTER,
                    description="Two professional references, preferably from direct supervisors.",
                    evidence_type=EvidenceType.DOCUMENT,
                    due_offset_days=7,
                    required=True,
                ),
                ProgramRequirement(
                    title="Resume",
                    type=RequirementType.RESUME,
                    description="Current resume highlighting at least two years of work experience.",
                    evidence_type=EvidenceType.DOCUMENT,
                    due_offset_days=0,
                    required=True,
                ),
                ProgramRequirement(
                    title="Admissions Interview",
                    type=RequirementType.INTERVIEW,
                    description="A 30-minute virtual interview with the admissions committee.",
                    evidence_type=EvidenceType.URL,
                    due_offset_days=14,
                    required=False,
                ),
            ],
        )
        db.add_all([program_a, program_b])
        db.commit()
        db.refresh(program_a)
        db.refresh(program_b)
        yield [program_a, program_b]
    finally:
        db.close()
