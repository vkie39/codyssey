from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context

config = context.config
fileConfig(config.config_file_name)

# 🔥 여기 추가
import models
from database import Base

target_metadata = Base.metadata
