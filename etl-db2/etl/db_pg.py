# etl/db_pg.py
# Connects to localhost PostgreSQL (used as a stand-in for Db2 while Db2 is not available)

import os
import json
from pathlib import Path
from typing import Any, Dict

import psycopg2
from dotenv import load_dotenv

load_dotenv()

def load_config(config_path: str = "config/config.json") -> Dict[str, Any]:
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
    Config dict must contain:
      pg_host, pg_port, pg_dbname, pg_user, pg_password
    """
    conn = psycopg2.connect(
        host=cfg["pg_host"],
        port=cfg["pg_port"],
        dbname=cfg["pg_dbname"],
        user=cfg["pg_user"],
        password=cfg["pg_password"],
    )
    conn.autocommit = False  # we'll commit in the loader/schema code
    return conn
