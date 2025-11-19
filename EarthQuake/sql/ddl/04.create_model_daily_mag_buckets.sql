create table if not exists `project_id.dataset.daily_mag_buckets`
(
  event_date            date        not null,
  magnitude_bucket      string      not null,      
  event_count           int64,                     
  avg_depth_km          float64                    
)
partition by event_date



