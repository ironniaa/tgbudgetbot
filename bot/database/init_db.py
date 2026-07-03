from alembic.config import Config
from alembic import command

from bot.services.backup_service import backup_database


def init_db():
    backup_database()

    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")