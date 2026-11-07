---
name: palantir-for-family-trips
description: A Palantir-ish dark command-center dashboard for family trip planning with convoy routes, timeline playback, meal logistics, and Google Maps integration.
triggers:
  - "add a new family to the trip dashboard"
  - "customize the trip itinerary or timeline"
  - "set up the Google Maps route playback"
  - "modify meal or activity planning screens"
  - "add a new view or tab to the command center"
  - "configure environment variables for the maps key"
  - "hack on the trip model or seed data"
  - "run the family trip command center locally"
---

# Family Trip Command Center (Palantir for Family Trips)

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

A deliberately overbuilt, dark-themed operations dashboard for coordinating multi-family road trips. Built with React 19, Vite, Google Maps JS API, Framer Motion, and Lucide icons. Treats a weekend cabin trip like a live ops room: convoy tracking, arrival windows, day-by-day timeline playback, meal logistics, expense splits, and family checklists.

---

## Installation & Setup

```bash
git clone https://github.com/andrewjiang/palantir-for-family-trips.git
cd palantir-for-family-trips
npm install
cp .env.example .env
```

Edit `.env`:

```env
VITE_GOOGLE_MAPS_API_KEY=your_browser_maps_key_here
VITE_GOOGLE_MAP_ID=your_optional_google_map_id
```

```bash
npm run dev
```

Open `http://127.0.0.1:5173` (or the URL Vite prints).

> Without a Maps API key the UI fully renders but the live Google Map layer won't initialize. All other views work without it.

---

## Project Structure

```
src/
  App.jsx          # Main shell, tabs, timeline controls, overlays
  CommandMap.jsx   # Google Maps route rendering, convoy playback
  tripModel.js     # Seed trip document, families, routes, helpers
  main.jsx         # React entry point
  index.css        # Global dark-theme styles
public/
docs/              # Screenshot assets for README
.env.example
```

---

## Core Data Model (`src/tripModel.js`)

The trip is a single JS object (the "trip document") exported from `tripModel.js`. Everything — families, routes, days, meals, activities, expenses — lives here.

### Typical shape

```js
// src/tripModel.js (simplified)

export const trip = {
  name: "Pine Mountain Lake & Yosemite 2026",
  basecamp: {
    label: "Pine Mountain Lake Cabin",
    coords: { lat: 37.85, lng: -120.17 },
  },
  families: [
    {
      id: "fam-a",
      name: "The Johnsons",
      origin: { label: "San Francisco, CA", coords: { lat: 37.77, lng: -122.41 } },
      members: ["Alice", "Bob", "Charlie (8)", "Dana (5)"],
      vehicle: "Blue Minivan",
      arrivalWindow: { earliest: "2026-06-27T14:00:00", latest: "2026-06-27T16:00:00" },
      color: "#4ade80",
    },
    {
      id: "fam-b",
      name: "The Garcias",
      origin: { label: "San Jose, CA", coords: { lat: 37.33, lng: -121.88 } },
      members: ["Elena", "Marco", "Sofia (6)"],
      vehicle: "Silver SUV",
      arrivalWindow: { earliest: "2026-06-27T15:30:00", latest: "2026-06-27T17:00:00" },
      color: "#f97316",
    },
  ],
  days: [
    {
      date: "2026-06-27",
      label: "Arrival Day",
      events: [
        { time: "14:00", type: "arrival", familyId: "fam-a", note: "Johnsons ETA" },
        { time: "18:30", type: "meal", mealId: "dinner-fri", note: "Group dinner at basecamp" },
      ],
    },
    // …more days
  ],
  meals: [
    {
      id: "dinner-fri",
      label: "Friday Dinner",
      type: "dinner",
      location: "basecamp",
      assignedTo: "fam-a",
      menu: ["Tacos", "Chips & Guac", "Watermelon"],
      shoppingList: ["tortillas", "ground beef", "salsa"],
    },
  ],
  activities: [
    {
      id: "act-hike-1",
      label: "Mariposa Grove Hike",
      day: "2026-06-28",
      time: "09:00",
      durationHours: 3,
      location: { label: "Mariposa Grove, Yosemite", coords: { lat: 37.5, lng: -119.6 } },
      suitableAges: "5+",
      notes: "Bring water and snacks",
    },
  ],
  expenses: [
    { id: "exp-1", label: "Cabin rental", amount: 900, paidBy: "fam-a", splitAmong: ["fam-a", "fam-b"] },
  ],
  checklist: {
    "fam-a": ["Pack hiking boots", "Download offline maps", "Bring beach towels"],
    "fam-b": ["Bring board games", "Confirm car seats"],
  },
};

// Helper: get a family by id
export function getFamily(id) {
  return trip.families.find((f) => f.id === id);
}

// Helper: get events for a given date string "YYYY-MM-DD"
export function getDayEvents(dateStr) {
  const day = trip.days.find((d) => d.date === dateStr);
  return day ? day.events : [];
}

// Helper: total expense owed per family
export function splitExpense(expense) {
  const share = expense.amount / expense.splitAmong.length;
  return expense.splitAmong.map((famId) => ({ famId, owes: share }));
}
```

---

## Adding a New Family

Edit `src/tripModel.js`:

```js
families: [
  // …existing families
  {
    id: "fam-c",
    name: "The Nguyens",
    origin: { label: "Sacramento, CA", coords: { lat: 38.57, lng: -121.49 } },
    members: ["Linh", "Minh", "Jade (10)", "Owen (7)"],
    vehicle: "Red Crossover",
    arrivalWindow: { earliest: "2026-06-27T13:00:00", latest: "2026-06-27T15:00:00" },
    color: "#a78bfa", // pick a distinct color for map polyline + UI accents
  },
],
```

The map, timeline, and family view all consume `trip.families` reactively — adding a family here surfaces it everywhere.

---

## Google Maps & Route Playback (`src/CommandMap.jsx`)

`CommandMap` accepts props derived from the trip model and renders routes + convoy playback.

### Key props pattern

```jsx
// Inside App.jsx
import CommandMap from "./CommandMap";
import { trip } from "./tripModel";

<CommandMap
  families={trip.families}
  basecamp={trip.basecamp}
  playbackTime={currentPlaybackTime} // ISO string or null
  activeFamily={selectedFamilyId}    // highlight one convoy line
  onMarkerClick={(familyId) => setSelectedFamilyId(familyId)}
/>
```

### Adding a custom waypoint to a route

In `CommandMap.jsx`, each family's route is built with the Directions Service. To add a waypoint (e.g. a gas stop):

```js
// Inside CommandMap.jsx, where directionsService.route() is called:
directionsService.route(
  {
    origin: family.origin.coords,
    destination: trip.basecamp.coords,
    waypoints: [
      {
        location: { lat: 37.65, lng: -120.95 }, // e.g. Oakdale gas stop
        stopover: false,
      },
    ],
    travelMode: google.maps.TravelMode.DRIVING,
  },
  (result, status) => {
    if (status === "OK") {
      directionsRenderer.setDirections(result);
    }
  }
);
```

---

## Timeline Playback

The timeline in `App.jsx` steps through day events. The current day index and playback offset drive what the map and timeline panel show.

### Hooking into timeline state

```jsx
// App.jsx pattern
const [dayIndex, setDayIndex] = useState(0);
const currentDay = trip.days[dayIndex];

// Step forward
function advanceDay() {
  setDayIndex((i) => Math.min(i + 1, trip.days.length - 1));
}

// Render events for current day
currentDay.events.map((event) => (
  <TimelineEvent key={event.time} event={event} families={trip.families} />
));
```

---

## Adding a New Tab / View

Tabs are defined in `App.jsx`. To add a new view (e.g. a "Packing" tab):

```jsx
// 1. Define the tab in the tabs array
const TABS = [
  { id: "itinerary", label: "Itinerary" },
  { id: "map", label: "Map" },
  { id: "meals", label: "Meals" },
  { id: "activities", label: "Activities" },
  { id: "expenses", label: "Expenses" },
  { id: "families", label: "Families" },
  { id: "packing", label: "Packing" }, // ← new
];

// 2. Render it in the tab content switch
{activeTab === "packing" && (
  <PackingView checklist={trip.checklist} families={trip.families} />
)}
```

```jsx
// src/PackingView.jsx
export default function PackingView({ checklist, families }) {
  return (
    <div className="packing-view">
      {families.map((fam) => (
        <div key={fam.id} className="family-checklist">
          <h3 style={{ color: fam.color }}>{fam.name}</h3>
          <ul>
            {(checklist[fam.id] || []).map((item) => (
              <li key={item}>{item}</li>
            ))}
          </ul>
        </div>
      ))}
    </div>
  );
}
```

---

## Framer Motion Overlay Pattern

The mission launch overlay uses Framer Motion. Reuse this pattern for any dramatic full-screen overlay:

```jsx
import { AnimatePresence, motion } from "framer-motion";

<AnimatePresence>
  {showOverlay && (
    <motion.div
      className="overlay"
      initial={{ opacity: 0, scale: 0.95 }}
      animate={{ opacity: 1, scale: 1 }}
      exit={{ opacity: 0, scale: 0.95 }}
      transition={{ duration: 0.3, ease: "easeOut" }}
    >
      <h1>MISSION LAUNCH</h1>
      <button onClick={() => setShowOverlay(false)}>Dismiss</button>
    </motion.div>
  )}
</AnimatePresence>
```

---

## Expense Split Example

```js
import { trip, splitExpense } from "./tripModel";

// Show each family's share for all expenses
trip.expenses.forEach((exp) => {
  const splits = splitExpense(exp);
  console.log(`${exp.label} ($${exp.amount}):`);
  splits.forEach(({ famId, owes }) => {
    const fam = trip.families.find((f) => f.id === famId);
    console.log(`  ${fam.name} owes $${owes.toFixed(2)}`);
  });
});
```

---

## Environment Variables Reference

| Variable | Required | Purpose |
|---|---|---|
| `VITE_GOOGLE_MAPS_API_KEY` | Recommended | Enables Google Maps rendering and Directions API |
| `VITE_GOOGLE_MAP_ID` | Optional | Enables Cloud-based map styling / Advanced Markers |

Access in code:

```js
const apiKey = import.meta.env.VITE_GOOGLE_MAPS_API_KEY;
const mapId = import.meta.env.VITE_GOOGLE_MAP_ID;
```

---

## Common Patterns & Tips

- **All trip data lives in `tripModel.js`** — edit there first; the UI reacts automatically.
- **Family colors** are used for map polylines, timeline accents, and checklist headers. Pick hex values with enough contrast on dark backgrounds.
- **State is local** — no backend, no auth. Refresh resets to seed data unless you add `localStorage` persistence.
- **Optimized for desktop** — the dense dashboard layout is intentional; don't expect a responsive mobile layout out of the box.
- **Google Maps billing** — if you deploy with your key, usage is billed to your Google Cloud project. Restrict the key to your domain.

---

## Troubleshooting

| Problem | Fix |
|---|---|
| Map doesn't load | Check `VITE_GOOGLE_MAPS_API_KEY` in `.env`; ensure the key has Maps JS API and Directions API enabled in Google Cloud Console |
| `google is not defined` | The Maps script loads async; make sure `CommandMap` only calls Maps APIs inside the `onLoad` callback |
| Routes don't render | Directions API must be enabled separately from Maps JS API in your Cloud project |
| Vite dev server URL differs | Use whatever URL Vite prints, not a hardcoded port |
| Adding a family breaks layout | Give the new family a unique `color` and `id`; check that any hardcoded `familyId` references in `App.jsx` are generalized to `trip.families.map(...)` |
