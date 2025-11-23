import os
import logging

from etl.extract import extract_sales
from etl.transform import transform_sales
from etl.logging_config import setup_logging
from etl.validation import validate_sales, ValidationError
from etl.schema_pg import create_table_if_not_exists, get_max_order_id

backend = os.getenv("backend", "pg")  # fixed spelling from 'backened'

if backend == "pg":
    from etl.loader_pg import load_sales
    from etl.db_pg import load_config, get_pg_connection as get_connection
elif backend == "db2":
    from etl.db_db2 import load_config, get_db2_connection as get_connection
else:
    raise RuntimeError(f"Unknown backend: {backend}")


def main():
    # logging
    setup_logging()
    logger = logging.getLogger("etl_main")

    logger.info("ETL process started.")

    # Extract
    logger.info("Extracting data from CSV file...")
    df_raw = extract_sales("data/sales.csv")
    logger.info("%d rows Extracted", len(df_raw))

    # Transform
    logger.info("Transforming data...")
    df_clean = transform_sales(df_raw)
    logger.info("%d rows Transformed", len(df_clean))

    # Validation
    logger.info("Validating data...")
    try:
        df_clean = validate_sales(df_clean)
    except ValidationError:
        logger.error("ETL aborted due to validation errors")
        return

    # Load
    logger.info("Loading data into PostgreSQL (simulating Db2)...")
    cfg = load_config()
    conn = None

    try:
        conn = get_connection(cfg)
        create_table_if_not_exists(conn)

        # check load mode from env
        mode = os.getenv("load_mode", "upsert").lower()
        logger.info("load_mode from env: %s", mode)

        if mode == "upsert":
            # incremental load
            max_id = get_max_order_id(conn)
            if max_id is not None:
                logger.info("Current max order_id in target: %s", max_id)
                df_to_load = df_clean[df_clean["order_id"] > max_id]
                logger.info(
                    "Checking increments: %d rows to load", len(df_to_load)
                )
            else:
                logger.info("Target empty; full load of %d rows", len(df_clean))
                df_to_load = df_clean

            if df_to_load.empty:
                logger.info("No new rows to load. Exiting.")
                return
        else:
            # truncate mode: always load full dataset
            df_to_load = df_clean
            logger.info(
                "truncate mode: loading full %d rows (no incremental filter)",
                len(df_to_load),
            )

        # call loader (which handles truncate vs upsert internally)
        load_sales(conn, df_to_load)
        logger.info("ETL finished successfully.")
    except Exception:
        logger.exception("ETL failed")
        raise
    finally:
        if conn is not None:
            conn.close()
            logger.info("DB connection closed")


if __name__ == "__main__":
    main()
