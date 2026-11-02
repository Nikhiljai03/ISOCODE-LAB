from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
from aranya_api.shared.config import get_settings
from aranya_api.shared.database import Base
from aranya_api.accommodations import models as accommodation_models
from aranya_api.booking import models as booking_models
from aranya_api.inventory import models as inventory_models
from aranya_api.enquiries import models as enquiry_models

config = context.config
if config.config_file_name:
    fileConfig(config.config_file_name)
config.set_main_option("sqlalchemy.url", get_settings().database_url)
target_metadata = Base.metadata


def run_migrations_online() -> None:
    connectable = engine_from_config(config.get_section(config.config_ini_section, {}), prefix="sqlalchemy.", poolclass=pool.NullPool)
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()

run_migrations_online()
