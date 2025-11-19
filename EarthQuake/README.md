*** USGS - BigQuery ETL (California Earthquakes) ***
This is a project for a small batch ETL pipeline that needs to loads earthquake data
from the USGS Earthquake Catalog API into BigQuery, and needs to build a simple
daily aggregated model table.

It is designed to: 
- run as a local Python script, support incremental and idempotent loads using MERGE on the
USGS event id. It alse support backfills via date-range parameters, and uses
partitioned tables to stay within BigQuery's free tier.



*** structure ***
EarthQuake/
    -sql/
      --ddl/
        create_raw_events.sql
        create_raw_events_staging.sql
        create_model_daily_mag_buckets.sql
      --dml/
        merge_raw_events.sql
        refresh_daily_mag_buckets.sql
	  --analysis/
		daily_counts_by_bucket.sql
		strong_quakes_top_days.sql
		daily_bucket_mix.sql

    -src/
      usgs_to_bigquery.py  - main CLI / orchestration
      usgs_client.py       - USGS API client, pagination
      bigquery_io.py       - BigQuery load, merge, model refresh

    -tests/
      test_usgs_client.py  - sample unit tests
	
	-dags/
	  usgs_earthquake_dag.py - samle for apache airflow DAG .. not quite ready

    README.md
    requirements.txt



*** BigQuery setup ***
ProjectID: `earthquake`
Dataset: `usgs_earthquake`

  run `sql/ddl/01.01.create_schema.sql`.
  run `sql/ddl/02.create_raw_events.sql`.
  run `sql/ddl/03.create_raw_events_staging.sql`.
  run `sql/ddl/04.create_model_daily_mag_buckets.sql`.



*** dependencies ***
pip install -r requirements.txt




*** test run for date window (California, May 2018, M ≥ 3.0) ***
python src/usgs_to_bq.py   
	--project_id=earthquake   
	--dataset=usgs_earthquake   
	--start_date=2018-05-01   
	--end_date=2018-05-31   
	--min_mag=3.0


This should do the following: 
 - call the USGS API (`/count`, `/query`) for the given date range. 
 - Flatten GeoJSON features into rows. 
 - load them into staging.
 - merge them into `raw_events`.


*** helper to test just the USGS fetch and  flatten part
python src/debug_fetch_only.py



*** Parameters ***
--project_id
--dataset
--start-date
--end-date
--min-mag
--min-lat
--max-lat
--min-lon
--max-lon
--page-limit



*** Incremental and  idempotent loads *** 
- merge ensures: 
  new events - insert
  updated events - update
  same events - ignored
- safe re-runs.

