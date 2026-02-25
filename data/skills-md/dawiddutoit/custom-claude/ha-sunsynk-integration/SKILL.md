---
name: ha-sunsynk-integration
description: |
  Provides integration setup and configuration for Sunsynk/Deye solar inverters with Home
  Assistant using the SolarSynkV3 cloud API add-on including add-on configuration, entity
  naming patterns, troubleshooting, and dashboard setup. Use when setting up sunsynk
  integration, configuring deye inverter, troubleshooting "no permissions" errors,
  accessing solar system data, or monitoring battery/PV/grid/load sensors.
---

Works with Sunsynk/Deye hybrid inverters, api.sunsynk.net cloud API, and HA add-ons.
# Sunsynk/Deye Solar System Integration for Home Assistant

Integrate Sunsynk and Deye solar inverters with Home Assistant using the cloud-based SolarSynkV3 add-on. This skill covers setup, configuration, entity patterns, and troubleshooting for reliable solar monitoring.

## Quick Start

**Working Integration Method:**
```yaml
# Add-on: SolarSynkV3 (Cloud API)
# Repository: https://github.com/martinville/solarsynkv3
# Add-on slug: d4ae3b04_solar_synkv3

Configuration:
  sunsynk_user: "<your_sunsynk_account_email>"
  sunsynk_pass: "<your_sunsynk_account_password>"
  sunsynk_serial: "<INVERTER_SERIAL_FROM_PORTAL>"  # CRITICAL: Use inverter serial!
  Home_Assistant_IP: "<ha_ip_address>"
  Home_Assistant_PORT: 8123
  HA_LongLiveToken: "<ha_long_lived_token>"
  Refresh_rate: 300
  API_Server: "api.sunsynk.net"  # Region 2 (South Africa)
```

**Key Success Factor:** Use the **inverter serial number** from sunsynk.net portal (under Inverter menu), NOT the WiFi dongle serial. Using the wrong serial causes "No Permissions" API errors.

## Table of Contents

1. When to Use This Skill
2. What This Skill Does
3. Hardware Overview
4. Integration Setup
5. Entity Naming and Organization
6. Monitoring and Dashboards
7. Troubleshooting
8. WiFi Dongle Limitations
9. Alternative Integration Methods
10. Supporting Files
11. Requirements
12. Red Flags to Avoid

## When to Use This Skill

**Explicit Triggers:**
- "Set up sunsynk integration"
- "Configure deye inverter home assistant"
- "Add solar inverter to ha"
- "Sunsynk no permissions error"
- "SolarSynkV3 add-on setup"
- "Monitor solar system in home assistant"

**Implicit Triggers:**
- Working with Sunsynk/Deye hybrid inverters
- Need battery SOC, PV power, grid import/export data
- Building solar monitoring dashboards
- Troubleshooting solar integration issues

**Debugging Triggers:**
- API authentication failures
- Missing sensor entities
- Incorrect entity naming
- Cloud API connection problems

## What This Skill Does

This skill provides:

1. **Integration Setup** - Configure SolarSynkV3 add-on with correct parameters
2. **Entity Discovery** - Understand entity naming patterns and sensor organization
3. **Configuration Validation** - Verify critical settings (serial numbers, API servers)
4. **Troubleshooting Guidance** - Resolve common integration issues
5. **Dashboard Planning** - Identify key sensors for monitoring

## Usage

Follow the Quick Start section to configure the SolarSynkV3 add-on with correct parameters. Then use sections 4-7 for integration setup, entity discovery, monitoring dashboards, and troubleshooting. Always use the inverter serial number (not dongle serial) to avoid "No Permissions" errors.

## Hardware Overview

**Typical Sunsynk/Deye Setup:**

| Component | Purpose | Details |
|-----------|---------|---------|
| **Inverter** | DC-AC conversion, battery management | Deye 8kW Hybrid (example: SN 2305178402) |
| **WiFi Dongle** | Cloud connectivity | Sunsynk dongle (example: E47W23428459) |
| **Battery** | Energy storage | 280Ah capacity, 48V nominal (typical) |
| **PV Array** | Solar panels | 2 MPPT strings (typical) |

**Example Plant Information:**
- Inverter Serial: 2305178402 (use THIS for integration)
- WiFi Dongle Serial: E47W23428459 (NOT used for config)
- Location: South Africa (Region 2)
- Cloud Portal: https://sunsynk.net

## Integration Setup

### 4.1. Add-on Installation

**Step 1: Add Repository to HACS or Add-on Store**

Via Home Assistant:
1. Navigate to **Settings** > **Add-ons** > **Add-on Store**
2. Click **⋮** (three dots) > **Repositories**
3. Add repository: `https://github.com/martinville/solarsynkv3`
4. Install **SolarSynkV3** add-on

**Step 2: Identify Add-on**

Add-on slug: `d4ae3b04_solar_synkv3`

Configuration URL: `http://<ha_ip>:8123/hassio/addon/d4ae3b04_solar_synkv3/config`

### 4.2. Configuration Parameters

```yaml
sunsynk_user: "your_email@example.com"
sunsynk_pass: "your_sunsynk_password"
sunsynk_serial: "2305178402"  # INVERTER serial from portal
Home_Assistant_IP: "192.168.68.123"
Home_Assistant_PORT: 8123
HA_LongLiveToken: "<your_ha_long_lived_token>"
Refresh_rate: 300  # 5 minutes (recommended)
API_Server: "api.sunsynk.net"  # Region 2 (South Africa)
use_internal_api: false
Enable_HTTPS: false  # Use true if HA has HTTPS
```

**Parameter Reference:**

| Parameter | Purpose | Example |
|-----------|---------|---------|
| `sunsynk_user` | Account email for sunsynk.net | your_email@example.com |
| `sunsynk_pass` | Account password | your_password |
| `sunsynk_serial` | **INVERTER** serial (NOT dongle) | 2305178402 |
| `Home_Assistant_IP` | HA instance IP address | 192.168.68.123 |
| `Home_Assistant_PORT` | HA HTTP port | 8123 |
| `HA_LongLiveToken` | Long-lived access token from HA | eyJ0eXAiOiJKV1QiLCJhb... |
| `Refresh_rate` | Polling interval (seconds) | 300 (5 min) |
| `API_Server` | Regional API endpoint | api.sunsynk.net |

**Regional API Servers:**

| Region | API Server |
|--------|------------|
| Region 1 (Global) | api-internal.sunsynk.net |
| Region 2 (South Africa) | api.sunsynk.net |
| Region 3 (Europe) | api-eu.sunsynk.net |

### 4.3. Finding Your Inverter Serial

**CRITICAL:** Use the inverter serial number, NOT the WiFi dongle serial.

**How to Find Inverter Serial:**

1. Log into https://sunsynk.net (or your regional portal)
2. Navigate to your plant/system
3. Click **Inverter** menu or device details
4. Look for serial number starting with digits (e.g., `2305178402`)
5. **Do NOT use** the dongle serial (alphanumeric, e.g., `E47W23428459`)

**Visual Identification:**

```
Inverter Serial:  2305178402        ✓ USE THIS
Dongle Serial:    E47W23428459      ✗ NOT THIS
```

## Entity Naming and Organization

### 5.1. Entity ID Pattern

All entities follow this pattern:

```
sensor.solarsynkv3_{INVERTER_SERIAL}_{SENSOR_NAME}
```

**Example:**
```
sensor.solarsynkv3_2305178402_battery_soc
sensor.solarsynkv3_2305178402_pv_pac
sensor.solarsynkv3_2305178402_load_total_power
```

### 5.2. Key Sensor Categories

**Most Important Sensors for Dashboards:**

| Category | Entity ID | Description | Unit |
|----------|-----------|-------------|------|
| **Battery** | `battery_soc` | State of Charge | % |
| | `battery_power` | Charge/discharge power | W |
| **PV/Solar** | `pv_pac` | Total solar power | W |
| | `pv_etoday` | Today's solar yield | kWh |
| **Grid** | `grid_pac` | Grid import/export | W |
| | `grid_etoday_from` | Today imported | kWh |
| | `grid_etoday_to` | Today exported | kWh |
| **Load** | `load_total_power` | Total consumption | W |
| | `load_daily_used` | Today's usage | kWh |
| **Inverter** | `inverter_power` | Inverter output | W |
| | `runstatus` | Status (Normal/Fault) | - |

**Power Flow Understanding:**

```
PV → Inverter → [ Battery / Load / Grid ]
              ↑
         Grid Import (if needed)
```

### 5.3. Complete Sensor Reference

For a complete list of all 300+ available sensors across Battery, PV/Solar, Grid, Load, Inverter, and Energy categories, see [references/sensor-reference.md](references/sensor-reference.md).

## Monitoring and Dashboards

**Essential Dashboard Components:**

For complete dashboard examples including power flow charts, battery gauges, and daily energy summaries, see [examples/dashboard-config.yaml](examples/dashboard-config.yaml).

**Quick REST API Access:**
```bash
# Get battery state of charge
curl -s "http://<ha_ip>:8123/api/states/sensor.solarsynkv3_2305178402_battery_soc" \
  -H "Authorization: Bearer $HA_LONG_LIVED_TOKEN"
```

## Troubleshooting

### 7.1. "No Permissions" Error

**Symptom:** Add-on logs show "No Permissions" or API authentication failures.

**Root Cause:** Using WiFi dongle serial instead of inverter serial.

**Solution:**
1. Log into sunsynk.net portal
2. Navigate to **Inverter** menu (not device/dongle settings)
3. Copy the inverter serial (numeric, e.g., `2305178402`)
4. Update add-on configuration with correct serial
5. Restart add-on

**Verification:**
```bash
# Check add-on logs
ha addons logs d4ae3b04_solar_synkv3

# Look for successful authentication
# Expected: "Connected to API" or similar success message
```

**Alternative Causes:**
- Account lacks API access (installer accounts may be restricted)
- Wrong API server for your region
- Incorrect username/password

### 7.2. No Sensors Appearing

**Symptom:** Add-on running but no entities created in HA.

**Diagnostic Steps:**

1. **Check Add-on Logs:**
   ```bash
   ha addons logs d4ae3b04_solar_synkv3
   ```
   Look for errors during sensor creation.

2. **Verify HA Connection:**
   Check if add-on can reach HA API:
   - Confirm `Home_Assistant_IP` is correct
   - Verify `HA_LongLiveToken` is valid
   - Check HA firewall rules

3. **Force Entity Discovery:**
   - Restart Home Assistant core
   - Reload integration from Settings > Devices & Services
   - Check Developer Tools > States for entities starting with `sensor.solarsynkv3_`

4. **Check Entity Registry:**
   ```bash
   # Search for solarsynk entities
   curl -s "http://<ha_ip>:8123/api/states" \
     -H "Authorization: Bearer $HA_LONG_LIVED_TOKEN" | \
     jq '.[] | select(.entity_id | contains("solarsynk"))'
   ```

### 7.3. Connection Test Issues

**Symptom:** Connection test shows unusual values (e.g., 100A current).

**Interpretation:**
- Test data showing 100A is often a **dummy/test value**
- Indicates HA connection is OK
- Actual issue may be with Sunsynk API authentication

**Action:**
- Don't focus on test values
- Check API authentication in logs
- Verify inverter serial and credentials

## WiFi Dongle Limitations

**Stock Sunsynk WiFi Dongle:**

The stock WiFi dongle (e.g., `E47W23428459`) is **cloud-only** - it does NOT expose local Modbus/TCP ports.

**Port Scan Results:**
```bash
nmap -p 8899,502,6666 <dongle_ip>
# Result: All ports closed
```

**Why Local Integration Won't Work:**

- Kellerza/sunsynk integration requires Modbus access (port 502 or 8899)
- Stock dongle firmware blocks all local network access
- Only cloud API path is available

**Alternatives for Local Integration:**

1. **Replace Dongle:**
   - Use Solarman LSW-3 dongle (supports local Modbus)
   - Cost: ~$50-100 USD

2. **Custom Firmware:**
   - Flash ESPHome to ESP-based dongle
   - Requires hardware expertise
   - Risk of bricking dongle

3. **Direct RS485 Connection:**
   - Connect Raspberry Pi or ESP32 directly to inverter RS485 ports
   - Use Modbus RTU protocol
   - Most complex but most reliable

**Recommendation:** Use cloud API (SolarSynkV3) unless you have strong requirement for local-only control.

## Alternative Integration Methods

**Comparison of Methods:**

| Method | Type | Pros | Cons |
|--------|------|------|------|
| **SolarSynkV3** | Cloud API | Easy setup, no hardware changes | Depends on cloud service |
| **Kellerza/Sunsynk** | Local Modbus | Fast updates, local control | Requires dongle replacement |
| **HASS-Sunsynk-Multi** | Local Modbus | Multiple inverter support | Stock dongle incompatible |
| **ESPHome Custom** | Direct RS485 | Full control, no cloud | Complex setup, DIY hardware |

**When to Use Each:**

- **Cloud API (SolarSynkV3)** - Default choice for most users
- **Local Modbus** - When cloud is unreliable or privacy-sensitive
- **ESPHome/Direct** - Advanced users, custom automation requirements

## Supporting Files

**References:**
- `references/sensor-reference.md` - Complete list of 300+ entities with descriptions
- `references/api-specification.md` - Sunsynk API endpoints and authentication
- `references/modbus-registers.md` - Modbus register map for direct integration

**Examples:**
- `examples/dashboard-config.yaml` - Complete solar dashboard example
- `examples/automations.yaml` - Battery management automations
- `examples/api-queries.sh` - REST API query examples

**Scripts:**
- `scripts/verify-integration.py` - Test integration and list available entities
- `scripts/entity-discovery.py` - Discover all Sunsynk entities in HA
- `scripts/generate-sensor-list.sh` - Export sensor list from add-on logs

## Requirements

**Hardware:**
- Sunsynk or Deye hybrid inverter
- WiFi dongle (cloud-connected)
- Home Assistant instance

**Software:**
- Home Assistant 2023.1+ (for add-on support)
- Add-on Store or HACS access
- Long-lived access token

**Access:**
- Sunsynk.net account credentials
- Inverter serial number (from portal)
- Network access to Home Assistant

**Knowledge:**
- Basic Home Assistant configuration
- YAML syntax (for dashboards)
- REST API usage (optional, for scripting)

## Red Flags to Avoid

**Configuration Mistakes:**
- [ ] Using WiFi dongle serial instead of inverter serial
- [ ] Wrong API server for your region
- [ ] Forgetting to restart add-on after config changes
- [ ] Using expired or invalid HA token

**Integration Issues:**
- [ ] Expecting local Modbus from stock WiFi dongle
- [ ] Installing multiple conflicting Sunsynk add-ons
- [ ] Not checking add-on logs during troubleshooting
- [ ] Assuming test values are real sensor data

**Dashboard/Automation Problems:**
- [ ] Hardcoding entity IDs without checking they exist
- [ ] Not accounting for negative values (battery_power)
- [ ] Using instantaneous power for energy calculations
- [ ] Polling too frequently (< 60 second refresh rate)

**Security:**
- [ ] Storing credentials in YAML files
- [ ] Using admin account instead of restricted API user
- [ ] Exposing HA token in public repositories
- [ ] Not using HTTPS when HA is internet-accessible

## Notes

**Refresh Rate Considerations:**
- 300 seconds (5 minutes) is recommended default
- Faster polling may hit API rate limits
- Slower polling reduces cloud service load

**Entity Count:**
- Expect 300-400 entities depending on inverter model
- Disable unused entities to reduce database size
- Group related entities for dashboard organization

**Cloud Dependency:**
- Integration requires internet access to api.sunsynk.net
- Local network outage won't affect monitoring if HA has internet
- Consider UPS for router and HA server

**Support Resources:**
- GitHub Issues: https://github.com/martinville/solarsynkv3/issues
- Home Assistant Forum: community.home-assistant.io
- Sunsynk Support: support@sunsynk.net
