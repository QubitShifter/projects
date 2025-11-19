import math
import time
import requests
import datetime as dt

usgs_base_url = "https://earthquake.usgs.gov/fdsnws/event/1"


def ms_to_ts(ms):
    if ms is None:
        return None
    dt_utc = dt.datetime.fromtimestamp(ms / 1000.0, tz=dt.timezone.utc)
    return dt_utc.isoformat()


def flatten_feature(f):
    props = f.get("properties", {}) or {}
    geom = f.get("geometry", {}) or {}
    coords = geom.get("coordinates") or [None, None, None]

    event_time = ms_to_ts(props.get("time"))
    updated = ms_to_ts(props.get("updated"))   

    event_date = None
    if event_time:
        d = dt.datetime.fromisoformat(event_time)
        event_date = d.date().isoformat()

    return {
        "id": f.get("id"),
        "event_time": event_time,
        "updated": updated,         
        "event_date": event_date,
        "magnitude": props.get("mag"),
        "depth_km": coords[2],
        "latitude": coords[1],
        "longitude": coords[0],
        "place": props.get("place"),
        "type": props.get("type"),
        "status": props.get("status"),
        "mmi": props.get("mmi"),
    }


def usgs_count(params):
    url = f"{usgs_base_url}/count"
    r = requests.get(url, params=params, timeout=30)
    r.raise_for_status()
    #return r.json().get("count", 0)
    text = r.text.strip()
    try:
        count = int(text)
    except ValueError:
        print(f"[USGS] count error: {text!r}")
        count = 0

    print(f"[USGS] count error : {count}")
    return count

def usgs_query_all(params, page_limit):
    total = usgs_count(params)
    print(f"[USGS] count: {total}")
    if total == 0:
        return []

    rows = []
    pages = math.ceil(total / page_limit)
    offset = 1

    for page in range(pages):
        print(f"[USGS] page {page + 1}/{pages} (offset={offset})")
        q = params.copy()
        q.update({
            "format": "geojson",
            "limit": page_limit,
            "offset": offset,
            "orderby": "time-asc",
        })
        url = f"{usgs_base_url}/query"
        r = requests.get(url, params=q, timeout=60)
        r.raise_for_status()
        data = r.json()
        features = data.get("features") or []
        print(f"[USGS] Page {page + 1}: {len(features)} features")

        for f in features:
            rows.append(flatten_feature(f))

        offset += page_limit
        time.sleep(0.2)

    print(f"[USGS] number od flattened rows: {len(rows)}")
    return rows
