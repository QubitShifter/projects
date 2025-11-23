# etl/db_pg.py
# Connects to localhost PostgreSQL (used as a stand-in for Db2)

import json
import os
from pathlib import Path
from typing import Any, Dict

import psycopg2
from dotenv import load_dotenv


# Load .env from the project root
project_root = Path(__file__).resolve().parent.parent
dotenv_path = project_root / "config" / ".env"

load_dotenv(dotenv_path=dotenv_path)

def load_config(config_path: str = "config/config.json") -> Dict[str, Any]:
    """
    Load PostgreSQL connection settings from a JSON file.
    Supports ${VAR} placeholders that are resolved from environment variables.
    """
    path = Path(config_path)
    if not path.exists():
        raise FileNotFoundError(f"Config file not found: {path}")

    with path.open() as f:
        raw = json.load(f)

    cfg: Dict[str, Any] = {}

    for key, value in raw.items():
        if isinstance(value, str) and value.startswith("${") and value.endswith("}"):
            env_name = value[2:-1]  # strip ${ and }
            cfg[key] = os.getenv(env_name)
        else:
            cfg[key] = value

    return cfg


def get_pg_connection(cfg: Dict[str, Any]):
    """
    Create and return a connection to PostgreSQL using psycopg2.
    cfg keys: pg_host, pg_port, pg_dbname, pg_user, pg_password
    """
    print("DEBUG config in get_pg_connection:", cfg)  # keep this for now

    conn = psycopg2.connect(
        host=cfg["pg_host"],
        port=int(cfg["pg_port"]),
        dbname=cfg["pg_dbname"],
        user=cfg["pg_user"],
        password=cfg["pg_password"],
    )
    conn.autocommit = False
    return conn
