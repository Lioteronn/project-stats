import asyncio
import logging
import os
from pathlib import Path

from dotenv import load_dotenv
from nextcord.ext import commands
from tortoise import Tortoise

load_dotenv()


def get_model_modules():
    models_dir = Path("models")
    if not models_dir.exists():
        return ["models.users"]

    model_files = []
    for py_file in models_dir.glob("*.py"):
        if py_file.name != "__init__.py":
            module_path = (
                str(py_file).replace("/", ".").replace("\\", ".").replace(".py", "")
            )
            model_files.append(module_path)

    return model_files if model_files else ["models.users"]


def setup_logging() -> None:
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )


async def init_db() -> None:
    db_url = os.getenv("SUPABASE_URL")
    if not db_url:
        print("Warning: No SUPABASE_URL found. Using SQLite database.")
        db_url = "sqlite://./project_stats.db"

    print(f"Connecting to database: {db_url}")

    try:
        await Tortoise.init(
            db_url=db_url,
            modules={"models": get_model_modules()},
        )
        await Tortoise.generate_schemas()
        print("Database initialized successfully!")
    except Exception as e:
        print(f"Database initialization failed: {e}")
        raise


async def main() -> None:
    setup_logging()

    await init_db()

    bot = commands.Bot(command_prefix="!")

    @bot.event
    async def on_ready():
        print(f"Logged in as {bot.user}")

    token = os.getenv("TOKEN")
    if not token:
        print("Warning: No Discord token found. Set the TOKEN environment variable.")
        return

    await bot.start(token)


if __name__ == "__main__":
    asyncio.run(main())
