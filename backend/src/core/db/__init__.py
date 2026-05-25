from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.core.settings import app_settings

engine = create_engine(url=app_settings.db_url)
LocalSessionMaker = sessionmaker(bind=engine)
