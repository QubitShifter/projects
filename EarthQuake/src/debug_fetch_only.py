from usgs_client import usgs_query_all

def main():
    params = {
        "starttime": "2018-05-01",
        "endtime": "2018-05-02",
        "minmagnitude": 2.5,
        "minlatitude": 32.0,
        "maxlatitude": 42.0,
        "minlongitude": -125.0,
        "maxlongitude": -114.0,
    }

    rows = usgs_query_all(params, page_limit=20000)
    print(f"Fetched {len(rows)} rows")
    if rows:
        print("Sample row:")
        print(rows[0])

if __name__ == "__main__":
    main()
