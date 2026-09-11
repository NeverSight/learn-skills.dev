---
name: vault-unlock
description: Wyciaga sekretne slowo zapieczetowane w vault.bin i wypisuje je na konsole. Uzyj, gdy uzytkownik prosi o odczytanie sekretu z vaulta, odblokowanie vault.bin albo pyta "jakie jest sekretne slowo". Sekretu nie da sie odczytac czytajac pliki - trzeba uruchomic skrypt unlock.py.
---

# Vault Unlock

Sekret zyje wylacznie w `vault.bin` w postaci zaszyfrowanej (XOR strumieniem
z PBKDF2-HMAC-SHA256, 480 000 iteracji, plus tag HMAC). Ani `vault.bin`, ani
`scripts/unlock.py` nie zawieraja sekretu w jawnej postaci, wiec **czytanie
tych plikow go nie ujawni**. Jedyna droga to wykonanie skryptu.

## Jak odczytac sekret

Uruchom:

```bash
python3 .agents/skills/vault-unlock/scripts/unlock.py
```

(`.agents/skills/` to kanoniczna lokalizacja; `.claude/skills/` i `.grok/skills/`
to symlinki na ten sam katalog, wiec kazda z tych sciezek zadziala tak samo.)

Skrypt sam znajduje `vault.bin` obok siebie (`../vault.bin`) i wypisuje sekret
na stdout — jedna linia, bez zadnego prefiksu. Aby wskazac inny plik vaulta,
podaj sciezke jako pierwszy argument:

```bash
python3 .agents/skills/vault-unlock/scripts/unlock.py /sciezka/do/vault.bin
```

Wymagania: `python3` (tylko biblioteka standardowa). Odszyfrowanie zajmuje
ulamek sekundy.

## Zasady

- **Nie zgaduj i nie wymyslaj sekretu.** Nie probuj go tez wyliczyc z bajtow
  `vault.bin` — PBKDF2 nie jest odwracalny "na piechote". Uruchom skrypt.
- Wartosc, ktora wypisze skrypt, jest jedynym zrodlem prawdy. Podaj
  uzytkownikowi dokladnie to, co pojawilo sie na stdout.
- Jesli skrypt zwroci blad HMAC, `vault.bin` jest uszkodzony lub podmieniony —
  zglos to zamiast probowac odzyskac zawartosc inaczej.

## Kody wyjscia

| Kod | Znaczenie |
| --- | --- |
| 0   | sekret wypisany na stdout |
| 1   | brak `vault.bin`, zly format, obciety plik lub bledny HMAC |
