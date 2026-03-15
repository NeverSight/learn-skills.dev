---
name: hk-cinema-now-playing
description: |
  Hong Kong Cinema helper with 4-step flow:
  
  1. List now playing movies (numbered)
  2. Show movie details with brief showtimes (unique cinemas + dates only)
  3. Filter showtimes by cinema/date when user specifies
  4. Book tickets via direct link
  
  Note: Uses /now-playing endpoint to include rescreening of older popular movies.
  Use when user asks about HK movies, cinema showtimes, or ticket booking.
---

# HK Cinema Now Playing

## APIs

### TMDB (Movie List)
```
GET https://api.themoviedb.org/3/movie/now-playing?region=HK&language=zh-HK
```

Headers:
- `Authorization: Bearer ${TMDB_API_KEY}`
- `accept: application/json`

### International Showtimes (Direct API - Recommended)
```
GET https://api.internationalshowtimes.com/v5/showtimes?movie_id={tmdb_id}&countries=HK
```

Headers:
- `X-API-Key: ${IS_API_KEY}`
- OR `Authorization: Token token=${IS_API_KEY}`

Also supports `countries=HK` (plural) - both work.

### RapidAPI Wrapper (Legacy - often broken)
```
GET https://international-showtimes.p.rapidapi.com/v5/movies/{tmdb_id}/showtimes?countries=HK
```

Headers:
- `X-RapidAPI-Key: ${RAPIDAPI_KEY}`
- `X-RapidAPI-Host: international-showtimes.p.rapidapi.com`

Note: The RapidAPI endpoints frequently return errors. Use the direct API instead.

## Cinema Chain Booking URLs (fallback when API doesn't provide booking_link)

| Chain | Booking URL |
|-------|-------------|
| MCL Cinemas | https://www.mclcinema.com |
| Broadway Circuit | https://www.broadwaycinema.com.hk |
| Golden Harvest | https://www.goldenharvest.com |
| Emperor Cinemas | https://www.emperorcinemas.com |
| UA Cinemas | https://www.uacinemas.com.hk |
| Cinema City | https://www.cinemacity.com.hk |
| MOViE MOViE | https://www.pacificplace.com.hk/en/entertainment/cinema |
| Premiere Elements | https://www.premiereelements.com.hk |
| StagE | https://www.cinema.com.hk |
| Black Box | https://www.blackbox.com.hk |

## Display Rules

### Step 1: List Movies
When user asks "what's playing in Hong Kong" or similar:
- Call TMDB: `GET /movie/now-playing?region=HK&language=zh-HK`
- Cache movie list with TMDB IDs
- Show numbered list (Chinese title + English title from `title` and `original_title` fields)

Format:
```
香港上映中:

1. [電影中文名] ([英文名])
2. [電影中文名] ([英文名])
3. [電影中文名] ([英文名])
...
```

### Step 2: Movie Details (Brief)
When user asks about a specific movie (e.g., "第一套詳細啲", "毒蛇律師2有咩上?"):

1. Get TMDB movie ID from cached list
2. Call TMDB: `GET /movie/{id}?language=zh-HK` for title + overview
3. Call IS: `GET /v5/showtimes?movie_id={tmdb_id}&countries=HK`
4. Extract unique cinemas (from `showtimes[].cinema.name`)
5. Extract unique dates (from `showtimes[].start_at`, format as "3月14日")

Display format:
```
[TITLE]

簡介: [overview]

上映戲院:
- [Cinema 1]
- [Cinema 2]
- ...

上映日期:
- [Date 1]
- [Date 2]
- ...
```

### Step 3: Filtered Showtimes
When user specifies a cinema OR date (e.g., "MCL", "聽日", "MCL聽日"):

1. Parse user input to identify:
   - Cinema name (match against available cinemas)
   - Date (parse relative dates: "今日", "聽日", "後日", or specific date)
2. Filter showtimes:
   - If cinema specified: show only that cinema's showtimes
   - If date specified: show only that date's showtimes
   - If both: apply both filters
3. For each date, list all available times

Display format:
```
[Cinema Name] - [Movie Title]

[Date 1]: [Time 1] | [Time 2] | [Time 3]
[Date 2]: [Time 1] | [Time 2]
...

購票: [booking_link]
```

### Step 4: Book Tickets
When user confirms a specific showtime (e.g., "聽日7點MCL", "我要買飛"):

1. Extract cinema + date + time from user message
2. Find matching showtime from cached data
3. Use `booking_link` from API response
4. Open booking URL in browser

Response format:
```
🎫 [Cinema Name] - [Date] [Time]

[booking_link]

[Open in browser]
```

If user says "book it" without details, ask which cinema and time they prefer.

## Response Parsing

From `/movie/now-playing`:
- `results[]`: Array of movies
  - `id`: TMDB movie ID
  - `title`: Chinese title (zh-HK)
  - `original_title`: Original/English title

From `/movie/{id}`:
- `title`: Chinese title
- `overview`: Chinese synopsis

From `/movies/{tmdb_id}/showtimes`:
- `showtimes[]`: Array of showtimes
  - `cinema.id`: Cinema ID
  - `cinema.name`: Cinema name (e.g., "MCL Cinemas", "百老匯")
  - `start_at`: ISO datetime (e.g., "2024-03-15T19:30:00+08:00")
  - `booking_link`: Direct ticket URL
  - `movie_id`: TMDB movie ID

## Date Parsing (Cantonese/Chinese)
- "今日" = today
- "聽日" = tomorrow
- "後日" = day after tomorrow
- "尋日" = yesterday
- Or parse "3月15日" format

## Cinema Name Matching
Match user input against available cinema names (partial match OK):
- "MCL" → "MCL Cinemas"
- "百老匯" → "Broadway Circuit"
- " Cinema City" → "Cinema City"

## Error Handling
- If TMDB fails: "無法取得電影資料，請再試一次。"
- If no showtimes: "暫時未有呢套戲既場次資料。"
- If API errors: Show available data, note "部分場次資料可能不完整。"
