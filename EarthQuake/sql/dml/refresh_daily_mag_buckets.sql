delete from `earthquake.usgs_earthquake.daily_mag_buckets`
where event_date between date('{{start_date}}') and date('{{end_date}}');

insert into `earthquake.usgs_earthquake.daily_mag_buckets` (
        event_date,
        mag_bucket,
        event_count,
        avg_depth_km
)
select
  event_date,
    case
        when magnitude < 3.5 then '<3.5'
        when magnitude < 4.5 then '3.5–4.4'
        else '>=4.5'
    end as mag_bucket,
    count(*) as event_count,
    avg(depth_km) as avg_depth_km

from `earthquake.usgs_earthquake.raw_events`
where event_date between date('{{start_date}}') and date('{{end_date}}')
group by event_date, mag_bucket

