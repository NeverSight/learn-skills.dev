---
name: microsoft-security
description: "Microsoft security ecosystem including Defender XDR, Microsoft Sentinel, Entra ID (Azure AD), Defender for Endpoint, Defender for Cloud, and Purview. Use when working with Microsoft Graph Security API, KQL queries, Sentinel analytics rules, Entra ID security, or integrating Microsoft security tools."
---

# Microsoft Security Platform

## Overview

Comprehensive Microsoft security stack covering XDR, SIEM, identity, and cloud security.

## Quick Reference

| Product | Purpose | API |
|---------|---------|-----|
| Defender XDR | Unified XDR | Microsoft Graph Security |
| Sentinel | Cloud SIEM | Log Analytics API |
| Defender for Endpoint | EDR | MDE API |
| Entra ID | Identity security | Microsoft Graph |
| Defender for Cloud | CSPM/CWPP | Azure Resource Manager |

## Authentication

```python
from azure.identity import ClientSecretCredential
import requests

def get_graph_token(tenant_id: str, client_id: str, client_secret: str) -> str:
    """Get Microsoft Graph API token."""
    credential = ClientSecretCredential(tenant_id, client_id, client_secret)
    token = credential.get_token("https://graph.microsoft.com/.default")
    return token.token

def graph_headers(token: str) -> dict:
    return {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
```

## Microsoft Defender XDR

### Incident Management

```python
GRAPH_URL = "https://graph.microsoft.com/v1.0"

def get_incidents(token: str, filter_query: str = None) -> list:
    """Get security incidents."""
    url = f"{GRAPH_URL}/security/incidents"
    params = {"$filter": filter_query} if filter_query else {}
    
    return requests.get(url, headers=graph_headers(token), params=params).json().get("value", [])

def get_alerts(token: str, severity: str = None) -> list:
    """Get security alerts."""
    url = f"{GRAPH_URL}/security/alerts_v2"
    params = {"$filter": f"severity eq '{severity}'"} if severity else {}
    
    return requests.get(url, headers=graph_headers(token), params=params).json().get("value", [])

def update_incident(token: str, incident_id: str, status: str, 
                    classification: str = None, determination: str = None) -> dict:
    """Update incident. Status: active, resolved, redirected"""
    body = {"status": status}
    if classification:
        body["classification"] = classification  # truePositive, falsePositive, benignPositive
    if determination:
        body["determination"] = determination
    
    return requests.patch(
        f"{GRAPH_URL}/security/incidents/{incident_id}",
        headers=graph_headers(token),
        json=body
    ).json()
```

### Advanced Hunting (KQL)

```python
def run_advanced_hunting(token: str, query: str) -> dict:
    """Execute advanced hunting query."""
    return requests.post(
        f"{GRAPH_URL}/security/runHuntingQuery",
        headers=graph_headers(token),
        json={"Query": query}
    ).json()

# Common KQL queries
SUSPICIOUS_POWERSHELL = '''
DeviceProcessEvents
| where FileName =~ "powershell.exe"
| where ProcessCommandLine has_any ("-enc", "-encodedcommand", "bypass")
| project Timestamp, DeviceName, AccountName, ProcessCommandLine
| order by Timestamp desc
'''

FAILED_LOGONS = '''
IdentityLogonEvents
| where ActionType == "LogonFailed"
| summarize FailedAttempts = count() by AccountUpn, DeviceName
| where FailedAttempts > 5
'''

LATERAL_MOVEMENT = '''
DeviceNetworkEvents
| where RemotePort in (445, 135, 5985, 5986)
| where RemoteIPType == "Private"
| summarize ConnectionCount = count() by DeviceName, RemoteIP, RemotePort
| order by ConnectionCount desc
'''
```

## Microsoft Sentinel

### Analytics Rules

```python
def create_analytics_rule(token: str, subscription_id: str, resource_group: str,
                          workspace_name: str, rule_name: str, query: str,
                          severity: str, frequency: str, period: str) -> dict:
    """Create Sentinel analytics rule."""
    url = f"https://management.azure.com/subscriptions/{subscription_id}/resourceGroups/{resource_group}/providers/Microsoft.OperationalInsights/workspaces/{workspace_name}/providers/Microsoft.SecurityInsights/alertRules/{rule_name}?api-version=2023-02-01"
    
    return requests.put(
        url,
        headers=graph_headers(token),
        json={
            "kind": "Scheduled",
            "properties": {
                "displayName": rule_name,
                "query": query,
                "severity": severity,
                "queryFrequency": frequency,
                "queryPeriod": period,
                "triggerOperator": "GreaterThan",
                "triggerThreshold": 0,
                "enabled": True
            }
        }
    ).json()
```

### Log Analytics Queries

```python
def query_log_analytics(token: str, workspace_id: str, query: str) -> dict:
    """Execute Log Analytics KQL query."""
    return requests.post(
        f"https://api.loganalytics.io/v1/workspaces/{workspace_id}/query",
        headers=graph_headers(token),
        json={"query": query}
    ).json()

# Common Sentinel queries
SECURITY_EVENTS = '''
SecurityEvent
| where TimeGenerated > ago(24h)
| where EventID in (4625, 4648, 4672, 4720, 4726)
| summarize count() by EventID, Account, Computer
'''

AZURE_SIGNIN_FAILURES = '''
SigninLogs
| where ResultType != "0"
| summarize FailedSignIns = count() by UserPrincipalName, IPAddress, Location
| where FailedSignIns > 5
'''
```

## Entra ID (Azure AD)

### Risky Users and Sign-ins

```python
def get_risky_users(token: str) -> list:
    """Get users flagged as risky."""
    return requests.get(
        f"{GRAPH_URL}/identityProtection/riskyUsers",
        headers=graph_headers(token)
    ).json().get("value", [])

def get_risky_signins(token: str, risk_level: str = None) -> list:
    """Get risky sign-in events."""
    url = f"{GRAPH_URL}/identityProtection/riskySignIns"
    params = {"$filter": f"riskLevel eq '{risk_level}'"} if risk_level else {}
    
    return requests.get(url, headers=graph_headers(token), params=params).json().get("value", [])

def dismiss_risky_user(token: str, user_id: str) -> dict:
    """Dismiss user risk."""
    return requests.post(
        f"{GRAPH_URL}/identityProtection/riskyUsers/dismiss",
        headers=graph_headers(token),
        json={"userIds": [user_id]}
    ).json()
```

### Conditional Access

```python
def get_conditional_access_policies(token: str) -> list:
    """List Conditional Access policies."""
    return requests.get(
        f"{GRAPH_URL}/identity/conditionalAccess/policies",
        headers=graph_headers(token)
    ).json().get("value", [])

def get_named_locations(token: str) -> list:
    """Get named locations for CA policies."""
    return requests.get(
        f"{GRAPH_URL}/identity/conditionalAccess/namedLocations",
        headers=graph_headers(token)
    ).json().get("value", [])
```

## Defender for Cloud

```python
def get_security_score(token: str, subscription_id: str) -> dict:
    """Get subscription security score."""
    url = f"https://management.azure.com/subscriptions/{subscription_id}/providers/Microsoft.Security/secureScores/ascScore?api-version=2020-01-01"
    return requests.get(url, headers=graph_headers(token)).json()

def get_recommendations(token: str, subscription_id: str) -> list:
    """Get security recommendations."""
    url = f"https://management.azure.com/subscriptions/{subscription_id}/providers/Microsoft.Security/assessments?api-version=2020-01-01"
    return requests.get(url, headers=graph_headers(token)).json().get("value", [])

def get_alerts_dfc(token: str, subscription_id: str) -> list:
    """Get Defender for Cloud alerts."""
    url = f"https://management.azure.com/subscriptions/{subscription_id}/providers/Microsoft.Security/alerts?api-version=2022-01-01"
    return requests.get(url, headers=graph_headers(token)).json().get("value", [])
```

## KQL Quick Reference

| Operator | Description | Example |
|----------|-------------|---------|
| `where` | Filter rows | `where Severity == "High"` |
| `project` | Select columns | `project Timestamp, User` |
| `summarize` | Aggregate | `summarize count() by User` |
| `extend` | Add column | `extend Risk = iff(Score > 80, "High", "Low")` |
| `join` | Combine tables | `join kind=inner (Table2) on Key` |
| `has` | Contains word | `where Cmd has "password"` |
| `has_any` | Contains any | `where Cmd has_any ("enc", "bypass")` |
| `matches regex` | Regex match | `where Url matches regex @".*\.exe$"` |
