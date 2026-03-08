---
name: strava
description: Strava API v3 via curl. Use this skill to query athlete activities, segments, clubs, gear, and routes on Strava. Create, update, and upload activities. Use when users mention Strava, running/cycling activities, fitness tracking, or want to retrieve workout data.
vm0_secrets:
  - STRAVA_TOKEN
---

# Strava API

Use the Strava API v3 via `curl` to access **athlete activities, segments, clubs, gear, and routes**. Create, update, and upload activities.

> Official docs: https://developers.strava.com/docs/reference/

---

## When to Use

Use this skill when you need to:

- Get athlete profile and statistics
- List, search, and filter activities
- Create manual activities or upload activity files (GPX/FIT/TCX)
- Update activity name, description, sport type, and other metadata
- Access activity streams (GPS, heart rate, power data)
- View segments, clubs, gear, and routes

---

> **Important:** When using `$VAR` in a command that pipes to another command, wrap the command containing `$VAR` in `bash -c '...'`. Due to a Claude Code bug, environment variables are silently cleared when pipes are used directly.

> **Placeholders:** Values in `<angle-brackets>` like `<activity-id>` are placeholders. Replace them with actual values when executing.

---

## Athlete

### Get Authenticated Athlete Profile

```bash
bash -c 'curl -s "https://www.strava.com/api/v3/athlete" --header "Authorization: Bearer $STRAVA_TOKEN"' | jq '{id, firstname, lastname, city, country, sex, premium, created_at, follower_count, friend_count}'
```

### Get Athlete Statistics

Replace `<athlete-id>` with the `id` from the athlete profile above:

```bash
bash -c 'curl -s "https://www.strava.com/api/v3/athletes/<athlete-id>/stats" --header "Authorization: Bearer $STRAVA_TOKEN"' | jq '{recent_run_totals, recent_ride_totals, ytd_run_totals, ytd_ride_totals, all_run_totals, all_ride_totals}'
```

---

## Activities

### List Recent Activities

```bash
bash -c 'curl -s "https://www.strava.com/api/v3/athlete/activities?per_page=30" --header "Authorization: Bearer $STRAVA_TOKEN"' | jq '.[] | {id, name, sport_type, distance, moving_time, elapsed_time, total_elevation_gain, start_date_local, average_speed, max_speed}'
```

Query parameters:
- `before=EPOCH` — Activities before timestamp
- `after=EPOCH` — Activities after timestamp
- `page=1` — Page number
- `per_page=30` — Results per page (max 200)

### Get Activity Details

```bash
bash -c 'curl -s "https://www.strava.com/api/v3/activities/<activity-id>" --header "Authorization: Bearer $STRAVA_TOKEN"' | jq '{id, name, sport_type, distance, moving_time, elapsed_time, total_elevation_gain, average_speed, max_speed, average_heartrate, max_heartrate, calories, description, gear_id}'
```

### Create Manual Activity

Write to `/tmp/strava_request.json`:

```json
{
  "name": "Morning Run",
  "sport_type": "Run",
  "start_date_local": "2025-01-15T08:00:00Z",
  "elapsed_time": 3600,
  "distance": 10000,
  "description": "Easy morning run"
}
```

Then run:

```bash
bash -c 'curl -s -X POST "https://www.strava.com/api/v3/activities" --header "Authorization: Bearer $STRAVA_TOKEN" --header "Content-Type: application/json" -d @/tmp/strava_request.json' | jq '{id, name, sport_type, distance}'
```

Required fields: `name`, `sport_type`, `start_date_local` (ISO 8601), `elapsed_time` (seconds).
Optional: `distance` (meters), `description`, `trainer` (0/1), `commute` (0/1).

Sport types: `Run`, `TrailRun`, `Ride`, `MountainBikeRide`, `GravelRide`, `EBikeRide`, `Swim`, `Walk`, `Hike`, `WeightTraining`, `Yoga`, `Workout`, `Rowing`, `Kayaking`, `Surfing`, `RockClimbing`, `Golf`, `Soccer`, `Tennis`, `Pickleball`, `Skateboard`, `Snowboard`, `AlpineSki`, `NordicSki`, etc.

### Update Activity

Write to `/tmp/strava_request.json`:

```json
{
  "name": "Updated Name",
  "description": "Updated description",
  "sport_type": "Run",
  "gear_id": "<gear-id>",
  "commute": false,
  "hide_from_home": false
}
```

Then run:

```bash
bash -c 'curl -s -X PUT "https://www.strava.com/api/v3/activities/<activity-id>" --header "Authorization: Bearer $STRAVA_TOKEN" --header "Content-Type: application/json" -d @/tmp/strava_request.json' | jq '{id, name, description, sport_type}'
```

Updatable fields: `name`, `sport_type`, `description`, `gear_id` (set to `"none"` to remove), `trainer`, `commute`, `hide_from_home`.

---

## Uploads

### Upload Activity File (GPX/FIT/TCX)

```bash
bash -c 'curl -s -X POST "https://www.strava.com/api/v3/uploads" --header "Authorization: Bearer $STRAVA_TOKEN" -F "data_type=gpx" -F "file=@/path/to/activity.gpx" -F "name=My Activity" -F "description=Uploaded via API"'
```

Supported formats: `fit`, `fit.gz`, `tcx`, `tcx.gz`, `gpx`, `gpx.gz`.

### Check Upload Status

Uploads are processed asynchronously. Poll for status:

```bash
bash -c 'curl -s "https://www.strava.com/api/v3/uploads/<upload-id>" --header "Authorization: Bearer $STRAVA_TOKEN"' | jq '{id, status, error, activity_id}'
```

When `activity_id` is populated, the upload is complete.

---

## Activity Details

### List Activity Comments

```bash
bash -c 'curl -s "https://www.strava.com/api/v3/activities/<activity-id>/comments" --header "Authorization: Bearer $STRAVA_TOKEN"' | jq '.[] | {id, text, created_at, athlete: .athlete.firstname}'
```

### List Activity Kudoers

```bash
bash -c 'curl -s "https://www.strava.com/api/v3/activities/<activity-id>/kudos" --header "Authorization: Bearer $STRAVA_TOKEN"' | jq '.[] | {id, firstname, lastname}'
```

### Get Activity Laps

```bash
bash -c 'curl -s "https://www.strava.com/api/v3/activities/<activity-id>/laps" --header "Authorization: Bearer $STRAVA_TOKEN"' | jq '.[] | {id, name, elapsed_time, distance, average_speed, average_heartrate}'
```

### Get Activity Photos

```bash
bash -c 'curl -s "https://www.strava.com/api/v3/activities/<activity-id>/photos?photo_sources=true&size=600" --header "Authorization: Bearer $STRAVA_TOKEN"' | jq '.[] | {unique_id, urls, caption, source, location}'
```

### Get Activity Streams (GPS/HR/Power Data)

```bash
bash -c 'curl -s "https://www.strava.com/api/v3/activities/<activity-id>/streams?keys=time,distance,heartrate,velocity_smooth&key_by_type=true" --header "Authorization: Bearer $STRAVA_TOKEN"' | jq 'keys'
```

Available stream keys: `time`, `distance`, `latlng`, `altitude`, `velocity_smooth`, `heartrate`, `cadence`, `watts`, `temp`, `moving`, `grade_smooth`.

---

## Segments

### List Starred Segments

```bash
bash -c 'curl -s "https://www.strava.com/api/v3/segments/starred" --header "Authorization: Bearer $STRAVA_TOKEN"' | jq '.[] | {id, name, distance, average_grade, maximum_grade, city, state, country}'
```

### Get Segment Details

```bash
bash -c 'curl -s "https://www.strava.com/api/v3/segments/<segment-id>" --header "Authorization: Bearer $STRAVA_TOKEN"' | jq '{id, name, activity_type, distance, average_grade, maximum_grade, elevation_high, elevation_low, city, country, effort_count, athlete_count}'
```

### Get Segment Leaderboard

```bash
bash -c 'curl -s "https://www.strava.com/api/v3/segments/<segment-id>/leaderboard?per_page=10" --header "Authorization: Bearer $STRAVA_TOKEN"' | jq '{entry_count, entries: [.entries[] | {rank, athlete_name, elapsed_time, moving_time, start_date_local}]}'
```

Parameters: `gender` (M/F), `age_group`, `weight_class`, `following` (true/false), `per_page`.

---

## Gear

### Get Athlete's Gear

```bash
bash -c 'curl -s "https://www.strava.com/api/v3/athlete" --header "Authorization: Bearer $STRAVA_TOKEN"' | jq '{bikes: .bikes, shoes: .shoes}'
```

### Get Gear Details

Bike IDs start with `b`, shoe IDs start with `g`:

```bash
bash -c 'curl -s "https://www.strava.com/api/v3/gear/<gear-id>" --header "Authorization: Bearer $STRAVA_TOKEN"' | jq '{id, name, brand_name, model_name, distance, converted_distance}'
```

---

## Clubs

### List Athlete Clubs

```bash
bash -c 'curl -s "https://www.strava.com/api/v3/athlete/clubs" --header "Authorization: Bearer $STRAVA_TOKEN"' | jq '.[] | {id, name, sport_type, city, country, member_count}'
```

### Get Club Details

```bash
bash -c 'curl -s "https://www.strava.com/api/v3/clubs/<club-id>" --header "Authorization: Bearer $STRAVA_TOKEN"' | jq '{id, name, sport_type, city, country, member_count, description}'
```

### List Club Activities

```bash
bash -c 'curl -s "https://www.strava.com/api/v3/clubs/<club-id>/activities?per_page=20" --header "Authorization: Bearer $STRAVA_TOKEN"' | jq '.[] | {name, sport_type, distance, moving_time, athlete: (.athlete.firstname + " " + .athlete.lastname)}'
```

---

## Routes

### Get Athlete Routes

```bash
bash -c 'curl -s "https://www.strava.com/api/v3/athletes/<athlete-id>/routes?per_page=20" --header "Authorization: Bearer $STRAVA_TOKEN"' | jq '.[] | {id, name, type, distance, elevation_gain, estimated_moving_time}'
```

---

## Guidelines

1. **Token expiry**: Access tokens expire every 6 hours — the platform handles refresh automatically via the connector
2. **Pagination**: Use `page` and `per_page` (max 200) for list endpoints
3. **Time filters**: Use Unix epoch timestamps for `before`/`after` parameters
4. **Scope requirements**: Ensure token has correct scopes; `activity:read_all` needed for private activities, `activity:write` needed to create/edit
5. **Rate limits**: 200 req/15min, 2000 req/day — add delays for bulk operations. Returns `429` when exceeded
6. **Distance units**: All distances are in **meters**, speeds in **meters/second**
7. **Time units**: All durations are in **seconds**
8. **Sport type vs type**: Prefer `sport_type` over deprecated `type` field

---

## API Reference

- REST Reference: https://developers.strava.com/docs/reference/
- Authentication: https://developers.strava.com/docs/authentication/
- Rate Limits: https://developers.strava.com/docs/rate-limits/
- Uploads: https://developers.strava.com/docs/uploads/
