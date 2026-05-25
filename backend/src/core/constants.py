from enum import Enum


class UserRole(str, Enum):
    APPLICANT = "applicant"
    COUNSELOR = "counselor"


class DegreeType(str, Enum):
    BS = "bs"
    MS = "ms"
    PHD = "phd"
    MBA = "mba"
    MFA = "mfa"


class RequirementType(str, Enum):
    TRANSCRIPT = "transcript"
    TEST_SCORE = "test_score"
    ESSAY = "essay"
    RECOMMENDATION_LETTER = "recommendation_letter"
    RESUME = "resume"
    PORTFOLIO = "portfolio"
    INTERVIEW = "interview"


class EvidenceType(str, Enum):
    DOCUMENT = "document"
    SCORE = "score"
    TEXT = "text"
    URL = "url"


class ChecklistItemStatus(str, Enum):
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETE = "complete"


class TimelineEventStatus(str, Enum):
    UPCOMING = "upcoming"
    DUE_SOON = "due_soon"
    OVERDUE = "overdue"
    COMPLETED = "completed"
