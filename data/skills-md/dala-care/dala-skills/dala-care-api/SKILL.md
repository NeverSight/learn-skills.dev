---
name: dala-care-api
description: Interact with the Dala Care healthcare workforce management platform via its GraphQL API
metadata:
  author: careverk
  version: "1.0.0"
  skillport:
    category: api
    tags: [healthcare, graphql, api, scheduling, workforce-management]
---

# Dala Care GraphQL API

This skill teaches how to interact with the Dala Care healthcare workforce management platform via its GraphQL API.

## Authentication

All API requests require an API key passed in the `Authorization` header:

```
Authorization: <api-key>
```

API keys have associated roles that determine access permissions across the organization hierarchy (Tenant > Division > Region > Office).

## Endpoints

- **EU:** `https://api.eu.dala.care/graphql`
- **US:** `https://api.us.dala.care/graphql`

## Making Requests

Send POST requests with:
- `Content-Type: application/json`
- Body: `{"query": "...", "variables": {...}}`

## Date/Time Format

All dates use ISO 8601 format: `2025-01-15T08:00:00.000Z`

---

## Core Queries

### Get Offices

Returns all offices the authenticated user has access to, with their organizational hierarchy.

```graphql
query Offices {
  offices {
    id
    name
    type          # OFFICE or CARE_HOME
    region {
      id
      name
      division {
        id
        name
      }
    }
  }
}
```

---

### Get Care Recipients

List care recipients. Pass empty `officeIds` array to get all accessible care recipients.

```graphql
query CareRecipients($officeIds: [String!]!) {
  careRecipients(filter: { officeIds: $officeIds }) {
    id
    firstName
    lastName
    gender          # MALE, FEMALE, OTHER
    email
    phone
    homePhone
    careRecipientRoles {
      deactivatedAt
      office {
        id
        name
      }
    }
  }
}
```

**Variables:**
```json
{
  "officeIds": []
}
```

---

### Get Care Recipient Details

Get comprehensive information including contacts, address, care plan, and files.

```graphql
query CareRecipientById($id: ID!) {
  careRecipientById(id: $id) {
    id
    firstName
    lastName
    pid
    birthDate
    phone
    homePhone
    email
    gender

    address {
      addressLine1
      addressLine2
      city
      state
      zipCode
      homeInformation
    }

    contacts {
      id
      firstName
      lastName
      relationshipType  # SPOUSE, PARENT, CHILD, SIBLING, etc.
      email
      phone
      isPrimary
      isPayer
      hasPowerOfAttorney
    }

    primaryContact {
      id
      firstName
      lastName
      phone
      email
    }

    careRecipientRoles {
      deactivatedAt
      office {
        id
        name
        type
      }
    }

    carePlan {
      fields {
        ... on RadioField {
          __typename
          id
          name
          description
          availableValues
          value
          required
        }
        ... on CheckboxField {
          __typename
          id
          name
          description
          availableValues
          values
          required
        }
        ... on TextField {
          __typename
          id
          name
          description
          value
          required
        }
        ... on TextArea {
          __typename
          id
          name
          description
          value
          required
        }
        ... on DateField {
          __typename
          id
          name
          description
          value
          required
        }
      }
    }

    files {
      name
      url
    }
  }
}
```

---

### Get Care Recipients Visits

Query visits for a specific care recipient within a date range.

```graphql
query CareRecipientVisits($careRecipientId: ID!, $from: String!, $to: String!) {
  visitsByCareRecipientId(
    careRecipientId: $careRecipientId
    from: $from
    to: $to
  ) {
    id
    visitDefinitionId
    officeId
    subjectId
    subjectType       # CARE_RECIPIENT or CARE_HOME
    start
    durationMinutes
    cancelledAt
    cancelledReason   # CANCELLED_BY_CARE_RECIPIENT, CANCELLED_BY_CARE_PROVIDER, etc.

    visitorsV2 {
      id
      firstName
      lastName
      clockInTime
      clockOutTime
    }

    visitType {
      id
      title
      code
    }

    labels {
      id
      name
    }

    visitNotes {
      id
      note
      createdAt
      sentiment {
        positive
        negative
        neutral
        mixed
      }
      author {
        id
        firstName
        lastName
      }
    }
  }
}
```

**Variables:**
```json
{
  "careRecipientId": "uuid",
  "from": "2025-01-01T00:00:00.000Z",
  "to": "2025-01-31T23:59:59.999Z"
}
```

---

### Get Caregivers

List caregivers for specified offices.

```graphql
query CareGivers($officeIds: [String!]!) {
  careGivers(filter: { officeIds: $officeIds }) {
    id
    firstName
    lastName
    email
    phone
    homePhone
    birthDate
    pid
    lastLogin
    caregiverRoles {
      userId
      hireDate
      deactivatedAt
      office {
        id
        name
      }
    }
  }
}
```

---

### Get Events by Office (Day Summary)

Get all events (visits and absences) for offices in a date range. This is the primary query for understanding daily scheduling status.

```graphql
query EventsByOfficeIds($officeIds: [ID!]!, $from: String!, $to: String!) {
  eventsByOfficeIds(officeIds: $officeIds, from: $from, to: $to) {
    ... on Visit {
      id
      visitDefinitionId
      officeId
      subjectId
      subjectType
      start
      durationMinutes
      isVisitLog
      cancelledAt
      cancelledReason
      requiredCaregiversCount

      visitorsV2 {
        id
        firstName
        lastName
        clockInTime
        clockOutTime
      }

      subject {
        ... on CareRecipient {
          id
          firstName
          lastName
        }
        ... on CareHome {
          id
          name
        }
      }

      visitType {
        id
        title
        code
      }

      labels {
        id
        name
      }
    }
    ... on Absence {
      id
      userId
      start
      end
      allDay
      reason
      description
    }
  }
}
```

**Visit Status Logic:**
- **Open:** `requiredCaregiversCount > visitorsV2.length` and not cancelled
- **Scheduled:** Future visit with sufficient caregivers assigned
- **Late:** `start + durationMinutes < now` and has `clockInTime` but no `clockOutTime`
- **Missed:** Past visit with no `clockInTime` on any visitor
- **Cancelled:** Has `cancelledAt` value
- **Completed:** `isVisitLog = true` or has `clockOutTime` on visitors

---

### Check Caregiver Availability

Query which caregivers are available for a proposed visit time.

```graphql
query CaregiverAvailabilities($officeIds: [ID!]!, $input: VisitorAvailabilityInput!) {
  caregiverAvailabilitiesByOfficeIds(officeIds: $officeIds, input: $input) {
    visitorId
    visitor {
      id
      firstName
      lastName
      email
      phone
    }
    firstVisit         # Available for the first occurrence
    allVisits          # Available for all occurrences (if recurring)
    conflictFirstVisit # Has conflict on first occurrence
    conflictInSeries   # Has conflict somewhere in series
  }
}
```

**Variables:**
```json
{
  "officeIds": ["office-uuid"],
  "input": {
    "start": "2025-01-15T09:00:00.000Z",
    "durationMinutes": 60,
    "end": "2025-03-15T09:00:00.000Z",
    "rRule": {
      "frequency": "WEEKLY",
      "weekdays": ["MONDAY", "WEDNESDAY", "FRIDAY"],
      "interval": 1,
      "weekStart": "MONDAY"
    }
  }
}
```

---

## Core Mutations

### Schedule a Visit

Create a new visit (one-time or recurring).

```graphql
mutation ScheduleVisit($input: VisitCreateInputV2!) {
  visitCreateV2(input: $input) {
    id
    subjectId
    subjectType
    recurrences {
      id
      start
      end
      durationMinutes
      visitorIds
      visitors {
        id
        firstName
        lastName
      }
      rRule {
        frequency
        weekdays
        interval
        weekStart
      }
    }
  }
}
```

**Variables for one-time visit:**
```json
{
  "input": {
    "subjectId": "care-recipient-uuid",
    "subjectType": "CARE_RECIPIENT",
    "officeId": "office-uuid",
    "start": "2025-01-15T09:00:00.000Z",
    "durationMinutes": 60,
    "visitorIds": ["caregiver-uuid-1", "caregiver-uuid-2"],
    "requiredCaregiversCount": 1
  }
}
```

**Variables for recurring visit:**
```json
{
  "input": {
    "subjectId": "care-recipient-uuid",
    "subjectType": "CARE_RECIPIENT",
    "officeId": "office-uuid",
    "start": "2025-01-15T09:00:00.000Z",
    "end": "2025-06-15T09:00:00.000Z",
    "durationMinutes": 60,
    "visitorIds": ["caregiver-uuid"],
    "requiredCaregiversCount": 1,
    "rRule": {
      "frequency": "WEEKLY",
      "weekdays": ["MONDAY", "WEDNESDAY", "FRIDAY"],
      "interval": 1,
      "weekStart": "MONDAY"
    }
  }
}
```

---

### Update a Visit (Future)

Modify a future visit instance.

```graphql
mutation UpdateVisit($input: VisitUpdateInput!) {
  visitUpdate(input: $input) {
    id
    visitDefinitionId
    officeId
    subjectId
    start
    durationMinutes
    requiredCaregiversCount
    visitorsV2 {
      id
      firstName
      lastName
    }
  }
}
```

**Variables:**
```json
{
  "input": {
    "visitInstanceId": "visit-uuid",
    "visitorIds": ["caregiver-uuid-1", "caregiver-uuid-2"],
    "durationMinutes": 90,
    "start": "2025-01-15T10:00:00.000Z",
    "requiredCaregiversCount": 2
  }
}
```

---

### Update a Visit Log (Past)

Modify a past visit (visit log).

```graphql
mutation UpdateVisitLog($visitInstanceId: ID!, $input: VisitLogUpdateInput!) {
  visitLogUpdate(visitInstanceId: $visitInstanceId, input: $input) {
    id
    visitDefinitionId
    officeId
    subjectId
    start
    durationMinutes
    visitorsV2 {
      id
      firstName
      lastName
    }
  }
}
```

**Variables:**
```json
{
  "visitInstanceId": "visit-uuid",
  "input": {
    "visitors": [
      {
        "id": "caregiver-uuid",
        "clockInTime": "2025-01-15T09:00:00.000Z",
        "clockOutTime": "2025-01-15T10:00:00.000Z"
      }
    ],
    "startDate": "2025-01-15T09:00:00.000Z",
    "durationMinutes": 60
  }
}
```

---

### Update Care Plan

Modify care plan fields for a care recipient.

```graphql
mutation CareRecipientCarePlanUpsert($careRecipientId: String!, $input: CarePlanInput!) {
  carePlanForCareRecipientUpsert(careRecipientId: $careRecipientId, input: $input) {
    id
  }
}
```

**Variables:**
```json
{
  "careRecipientId": "care-recipient-uuid",
  "input": {
    "fields": [
      {
        "id": "field-id-1",
        "type": "RADIO_FIELD",
        "value": "Option A"
      },
      {
        "id": "field-id-2",
        "type": "CHECKBOX_FIELD",
        "value": "Option 1,Option 3"
      },
      {
        "id": "field-id-3",
        "type": "TEXT_FIELD",
        "value": "Some text value"
      },
      {
        "id": "field-id-4",
        "type": "DATE_FIELD",
        "value": "2025-01-15"
      }
    ]
  }
}
```

**Field Types:**
- `RADIO_FIELD`: Single value from `availableValues`
- `CHECKBOX_FIELD`: Comma-separated values from `availableValues`
- `TEXT_FIELD`: Free text (short)
- `TEXT_AREA`: Free text (long)
- `DATE_FIELD`: Date string

---

### Cancel a Visit

```graphql
mutation CancelVisit(
  $visitInstanceId: ID!
  $cancelledAt: String!
  $cancelledReason: CancelledReason!
  $cancelFollowing: Boolean!
  $cancelledAdditionalInformation: String
) {
  visitCancel(
    visitInstanceId: $visitInstanceId
    cancelledAt: $cancelledAt
    cancelledReason: $cancelledReason
    cancelFollowing: $cancelFollowing
    cancelledAdditionalInformation: $cancelledAdditionalInformation
  ) {
    id
    cancelledAt
    cancelledReason
  }
}
```

**Variables:**
```json
{
  "visitInstanceId": "visit-uuid",
  "cancelledAt": "2025-01-15T08:00:00.000Z",
  "cancelledReason": "CANCELLED_BY_CARE_RECIPIENT",
  "cancelFollowing": false,
  "cancelledAdditionalInformation": "Patient hospitalized"
}
```

**Cancellation Reasons:**
- `CANCELLED_BY_CARE_RECIPIENT`
- `CANCELLED_BY_CARE_PROVIDER`
- `HOSPITAL_CARE_FACILITY`
- `HOLIDAY`
- `RESCHEDULED`
- `OTHER`

---

## Reference Types

### Recurrence (rRule)

```graphql
input RRuleInput {
  frequency: Frequency!    # DAILY, WEEKLY, MONTHLY
  weekdays: [Weekday!]     # Required for WEEKLY
  interval: Int            # Every N periods (default: 1)
  weekStart: Weekday!      # MONDAY, TUESDAY, etc.
}
```

### Weekdays

`MONDAY`, `TUESDAY`, `WEDNESDAY`, `THURSDAY`, `FRIDAY`, `SATURDAY`, `SUNDAY`

### Relationship Types

`SPOUSE`, `PARENT`, `CHILD`, `SIBLING`, `IN_LAW`, `GRANDPARENT`, `GRANDCHILD`, `FAMILY`, `FRIEND`, `NEIGHBOR`, `MEDICAL`, `THERAPY`, `OTHER`

### Absence Reasons (Caregiver)

`PAID_LEAVE`, `UNPAID_LEAVE`, `PAID_SICK_LEAVE`, `UNPAID_SICK_LEAVE`, `SICK_CHILD`, `UNPAID_SICK_CHILD`, `TRAINING`, `OTHER`

### Absence Reasons (Care Recipient)

`CANCELLED_BY_CARE_RECIPIENT`, `CANCELLED_BY_CARE_PROVIDER`, `HOSPITAL_CARE_FACILITY`, `HOLIDAY`, `OTHER`

### Role Types

- `ADMIN`: Full administrative access
- `SCHEDULING_MANAGER`: Manage schedules and visits
- `SUCCESS_MANAGER`: Manage care recipients and caregivers
- `CAREGIVER`: Field worker providing care
- `CARE_RECIPIENT`: Person receiving care
- `CONTACT`: Family member or emergency contact

### Resource Hierarchy

```
Tenant (organization)
  └── Division
        └── Region
              └── Office
                    └── Care Recipients & Caregivers
```

---

## Common Workflows

### Find Available Caregivers and Schedule a Visit

1. Query `Offices` to get office IDs
2. Query `CareRecipients` to find the care recipient
3. Query `CaregiverAvailabilities` with proposed time to find available caregivers
4. Execute `ScheduleVisit` mutation with selected caregivers

### View Daily Schedule and Find Open Visits

1. Query `EventsByOfficeIds` for the target date range
2. Filter visits where `requiredCaregiversCount > visitorsV2.length` and `cancelledAt` is null
3. These are visits that need additional caregiver assignments

### Assign Caregiver to Existing Visit

1. Determine if visit is future (`start > now`) or past
2. For future visits: use `UpdateVisit` mutation with updated `visitorIds`
3. For past visits: use `UpdateVisitLog` mutation with visitor details

### Update Care Plan Information

1. Query `CareRecipientById` to get current care plan fields with their IDs and available values
2. For `RADIO_FIELD`: value must be one of `availableValues`
3. For `CHECKBOX_FIELD`: value is comma-separated list from `availableValues`
4. Execute `CareRecipientCarePlanUpsert` with field updates
