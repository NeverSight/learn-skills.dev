---
name: change-management
description: Create and transition ServiceNow change requests (normal/standard/emergency), change tasks, affected CIs, approval routing, CAB scheduling, and conflict detection across maintenance windows.
license: Apache-2.0
compatibility: Designed for Serac and ServiceNow development
metadata:
  author: serac
  version: "1.0.0"
  category: servicenow
tools:
  - snow_change_manage
  - snow_change_query
  - snow_query_table
  - snow_artifact_manage
---

# Change Management for ServiceNow

Change Management ensures controlled modifications to IT infrastructure through standardized processes and approvals.

## Change Types

| Type          | Approval            | Risk   | Example                 |
| ------------- | ------------------- | ------ | ----------------------- |
| **Standard**  | Pre-approved        | Low    | Password reset template |
| **Normal**    | CAB approval        | Medium | Server patching         |
| **Emergency** | Post-implementation | High   | Production outage fix   |

## Change Request Structure

```
Change Request: CHG0010001
├── Risk Assessment
│   ├── Impact: Medium
│   ├── Risk: Low
│   └── Conflict Status: Clear
├── Schedule
│   ├── Planned Start: 2024-03-15 22:00
│   └── Planned End: 2024-03-15 23:00
├── Approvals
│   ├── Manager Approval: Approved
│   └── CAB Approval: Pending
├── Change Tasks
│   ├── Task 1: Backup current config
│   ├── Task 2: Apply patches
│   └── Task 3: Verify functionality
└── Affected CIs
    ├── PROD-WEB-001
    └── PROD-DB-001
```

## Creating Changes

### Normal Change (ES5)

```javascript
// Create normal change request
var change = new GlideRecord("change_request")
change.initialize()

// Basic info
change.setValue("short_description", "Apply security patches to web servers")
change.setValue("description", "Monthly security patch deployment for production web tier")
change.setValue("type", "normal") // normal, standard, emergency

// Classification
change.setValue("category", "Software")
change.setValue("priority", 3)

// Risk assessment
change.setValue("risk", "low") // high, moderate, low
change.setValue("impact", 2) // 1-High, 2-Medium, 3-Low

// Schedule
var startDate = new GlideDateTime()
startDate.addDaysLocalTime(7)
startDate.setValue("2024-03-15 22:00:00")
change.setValue("start_date", startDate)

var endDate = new GlideDateTime(startDate)
endDate.addSeconds(3600) // 1 hour
change.setValue("end_date", endDate)

// Assignment
change.setValue("assignment_group", getGroupSysId("Change Management"))
change.setValue("assigned_to", getOnCallUser())

// Implementation plan
change.setValue(
  "implementation_plan",
  "1. Take backup of current configuration\\n" +
    "2. Stop web services\\n" +
    "3. Apply security patches\\n" +
    "4. Restart services\\n" +
    "5. Verify functionality",
)

change.setValue(
  "backout_plan",
  "1. Stop web services\\n" + "2. Restore from backup\\n" + "3. Restart services\\n" + "4. Verify rollback successful",
)

change.setValue(
  "test_plan",
  "1. Check web server response\\n" + "2. Verify all pages load\\n" + "3. Run automated health checks",
)

var changeSysId = change.insert()
```

### Emergency Change (ES5)

```javascript
// Create emergency change
var emergencyChange = new GlideRecord("change_request")
emergencyChange.initialize()

emergencyChange.setValue("short_description", "Emergency: Fix production database connection leak")
emergencyChange.setValue("type", "emergency")
emergencyChange.setValue("priority", 1)
emergencyChange.setValue("risk", "high")
emergencyChange.setValue("impact", 1)

// Emergency justification
emergencyChange.setValue(
  "justification",
  "Production database connections exhausted causing service outage. " + "Immediate fix required to restore service.",
)

// Immediate start
emergencyChange.setValue("start_date", new GlideDateTime())

var endDate = new GlideDateTime()
endDate.addSeconds(7200) // 2 hours
emergencyChange.setValue("end_date", endDate)

emergencyChange.insert()

// Emergency changes bypass normal CAB
gs.eventQueue("change.emergency.created", emergencyChange)
```

### Standard Change (ES5)

```javascript
// Create from standard change template
function createStandardChange(templateName, variables) {
  // Find template
  var template = new GlideRecord("std_change_producer")
  template.addQuery("name", templateName)
  template.query()

  if (!template.next()) {
    gs.error("Standard change template not found: " + templateName)
    return null
  }

  // Create change from template
  var change = new GlideRecord("change_request")
  change.initialize()

  // Copy template values
  change.setValue("short_description", template.getValue("short_description"))
  change.setValue("description", template.getValue("description"))
  change.setValue("type", "standard")
  change.setValue("std_change_producer", template.getUniqueValue())

  // Apply variables
  for (var key in variables) {
    if (variables.hasOwnProperty(key) && change.isValidField(key)) {
      change.setValue(key, variables[key])
    }
  }

  return change.insert()
}

// Usage
createStandardChange("Password Reset", {
  requested_by: userSysId,
  cmdb_ci: applicationSysId,
})
```

## Change Tasks

### Creating Change Tasks (ES5)

```javascript
// Add tasks to change
function addChangeTask(changeSysId, taskConfig) {
  var task = new GlideRecord("change_task")
  task.initialize()
  task.setValue("change_request", changeSysId)
  task.setValue("short_description", taskConfig.description)
  task.setValue("order", taskConfig.order)
  task.setValue("assignment_group", taskConfig.group)
  task.setValue("planned_start_date", taskConfig.start)
  task.setValue("planned_end_date", taskConfig.end)
  return task.insert()
}

// Create implementation tasks
var tasks = [
  { description: "Pre-implementation backup", order: 100, group: "Database Team" },
  { description: "Apply patches", order: 200, group: "Server Team" },
  { description: "Verify functionality", order: 300, group: "QA Team" },
  { description: "Update documentation", order: 400, group: "Change Management" },
]

for (var i = 0; i < tasks.length; i++) {
  addChangeTask(changeSysId, tasks[i])
}
```

## Affected CIs

### Linking CIs to Change (ES5)

```javascript
// Add affected CIs
function addAffectedCI(changeSysId, ciSysId) {
  var task = new GlideRecord("task_ci")
  task.initialize()
  task.setValue("task", changeSysId)
  task.setValue("ci_item", ciSysId)
  return task.insert()
}

// Add all affected servers
var servers = ["server1_sys_id", "server2_sys_id", "db_sys_id"]
for (var i = 0; i < servers.length; i++) {
  addAffectedCI(changeSysId, servers[i])
}
```

## Approvals

### Check Approval Status (ES5)

```javascript
// Get approval status
function getApprovalStatus(changeSysId) {
  var approvals = []

  var approval = new GlideRecord("sysapproval_approver")
  approval.addQuery("sysapproval", changeSysId)
  approval.query()

  while (approval.next()) {
    approvals.push({
      approver: approval.approver.getDisplayValue(),
      state: approval.state.getDisplayValue(),
      comments: approval.getValue("comments"),
      sys_updated_on: approval.getValue("sys_updated_on"),
    })
  }

  return approvals
}
```

### Request Approval (ES5)

```javascript
// Add approval request
function requestApproval(changeSysId, approverSysId) {
  var approval = new GlideRecord("sysapproval_approver")
  approval.initialize()
  approval.setValue("sysapproval", changeSysId)
  approval.setValue("approver", approverSysId)
  approval.setValue("state", "requested")
  return approval.insert()
}
```

## Change Conflict Detection

### Check for Conflicts (ES5)

```javascript
// Check for scheduling conflicts
function checkChangeConflicts(changeSysId) {
  var change = new GlideRecord("change_request")
  if (!change.get(changeSysId)) return []

  var conflicts = []
  var startDate = change.getValue("start_date")
  var endDate = change.getValue("end_date")

  // Find overlapping changes on same CIs
  var affected = new GlideAggregate("task_ci")
  affected.addQuery("task", changeSysId)
  affected.groupBy("ci_item")
  affected.query()

  while (affected.next()) {
    var ciSysId = affected.ci_item.toString()

    // Find other changes affecting this CI
    var otherChanges = new GlideRecord("change_request")
    otherChanges.addQuery("sys_id", "!=", changeSysId)
    otherChanges.addQuery("state", "NOT IN", "closed,cancelled")
    otherChanges.addQuery("start_date", "<=", endDate)
    otherChanges.addQuery("end_date", ">=", startDate)

    // Join to task_ci
    otherChanges.addJoinQuery("task_ci", "sys_id", "task").addCondition("ci_item", ciSysId)

    otherChanges.query()

    while (otherChanges.next()) {
      conflicts.push({
        change: otherChanges.getValue("number"),
        ci: ciSysId,
        start: otherChanges.getValue("start_date"),
        end: otherChanges.getValue("end_date"),
      })
    }
  }

  return conflicts
}
```

## State Transitions

### Change States

| State     | Next States          | Conditions                |
| --------- | -------------------- | ------------------------- |
| New       | Assess               | Submitted                 |
| Assess    | Authorize, Cancelled | Assessment complete       |
| Authorize | Scheduled, Cancelled | Approvals complete        |
| Scheduled | Implement, Cancelled | Within maintenance window |
| Implement | Review, Cancelled    | Tasks completed           |
| Review    | Closed               | PIR complete              |
| Closed    | -                    | Final state               |

### Transition Change (ES5)

```javascript
// Move change to next state
function transitionChange(changeSysId, newState, notes) {
  var change = new GlideRecord("change_request")
  if (!change.get(changeSysId)) {
    gs.error("Change not found: " + changeSysId)
    return false
  }

  // Validate transition
  var currentState = change.getValue("state")
  var validTransitions = {
    "-5": ["-4", "4"], // New -> Assess or Cancelled
    "-4": ["-3", "4"], // Assess -> Authorize or Cancelled
    "-3": ["-2", "4"], // Authorize -> Scheduled or Cancelled
    "-2": ["-1", "4"], // Scheduled -> Implement or Cancelled
    "-1": ["0", "4"], // Implement -> Review or Cancelled
    0: ["3"], // Review -> Closed
  }

  if (!validTransitions[currentState] || validTransitions[currentState].indexOf(newState) === -1) {
    gs.error("Invalid state transition: " + currentState + " -> " + newState)
    return false
  }

  change.setValue("state", newState)
  if (notes) {
    change.work_notes = notes
  }
  change.update()

  return true
}
```

## MCP Tool Integration

### Available Change Tools

| Tool                                            | Purpose          |
| ----------------------------------------------- | ---------------- |
| `snow_change_manage` (`action='create'`)        | Create change    |
| `snow_change_manage` (`action='create_task'`)   | Add tasks        |
| `snow_change_query` (`action='get'`)            | Get details      |
| `snow_change_manage` (`action='update_state'`)  | Transition state |
| `snow_change_query` (`action='search'`)         | Find changes     |
| `snow_change_manage` (`action='schedule_cab'`)  | Schedule CAB     |

### Example Workflow

```javascript
// 1. Create change (scheduling happens later via action: "update_state" -> "scheduled")
var changeId = await snow_change_manage({
  action: "create",
  short_description: "Database upgrade",
  type: "normal",
  risk: "medium",
})

// 2. Add tasks
await snow_change_manage({
  action: "create_task",
  sys_id: changeId,
  short_description: "Backup database",
})

// 3. Check conflicts: search for overlapping open changes in the same window
// (see checkChangeConflicts above for per-CI conflict detection)
var conflicts = await snow_change_query({
  action: "search",
  query: "stateNOT INclosed,cancelled^start_date<=2024-03-21 02:00:00^end_date>=2024-03-20 22:00:00",
})

// 4. Submit for approval
await snow_change_manage({
  action: "update_state",
  sys_id: changeId,
  state: "assess",
})
```

## Best Practices

1. **Complete Documentation** - Implementation, backout, test plans
2. **Risk Assessment** - Accurate risk and impact ratings
3. **CI Linking** - All affected CIs attached
4. **Proper Scheduling** - Within maintenance windows
5. **Task Breakdown** - Clear implementation steps
6. **Approval Chain** - All required approvals
7. **Conflict Check** - Verify no overlapping changes
8. **PIR** - Post-implementation review for lessons learned
