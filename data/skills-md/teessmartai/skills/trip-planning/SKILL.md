---
name: trip-planning
description: Plan comprehensive trips including destination research, accommodations, transportation, activities, and itineraries. Use when someone needs help planning a vacation, business trip, road trip, or any travel requiring coordination of multiple elements.
---

# Trip Planning Skill

Help users plan comprehensive trips by gathering requirements, researching options, and creating detailed itineraries with budget tracking.

## Phase 1: Information Gathering

Gather essential trip details through conversation. Ask questions in logical groups.

### Core Trip Details (Ask First)
- **Destination**: Where are you planning to go? (specific city/region or open to suggestions?)
- **Travel Dates**: When are you planning to travel? (fixed dates or flexible?)
- **Duration**: How long is the trip?
- **Travelers**: Who is traveling? (number of adults, children with ages, any accessibility needs?)
- **Budget**: What's your overall budget? (or per-person budget?)

### Trip Type & Preferences (Ask Second)
- **Purpose**: What type of trip? (relaxation, adventure, cultural, business, family, romantic, etc.)
- **Pace**: Preferred pace? (packed itinerary, relaxed with downtime, mix of both?)
- **Accommodation Style**: Hotel, resort, vacation rental, hostel, camping?
- **Transportation**: Flying, driving, train, or combination?
- **Activity Interests**: What activities appeal to you? (museums, outdoor activities, food tours, nightlife, shopping, etc.)

### Constraints & Preferences (Ask Third)
- **Dietary Restrictions**: Any food allergies or dietary preferences?
- **Mobility Considerations**: Any physical limitations to consider?
- **Must-Sees**: Any specific attractions or experiences that are non-negotiable?
- **Avoid**: Anything you want to avoid? (crowds, certain areas, specific activities?)
- **Previous Visits**: Have you been to this destination before?

### Required Information Checklist
- [ ] Destination (specific or general region)
- [ ] Travel dates or timeframe
- [ ] Number and type of travelers
- [ ] Budget range
- [ ] Trip purpose/style
- [ ] Accommodation preferences
- [ ] Transportation needs

## Phase 2: Destination Research

If the destination is set, research specific options. If open to suggestions, recommend destinations based on preferences.

### Destination Suggestions (If Needed)

Search for destinations matching the user's criteria:
- `[trip type] destinations [season] [budget level]`
- `best places to visit in [region] [month]`
- `[interest]-focused travel destinations`

Provide 3-5 destination options with:

| Destination | Why It Fits | Best Time to Visit | Budget Level | Key Highlights |
|-------------|-------------|-------------------|--------------|----------------|
| City/Region | Match to preferences | Optimal months | $/$$/$$$/$$$$ | Top 3 attractions |

### Destination Deep Dive

Once destination is confirmed, research:

**Getting There**
- Search: `flights to [destination] from [origin] [dates]`
- Search: `best way to get to [destination]`
- Note flight duration, layover options, airport proximity to city

**Accommodation Options**
- Search: `[accommodation type] [destination] [neighborhood]`
- Search: `best areas to stay in [destination] for [trip type]`

Collect for each option:

| Property | Location | Price/Night | Rating | Amenities | Distance to Center |
|----------|----------|-------------|--------|-----------|-------------------|
| Name | Neighborhood | $XXX | X.X/5 | Key features | X min walk/transit |

**Transportation Within Destination**
- Search: `getting around [destination]`
- Search: `[destination] public transit guide`
- Options: rental car, public transit, rideshare, walking, biking

**Activities & Attractions**
- Search: `things to do in [destination]`
- Search: `[destination] [interest] activities`
- Search: `[destination] hidden gems local recommendations`

Collect for each activity:

| Activity | Type | Duration | Cost | Location | Booking Required? |
|----------|------|----------|------|----------|-------------------|
| Name | Category | X hours | $XX | Area/Address | Yes/No |

See [destination-guide.md](references/destination-guide.md) for detailed research strategies by trip type.

## Phase 3: Budget Planning

Create comprehensive budget breakdown.

### Budget Categories

| Category | Estimated Cost | Notes |
|----------|---------------|-------|
| **Transportation** | | |
| - Flights/Travel to destination | $XXX | |
| - Airport transfers | $XX | |
| - Local transportation | $XX/day × days | |
| - Car rental (if applicable) | $XX/day | Plus fuel, parking |
| **Accommodation** | | |
| - Lodging | $XXX/night × nights | |
| - Taxes/fees | $XX | |
| **Food & Drink** | | |
| - Breakfast | $XX/day × days | |
| - Lunch | $XX/day × days | |
| - Dinner | $XX/day × days | |
| - Snacks/drinks | $XX/day × days | |
| **Activities** | | |
| - Paid attractions | $XXX | List each |
| - Tours | $XXX | |
| - Entertainment | $XX | |
| **Other** | | |
| - Travel insurance | $XX | |
| - Tips | $XX | |
| - Souvenirs | $XX | |
| - Contingency (10-15%) | $XXX | |
| **TOTAL** | $X,XXX | |

See [budget-and-logistics.md](references/budget-and-logistics.md) for cost estimation by destination type.

## Phase 4: Itinerary Creation

Build day-by-day itinerary based on research and preferences.

### Itinerary Format

For each day, provide:

---

### Day X: [Date] - [Theme/Focus]

**Morning**
- [ ] Activity/Location (Time - Duration)
  - Details, tips, booking info
  - Cost: $XX

**Afternoon**
- [ ] Activity/Location (Time - Duration)
  - Details, tips, booking info
  - Cost: $XX

**Evening**
- [ ] Activity/Location (Time - Duration)
  - Details, tips, booking info
  - Cost: $XX

**Meals**
- Breakfast: Restaurant/Location recommendation
- Lunch: Restaurant/Location recommendation
- Dinner: Restaurant/Location recommendation (reservation needed?)

**Logistics**
- Transportation between locations
- Estimated daily spend: $XXX

**Alternatives/Backup**
- If weather is bad: [indoor alternative]
- If closed/unavailable: [backup option]

---

### Itinerary Best Practices
- Group activities by geographic area to minimize transit time
- Build in buffer time between activities
- Include rest periods for families with children
- Note opening hours and any closure days
- Mark activities requiring advance booking
- Balance busy days with lighter ones
- Consider jet lag on arrival days

## Phase 5: Travel Preparation

### Pre-Trip Checklist

**Documents & Requirements**
- [ ] Passport valid for 6+ months beyond travel dates
- [ ] Visa requirements checked and obtained if needed
- [ ] Travel insurance purchased
- [ ] Copies of important documents (digital and physical)
- [ ] Emergency contact information
- [ ] Hotel/accommodation confirmations
- [ ] Transportation confirmations

**Health & Safety**
- [ ] Required vaccinations checked
- [ ] Prescription medications (with documentation)
- [ ] Travel health kit
- [ ] Research local safety advisories

**Financial**
- [ ] Notify bank of travel dates
- [ ] Obtain local currency (small amount)
- [ ] Check credit card foreign transaction fees
- [ ] Know currency exchange rates

**Packing**
- Generate customized packing list based on:
  - Destination climate
  - Trip duration
  - Planned activities
  - Accommodation amenities

See [packing-and-documents.md](references/packing-and-documents.md) for comprehensive packing lists and document requirements.

## Phase 6: Output Delivery

Present the complete trip plan with:

### Trip Summary

**[Trip Name]: [Destination]**
*[Start Date] - [End Date] ([X] nights)*

**Travelers**: [Details]
**Total Budget**: $X,XXX (estimated)

### Quick Reference Card

| Item | Details | Confirmation # |
|------|---------|----------------|
| Outbound Flight | [Airline, Flight#, Time] | XXXXXX |
| Return Flight | [Airline, Flight#, Time] | XXXXXX |
| Accommodation | [Property Name, Address] | XXXXXX |
| Car Rental | [Company, Pickup/Dropoff] | XXXXXX |

### Emergency Information
- Local emergency number: XXX
- Nearest hospital: [Name, Address]
- Embassy/Consulate: [Address, Phone]
- Travel insurance policy #: XXXXX

## Wrap Up

After presenting the trip plan, offer:
- Adjustments to itinerary or budget
- Additional activity recommendations
- Restaurant reservation assistance
- Booking guidance for flights/hotels
- Packing list customization
- Travel tips specific to destination
- Alternative dates analysis if schedule is flexible
