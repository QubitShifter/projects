# etl/db_db2.py

import json
from pathlib import Path
from typing import Any, Dict

import ibm_db  # once Db2 is ready and working


def load_config(config_path: str = "config/config_db2.json") -> Dict[str, Any]:
    path = Path(config_path)
    with path.open() as f:
        return json.load(f)


def get_db2_connection(cfg: Dict[str, Any]):
    conn_str = (
        f"database={cfg['db2_dbname']};"
        f"hostname={cfg['db2_host']};"
        f"port={cfg['db2_port']};"
        f"protocol={cfg['db2_protocol']};"
        f"uid={cfg['db2_user']};"
        f"pwd={cfg['db2_password']};"
    )
    return ibm_db.connect(conn_str, "", "")
