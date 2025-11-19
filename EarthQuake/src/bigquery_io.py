from google.cloud import bigquery


def load_staging_and_merge(project_id, dataset, rows):
    client = bigquery.Client(project=project_id)
    staging = f"{project_id}.{dataset}.raw_events_staging"
    target = f"{project_id}.{dataset}.raw_events"

    # truncate staging
    print(f"[BigQuery] truncating staging table: {staging}")
    client.query(f"truncate table `{staging}`").result()

    # load JSON rows into staging
    print(f"[BigQuery] loading {len(rows)} rows into {staging} ...")
    job = client.load_table_from_json(
        rows,
        staging,
        job_config=bigquery.LoadJobConfig(write_disposition="write append"),
    )
    job.result()
    print(f"loaded {len(rows)} rows into {staging}")

    # check number of rows in staging after load
    staging_count_query = f"select count(*) as count from `{staging}`"
    staging_cnt = list(client.query(staging_count_query))[0]["count"]
    print(f"staging row count after load: {staging_cnt}")

    print(f"sunning merge from staging into {target} ...")

    # run merge_raw_events.sql
    merge_sql_path = "sql/dml/merge_raw_events.sql"
    with open(merge_sql_path, "r", encoding="utf-8") as f:
        merge_sql = f.read()
    client.query(merge_sql).result()
    print("merge into raw_events completed.")


def refresh_model(project_id, dataset, start_date, end_date):
    client = bigquery.Client(project=project_id)
    sql_path = "sql/dml/refresh_daily_mag_buckets.sql"
    print(f"[BigQuery] refreshing daily_mag_buckets for {start_date}..{end_date}")
    with open(sql_path, "r", encoding="utf-8") as f:
        template = f.read()
    sql = (
        template
        .replace("{{start_date}}", start_date)
        .replace("{{end_date}}", end_date)
    )
    client.query(sql).result()
    print("[BigQuery] refreshed daily_mag_buckets.")
