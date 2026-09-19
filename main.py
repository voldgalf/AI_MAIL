from server import server_manager
from sessions import session_manager
from database import engine_manager
from routes import router
import tomllib
from pathlib import Path

config = tomllib.loads(Path("./config.toml").read_text())

session_manager.start(config)
engine_manager.start(config)

server_manager.app.include_router(router)

server_manager.run(config)