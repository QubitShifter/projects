create table if not exists `project_id.dataset.raw_events_staging`
(
  id                string      not null,
  event_time        timestamp   not null, 
  event_date        date        not null,
  updated           timestamp,
  magnitude         float64,
  depth_km          float64,
  latitude          float64,
  longitude         float64,
  place             string,
  type              string,
  status            string,
  mmi               float64
)
partition by event_date
