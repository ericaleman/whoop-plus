# WHOOP+ <!-- omit in toc -->

Track long term trends in your health using your WHOOP device. Get your first month with WHOOP free at https://join.whoop.com/46A8F8.

## Contents <!-- omit in toc -->

- [Setup](#setup)
- [API Requests](#api-requests)
  - [Get Basic Profile](#get-basic-profile)
  - [Get Body Measurements](#get-body-measurements)
  - [Get Cycle Collection](#get-cycle-collection)
  - [Get Recovery Collection](#get-recovery-collection)
  - [Get Sleep Collection](#get-sleep-collection)
  - [Get Workout Collection](#get-workout-collection)

## Setup

Store your WHOOP email and password in a `.env` file:

```bash
# WHOOP credentials
USERNAME="<USERNAME>"
PASSWORD="<PASSWORD>"
```

## API Requests

`WHOOP+` can make six different types of requests, pulling down Cycle/Recovery/Sleep/Workout collections for the last n days and pulling down basic profile information. 

### Get Basic Profile

Get your login info

**Example Response**:

```python
{
    "user_id": 123,
    "email": "ericaleman@mail.com",
    "first_name": "Eric",
    "last_name": "Aleman"
}
```

### Get Body Measurements

Get your body measurements

**Example Response**:

```python
{
    "height_meter": 1.80,
    "weight_kilogram": 85.0,
    "max_heart_rate": 194
}
```

### Get Cycle Collection

Get your last n daily cycles.

**Example Response**:

```python
[
    {
       "id":311600261,
       "user_id":26414,
       "created_at":"2022-12-25T12:34:38.809Z",
       "updated_at":"2022-12-25T12:34:38.809Z",
       "start":"2022-12-25T03:49:58.295Z",
       "end":"None",
       "timezone_offset":"-05:00",
       "score_state":"SCORED",
       "score":{
          "strain":0.051671274,
          "kilojoule":3309.1736,
          "average_heart_rate":63,
          "max_heart_rate":112
       }
    },
    ...
]
```

### Get Recovery Collection

Get your last n daily recoveries.

**Example Response**:

```python
[
    {
        "cycle_id": 93845,
        "sleep_id": 10235,
        "user_id": 10129,
        "created_at": "2022-04-24T11:25:44.774Z",
        "updated_at": "2022-04-24T14:25:44.774Z",
        "score_state": "SCORED",
        "score": {
            "user_calibrating": False,
            "recovery_score": 44,
            "resting_heart_rate": 64,
            "hrv_rmssd_milli": 31.813562,
            "spo2_percentage": 95.6875,
            "skin_temp_celsius": 33.7
        }
    },
    ...
]
```

### Get Sleep Collection

Get your last n daily sleep cyles.

**Example Response**:

```python
[
    {
        "id": 93845,
        "user_id": 10129,
        "created_at": "2022-04-24T11:25:44.774Z",
        "updated_at": "2022-04-24T14:25:44.774Z",
        "start": "2022-04-24T02:25:44.774Z",
        "end": "2022-04-24T10:25:44.774Z",
        "timezone_offset": "-05:00",
        "nap": False,
        "score_state": "SCORED",
        "score": {
            "stage_summary": {},
            "sleep_needed": {},
            "respiratory_rate": 16.11328125,
            "sleep_performance_percentage": 98,
            "sleep_consistency_percentage": 90,
            "sleep_efficiency_percentage": 91.69533848
        }
    },
    ...
]
```

### Get Workout Collection

Get your last n daily sleep cyles.

**Example Response**:

```python
[
    {
       "id":84653809,
       "user_id":26414,
       "created_at":"2020-06-26T00:05:00.505Z",
       "updated_at":"2020-06-26T00:11:08.624Z",
       "start":"2020-06-25T23:35:22.629Z",
       "end":"2020-06-26T00:04:54.192Z",
       "timezone_offset":"-04:00",
       "sport_id":0,
       "score_state":"SCORED",
       "score":{
          "strain":9.3621,
          "average_heart_rate":139,
          "max_heart_rate":171,
          "kilojoule":1303.4093,
          "percent_recorded":100.0,
          "distance_meter":3306.1038,
          "altitude_gain_meter":34.923603,
          "altitude_change_meter":0.088306166,
          "zone_duration":{
             "zone_zero_milli":0,
             "zone_one_milli":160999,
             "zone_two_milli":431999,
             "zone_three_milli":600999,
             "zone_four_milli":577996,
             "zone_five_milli":0
          }
       }
    },
    ...
]
```