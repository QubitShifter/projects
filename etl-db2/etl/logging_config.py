import logging
from pathlib import Path

log_dir = Path("logging")
log_dir.mkdir(exist_ok=True)

log_file = log_dir / "etl.log"

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers=[
            logging.FileHandler(log_file, encoding="utf-8"),
            logging.StreamHandler(),
        ],
    )

