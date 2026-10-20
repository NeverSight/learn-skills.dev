---
name: foraging-route
description: Solve the shortest walking route from the user's current location through every mapped fruit tree in the vault, and return a map link plus a Google Maps walking link. Use when the user names where they are, by cross street, address, place, tree, map link or coordinates, and asks for the route, order, or shortest walk to the apple or plum trees.
---

## Overview

The stops live in vault notes, one note per tree, which are the single source of truth for which trees exist.

Each tree note sits in the vault root at `/Users/mtm/Documents/Obsidian Vault` and carries `[[apples and plums near us]]` in its `part_of` front matter property.

The note `/Users/mtm/Documents/Obsidian Vault/apples and plums near us.md` is the hub that embeds those notes as a base and holds the route write-up, and it is not a stop.

The route is an open-path travelling salesman problem: start at the user, visit every stop once, and end wherever is shortest.

The public OSRM foot server solves it, and the answer is handed back as links the user can tap on a phone.

This skill reads the vault and writes nothing to it.

Saving a route into a note happens only when the user asks for that separately.

## Step 1: Resolve the start to one decimal position

Turn whatever the user gave into a single `latitude, longitude` pair in decimal degrees.

The user is usually speaking into a phone, so the input is most often a cross street or an address, and dictation may spell numbers as words.

Before classifying, rewrite spelled-out ordinals and numbers as digits, so "twenty-fourth and Madison" becomes "24th and Madison".

Classify the input as the first type below that matches, because the earlier types are unambiguous and the later ones are loose.

Only the start is ever looked up, since every tree already carries its coordinates in the note, so a run spends at most one lookup here.

### Google Maps short link

A `maps.app.goo.gl/...` or `goo.gl/maps/...` URL.

Expand it with `curl --silent --location --output /dev/null --write-out '%{url_effective}' <url>`, then resolve the expanded URL as a full Google Maps link.

### Google Maps full link

A URL whose host contains `google.` and whose path starts with `/maps`.

Take the place pin from `!3d<lat>!4d<lon>`, because the `@<lat>,<lon>` segment is only the map's viewport centre and can sit a block away.

Without `!3d`/`!4d`, fall back to `@<lat>,<lon>`, then to a `query=<lat>,<lon>` parameter.

### OpenStreetMap link

A URL on `openstreetmap.org`, resolved from its `mlat` and `mlon` parameters.

### Degrees, minutes, seconds

Text with a `°` sign, or with minute and second marks beside N, S, E or W, such as `47°37'13.4"N 122°18'40.2"W`.

Convert each half with degrees + minutes/60 + seconds/3600, and make S latitudes and W longitudes negative.

### Decimal pair

Two signed decimals such as `47.6204, -122.3112`, taken latitude first.

A first number near -122 means the pair arrived longitude first, so swap it.

### Tree from the note

Text naming one of the tree notes, such as "I'm at the East Pine tree" or "at the 16th Avenue tree".

Use that note's `latitude` and `longitude` properties, which costs no lookup.

This check comes before addresses and cross streets, because a tree heading reads like a street name.

### Street address

A house number followed by a street name, such as "2801 East Madison".

Strip any suite, unit or apartment number, append `, Seattle, WA`, and geocode with one Nominatim request:

```
curl --silent --max-time 20 --get --user-agent "foraging-route (taylormonacelli@gmail.com)" --data-urlencode "q=<address>, Seattle, WA" --data-urlencode "format=json" --data-urlencode "limit=1" https://nominatim.openstreetmap.org/search
```

### Cross street

Two street names joined by "and", "&", "at" or "corner of", with no house number, such as "24th and Madison".

Nominatim cannot resolve this, because "and" returns nothing and "&" only matches bus stops named after corners, often the wrong one.

Resolve it with one Overpass request for the node the two streets share inside Seattle, matching each street on its core name so the user can leave off the direction and street type:

```
[out:json][timeout:25];
area["name"="Seattle"]["boundary"="administrative"]->.city;
way(area.city)["highway"]["name"~"(^| )24th( |$)",i]->.a;
way(area.city)["highway"]["name"~"(^| )Madison( |$)",i]->.b;
node(w.a)(w.b);
out;
```

Send it with `curl --silent --max-time 40 --user-agent "foraging-route (taylormonacelli@gmail.com)" --data-urlencode data@<query file> https://overpass-api.de/api/interpreter`, writing the query file to `$CLAUDE_JOB_DIR/tmp`.

Nodes within 150ft of each other are one corner, so average them.

Distinct corners mean the core names were ambiguous, as with "24th Avenue East" and "24th Avenue South", so take the corner nearest the mean position of the trees and name the full street names in the report.

An empty result means the two streets do not meet on the map, so tell the user and ask for a nearby address rather than sending further queries.

### Place name

Any other text that names somewhere, such as "Macrina Bakery".

Geocode it with one Nominatim request bounded to Seattle, adding `--data-urlencode "viewbox=-122.46,47.73,-122.22,47.48" --data-urlencode "bounded=1" --data-urlencode "limit=5"` to the address request, and when several places match take the one nearest the mean position of the trees and name it in the report.

### No location

Text that identifies no place, such as "route me to the trees".

Ask the user for a cross street or address, because the skill cannot read the phone's position.

### Every type

Send each lookup once, and on an HTTP 429 wait 30s and retry once before telling the user the lookup service is busy.

Round every coordinate to 6 decimal places, about 4in of precision, and use that same rounded value in the request and in both links.

The step is done when one decimal pair is in hand together with its input type and which part of the user's input it came from.

## Step 2: Read the stops from the notes

Every `.md` file in `/Users/mtm/Documents/Obsidian Vault` whose `part_of` front matter property contains `[[apples and plums near us]]` is one stop, named by its file name without the extension, with its position in the `latitude` and `longitude` front matter properties.

Find them by listing the files in the vault root that mention `[[apples and plums near us]]` and keeping those with the `part_of` property, which leaves out the hub note itself and any other note that only links to it.

Files without both position properties are not stops.

Read the notes fresh on every run, because trees get added.

The step is done when every stop has a name and a decimal pair.

OSRM caps a trip at 100 coordinates, so more than 99 stops has to be reported to the user rather than silently truncated.

## Step 3: Call the trip solver

Build one request with the start first and every stop after it, each written longitude first, which is the reverse of how the note and Google write them:

```
https://routing.openstreetmap.de/routed-foot/trip/v1/foot/<start_lon>,<start_lat>;<lon1>,<lat1>;<lon2>,<lat2>?source=first&destination=any&roundtrip=false&overview=false
```

Fetch it with `curl --silent --max-time 20`.

`source=first` pins the walk to the user's position, and dropping it makes the server answer `NotImplemented`, because an open path needs a fixed start.

The routing.openstreetmap.de host serves a real foot profile, while router.project-osrm.org silently answers with driving distances whatever the URL path says.

The step is done when the response has `"code":"Ok"`, and any other code is reported to the user verbatim with the request URL.

## Step 4: Read the visiting order

Parse the JSON with a short script run through `uv run --no-active`, never by eye, and that one throwaway script may also read the note, build the request and build the links in Steps 2 to 5, kept in `$CLAUDE_JOB_DIR/tmp` and never in the vault.

The `waypoints` array stays in the order the coordinates were sent, and each entry's `waypoint_index` is that point's position in the solved walk, so sort by `waypoint_index` to get the order.

`trips[0].legs` holds one leg per consecutive pair in that solved order, and `trips[0].distance` and `trips[0].duration` are the totals in metres and seconds.

Each waypoint's `distance` is how far in metres OSRM snapped that point to the nearest path, and any point, start or stop, snapped more than 15m, about 50ft, gets named in the report because the route then begins or ends somewhere other than the pin.

The step is done when every stop has a position in the order and a leg distance.

## Step 5: Build the links

The map link draws the walk on the OSRM demo frontend, one `loc` per point in solved order, latitude first, with `profile=2` for foot and `center` set to the mean latitude and mean longitude of all the points:

```
https://map.project-osrm.org/?z=14&center=<lat>%2C<lon>&loc=<start_lat>%2C<start_lon>&loc=<lat1>%2C<lon1>&hl=en&alt=0&ly=openstreetmap.de&profile=2
```

The Google Maps link opens turn-by-turn walking directions, with `origin` left out so Maps starts from the phone's live position, the last stop as `destination`, and the stops between as `%7C`-separated `waypoints`, latitude first:

```
https://www.google.com/maps/dir/?api=1&travelmode=walking&destination=<last_lat>,<last_lon>&waypoints=<lat1>,<lon1>%7C<lat2>,<lon2>
```

Leaving `origin` out means Maps walks the solved order from wherever the phone is when the link is opened, so the order is only shortest while the user is still near the start they gave.

Google allows 9 waypoints in the Maps app and only 3 in a mobile browser, so with more than 3 tell the user to open it in the app, and with more than 9 split the walk into consecutive links where each starts at the previous link's last stop.

The step is done when both links are built from the solved order.

## Step 6: Report

Give distances in miles, dividing metres by 1,609.344, rounding to 2 decimal places and writing them squashed like `0.35mi`.

Give the total time rounded to the nearest minute and written compactly like `1h9m`.

Report in this order, one sentence per paragraph:

- the resolved start, its input type, and which part of the input it came from, with the full street or place name when a cross street or place name was matched
- the number of stops read from the notes
- the total distance and time, and the stop the walk ends at
- any point snapped more than 15m
- the table of the order
- the app-versus-browser warning when the Google link has more than 3 waypoints
- the map link and the Google Maps link

The legs are rounded one by one, so when they sum to 0.01mi more or less than the total, keep the total computed from the unrounded metres.

| stop | tree | leg |
| --- | --- | --- |
| 1 | <note name> | <miles> |
| total | | <miles> |

Put the map link and the Google Maps link bare on their own lines below the table.
