"""
Alembic Environment Configuration for FinPilot AI.

This file tells Alembic:
1. WHERE to connect (our PostgreSQL database from .env)
2. WHAT tables to create (by importing all our SQLAlchemy models)
"""
from logging.config import fileConfig
import os

from sqlalchemy import engine_from_config
from sqlalchemy import pool
from dotenv import load_dotenv

from alembic import context

# --- Step 1: Load environment variables from our .env file ---
# The .env file is one folder above /backend, so we go up two levels
# (from /backend/alembic/env.py → /trading_ai/.env)
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", "..", ".env"))

# --- Step 2: Import our Base class and ALL models ---
# Importing Base gives Alembic the MetaData object it needs.
# Importing models/__init__.py ensures every table is "registered" with Base.
from core.database import Base
import models  # This triggers models/__init__.py which imports all model classes

# --- Step 3: Standard Alembic setup ---
# This is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Override the dummy sqlalchemy.url from alembic.ini with our real DATABASE_URL
config.set_main_option("sqlalchemy.url", os.environ["DATABASE_URL"])

# Interpret the config file for Python logging.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# --- Step 4: Point Alembic at our models' metadata ---
# This is the key line that enables "autogenerate" to detect our tables.
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.
    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
