from google.cloud import bigquery

project_id = "earthquake-478811"  # your real project id
dataset = "usgs_earthquake"


def main():
    print("Starting BigQuery connection test...")

    # 1) Try to create a client
    print(f"Creating BigQuery client for project: {project_id} ...")
    client = bigquery.Client(project=project_id)
    print("BigQuery client created OK.")

    # 2) Run a simple query
    print("Running test query: SELECT 1 AS test_value ...")
    query = "SELECT 1 AS test_value"
    result = list(client.query(query))
    print("Query result:", result[0]["test_value"])

    # 3) List tables in the dataset
    print(f"Listing tables in dataset: {dataset} ...")
    dataset_ref = client.dataset(dataset)
    tables = list(client.list_tables(dataset_ref))

    if not tables:
        print("No tables found in dataset.")
    else:
        print("Tables found:")
        for t in tables:
            print(" -", t.table_id)

    print("BigQuery connection test finished successfully.")


if __name__ == "__main__":
    print("test_bq_connection.py is running as a script.")
    main()
