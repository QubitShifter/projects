# etl/loader_pg.py
import os
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv

project_root = Path(__file__).resolve().parent.parent
dotenv_path = project_root / "config" / ".env"

load_dotenv(dotenv_path=dotenv_path)




def load_sales(conn, df: pd.DataFrame) -> None:
    """
    Insert the transformed DataFrame rows into the sales_etl table in PostgreSQL.
    it depends on the two modes:
      - truncate: de;ete all from table before insert
      -upsert: insert.. on conflict (order_id) dp update 
    """

    mode = os.getenv("load_mode", "upsert").lower()
    print(f"MODE in loader_pg: {mode}")

    with conn.cursor() as cur:
        if mode == "truncate":
            # wipe existing data
            cur.execute("truncate table etl_sales;")

            insert_sql = """
            INSERT INTO etl_sales (order_id, customer, amount, currency, amount_eur)
            VALUES (%s, %s, %s, %s, %s)
            """
        elif mode == "upsert":
            insert_sql = """
            insert into etl_sales (order_id, customer, amount, currency, amount_eur)
            values (%s, %s, %s, %s, %s)
            on conflict (order_id) do update
            set
                customer = excluded.customer,
                amount = excluded.amount,
                currency = excluded.currency,
                amount_eur = excluded.amount_eur;
            """
        else:
            raise ValueError(f"Unknown load_mode: {mode!r}. Use 'truncate' or 'upsert'.")

        rows = [
            (
                int(row["order_id"]),
                str(row["customer"]),
                float(row["amount"]),
                str(row["currency"]),
                float(row["amount_eur"]),
            )
            for _, row in df.iterrows()
        ]

        # batch insert/upsert
        cur.executemany(insert_sql, rows)
        conn.commit()
        print(f"{mode.upper()}: processed {len(rows)} rows into etl_sales.")