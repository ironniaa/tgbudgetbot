from bot.database.database import engine
from bot.models.expense import Base


def init_db():
    Base.metadata.create_all(bind=engine)