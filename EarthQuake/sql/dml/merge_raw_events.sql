merge `earthquake-478811.usgs_earthquake.raw_events` as t
using `earthquake-478811.usgs_earthquake.raw_events_staging` as s
on t.id = s.id
when matched and (
    t.updated is null
    or (s.updated is not null and s.updated > t.updated)
) then
  update set
    t.event_time = s.event_time,
    t.updated    = s.updated,
    t.event_date = s.event_date,
    t.magnitude  = s.magnitude,
    t.depth_km   = s.depth_km,
    t.latitude   = s.latitude,
    t.longitude  = s.longitude,
    t.place      = s.place,
    t.type       = s.type,
    t.status     = s.status,
    t.mmi        = s.mmi
when not matched then
  insert (
    id, event_time, updated, event_date, magnitude, depth_km, latitude,
    longitude, place, type, status, mmi
  )
  values (
    s.id, s.event_time, s.updated, s.event_date, s.magnitude, s.depth_km,
    s.latitude, s.longitude, s.place, s.type, s.status, s.mmi
  )
