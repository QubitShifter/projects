select
  event_date,
  event_count as strong_quakes,
  avg_depth_km
from `earthquake.usgs_earthquake.daily_mag_buckets`
where mag_bucket = '>=4.5'
order by strong_quakes desc
limit 10
