select
  event_date,
  mag_bucket,
  event_count,
  avg_depth_km
from `earthquake.usgs_earthquake.daily_mag_buckets`
where event_date between '2018-05-01' and '2018-05-31'
order by event_date, mag_bucket