---
name: travel-assistant
description: "Travel assistant for quickly looking up flights and hotels. Use when the user wants to search for flights, compare airfare prices, find hotels, or plan travel. Triggers include requests like 'find flights to Paris', 'search hotels in Tokyo', 'compare flight prices', 'plan my trip', or any travel booking research."
---

# Travel Assistant Skill

Expert guidance for researching flights and hotels using popular online travel tools.

## Capabilities

This skill helps you:
- Search for flights using Google Flights, Skyscanner, Kayak
- Find and compare hotel options using Booking.com, Hotels.com, Expedia
- Build optimized search URLs for travel sites
- Compare prices across multiple platforms
- Find the best travel deals and timing

## Flight Search Workflow

### 1) Gather Trip Details

Before searching, collect:
- **Origin**: Departure city/airport (use IATA codes when possible, e.g., LAX, JFK, LHR)
- **Destination**: Arrival city/airport
- **Dates**: Departure date and return date (if round trip)
- **Passengers**: Number of travelers, any children
- **Class**: Economy, Premium Economy, Business, First
- **Flexibility**: Exact dates or flexible (+/- days)

### 2) Search Flight Aggregators

**Google Flights** (Recommended first stop)
- URL: https://www.google.com/travel/flights
- Features: Price tracking, date grid, "Explore" for flexible destinations
- Tip: Use "Track prices" to get alerts for price drops

**Skyscanner**
- URL: https://www.skyscanner.com
- Features: "Everywhere" search, whole month view, price alerts
- Best for: Finding cheapest dates, budget airlines

**Kayak**
- URL: https://www.kayak.com/flights
- Features: Price forecast, fare comparison, hacker fares
- Best for: Mixing airlines for better prices

### 3) Build Direct Search URLs

**Google Flights URL format:**
```
https://www.google.com/travel/flights?q=Flights%20to%20{DESTINATION}%20from%20{ORIGIN}%20on%20{DATE}
```

**Skyscanner URL format:**
```
https://www.skyscanner.com/transport/flights/{ORIGIN}/{DESTINATION}/{YYMMDD}/{YYMMDD}/
```
Example: `https://www.skyscanner.com/transport/flights/lax/cdg/250315/250322/`

### 4) Flight Search Tips

- **Best booking window**: Domestic 1-3 months ahead, International 2-8 months ahead
- **Cheapest days to fly**: Typically Tuesday, Wednesday, Saturday
- **Use incognito mode**: Prevents potential price tracking cookies
- **Check airline sites directly**: Sometimes have exclusive deals
- **Consider nearby airports**: Can save significantly
- **Set price alerts**: On Google Flights or Skyscanner

## Hotel Search Workflow

### 1) Gather Stay Details

Before searching, collect:
- **Location**: City, neighborhood, or specific address/landmark
- **Check-in/Check-out dates**
- **Guests**: Number of adults, children, rooms needed
- **Budget**: Price range per night
- **Preferences**: Star rating, amenities (pool, gym, breakfast, parking, WiFi)

### 2) Search Hotel Aggregators

**Booking.com**
- URL: https://www.booking.com
- Features: Free cancellation filters, Genius discounts, verified reviews
- Best for: Wide selection, flexible cancellation

**Hotels.com**
- URL: https://www.hotels.com
- Features: Rewards program (stay 10 nights, get 1 free)
- Best for: Loyalty rewards

**Expedia**
- URL: https://www.expedia.com/Hotels
- Features: Bundle deals (flight + hotel), member prices
- Best for: Package deals

**Google Hotels**
- URL: https://www.google.com/travel/hotels
- Features: Price comparison across sites, map view
- Best for: Quick comparison, seeing all options

**Kayak Hotels**
- URL: https://www.kayak.com/hotels
- Features: Price forecast, deal ratings
- Best for: Finding underpriced hotels

### 3) Build Direct Search URLs

**Booking.com URL format:**
```
https://www.booking.com/searchresults.html?ss={LOCATION}&checkin={YYYY-MM-DD}&checkout={YYYY-MM-DD}&group_adults={N}
```

**Google Hotels URL format:**
```
https://www.google.com/travel/hotels/{LOCATION}?q={LOCATION}%20hotels
```

### 4) Hotel Search Tips

- **Check multiple sites**: Prices vary significantly between aggregators
- **Look for member/loyalty prices**: Often 10-20% off
- **Read recent reviews**: Focus on reviews from last 6 months
- **Check location on map**: Proximity to attractions matters
- **Look for free cancellation**: Book early, cancel if you find better
- **Contact hotel directly**: Sometimes match or beat online prices
- **Check for hidden fees**: Resort fees, parking, WiFi charges

## Price Comparison Strategy

For the best deals, follow this order:

### Flights
1. **Google Flights** - Get baseline prices and explore dates
2. **Skyscanner** - Check budget airlines and alternative routes
3. **Kayak** - Look for hacker fares (mixed airlines)
4. **Airline websites** - Check for exclusive web fares
5. **Set alerts** - Track prices for 1-2 weeks if flexible

### Hotels
1. **Google Hotels** - Quick price comparison across all sites
2. **Booking.com** - Wide selection, good cancellation
3. **Hotel website directly** - Check for best rate guarantee
4. **Bundle options** - Expedia/Kayak for flight+hotel

## Using WebFetch for Travel Research

When I need to look up specific travel information, I can use WebFetch to:
- Check current prices on travel sites
- Verify flight availability
- Look up hotel amenities and reviews
- Get real-time travel advisories

Example prompts for WebFetch:
- "What are the current flight prices shown on this page?"
- "What hotels are listed and at what prices?"
- "What are the check-in times and amenities for this hotel?"

## Sample Queries I Can Help With

- "Find flights from San Francisco to Tokyo in March"
- "What's the cheapest time to fly to Europe from NYC?"
- "Search for hotels near the Eiffel Tower under $200/night"
- "Compare flight prices to London for next month"
- "Find pet-friendly hotels in Seattle"
- "What airlines fly direct from LAX to Barcelona?"

## Travel Planning Checklist

When planning a trip, consider:

- [ ] **Flights**: Book 2-3 months ahead for best prices
- [ ] **Hotels**: Compare at least 3 aggregators
- [ ] **Visa requirements**: Check destination country requirements
- [ ] **Travel insurance**: Consider for international trips
- [ ] **Local transportation**: Airport transfers, car rental needs
- [ ] **Currency**: Check exchange rates, notify bank of travel
- [ ] **Weather**: Pack appropriately for season
- [ ] **Health**: Vaccinations, medications, travel advisories

## Airport Code Reference

Common IATA codes for quick searches:

**US Major Hubs**
- LAX (Los Angeles), SFO (San Francisco), JFK/LGA/EWR (New York area)
- ORD (Chicago O'Hare), ATL (Atlanta), DFW (Dallas), MIA (Miami)
- SEA (Seattle), DEN (Denver), BOS (Boston), IAD/DCA (Washington DC)

**International Hubs**
- LHR (London Heathrow), CDG (Paris), FRA (Frankfurt), AMS (Amsterdam)
- NRT/HND (Tokyo), HKG (Hong Kong), SIN (Singapore), DXB (Dubai)
- SYD (Sydney), MEX (Mexico City), GRU (Sao Paulo), YYZ (Toronto)
