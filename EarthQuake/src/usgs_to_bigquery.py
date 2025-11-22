import os
import argparse

from usgs_client import usgs_query_all
from bigquery_io import load_staging_and_merge, refresh_model


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--project_id", default=os.getenv("project_id", "earthquake"))
    parser.add_argument("--dataset", default="usgs_earthquake")
    parser.add_argument("--start-date", required=True)
    parser.add_argument("--end-date", required=True)
    parser.add_argument("--min-magnitude", type=float, default=3.0)
    parser.add_argument("--min-latitude", type=float, default=32.0)
    parser.add_argument("--max-latitude", type=float, default=42.0)
    parser.add_argument("--min-longitude", type=float, default=-125.0)
    parser.add_argument("--max-longitude", type=float, default=-114.0)
    parser.add_argument("--page-limit", type=int, default=20000)
    return parser.parse_args()


def main():
    args = parse_args()

    print(" [USGS] - [BigQuery] ETL")
    print(f"Project: {args.project_id}, Dataset: {args.dataset}")
    print(f"Date range: {args.start_date} to {args.end_date}")
    print(f"Min magnitude: {args.min_magnitude}")
    print(
        f"Bounding box: "
        f"lat {args.min_latitude}..{args.max_latitude}, "
        f"lon {args.min_longitude}..{args.max_longitude}"
    )

    params = {
        "starttime": args.start_date,
        "endtime": args.end_date,
        "minmagnitude": args.min_magnitude,
        "minlatitude": args.min_latitude,
        "maxlatitude": args.max_latitude,
        "minlongitude": args.min_longitude,
        "maxlongitude": args.max_longitude,
    }

    print("call to USGS API with params:", params)

    rows = usgs_query_all(params, args.page_limit)
    print(f"{len(rows)} flattened rows from USGS.")

    if not rows:
        print("no data returned from USGS. nothing to load.")
        return

    # example row for a refference
    print("sample flattened row:")
    print(rows[0])

    print("loading rows into BigQuery staging and merging into raw_events")
    load_staging_and_merge(args.project_id, args.dataset, rows)

    print(
        f"refreshing daily_mag_buckets: "
        f"{args.start_date} to {args.end_date}"
    )
    refresh_model(args.project_id, args.dataset, args.start_date, args.end_date)

    print("ETL finished successfully.")


if __name__ == "__main__":
    main()
