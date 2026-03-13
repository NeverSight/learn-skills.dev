---
name: smhi-weather
description: Hämta väderprognoser från SMHI för de inbyggda orterna Mjölby, Linköping, Norrköping, Motala och Vadstena, samt vädervarningar för Östergötland. Använd när användaren frågar om väder, temperatur, nederbörd, vind eller prognos för någon av dessa orter, eller om vädervarningar i Östergötland.
---

# SMHI Weather

Hämta aktuell väderprognos och väderinformation från SMHI:s öppna API för svenska platser.

## Quick Start

### CLI-verktyg (Rekommenderat - Clean Output)

För enkel och clean output, använd `weather_cli.py`:

```bash
# Aktuellt väder
cd scripts && python weather_cli.py current linköping

# Prognos (12 timmar, standard)
cd scripts && python weather_cli.py forecast mjölby

# Prognos med custom antal timmar
cd scripts && python weather_cli.py forecast mjölby 24

# Vädervarningar
cd scripts && python weather_cli.py warnings
```

### Python API (För programmatisk användning)

För grundläggande väderinformation, använd `smhi_api.py`:

```python
from scripts.smhi_api import SMHIWeather

client = SMHIWeather()

# Hämta aktuellt väder för Mjölby (standardplats)
current = client.get_current_weather()

# Hämta aktuellt väder för en specifik plats
current = client.get_current_weather("linköping")

# Hämta sammanfattning (12 timmar framåt)
summary = client.get_weather_summary("norrköping", hours=12)

# Hämta fullständig prognos
forecast = client.get_forecast("mjölby")
```

## Workflow

### 1. Identifiera Plats

**Standardplats**: Mjölby (om ingen plats anges)

**Tillgängliga platser**:
- mjölby
- linköping  
- norrköping
- motala
- vadstena

Om användaren anger en annan plats, informera om att skillen bara har inbyggt stöd för orterna ovan och föreslå närmaste alternativ.

### 2. Avgör Typ av Väderinformation

**Aktuellt väder** (nu):
```python
client.get_current_weather("mjölby")
```

**Kort sammanfattning** (kommande timmar):
```python
client.get_weather_summary("mjölby", hours=12)
```

**Fullständig prognos** (flera dagar):
```python
client.get_forecast("mjölby")
```

### 3. Presentera Information

Format informationen på ett lättläst sätt på svenska:

**För aktuellt väder**:
```
Väder i Mjölby just nu:
• Temperatur: -4.5°C
• Nederbörd: Snö
• Vind: 2.5 m/s från nordost
• Luftfuktighet: 87%
• Molnighet: Mulet (8/8)
```

**För prognos**:
```
Väderprognos Mjölby 25 januari:

12:00 - -4.5°C, Snö, Vind 2.5 m/s
13:00 - -4.5°C, Snö, Vind 3.1 m/s
14:00 - -4.6°C, Snö, Vind 2.9 m/s
...
```

### 4. Hantera Fel

Om platsen inte finns:
- Informera användaren om tillgängliga platser
- Föreslå närmaste alternativ

Om API-anrop misslyckas:
- Förklara att SMHI:s API inte svarade
- Föreslå att försöka igen om en stund

## Vanliga Användarfrågor

### "Hur är vädret?"
→ Använd standardplats (Mjölby), visa aktuellt väder

### "Vad blir det för väder i Linköping?"
→ Hämta aktuellt väder + kort prognos för Linköping

### "Kommer det regna imorgon?"
→ Hämta prognos för nästa 24 timmar, fokusera på nederbörd

### "Väder nästa vecka i Norrköping"
→ Hämta fullständig prognos, sammanfatta per dag

### "Finns det vädervarningar?"
→ Använd `client.get_warnings_summary()` för formaterad sammanfattning

### "Varningar för Östergötland"
→ Använd `client.get_warnings()` för strukturerad data

### "Är det farligt väder?"
→ Kolla `highest_level` i warnings-data eller sammanfattningen

## Python Script Reference

### `scripts/smhi_api.py`

Main API client med följande metoder:

**`get_current_weather(location="mjölby")`**
- Returnerar: Dict med aktuellt väder
- Fält: location, time, temperature, humidity, precipitation, wind_speed, wind_direction, cloud_cover

**`get_weather_summary(location="mjölby", hours=12)`**
- Returnerar: Formaterad sträng med vädersammanfattning
- Parametrar: location (platsnamn), hours (antal timmar framåt)

**`get_forecast(location="mjölby")`**
- Returnerar: Komplett prognosdata med alla detaljer
- Innehåller: 24 timmars prognos med alla tillgängliga parametrar

**`get_warnings(county="Östergötland")`**
- Returnerar: Dict med alla aktiva varningar för länet
- Fält: county, warnings (lista), highest_level, fetched_at
- Inkluderar: Alla varningstyper (väder, brand, vatten)

**`get_warnings_summary(county="Östergötland")`**
- Returnerar: Formaterad sträng med varningssammanfattning (MEDIUM detaljnivå)
- Inkluderar: Varningstyp, svårighetsgrad, giltighetstid, beskrivning, råd

### Exempel på Användning

```python
from scripts.smhi_api import SMHIWeather

client = SMHIWeather()

# Scenario 1: "Hur är vädret?"
weather = client.get_current_weather()
print(f"Det är {weather['temperature']}°C i {weather['location']}")
print(f"Nederbörd: {weather['precipitation']}")

# Scenario 2: "Väder nästa 6 timmar"
summary = client.get_weather_summary("linköping", hours=6)
print(summary)

# Scenario 3: Detaljerad prognos
forecast = client.get_forecast("norrköping")
for entry in forecast['forecast'][:8]:
    time = entry['valid_time']
    temp = entry['temperature']
    print(f"{time}: {temp}°C")

# Scenario 4: "Finns det vädervarningar?"
warnings_summary = client.get_warnings_summary()
print(warnings_summary)

# Scenario 5: Strukturerad varningsdata
warnings_data = client.get_warnings()
if warnings_data['highest_level'] != 'NONE':
    print(f"Högsta varningsnivå: {warnings_data['highest_level']}")
    for warning in warnings_data['warnings']:
        print(f"- {warning['severity_sv']} varning: {warning['title']}")
```

### Output-exempel (Vädervarningar)

När det finns aktiva varningar:

```
AKTIVA VARNINGAR - Östergötland
============================================================

🟠 ⛈️ ORANGE VARNING - Snöfall i kombination med vind
Gäller: 26 jan 09:00 - 27 jan 08:00
Områden: Östergötlands län
Beskrivning: Snöfall 10-20 cm i kombination med hård vind...
Råd: Undvik onödiga resor, håll extra avstånd i trafiken...

🟡 🔥 GUL VARNING - Gräsbrandrisk
Gäller: 26 jan 12:00 - 27 jan 18:00
Områden: Östergötlands län
Beskrivning: Hög brandrisk på grund av torrt väder...

✅ Inga vattenvarningar aktiva.
```

När det inte finns varningar:

```
✅ Inga aktiva varningar för Östergötland.
```

## Tips

- **Caching**: SMHI uppdaterar prognoser ~4 gånger/dag. Cache data i minst 1 timme
- **Tolkningar**: Se `references/smhi_api_reference.md` för detaljerade parameterbeskrivningar
- **Tillägg**: Lägg till fler platser genom att uppdatera `LOCATIONS` i `smhi_api.py`

## Resources

### references/smhi_api_reference.md
Detaljerad API-dokumentation med:
- Fullständig parameterlista
- Väderssymboler och deras betydelse
- Vindstyrkeinterpretationer
- Nederbördskategorier
- API-endpoints och felhantering
