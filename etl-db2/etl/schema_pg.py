#import ibm_db

def create_table_if_not_exists(conn) -> None:
    
    #Create the etl_sales table if it does not exist.
    create_sql = """
    create table if not exists etl_sales (
        order_id integer primary key,
        customer varchar(100),
        amount decimal(10,2),
        currency varchar(10),
        amount_eur decimal(10,2)
    )
    """
    with conn.cursor() as cur:
        cur.execute(create_sql)
        conn.commit()
        print("Table etl_sales is ready.")
