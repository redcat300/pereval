import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from alembic import context
from logging.config import fileConfig
from database import Base
from models import User, Coords, Level, Image, PerevalAdded


load_dotenv()

FSTR_DB_HOST = os.getenv('FSTR_DB_HOST')
FSTR_DB_PORT = os.getenv('FSTR_DB_PORT')
FSTR_DB_LOGIN = os.getenv('FSTR_DB_LOGIN')
FSTR_DB_PASS = os.getenv('FSTR_DB_PASS')
FSTR_DB_NAME = os.getenv('FSTR_DB_NAME')


config = context.config
config.set_main_option('sqlalchemy.url', f'postgresql://{FSTR_DB_LOGIN}:{FSTR_DB_PASS}@{FSTR_DB_HOST}:{FSTR_DB_PORT}/{FSTR_DB_NAME}')

# Logging configuration
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Set metadata
target_metadata = Base.metadata

def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(url=url, target_metadata=target_metadata, literal_binds=True)

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    """Run migrations in 'online' mode."""
    connectable = create_engine(config.get_main_option("sqlalchemy.url"))

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
