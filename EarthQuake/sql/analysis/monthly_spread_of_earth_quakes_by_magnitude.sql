select
  event_date,
  sum(case when mag_bucket = '<3.5' then event_count else 0 end) as small_quakes,
  sum(case when mag_bucket = '3.5–4.4' then event_count else 0 end) as medium_quakes,
  sum(case when mag_bucket = '>=4.5' then event_count else 0 end) as large_quakes
from `earthquake.usgs_earthquake.daily_mag_buckets`
where event_date between '2018-05-01' and '2018-05-31'
group by event_date
order by event_date