from typer import Typer
from app.providers.init_db import init_db
from app.providers.database import SessionLocal
from app.utils.coroutine import coro_wrap

db_app = Typer()


@db_app.command()
@coro_wrap
async def init() -> None:
    db = SessionLocal()
    print("start init db.")
    await init_db(db)
    print("initial data created.")


main = Typer()
main.add_typer(db_app, name="db")


if __name__ == "__main__":
    main()
