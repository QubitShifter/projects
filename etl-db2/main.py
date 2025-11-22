#import ibm_db
from etl.extract import extract_sales
from etl.transform import transform_sales
from etl.db_pg import load_config, get_pg_connection
from etl.schema_pg import create_table_if_not_exists
from etl.loader_pg import load_sales

print(">>> main.py STARTED")

def main():
    # 1. Extract
    print("Extracting data from CSV file...")
    df_raw = extract_sales("data/sales.csv")
    print(df_raw)

    # 2. Transform
    print("Transforming data...")
    df_clean = transform_sales(df_raw)
    print(df_clean)

    # 3. Load
    print("Loading data into PostgreSQL (simulating Db2)...")
    cfg = load_config()
    conn = None

    try:
        conn = get_pg_connection(cfg)
        create_table_if_not_exists(conn)
        load_sales(conn, df_clean)
        print("ETL finished successfully.")
    finally:
        if conn is not None:
            conn.close()


if __name__ == "__main__":
    print(">>> inside __main__ guard")
    main()
