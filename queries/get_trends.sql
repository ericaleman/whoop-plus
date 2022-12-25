WITH 

core_data as (
  SELECT
    cycle.day,
    {metric}
  FROM cycle
  LEFT JOIN recovery
    on recovery.cycle_id = cycle.id
  LEFT JOIN sleep
    on recovery.sleep_id = sleep.id
    and sleep.nap = FALSE
),

all_dates as (
SELECT
    calendar.day,
    row_number() over (order by calendar.day) as day_num,
    {metric} as trend_1_day
FROM calendar
LEFT JOIN core_data
    on core_data.day = calendar.day
)

SELECT
  day,
  trend_1_day,
  case
    when day_num >= 3 then avg(trend_1_day) over (order by day rows 2 preceding)
  end as trend_3_day,
  case
    when day_num >= 5 then avg(trend_1_day) over (order by day rows 4 preceding)
  end as trend_5_day,
  case
    when day_num >= 7 then avg(trend_1_day) over (order by day rows 6 preceding)
  end as trend_1_week,
  case
    when day_num >= 14 then avg(trend_1_day) over (order by day rows 13 preceding)
  end as trend_2_week,
  case
    when day_num >= 21 then avg(trend_1_day) over (order by day rows 20 preceding)
  end as trend_3_week,
  case
    when day_num >= 28 then avg(trend_1_day) over (order by day rows 27 preceding)
  end as trend_4_week
FROM all_dates