---
name: wow-api-achievements
description: "Complete reference for WoW Retail Achievement, Statistics, and Achievement Criteria APIs. Covers C_AchievementInfo, global achievement functions (GetAchievementInfo, GetAchievementCriteriaInfo, GetStatistic, GetComparisonStatistic), achievement categories, guild achievements, achievement links, tracked achievements, toast notifications, and achievement-related events. Use when working with achievement tracking, achievement display, statistics, achievement criteria, guild achievements, or achievement completion detection."
---

# Achievements API (Retail — Patch 12.0.0)

Comprehensive reference for achievements, statistics, and criteria APIs.

> **Source:** https://warcraft.wiki.gg/wiki/World_of_Warcraft_API
> **Current as of:** Patch 12.0.0 (Build 65655) — January 28, 2026
> **Scope:** Retail only.

---

## Scope

- **Achievement Functions** — GetAchievementInfo, criteria, categories
- **Statistics** — GetStatistic, comparison
- **Tracking** — Tracked achievements
- **Guild Achievements** — Guild-specific achievements

---

## Achievement Info

### Core Functions

| Function | Returns | Description |
|----------|---------|-------------|
| `GetAchievementInfo(achievementID)` | `id, name, points, completed, month, day, year, description, flags, icon, rewardText, isGuild, wasEarnedByMe, earnedBy, isStatistic` | Achievement details |
| `GetAchievementInfoFromCriteria(criteriaID)` | `id, name, points, completed, ...` | Achievement from criteria |
| `GetAchievementLink(achievementID)` | `link` | Achievement hyperlink |
| `GetAchievementNumRewards(achievementID)` | `numRewards` | Reward count |
| `GetAchievementReward(achievementID, rewardIndex)` | `text, type, ...` | Reward info |
| `GetPreviousAchievement(achievementID)` | `prevAchievementID` | Achievement chain prev |
| `GetNextAchievement(achievementID)` | `nextAchievementID` | Achievement chain next |
| `GetTotalAchievementPoints([isGuild])` | `points` | Total achievement points |
| `GetComparisonAchievementPoints()` | `points` | Compared player's points |
| `SetAchievementSearchString(searchText)` | `numResults` | Search achievements |
| `GetAchievementSearchSize()` | `numResults` | Search result count |
| `GetAchievementSearchProgress()` | `progress` | Search progress |
| `GetFilteredAchievementID(index)` | `achievementID` | Filtered result at index |

### Achievement Criteria

| Function | Returns | Description |
|----------|---------|-------------|
| `GetAchievementNumCriteria(achievementID)` | `numCriteria` | Number of criteria |
| `GetAchievementCriteriaInfo(achievementID, criteriaIndex)` | `criteriaString, criteriaType, completed, quantity, reqQuantity, charName, flags, assetID, quantityString, criteriaID, eligible, duration, elapsed` | Criteria details |
| `GetAchievementCriteriaInfoByID(achievementID, criteriaID)` | `criteriaString, criteriaType, completed, quantity, reqQuantity, charName, flags, assetID, quantityString, criteriaID, eligible` | Criteria by ID |

### Achievement Categories

| Function | Returns | Description |
|----------|---------|-------------|
| `GetCategoryList()` | `categoryIDs` | All achievement categories |
| `GetCategoryInfo(categoryID)` | `title, parentCategoryID, flags` | Category info |
| `GetCategoryNumAchievements(categoryID [, includeAll])` | `numAchievements, numCompleted, numIncomplete` | Category stats |
| `GetAchievementCategory(achievementID)` | `categoryID` | Achievement's category |

### Achievement Comparison (Inspect)

| Function | Returns | Description |
|----------|---------|-------------|
| `GetComparisonStatistic(achievementID)` | `value` | Compared player's statistic |
| `ClearAchievementComparisonUnit()` | — | Clear comparison |
| `SetAchievementComparisonUnit(unit)` | `success` | Set comparison target |

---

## Statistics

| Function | Returns | Description |
|----------|---------|-------------|
| `GetStatistic(achievementID)` | `value` | Statistic value (string) |
| `GetStatisticsCategoryList()` | `categoryIDs` | Statistic categories |
| `GetCategoryAchievementPoints(categoryID, includeAll)` | `points, completedPoints` | Category points |

---

## Achievement Tracking

| Function | Returns | Description |
|----------|---------|-------------|
| `GetTrackedAchievements()` | `... (achievementIDs)` | All tracked achievements |
| `GetNumTrackedAchievements()` | `numTracked` | Tracked count |
| `AddTrackedAchievement(achievementID)` | — | Track achievement |
| `RemoveTrackedAchievement(achievementID)` | — | Untrack achievement |
| `IsTrackedAchievement(achievementID)` | `isTracked` | Is tracked? |

---

## Common Patterns

### Check Achievement Completion

```lua
local function IsAchievementDone(achievementID)
    local _, _, _, completed = GetAchievementInfo(achievementID)
    return completed
end
```

### Display Achievement Criteria Progress

```lua
local function PrintCriteriaProgress(achievementID)
    local _, name = GetAchievementInfo(achievementID)
    print("Achievement:", name)
    local numCriteria = GetAchievementNumCriteria(achievementID)
    for i = 1, numCriteria do
        local criteriaString, _, completed, quantity, reqQuantity = 
            GetAchievementCriteriaInfo(achievementID, i)
        local status = completed and "DONE" or (quantity .. "/" .. reqQuantity)
        print("  ", criteriaString, status)
    end
end
```

### Search Achievements

```lua
local function SearchAchievements(text)
    local numResults = SetAchievementSearchString(text)
    local results = {}
    for i = 1, GetAchievementSearchSize() do
        local achievementID = GetFilteredAchievementID(i)
        local _, name, points, completed = GetAchievementInfo(achievementID)
        table.insert(results, {id = achievementID, name = name, points = points, done = completed})
    end
    return results
end
```

---

## Key Events

| Event | Payload | Description |
|-------|---------|-------------|
| `ACHIEVEMENT_EARNED` | achievementID, alreadyEarned | Achievement completed |
| `CRITERIA_EARNED` | achievementID, criteriaString | Criteria completed |
| `CRITERIA_UPDATE` | — | Criteria progress updated |
| `CRITERIA_COMPLETE` | — | All criteria complete |
| `TRACKED_ACHIEVEMENT_LIST_CHANGED` | achievementID, added | Tracking changed |
| `TRACKED_ACHIEVEMENT_UPDATE` | achievementID | Tracked achievement updated |
| `ACHIEVEMENT_SEARCH_UPDATED` | — | Search results ready |
| `INSPECT_ACHIEVEMENT_READY` | guid | Inspect achievement data ready |
| `RECEIVED_ACHIEVEMENT_MEMBER_LIST` | achievementID | Member list received |

---

## Gotchas & Restrictions

1. **GetAchievementInfo returns 15 values** — Destructure carefully. The `completed` boolean is the 4th return.
2. **Guild vs personal** — Pass `true` as `isGuild` to `GetCategoryNumAchievements()` for guild achievements.
3. **Statistics are strings** — `GetStatistic()` returns a formatted string, not a number. Parse with `tonumber()` if needed.
4. **Criteria index is 1-based** — Criteria indices start at 1, up to `GetAchievementNumCriteria()`.
5. **Achievement chains** — Some achievements are chained (10/25/50 kills etc.). Use `GetPreviousAchievement()`/`GetNextAchievement()`.
6. **Search is async** — `SetAchievementSearchString()` may not return all results immediately. Wait for `ACHIEVEMENT_SEARCH_UPDATED`.
7. **Tracking limit** — There's a maximum number of tracked achievements.
8. **Inspect data** — Achievement comparison requires `SetAchievementComparisonUnit()` and waiting for `INSPECT_ACHIEVEMENT_READY`.
