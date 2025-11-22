# etl/loader_pg.py

import pandas as pd


def load_sales(conn, df: pd.DataFrame) -> None:
    """
    Insert the transformed DataFrame rows into the sales_etl table in PostgreSQL.
    """
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

    with conn.cursor() as cur:
        for _, row in df.iterrows():
            cur.execute(
                insert_sql,
                (
                    int(row["order_id"]),
                    str(row["customer"]),
                    float(row["amount"]),
                    str(row["currency"]),
                    float(row["amount_eur"]),
                ),
            )
        conn.commit()
        print(f"Inserted {len(df)} rows into etl_sales.")
