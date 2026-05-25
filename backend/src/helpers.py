from src.core.db import engine
from src.core.db.mixins import Base
from src.core.models import *


def create_all_models() -> None:
    Base.metadata.create_all(bind=engine)
