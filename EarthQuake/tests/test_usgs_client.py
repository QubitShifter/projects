import datetime as dt
from src.usgs_client import flatten_feature

def test_flatten_feature_basic():
    feature = {
        "id": "test123",
        "properties": {
            "time": 1525132800000,   
            "updated": 1525136400000,
            "mag": 3.7,
            "place": "Californiq",
            "type": "earthquake",
            "status": "reviewed",
            "mmi": 4.2,
        },
        "geometry": {
            "type": "Point",
            "coordinates": [-120.5, 35.1, 7.3]  
        }
    }

    row = flatten_feature(feature)

    assert row["id"] == "test123"
    assert row["magnitude"] == 3.7
    assert row["depth_km"] == 7.3
    assert row["latitude"] == 35.1
    assert row["longitude"] == -120.5
    assert row["place"] == "Californiq"
    assert row["type"] == "earthquake"
    assert row["status"] == "reviewed"
    assert row["mmi"] == 4.2

    
    assert row["event_time"].endswith("00:00") 
    assert row["event_date"] == "2018-05-01" 


