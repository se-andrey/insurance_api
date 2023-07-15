from tortoise import Tortoise
from .config import DATABASE_URL


async def init_db():
    await Tortoise.init(
        db_url=DATABASE_URL,
        modules={"models": ["src.api.models"]},
    )
    await Tortoise.generate_schemas()


async def close_db():
    await Tortoise.close_connections()


def create_db_session():
    return Tortoise.get_connection("default")
