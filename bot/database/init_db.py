from alembic.config import Config
from alembic import command


def init_db():
    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")