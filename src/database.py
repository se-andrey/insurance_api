from tortoise import Tortoise

from .config import DATABASE_URL
from .logger import logger


async def init_db():
    await Tortoise.init(
        db_url=DATABASE_URL,
        modules={"models": ["src.api.models"]},
    )
    await Tortoise.generate_schemas()
    logger.info("Init db")


async def close_db():
    await Tortoise.close_connections()
    logger.info("Close db")


def create_db_session():
    return Tortoise.get_connection("default")
