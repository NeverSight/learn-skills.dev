---
name: tesla
version: "3.0.0"
description: Complete Tesla Fleet API control - all 66 vehicle commands, energy/Powerwall management, vehicle sharing, charging history, navigation, media, V2G/Powershare, and multi-vehicle management from the terminal.
author: mvanhorn
license: MIT
repository: https://github.com/mvanhorn/clawdbot-skill-tesla
homepage: https://developer.tesla.com/docs/fleet-api
metadata:
  openclaw:
    emoji: "🚗"
    requires:
      env:
        - TESLA_EMAIL
    primaryEnv: TESLA_EMAIL
    tags:
      - tesla
      - vehicle
      - iot
      - fleet-api
      - electric-vehicle
      - ev
      - charging
      - supercharger
      - powerwall
      - solar
      - energy
      - automotive
      - cybertruck
      - v2g
      - powershare
      - navigation
      - media
    triggers:
      - tesla
      - my car
      - my vehicle
      - battery level
      - charge status
      - lock my car
      - unlock my car
      - car location
      - where is my car
      - climate control
      - precondition
      - supercharger
      - powerwall
      - solar panels
      - energy usage
      - fleet api
      - honk horn
      - flash lights
      - charge my car
      - sentry mode
      - valet mode
      - dog mode
      - camp mode
      - navigate to
      - media controls
      - seat heater
      - steering wheel heater
      - charge history
      - share my car
      - guest mode
      - speed limit
      - software update
      - boombox
      - bioweapon defense
      - cabin overheat
      - v2g
      - powershare
---

# Tesla

Complete Tesla Fleet API control from OpenClaw. All 66 vehicle commands, energy/Powerwall management, vehicle sharing, charging history, navigation, media controls, V2G/Powershare, and multi-vehicle management.

> **Fleet API (2026):** Tesla has deprecated the legacy Owner API. All vehicles now use the Fleet API at
> `fleet-api.prd.na.vn.cloud.tesla.com`. Vehicles on firmware 2024.26+ require the Vehicle Command Protocol
> (VCP). The `tesla-fleet-api` Python package handles both paths automatically.

---

## Setup

### Prerequisites

- Python 3.10+
- A Tesla account with at least one vehicle, Powerwall, or solar system
- `TESLA_EMAIL` environment variable set to your Tesla account email

### First-time authentication

```bash
TESLA_EMAIL="you@email.com" python3 {baseDir}/scripts/tesla.py auth
```

Steps:
1. The script displays a Tesla login URL
2. Open it in your browser, sign in, and authorize the application
3. Copy the callback URL from your browser's address bar (starts with `https://auth.tesla.com/void/callback?...`)
4. Paste it back into the terminal
5. Token is cached at `~/.tesla_cache.json` for ~30 days with automatic refresh

### Environment variables

| Variable | Required | Description |
|---|---|---|
| `TESLA_EMAIL` | Yes | Your Tesla account email address |

Token storage: `~/.tesla_cache.json` (auto-created on first auth, auto-refreshes)

---

## Vehicle Command Protocol (VCP)

Vehicles running firmware 2024.26 or later require VCP for sending commands. Without VCP configured, status queries will work but commands (lock, unlock, climate, charge start/stop) will fail with a `vehicle_command_protocol_required` error.

### How to check if VCP is needed

```bash
python3 {baseDir}/scripts/tesla.py status
```

If you see a VCP error in the output, your vehicle needs VCP setup.

### VCP setup

1. Generate a public/private key pair on your machine:
   ```bash
   openssl ecparam -name prime256v1 -genkey -noout -out private_key.pem
   openssl ec -in private_key.pem -pubout -out public_key.pem
   ```

2. Register your public key with Tesla's servers. This requires creating a third-party application at https://developer.tesla.com/ and uploading your `public_key.pem` to a `.well-known` endpoint on your registered domain.

3. Pair your key with each vehicle. Sit inside the vehicle with the key card on the center console, then run:
   ```bash
   python3 {baseDir}/scripts/tesla.py vcp-pair --key private_key.pem
   ```
   Tap "Approve" on the vehicle's touchscreen when prompted.

4. Once paired, commands are end-to-end encrypted between your machine and the vehicle. The `tesla-fleet-api` package handles signing automatically when it finds your key.

> **Note:** If you are only reading vehicle data (status, location, charge state), VCP is not required. VCP is only needed for sending commands.

---

## Dashboard

Get a unified view of all your vehicles in one command:

```bash
python3 {baseDir}/scripts/tesla.py dashboard
```

Output includes for each vehicle:
- Name, model, and state (online/asleep/offline)
- Battery level and estimated range
- Charging state and time remaining (if charging)
- Location as a human-readable address (reverse geocoded from GPS)
- Lock status (locked/unlocked)
- Climate state (on/off, cabin temperature)
- Software version and any pending updates
- Sentry mode status

Example output:
```
--- Dashboard ---

1. Snowflake (Model Y - Online)
   Battery: 78% (245 mi)    Charging: Not charging
   Location: 4521 Mercer Way, Mercer Island, WA 98040
   Locked: Yes    Sentry: On    Climate: Off (68F inside)
   Software: 2025.48.3 (up to date)

2. Stella (Model 3 - Asleep)
   Battery: 92% (310 mi)    Charging: Complete
   Location: 1200 NE 45th St, Seattle, WA 98105
   Locked: Yes    Sentry: Off    Climate: Off
   Software: 2025.48.3 (update available: 2025.50.1)
```

---

## Multi-Vehicle Management

### List all vehicles

```bash
python3 {baseDir}/scripts/tesla.py list
```

Shows all vehicles on your account with name, VIN, model, state, and battery level.

### Select a specific vehicle

Use `--car` or `-c` with any command to target a specific vehicle by its display name:

```bash
python3 {baseDir}/scripts/tesla.py --car "Snowflake" status
python3 {baseDir}/scripts/tesla.py -c "Stella" lock
python3 {baseDir}/scripts/tesla.py --car "Snowflake" climate on
```

Without `--car`, commands target your first vehicle.

### Set a default vehicle

If you have multiple vehicles and mostly control one, set a default:

```bash
python3 {baseDir}/scripts/tesla.py set-default "Stella"
```

The default persists in `~/.tesla_cache.json`. Override it anytime with `--car`.

---

## Vehicle Commands Reference (66 commands)

### Doors and Access

```bash
# Lock/unlock
python3 {baseDir}/scripts/tesla.py lock                    # door_lock
python3 {baseDir}/scripts/tesla.py unlock                  # door_unlock

# Trunk and frunk (actuate_trunk)
python3 {baseDir}/scripts/tesla.py trunk open              # actuate_trunk rear
python3 {baseDir}/scripts/tesla.py frunk open              # actuate_trunk front

# Windows (window_control)
python3 {baseDir}/scripts/tesla.py windows vent            # Vent all windows
python3 {baseDir}/scripts/tesla.py windows close           # Close all windows

# Sunroof (sun_roof_control) - vehicles with panoramic sunroof
python3 {baseDir}/scripts/tesla.py sunroof vent            # Vent sunroof
python3 {baseDir}/scripts/tesla.py sunroof close           # Close sunroof

# HomeLink (trigger_homelink) - garage door
python3 {baseDir}/scripts/tesla.py homelink                # Trigger nearest HomeLink device
python3 {baseDir}/scripts/tesla.py homelink --lat 47.57 --lon -122.22  # Trigger at specific location
```

Fleet API endpoints: `door_lock`, `door_unlock`, `actuate_trunk`, `window_control`, `sun_roof_control`, `trigger_homelink`

### Charging

```bash
# Basic charging
python3 {baseDir}/scripts/tesla.py charge start            # charge_start
python3 {baseDir}/scripts/tesla.py charge stop             # charge_stop
python3 {baseDir}/scripts/tesla.py charge status           # GET charge_state

# Charge port
python3 {baseDir}/scripts/tesla.py charge port-open        # charge_port_door_open
python3 {baseDir}/scripts/tesla.py charge port-close       # charge_port_door_close

# Charge limit
python3 {baseDir}/scripts/tesla.py charge limit 80         # set_charge_limit (percentage)
python3 {baseDir}/scripts/tesla.py charge limit standard   # charge_standard (daily limit)
python3 {baseDir}/scripts/tesla.py charge limit max        # charge_max_range (trip limit)

# Charging amps (set_charging_amps) - limit current draw
python3 {baseDir}/scripts/tesla.py charge amps 32          # Set to 32A
python3 {baseDir}/scripts/tesla.py charge amps 16          # Set to 16A (reduce for shared circuits)

# Charge schedules (NEW - replaces deprecated set_scheduled_charging)
python3 {baseDir}/scripts/tesla.py charge schedule add 23:00 06:00    # add_charge_schedule (off-peak window)
python3 {baseDir}/scripts/tesla.py charge schedule add 01:00 05:00 --days mon,tue,wed,thu,fri
python3 {baseDir}/scripts/tesla.py charge schedule remove 1           # remove_charge_schedule (by schedule ID)
python3 {baseDir}/scripts/tesla.py charge schedule list               # List active charge schedules
```

Fleet API endpoints: `charge_start`, `charge_stop`, `charge_port_door_open`, `charge_port_door_close`, `charge_standard`, `charge_max_range`, `set_charge_limit`, `set_charging_amps`, `add_charge_schedule`, `remove_charge_schedule`

> **Deprecation:** `set_scheduled_charging` is deprecated. Use `add_charge_schedule` / `remove_charge_schedule` instead.

### Climate

```bash
# On/off (auto_conditioning_start / auto_conditioning_stop)
python3 {baseDir}/scripts/tesla.py climate on
python3 {baseDir}/scripts/tesla.py climate off

# Temperature (set_temps)
python3 {baseDir}/scripts/tesla.py climate temp 72                 # Fahrenheit (default)
python3 {baseDir}/scripts/tesla.py climate temp 22 --celsius       # Celsius
python3 {baseDir}/scripts/tesla.py climate temp 72 --driver-only   # Driver side only

# Max preconditioning (set_preconditioning_max)
python3 {baseDir}/scripts/tesla.py climate max-precondition on     # Maximum defrost/heat
python3 {baseDir}/scripts/tesla.py climate max-precondition off

# Precondition schedules (NEW - replaces deprecated set_scheduled_departure)
python3 {baseDir}/scripts/tesla.py climate schedule add 07:30              # add_precondition_schedule
python3 {baseDir}/scripts/tesla.py climate schedule add 07:30 --days weekdays
python3 {baseDir}/scripts/tesla.py climate schedule remove 1               # remove_precondition_schedule
python3 {baseDir}/scripts/tesla.py climate schedule list

# Seat heater (remote_seat_heater_request) - 0=off, 1=low, 2=medium, 3=high
python3 {baseDir}/scripts/tesla.py climate seat-heater driver 2
python3 {baseDir}/scripts/tesla.py climate seat-heater passenger 1
python3 {baseDir}/scripts/tesla.py climate seat-heater rear-left 3
python3 {baseDir}/scripts/tesla.py climate seat-heater rear-center 1
python3 {baseDir}/scripts/tesla.py climate seat-heater rear-right 2

# Seat cooler (remote_seat_cooler_request) - vehicles with ventilated seats
python3 {baseDir}/scripts/tesla.py climate seat-cooler driver 2
python3 {baseDir}/scripts/tesla.py climate seat-cooler passenger 1

# Steering wheel heater (remote_steering_wheel_heater_request)
python3 {baseDir}/scripts/tesla.py climate steering-heater on
python3 {baseDir}/scripts/tesla.py climate steering-heater off

# Bioweapon defense mode (set_bioweapon_mode) - vehicles with HEPA filter
python3 {baseDir}/scripts/tesla.py climate bioweapon on
python3 {baseDir}/scripts/tesla.py climate bioweapon off

# Cabin overheat protection (set_cabin_overheat_protection)
python3 {baseDir}/scripts/tesla.py climate overheat-protection on
python3 {baseDir}/scripts/tesla.py climate overheat-protection off
python3 {baseDir}/scripts/tesla.py climate overheat-protection fan-only  # No AC, fan only

# Climate keeper mode (set_climate_keeper_mode)
python3 {baseDir}/scripts/tesla.py climate keeper off       # Off
python3 {baseDir}/scripts/tesla.py climate keeper keep      # Keep climate on
python3 {baseDir}/scripts/tesla.py climate keeper dog       # Dog mode (display shows temp)
python3 {baseDir}/scripts/tesla.py climate keeper camp      # Camp mode (media + climate)
```

Fleet API endpoints: `auto_conditioning_start`, `auto_conditioning_stop`, `set_temps`, `set_preconditioning_max`, `add_precondition_schedule`, `remove_precondition_schedule`, `remote_seat_heater_request`, `remote_seat_cooler_request`, `remote_steering_wheel_heater_request`, `set_bioweapon_mode`, `set_cabin_overheat_protection`, `set_climate_keeper_mode`

> **Deprecation:** `set_scheduled_departure` is deprecated. Use `add_precondition_schedule` / `remove_precondition_schedule` instead.

### Security

```bash
# Sentry mode (set_sentry_mode)
python3 {baseDir}/scripts/tesla.py sentry on
python3 {baseDir}/scripts/tesla.py sentry off

# Valet mode (set_valet_mode)
python3 {baseDir}/scripts/tesla.py valet on                # Enable valet mode
python3 {baseDir}/scripts/tesla.py valet on --pin 1234     # Enable with PIN
python3 {baseDir}/scripts/tesla.py valet off --pin 1234    # Disable with PIN

# Reset valet PIN (reset_valet_pin)
python3 {baseDir}/scripts/tesla.py valet reset-pin

# PIN to drive (set_pin_to_drive)
python3 {baseDir}/scripts/tesla.py pin-to-drive on --pin 1234   # Require PIN to shift out of park
python3 {baseDir}/scripts/tesla.py pin-to-drive off --pin 1234

# Speed limit (speed_limit_activate / speed_limit_deactivate / speed_limit_set_limit)
python3 {baseDir}/scripts/tesla.py speed-limit set 70      # Set limit to 70 mph (50-90 mph range)
python3 {baseDir}/scripts/tesla.py speed-limit activate --pin 1234
python3 {baseDir}/scripts/tesla.py speed-limit deactivate --pin 1234

# Guest mode (guest_mode)
python3 {baseDir}/scripts/tesla.py guest-mode on           # Enable guest restrictions
python3 {baseDir}/scripts/tesla.py guest-mode off

# Remote start drive (remote_start_drive) - start without key for 2 minutes
python3 {baseDir}/scripts/tesla.py remote-start

# Erase user data (erase_user_data) - factory reset personal data
python3 {baseDir}/scripts/tesla.py erase-data --confirm    # Requires --confirm flag
```

Fleet API endpoints: `set_sentry_mode`, `set_valet_mode`, `reset_valet_pin`, `set_pin_to_drive`, `speed_limit_activate`, `speed_limit_deactivate`, `speed_limit_set_limit`, `guest_mode`, `remote_start_drive`, `erase_user_data`

### Navigation

```bash
# Navigate to address (navigation_request)
python3 {baseDir}/scripts/tesla.py navigate "1600 Amphitheatre Parkway, Mountain View, CA"

# Navigate to GPS coordinates (navigation_gps_request)
python3 {baseDir}/scripts/tesla.py navigate --gps 47.6062 -122.3321

# Navigate to nearest Supercharger (navigation_sc_request)
python3 {baseDir}/scripts/tesla.py navigate --supercharger
python3 {baseDir}/scripts/tesla.py navigate --supercharger "Bellevue"  # Specific Supercharger

# Multi-stop route (navigation_waypoints_request)
python3 {baseDir}/scripts/tesla.py navigate --waypoints "Seattle, WA" "Portland, OR" "San Francisco, CA"
```

Fleet API endpoints: `navigation_request`, `navigation_gps_request`, `navigation_sc_request`, `navigation_waypoints_request`

### Media

```bash
# Playback
python3 {baseDir}/scripts/tesla.py media play              # media_toggle_playback (play/pause)
python3 {baseDir}/scripts/tesla.py media pause              # media_toggle_playback

# Track navigation
python3 {baseDir}/scripts/tesla.py media next               # media_next_track
python3 {baseDir}/scripts/tesla.py media prev               # media_prev_track

# Favorites
python3 {baseDir}/scripts/tesla.py media next-fav           # media_next_fav
python3 {baseDir}/scripts/tesla.py media prev-fav           # media_prev_fav

# Volume
python3 {baseDir}/scripts/tesla.py media volume up          # adjust_volume (increment)
python3 {baseDir}/scripts/tesla.py media volume down         # media_volume_down
python3 {baseDir}/scripts/tesla.py media volume 7            # adjust_volume (absolute, 0-11)
```

Fleet API endpoints: `media_toggle_playback`, `media_next_track`, `media_prev_track`, `media_next_fav`, `media_prev_fav`, `media_volume_down`, `adjust_volume`

### Other Commands

```bash
# Honk and flash
python3 {baseDir}/scripts/tesla.py honk                     # honk_horn
python3 {baseDir}/scripts/tesla.py flash                     # flash_lights

# Boombox (remote_boombox) - external speaker, vehicle must be in park
python3 {baseDir}/scripts/tesla.py boombox play              # Play boombox sound
python3 {baseDir}/scripts/tesla.py boombox stop              # Stop boombox

# Vehicle name (set_vehicle_name)
python3 {baseDir}/scripts/tesla.py set-name "Snowflake"

# Software updates (schedule_software_update / cancel_software_update)
python3 {baseDir}/scripts/tesla.py software-update start     # Install now
python3 {baseDir}/scripts/tesla.py software-update schedule 120  # Schedule in 120 minutes
python3 {baseDir}/scripts/tesla.py software-update cancel    # Cancel pending update

# Wake
python3 {baseDir}/scripts/tesla.py wake                     # Wake sleeping vehicle
```

Fleet API endpoints: `honk_horn`, `flash_lights`, `remote_boombox`, `set_vehicle_name`, `schedule_software_update`, `cancel_software_update`

---

## Vehicle Sharing (6 endpoints)

Share vehicle access with other Tesla accounts.

```bash
# List sharing invitations
python3 {baseDir}/scripts/tesla.py sharing invitations           # GET /invitations

# Send sharing invitation
python3 {baseDir}/scripts/tesla.py sharing invite user@email.com  # POST /invitations

# Redeem an invitation (as the recipient)
python3 {baseDir}/scripts/tesla.py sharing redeem <invitation_code>  # POST /invitations/redeem

# Revoke an invitation
python3 {baseDir}/scripts/tesla.py sharing revoke <invitation_id>    # POST /invitations/{id}/revoke

# List drivers with access
python3 {baseDir}/scripts/tesla.py sharing drivers               # GET /drivers

# Remove a driver
python3 {baseDir}/scripts/tesla.py sharing remove-driver <driver_id>  # DELETE /drivers
```

Fleet API endpoints: `GET /invitations`, `POST /invitations`, `POST /invitations/redeem`, `POST /invitations/{id}/revoke`, `GET /drivers`, `DELETE /drivers`

---

## Vehicle Info Endpoints

```bash
# Vehicle specifications
python3 {baseDir}/scripts/tesla.py info specs                    # GET /specs

# Vehicle options (original build configuration)
python3 {baseDir}/scripts/tesla.py info options                  # GET /options

# Release notes for current firmware
python3 {baseDir}/scripts/tesla.py info release-notes            # GET /release_notes

# Recent vehicle alerts
python3 {baseDir}/scripts/tesla.py info alerts                   # GET /recent_alerts

# Service data (maintenance history)
python3 {baseDir}/scripts/tesla.py info service                  # GET /service_data

# Warranty details
python3 {baseDir}/scripts/tesla.py info warranty                 # GET /warranty_details
```

Fleet API endpoints: `GET /specs`, `GET /options`, `GET /release_notes`, `GET /recent_alerts`, `GET /service_data`, `GET /warranty_details`

---

## Energy Monitoring (Powerwall / Solar) - 12 endpoints

If your Tesla account includes Powerwall or solar products, you can monitor and control them.

### List energy sites

```bash
python3 {baseDir}/scripts/tesla.py energy list                   # GET /products
```

Shows all energy products on your account (Powerwall, Solar Roof, standalone solar).

### Energy status

```bash
# Site info (GET /site_info)
python3 {baseDir}/scripts/tesla.py energy info

# Current energy flow (GET /live_status)
python3 {baseDir}/scripts/tesla.py energy status

# Example output:
# Home Energy Status:
#   Solar: 4.2 kW generating
#   Powerwall: 87% (10.4 kWh stored)
#   Grid: Exporting 1.8 kW
#   Home: Using 2.4 kW
#   Mode: Self-Powered
```

### Energy history

```bash
# Energy production/consumption history (GET /calendar_history?kind=energy)
python3 {baseDir}/scripts/tesla.py energy history --days 7       # Watt hours over last 7 days
python3 {baseDir}/scripts/tesla.py energy history --months 1     # Monthly summary

# Backup events (GET /calendar_history?kind=backup)
python3 {baseDir}/scripts/tesla.py energy backup-history         # Off-grid events log

# Wall Connector telemetry (GET /telemetry_history?kind=charge)
python3 {baseDir}/scripts/tesla.py energy wall-connector-history # Wall Connector charge sessions
```

### Powerwall controls

```bash
# Set backup reserve percentage (POST /backup)
python3 {baseDir}/scripts/tesla.py energy reserve 20

# Storm watch (POST /storm_mode)
python3 {baseDir}/scripts/tesla.py energy storm-watch on
python3 {baseDir}/scripts/tesla.py energy storm-watch off

# Time-of-use settings (POST /time_of_use_settings)
python3 {baseDir}/scripts/tesla.py energy tou-settings --peak-start 16:00 --peak-end 21:00

# Grid import/export config (POST /grid_import_export)
python3 {baseDir}/scripts/tesla.py energy grid-config --export on --import on

# Off-grid vehicle charging reserve (POST /off_grid_vehicle_charging_reserve)
python3 {baseDir}/scripts/tesla.py energy vehicle-charge-reserve 50  # Reserve 50% for vehicle charging

# Operating mode (POST /operation)
python3 {baseDir}/scripts/tesla.py energy mode self-powered      # Maximize solar self-consumption
python3 {baseDir}/scripts/tesla.py energy mode time-based        # Optimize for time-of-use rates
python3 {baseDir}/scripts/tesla.py energy mode backup-only       # Reserve for backup only
```

Fleet API endpoints: `GET /products`, `GET /site_info`, `GET /live_status`, `GET /calendar_history?kind=energy`, `GET /calendar_history?kind=backup`, `GET /telemetry_history?kind=charge`, `POST /backup`, `POST /storm_mode`, `POST /time_of_use_settings`, `POST /grid_import_export`, `POST /off_grid_vehicle_charging_reserve`, `POST /operation`

---

## Charging History (3 endpoints)

View past charging sessions and invoices.

```bash
# Charging history (GET /charging/history)
python3 {baseDir}/scripts/tesla.py charging history              # All charging sessions
python3 {baseDir}/scripts/tesla.py charging history --days 30    # Last 30 days
python3 {baseDir}/scripts/tesla.py charging history --type supercharger  # Supercharger sessions only

# Charging invoice (GET /charging/invoice/{id})
python3 {baseDir}/scripts/tesla.py charging invoice <invoice_id>

# Active charging sessions (GET /charging/sessions)
python3 {baseDir}/scripts/tesla.py charging sessions             # Currently active sessions
```

Fleet API endpoints: `GET /charging/history`, `GET /charging/invoice/{id}`, `GET /charging/sessions`

---

## Charge Station Finder

Find nearby Tesla Superchargers and destination chargers.

```bash
# Find Superchargers near your vehicle's current location
python3 {baseDir}/scripts/tesla.py chargers nearby

# Find chargers near a specific address
python3 {baseDir}/scripts/tesla.py chargers nearby --address "Seattle, WA"

# Find chargers near GPS coordinates
python3 {baseDir}/scripts/tesla.py chargers nearby --lat 47.6062 --lon -122.3321

# Filter by charger type
python3 {baseDir}/scripts/tesla.py chargers nearby --type supercharger
python3 {baseDir}/scripts/tesla.py chargers nearby --type destination

# Show availability (stalls in use vs total)
python3 {baseDir}/scripts/tesla.py chargers nearby --availability
```

Example output:
```
Superchargers near Snowflake (4521 Mercer Way, Mercer Island, WA):

1. Tesla Supercharger - Bellevue, WA (3.2 mi)
   1234 Bellevue Way NE - 12 stalls (8 available)
   250 kW - Open 24/7
   Navigate: https://www.google.com/maps/dir/?api=1&destination=47.6101,-122.2015

2. Tesla Supercharger - Renton, WA (5.8 mi)
   800 Rainier Ave S - 8 stalls (5 available)
   150 kW - Open 24/7
   Navigate: https://www.google.com/maps/dir/?api=1&destination=47.4799,-122.2034
```

### Navigate to charger

```bash
# Send navigation to the nearest Supercharger directly to your vehicle
python3 {baseDir}/scripts/tesla.py chargers navigate 1
```

---

## V2G / Powershare

Tesla's vehicle-to-grid (V2G) and Powershare features allow compatible vehicles to export energy back to the home or grid.

### Status

```bash
# Check Powershare status (PowershareStatus telemetry field)
python3 {baseDir}/scripts/tesla.py powershare status

# Example output:
# Powershare Status:
#   State: Exporting
#   Power: 5.2 kW to home
#   Battery: 72% (reserve set to 50%)
```

### Compatibility

- **Cybertruck:** V2G program available in Texas (launched Feb 2026). Requires Powershare Home Backup Gateway.
- **Powerwall 3:** Native bidirectional capability with compatible vehicles.
- **Telemetry:** `PowershareStatus` field available via Fleet API telemetry streaming.

---

## Deprecation Warnings

The following Fleet API endpoints are deprecated and will be removed in a future API version:

| Deprecated Endpoint | Replacement | Notes |
|---|---|---|
| `set_scheduled_charging` | `add_charge_schedule` / `remove_charge_schedule` | New schedule endpoints support multiple schedules and day-of-week filtering |
| `set_scheduled_departure` | `add_precondition_schedule` / `remove_precondition_schedule` | New schedule endpoints support multiple schedules and day-of-week filtering |

The skill uses the new endpoints by default. If you have scripts using the old `schedule charge-window` or `schedule precondition` syntax, they have been migrated to the new API automatically.

---

## Location

```bash
# Get location as address + GPS coordinates + Google Maps link
python3 {baseDir}/scripts/tesla.py location

# GPS coordinates only (no reverse geocoding)
python3 {baseDir}/scripts/tesla.py location --gps-only

# Example output:
# Snowflake Location:
#   Address: 4521 Mercer Way, Mercer Island, WA 98040
#   GPS: 47.5707, -122.2220
#   Map: https://www.google.com/maps?q=47.5707,-122.2220
#   Speed: Parked
#   Heading: 185 (S)
```

The location command reverse geocodes GPS coordinates to a human-readable street address using the Nominatim API (OpenStreetMap, no API key needed). Falls back to raw GPS if geocoding fails.

---

## Error Recovery

### Authentication expired

If your token has expired (after ~30 days without use), you will see:
```
Error: Token expired or revoked
```

Fix: Re-authenticate:
```bash
TESLA_EMAIL="you@email.com" python3 {baseDir}/scripts/tesla.py auth
```

### Vehicle asleep

Vehicles go to sleep after ~15 minutes of inactivity to save battery. The script automatically wakes the vehicle before sending commands, but if wake fails:
```
Error: Vehicle did not wake up within 30 seconds
```

Fix: Try again - the vehicle may need more time. The script retries up to 3 times with 10-second intervals:
```bash
python3 {baseDir}/scripts/tesla.py wake
# Then retry your command
python3 {baseDir}/scripts/tesla.py status
```

If the vehicle is in a deep sleep state (e.g., parked for days), it may take up to 2 minutes to wake. The script handles this automatically with exponential backoff.

### VCP not configured

If you see:
```
Error: vehicle_command_protocol_required
```

Your vehicle's firmware requires VCP for commands. See the [VCP setup section](#vehicle-command-protocol-vcp) above. Note that read-only operations (status, location, charge status) still work without VCP.

### Command timeout

If a command times out:
```
Error: Command timed out after 30 seconds
```

The vehicle may be in an area with poor cellular connectivity. The command may still execute - check status before retrying. Common in underground parking or remote areas.

### Rate limiting

The Tesla Fleet API enforces rate limits. If you see:
```
Error: 429 Too Many Requests
```

Wait 60 seconds before retrying. Avoid polling status more frequently than once per minute.

### Vehicle offline

If the vehicle shows as "offline", it has no cellular connection. Commands cannot be sent until it reconnects. This can happen in:
- Underground parking garages
- Remote areas without cell coverage
- When the 12V battery is very low

No fix except waiting for the vehicle to regain connectivity.

---

## Example Chat Usage

Ask naturally and the skill handles the rest:

- "Show me my Tesla dashboard"
- "Is my Tesla locked?"
- "Lock Stella"
- "What's Snowflake's battery level?"
- "Where is my Model Y?"
- "Turn on the AC in Stella and set it to 72"
- "Honk the horn on Snowflake"
- "Start charging my car"
- "Set the charge limit to 80%"
- "Open the frunk"
- "Set the charge amps to 16"
- "Turn on sentry mode"
- "Put Stella in dog mode"
- "Enable camp mode"
- "Turn on bioweapon defense mode"
- "Set a speed limit of 65 mph"
- "Enable valet mode with PIN 1234"
- "Navigate to Pike Place Market"
- "Send the nearest Supercharger to my car's nav"
- "Navigate with stops through Portland and San Francisco"
- "Play next track"
- "Set volume to 5"
- "Turn on the seat heater for the driver"
- "Turn on the seat cooler for the passenger"
- "Turn on the steering wheel heater"
- "Set cabin overheat protection to fan only"
- "Enable PIN to drive"
- "Start remote drive"
- "Precondition my car for 7:30 AM on weekdays"
- "Schedule charging between 11 PM and 6 AM"
- "Find the nearest Supercharger"
- "How much solar am I generating right now?"
- "What's my Powerwall battery at?"
- "Set Powerwall to self-powered mode"
- "Turn on storm watch"
- "Show my charging history"
- "Who has access to my car?"
- "Invite user@email.com to drive my Tesla"
- "Remove the guest driver"
- "Rename my car to Thunder"
- "Install the software update now"
- "Schedule the software update for 2 hours from now"
- "Cancel the software update"
- "Play the boombox"
- "Open the garage door"
- "What are my car's specs?"
- "Show the release notes"
- "Any recent alerts on my car?"
- "What's my warranty status?"
- "What's my Powershare status?"
- "Show my Wall Connector charging history"

---

## API Reference

This skill uses the Tesla Fleet API:
- **Endpoint:** `fleet-api.prd.na.vn.cloud.tesla.com`
- **Auth:** OAuth2 via `TESLA_EMAIL` with token cached locally
- **Python package:** `tesla-fleet-api` (handles Fleet API + VCP automatically)
- **Docs:** https://developer.tesla.com/docs/fleet-api

The Fleet API replaced the legacy Owner API (tesla-api.timdorr.com) which is no longer functional.

### Command coverage (66 vehicle commands)

| Category | Commands | Count |
|---|---|---|
| Doors/Access | door_lock, door_unlock, actuate_trunk (front/rear), window_control, sun_roof_control, trigger_homelink | 6 |
| Charging | charge_start, charge_stop, charge_port_door_open, charge_port_door_close, charge_standard, charge_max_range, set_charge_limit, set_charging_amps, add_charge_schedule, remove_charge_schedule | 10 |
| Climate | auto_conditioning_start, auto_conditioning_stop, set_temps, set_preconditioning_max, add_precondition_schedule, remove_precondition_schedule, remote_seat_heater_request, remote_seat_cooler_request, remote_steering_wheel_heater_request, set_bioweapon_mode, set_cabin_overheat_protection, set_climate_keeper_mode | 12 |
| Security | set_sentry_mode, set_valet_mode, reset_valet_pin, set_pin_to_drive, speed_limit_activate, speed_limit_deactivate, speed_limit_set_limit, guest_mode, erase_user_data, remote_start_drive | 10 |
| Navigation | navigation_request, navigation_gps_request, navigation_sc_request, navigation_waypoints_request | 4 |
| Media | media_toggle_playback, media_next_track, media_prev_track, media_next_fav, media_prev_fav, media_volume_down, adjust_volume | 7 |
| Other | honk_horn, flash_lights, remote_boombox, set_vehicle_name, schedule_software_update, cancel_software_update | 6 |
| **Subtotal** | | **55** |
| Sharing | GET/POST /invitations, POST /invitations/redeem, POST /invitations/{id}/revoke, GET /drivers, DELETE /drivers | 6 |
| Vehicle Info | GET /specs, /options, /release_notes, /recent_alerts, /service_data, /warranty_details | 6 |
| **Total vehicle endpoints** | | **67** |

Plus 12 energy endpoints and 3 charging history endpoints for a complete Fleet API integration.

---

## Privacy and Security

- All credentials are stored locally on your machine only
- OAuth2 refresh token cached in `~/.tesla_cache.json`
- No data is sent to any third party
- VCP commands are end-to-end encrypted between your machine and the vehicle
- Reverse geocoding uses OpenStreetMap Nominatim (sends only GPS coordinates, no account data)
- Tokens auto-refresh for ~30 days; re-auth required if unused for longer
- PIN-protected commands (valet, speed limit, pin-to-drive) require explicit PIN entry
- `erase_user_data` requires `--confirm` flag to prevent accidental data loss
