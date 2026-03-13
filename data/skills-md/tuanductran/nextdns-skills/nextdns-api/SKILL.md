---
name: nextdns-api
description:
  NextDNS API integration best practices for authentication, profile management, analytics, logs,
  and real-time streaming. This skill should be used when working with NextDNS API endpoints,
  handling DNS analytics, managing security profiles, or implementing DNS filtering solutions.
  Triggers on tasks involving NextDNS profiles, DNS logs, analytics queries, or API integration.
license: MIT
metadata:
  author: tuanductran
  version: '1.0.0'
---

<!-- @case-police-ignore Api -->

# NextDNS API skills

## Capability rules

| Rule                                                | Keywords                                                                   | Description                   |
| --------------------------------------------------- | -------------------------------------------------------------------------- | ----------------------------- |
| [authentication](rules/authentication.md)           | API key, X-Api-Key, authorization, authentication                          | Authenticate with NextDNS API |
| [profile-management](rules/profile-management.md)   | create profile, update profile, delete profile, profile settings           | Manage NextDNS profiles       |
| [security-settings](rules/security-settings.md)     | threat intelligence, cryptojacking, DNS rebinding, typosquatting           | Configure security features   |
| [privacy-settings](rules/privacy-settings.md)       | blocklists, native tracking, disguised trackers, affiliate                 | Configure privacy features    |
| [parental-control](rules/parental-control.md)       | parental control, safe search, youtube restricted, block bypass            | Configure parental controls   |
| [allowlist-denylist](rules/allowlist-denylist.md)   | allowlist, denylist, domain blocking, domain allowing                      | Manage allow/deny lists       |
| [analytics-queries](rules/analytics-queries.md)     | analytics, query parameters, date filtering, pagination                    | Query analytics data          |
| [analytics-endpoints](rules/analytics-endpoints.md) | status, domains, reasons, devices, protocols                               | Access analytics endpoints    |
| [time-series-data](rules/time-series-data.md)       | time series, charts, interval, alignment, timezone                         | Retrieve time series data     |
| [logs-management](rules/logs-management.md)         | logs, filtering, search, raw logs, deduplication                           | Query and filter logs         |
| [logs-streaming](rules/logs-streaming.md)           | SSE, real-time, streaming, Server-sent events                              | Stream logs in real-time      |
| [logs-clear](rules/logs-clear.md)                   | clear logs, delete logs, purge, gdpr                                       | Permanently delete all logs   |
| [error-handling](rules/error-handling.md)           | error response, validation, 400 error, error format                        | Handle API errors             |
| [pagination](rules/pagination.md)                   | cursor, limit, next page, pagination                                       | Paginate API responses        |
| [date-formats](rules/date-formats.md)               | ISO 8601, UNIX timestamp, relative dates, date parsing                     | Use correct date formats      |
| [nested-endpoints](rules/nested-endpoints.md)       | nested objects, child endpoints, PATCH, DELETE                             | Work with nested endpoints    |
| [rewrites](rules/rewrites.md)                       | rewrites, dns records, custom dns, hostname override, cname                | Manage DNS rewrite records    |
| [settings](rules/settings.md)                       | settings, logs, log retention, log location, cache boost, cname flattening | Manage profile settings       |

## Efficiency rules

| Rule                                        | Keywords                               | Description         |
| ------------------------------------------- | -------------------------------------- | ------------------- |
| [response-format](rules/response-format.md) | data, meta, errors, response structure | Parse API responses |
| [logs-download](rules/logs-download.md)     | download logs, export logs, redirect   | Download log files  |
