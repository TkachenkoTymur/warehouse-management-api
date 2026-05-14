from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
from sqlalchemy import engine_from_config, pool, text 

from config import get_settings
from src.db.entities import Base

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata

config.set_main_option("sqlalchemy.url", get_settings().DATABASE_URL)

SCHEMA_NAME = "py_khnu"

def include_object(object, name, type_, reflected, compare_to):
    """Фільтруємо об'єкти, щоб Alembic бачив тільки нашу схему (ст. 13)"""
    if type_ == "table":
        return object.schema == SCHEMA_NAME
    return True

def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        include_object=include_object,
        include_schemas=True,
        version_table_schema=SCHEMA_NAME
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        connection.execute(text(f'CREATE SCHEMA IF NOT EXISTS {SCHEMA_NAME}'))
        
        context.configure(
            connection=connection, 
            target_metadata=target_metadata,
            include_object=include_object,
            include_schemas=True,
            version_table_schema=SCHEMA_NAME
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()