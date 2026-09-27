---
name: localize-tr
description: Use when translating or localizing UI strings, marketing copy, documentation, or any source text into Turkish (Türkçe) for Turkey and Northern Cyprus. Turkic agglutinative, NO gender. The critical trap is dotted vs dotless i — İ/i and I/ı are separate phonemes; capitalization must preserve dot status (istanbul→İstanbul, ışık→IŞIK). Enforces two-dimensional vowel harmony, six-case suffixes, SOV order, siz/sen formality (siz default), singular noun after numbers (5 dosya), apostrophe before suffixes on proper nouns (Türkiye'de), sentence case not Title Case, TDK anti-anglicism (indirmek not downloadlamak), DD.MM.YYYY, and TRY ₺ (1.234,56).
---

# Localize: Turkish (tr → Türkçe)

You are translating source text into Turkish for Turkey and Northern Cyprus. This skill captures grammar, register, UI conventions, formatting, and Turkish-specific failure modes derived from a production translation prompt.

## Scope & Variants

**One unified standard for UI localization:**

- **tr-TR** — Turkish as used in the Republic of Turkey. The default. ~85 million native speakers; official, codified by Türk Dil Kurumu (TDK, the Turkish Language Society).
- **tr-CY** — Turkish in **Northern Cyprus** (Turkish Republic of Northern Cyprus, recognized only by Turkey). Uses the same Istanbul-based standard as Turkey for written/UI purposes. Some lexical and intonation differences exist in spoken Turkish Cypriot dialect, but they are NOT relevant for software localization — treat tr-CY UI as tr-TR.

Turkish is also spoken by significant diaspora communities (Germany ~3M, Bulgaria, Greece, Macedonia, Iraq, Syria) — they use the same standard.

**Script context — Atatürk's 1928 alphabet reform:**

- Before 1928, Turkish was written in **Ottoman Arabic script** (Osmanlıca) — right-to-left, with Persian/Arabic loanword consonants.
- In 1928, the **Harf Devrimi (Letter Revolution)** under Mustafa Kemal Atatürk replaced it with a 29-letter Latin alphabet specifically designed for Turkish phonology.
- This was followed by the **Öztürkçe (pure Turkish) movement** — a state-driven effort to replace Arabic/Persian loanwords with native Turkic roots or new coinages. Modern Turkish is significantly more "Turkic-rooted" than Ottoman Turkish was.
- Practical consequence: don't be surprised that Turkish UI prefers native verbs (`indirmek` "download") over English loans (`downloadlamak`) — this is **language policy**, not just taste.

**Native name:** Türkçe (the language); Türk (Turkish person, adjective). Use **Türkçe** for the language in UI.

## Identity Guardrail

**Turkish is Turkic, NOT Indo-European, NOT Arabic, NOT Persian.**

- **Closest sister language: Azerbaijani (Azərbaycan dili)** — Oghuz Turkic branch, ~80% mutually intelligible with Turkish.
- **Distant Turkic relatives:** Uzbek, Kazakh, Kyrgyz, Tatar, Bashkir, Turkmen, Uyghur, Yakut. All share agglutinative morphology and vowel harmony, but the lexical and grammatical distance to Turkish varies from "moderate" (Turkmen, Gagauz) to "very large" (Yakut, Chuvash).
- **NOT Indo-European** — Turkish is in the Turkic family (sometimes grouped with Mongolic, Tungusic, Korean, Japanese under the controversial "Altaic" hypothesis; this grouping is **not** accepted by most modern linguists).
- **NOT Arabic and NOT Persian** — despite many Arabic loanwords (kitap "book", saat "hour", aile "family", millet "nation") and Persian loanwords (şehir "city", hafta "week", pencere "window", merhaba "hello") in the lexicon, the **grammar is fundamentally Turkic**:
  - Agglutinative (suffix stacking), NOT inflectional like Arabic (root-and-pattern) or Persian (Indo-European).
  - SOV word order (Subject-Object-Verb), unlike Arabic VSO or Persian SOV-ish.
  - Vowel harmony — completely absent from Arabic and Persian.
  - NO grammatical gender — Arabic has masc/fem, Persian doesn't have it either but uses different mechanisms.
  - One pronoun "o" covers he/she/it.

**Do NOT translate Turkish by analogy with:**

- Arabic (different family, RTL script, no vowel harmony, gendered)
- Persian/Farsi (Indo-European, has ezafe, no vowel harmony, no agglutination on this scale)
- Russian (Slavic, has gender and case but inflectional not agglutinative)
- English (no harmony, no agglutination, SVO not SOV)

When loanwords from Arabic/Persian/French/English appear in Turkish text, they are **fully Turkified**: they take Turkish suffixes with Turkish vowel harmony based on **Turkish pronunciation**, not the original language's spelling.

## Register

**Default level: FORMAL (siz-form)** for software UI, errors, documentation, marketing. Equivalent to German Sie / French vous.

| | siz (formal / plural) | sen (informal singular) |
|---|---|---|
| Pronoun | siz | sen |
| Verb form (present) | -siniz/-sınız/-sunuz/-sünüz (2nd plural) | -sin/-sın/-sun/-sün (2nd singular) |
| Imperative | Kaydedin, Tıklayın, Yükleyin | Kaydet, Tıkla, Yükle |
| Possessive (your) | -ınız/-iniz/-unuz/-ünüz | -ın/-in/-un/-ün |
| Example | Ayarlarınızı değiştirebilirsiniz | Ayarlarını değiştirebilirsin |

**Critical insight:** Turkish `siz` is **BOTH the formal singular AND the actual plural "you"**. The verb form is 2nd-person plural regardless. There is no separate formal-singular form like Spanish `usted` (which uses 3rd person). So:

- "You (one person, formally)" → siz + 2pl verb
- "You all (multiple people)" → siz + 2pl verb (same)
- "You (one person, informally / friend / child)" → sen + 2sg verb

A third pseudo-formal form `zat-ı âliniz` ("your eminence") exists but is over-formal for UI — never use.

**Within a file, ONE register only.** Mixing siz and sen in possessives, verbs, or imperatives is always wrong (severity 2.0).

**Examples of inconsistency to reject:**

- ❌ "İşte kaçırdıklarınız (formal possessive). Kontrol et (informal imperative)." → ✅ "İşte kaçırdıklarınız. Kontrol edin."
- ❌ "Dosyalarınızı yükleyin. İncele." → ✅ "Dosyalarınızı yükleyin. İnceleyin."
- ❌ "Hesabını oluştur (informal) ve sonra giriş yapabilirsiniz (formal)" → ✅ all formal or all informal

When in doubt for software UI: **use siz**. Casual apps targeting Gen-Z, gaming, or social platforms may justify `sen` — confirm with the product team before defaulting.

## Critical Hard Rules

### Dotted vs Dotless i — THE Turkish Trap (severity 3.0)

Turkish has **four distinct i-letters**, paired into two completely separate phonemes:

| Letter | Description | Sound | Vowel type |
|---|---|---|---|
| **İ** (capital, dotted) | front, high, unrounded | [i] (like English "ee") | front unrounded |
| **i** (lowercase, dotted) | front, high, unrounded | [i] | front unrounded |
| **I** (capital, dotless) | back, high, unrounded | [ɯ] (no English equivalent) | back unrounded |
| **ı** (lowercase, dotless) | back, high, unrounded | [ɯ] | back unrounded |

**Capitalisation must preserve the dot status:**

| Lowercase | UPPERCASE | Explanation |
|---|---|---|
| istanbul | **İstanbul** | proper noun starts with dotted i; capital keeps the dot |
| ışık (light) | **IŞIK** | proper-noun-style capitalization keeps dotless I |
| Türkiye'de | TÜRKİYE'DE | dotted İ in capital |
| açık | AÇIK | dotless I in capital |
| dilim (my language) | DİLİM | dotted İ |
| dilim (slice) | DİLİM | same — context distinguishes |

**Common software bugs (avoid):**

- ❌ "Istanbul" (English-style — dotless capital I where dotted İ is correct)
- ❌ "ISIK" written for "ışık" (this would be read as a different word — "išık" doesn't exist; the IŞIK spelling is correct for "ışık", because the capital of dotless ı IS plain I)
- ❌ JavaScript `"i".toUpperCase()` defaulting to "I" without Turkish locale → wrong; use `"i".toLocaleUpperCase("tr-TR")` → "İ"
- ❌ JavaScript `"I".toLowerCase()` defaulting to "i" without Turkish locale → wrong in Turkish context; the lowercase of plain I in Turkish is ı

**When translating, NEVER:**

1. Write "Istanbul" — always **İstanbul**
2. Write "Izmir" — always **İzmir**
3. Write "Indir" (for "download") — the correct form is **İndir** (capital İ with dot, because the verb stem is "indir-" with dotted i)
4. Capitalize "ışık" as "Işık" if the surrounding context demands a dotted capital — but normally "ışık" → "Işık" IS correct because dotless ı capitalizes to dotless I.

**Quick rule:** lowercase **i** (dotted) ↔ uppercase **İ** (dotted); lowercase **ı** (dotless) ↔ uppercase **I** (dotless). They never cross.

### Turkish Alphabet — 29 Letters, No Q/W/X (severity 2.0)

The Turkish alphabet (Atatürk's 1928 reform):

```
A B C Ç D E F G Ğ H I İ J K L M N O Ö P R S Ş T U Ü V Y Z
a b c ç d e f g ğ h ı i j k l m n o p r s ş t u ü v y z
```

**Letters NOT in English** (6): Ç ç, Ğ ğ, I ı (dotless), İ i (dotted — i is in English but its capital İ isn't), Ö ö, Ş ş, Ü ü.

**English letters NOT in Turkish:** Q, W, X.

| Letter | Sound | Notes |
|---|---|---|
| **Ç ç** | [tʃ] (like "ch" in "chair") | always [tʃ], no exceptions |
| **Ğ ğ** | yumuşak ge (soft g) | **NEVER word-initial**; lengthens preceding vowel, often silent. dağ "mountain" sounds like "daa". |
| **I ı** | [ɯ] back unrounded high vowel | NO equivalent in English; some compare to the e in "roses" |
| **İ i** | [i] front unrounded high vowel | like "ee" in "see" |
| **J j** | [ʒ] (like "s" in "measure" / French j) | used only in loanwords (jandarma, mucize) |
| **Ö ö** | [œ] front rounded mid vowel | like German ö, French eu |
| **Ş ş** | [ʃ] (like "sh" in "ship") | always [ʃ] |
| **Ü ü** | [y] front rounded high vowel | like German ü, French u |

**Yumuşak ge (ğ) rules:**

- NEVER starts a word. If you see ğ initial, it's a typo or transliteration error.
- Between two front vowels (e, i, ö, ü): pronounced as a [j] glide. eğer "if" sounds like "eyer".
- Between back vowels or word-finally: silent, just lengthens preceding vowel. dağ "mountain", sağ "right", uğur "luck" — the ğ is mute.
- Always lowercase ğ, capital Ğ. **NEVER** replace ğ with plain g.
- ❌ dag (for "dağ") → ✅ dağ
- ❌ Türkce (for "Türkçe") → ✅ Türkçe
- ❌ degisiklik → ✅ değişiklik

**Q, W, X in Turkish text:** appear ONLY in foreign brand names (`Xerox`, `Windows`, `Wikipedia`, `Quasar`), proper nouns (Kurdish names with x or w), or transliteration. They keep their original spelling but take Turkish suffixes via apostrophe (`Xerox'tan`, `Windows'a`, `Wikipedia'ya`).

### Vowel Harmony — Two-Dimensional (severity 2.5)

**Every suffix in Turkish must harmonize with the stem's vowels.** Two independent harmony systems operate:

#### 1. Front-Back Harmony (low/mid vowels in suffixes)

Suffixes with **a/e** alternate based on whether the last vowel of the stem is front or back:

| Stem's last vowel | Type | a/e becomes |
|---|---|---|
| a, ı, o, u | **back** | **a** |
| e, i, ö, ü | **front** | **e** |

**Examples (locative -da/-de "in/at"):**

| Stem | Last vowel | Type | Locative |
|---|---|---|---|
| ev (house) | e | front | ev**de** |
| kitap (book) | a | back | kitap**ta** (also consonant assimilation, see below) |
| göz (eye) | ö | front | göz**de** |
| dosya (file) | a | back | dosya**da** |
| köprü (bridge) | ü | front | köprü**de** |
| oda (room) | a | back | oda**da** |
| şehir (city) | i | front | şehir**de** |

#### 2. Rounded-Unrounded Harmony (high vowels in suffixes)

Suffixes with **i/ı/u/ü** alternate on TWO axes — front/back AND rounded/unrounded — giving 4 forms:

| Stem's last vowel | Type | Suffix high vowel |
|---|---|---|
| a, ı | back unrounded | **ı** |
| e, i | front unrounded | **i** |
| o, u | back rounded | **u** |
| ö, ü | front rounded | **ü** |

**Examples (genitive/possessive -in/-ın/-un/-ün "your"):**

| Stem | Last vowel | Type | Possessive "your" |
|---|---|---|---|
| ev (house) | e | front unrounded | ev**in** (your house) |
| kitap (book) | a | back unrounded | kitab**ın** (your book) — also consonant softening, see below |
| göz (eye) | ö | front rounded | göz**ün** (your eye) |
| torun (grandchild) | u | back rounded | torun**un** (your grandchild) |
| sistem (system) | e | front unrounded | sistem**in** |
| oda (room) | a | back unrounded | oda**n** (your room — `n` because of vowel-stem buffer rule) |
| köprü (bridge) | ü | front rounded | köprü**n** |
| dolap (closet) | a | back unrounded | dolab**ın** |

**Combining both harmonies on the accusative -i/-ı/-u/-ü:**

| Stem | Accusative (definite object marker) |
|---|---|
| ev | ev**i** (front unrounded) |
| kitap | kitab**ı** (back unrounded, + softening) |
| göz | göz**ü** (front rounded) |
| okul | okul**u** (back rounded) |

**Common harmony errors (all severity 2.5):**

- ❌ sistem**da** → ✅ sistem**de** (sistem is front, not back)
- ❌ dosya**de** → ✅ dosya**da** (dosya is back)
- ❌ köprü**da** → ✅ köprü**de** (köprü is front-rounded)
- ❌ sistem**ım** → ✅ sistem**im** (front, unrounded high)
- ❌ kitap**im** → ✅ kitab**ım** (back, unrounded high — plus softening)
- ❌ göz**im** → ✅ göz**üm** (front rounded high)

**Disharmonic loanwords** (rare exceptions, mostly Arabic/Persian/French origin) keep their harmony based on **Turkish pronunciation** of the final syllable:

- saat ("hour", final vowel a sounds back, but pronounced [saːt]) → saat**te** (back) — back wins
- harf ("letter", a back) → harf**te** (back)
- kalp ("heart", a back, but the final l is "soft" l) → kalb**im** (front high! due to soft l)
- rol ("role") → rol**ü** (front rounded — due to soft l)

When unsure, look up the word — disharmony patterns are listed in TDK dictionaries.

### Agglutinative Suffix Stacking (severity 2.0)

Turkish builds complex meaning by **stacking suffixes onto a stem in a fixed order**. Each suffix obeys vowel harmony with the preceding vowel.

**Standard noun suffix order:**

```
STEM + PLURAL + POSSESSIVE + CASE + COPULA/VERB-MARKER
```

**Example: `evlerimdekilerden` = "from the ones at my houses"**

| Morpheme | Meaning | Form |
|---|---|---|
| ev | house | stem |
| -ler | plural | (front harmony) |
| -im | 1sg possessive ("my") | (front unrounded) |
| -de | locative ("at") | (front harmony) |
| -ki | relative ("the ones that are") | invariant |
| -ler | plural | (after relative ki, with front harmony) |
| -den | ablative ("from") | (front harmony) |

→ 7 morphemes, 1 word, ~5 English words to translate.

**More UI-relevant examples:**

- **dosya** (file) → **dosyalarım** (my files) = dosya + lar (plural) + ım (1sg possessive)
- **dosya** → **dosyalarınızda** (in your files [formal/plural]) = dosya + lar + ınız (2pl/formal possessive) + da (locative)
- **kullanıcı** (user) → **kullanıcılarımız** (our users) = kullanıcı + lar + ımız (1pl possessive)
- **ayar** (setting) → **ayarlarınızı** (your settings [accusative]) = ayar + lar + ınız + ı (accusative — definite object)

**Rules for suffix attachment:**

1. **No spaces, no hyphens** between stem and suffix.
   - ❌ ev de → ✅ evde
   - ❌ ev-de → ✅ evde
2. **Apostrophe required** with proper nouns and abbreviations (see Apostrophe section below).
3. Vowel harmony reset at each suffix based on the vowel just before it.

### Six-Case System (severity 2.0)

Turkish has **six grammatical cases**, all marked by suffixes (which obey vowel harmony). No prepositions for these — case suffixes do the work.

| Case | Suffix forms | Meaning | Example (ev "house") |
|---|---|---|---|
| **Nominative** | ∅ (no suffix) | subject; bare form | ev |
| **Accusative** | -i / -ı / -u / -ü | **definite** direct object | ev**i** (the house, as object) |
| **Dative** | -e / -a | to / toward / into | ev**e** (to the house) |
| **Locative** | -de / -da (after voiceless: -te / -ta) | in / at / on | ev**de** (at the house) |
| **Ablative** | -den / -dan (after voiceless: -ten / -tan) | from / out of | ev**den** (from the house) |
| **Genitive** | -in / -ın / -un / -ün | of / 's | ev**in** (of the house) |
| **Instrumental** | -le / -la (or separate word `ile`) | with / by means of | ev**le** / ev ile (with the house) |

(Instrumental is sometimes counted as the 7th case; older grammars count 6.)

**Critical location vs motion contrast:**

- ❌ dosyaya (when meaning "in the file") → ✅ **dosyada** (locative, "in/at")
- ❌ dosyada (when meaning "to the file") → ✅ **dosyaya** (dative, "to/into")
- ❌ sistem**dan** (back-harmonized but stem is front) → ✅ **sistemden** (ablative + front harmony)
- ❌ kitap**da** (no consonant assimilation) → ✅ **kitapta** (voiceless final p → suffix d hardens to t)

**Definite vs indefinite direct object:**

Turkish marks definiteness of the object with the accusative suffix:

| Sentence | Translation |
|---|---|
| Kitap okuyorum. (no suffix on kitap) | I'm reading a book. (any book, indefinite) |
| Kitab**ı** okuyorum. (accusative) | I'm reading the book. (specific, definite) |
| Bir kitap okuyorum. (bir = "a/one") | I'm reading a book. (explicit indefinite) |

So **accusative -i is ONLY for definite objects**. Don't add it to indefinite objects:

- ❌ "Bir dosyayı kaydetti" → ✅ "Bir dosya kaydetti" (saved a file — indefinite, no accusative)
- ❌ "Bir dosya kaydetti" (when meaning "saved THE file") → ✅ "Dosyayı kaydetti"

### Consonant Assimilation in Suffixes (severity 1.5)

When a suffix starting with d/c/g attaches to a stem ending in a **voiceless consonant** (p, t, k, ç, ş, s, f, h), the suffix initial **hardens to its voiceless counterpart**:

| Suffix | After voiceless | Example |
|---|---|---|
| -de / -da (locative) | -te / -ta | sokak**ta** (in the street), kitap**ta** (in the book), mektup**ta** (in the letter) |
| -den / -dan (ablative) | -ten / -tan | sokak**tan**, kitap**tan**, mektup**tan** |
| -ci / -cı / -cu / -cü (agent) | -çi / -çı / -çu / -çü | sa**at**çi → saatçi (watchmaker, after t voiceless), foto**ğraf**çı (photographer, after f voiceless) |

**Reverse — voicing of final consonants before vowel-initial suffix** (softening, severity 1.5):

When a stem ending in **p, t, k, ç** takes a vowel-initial suffix, the final consonant often **softens**:

| Final | Softens to | Example |
|---|---|---|
| p | b | kitap → kitab**ı** (book → the book, accusative); dolap → dolab**a** (closet → to the closet) |
| t | d | kanat → kanad**ı** (wing → the wing); tat → tad**ı** (taste → its taste) |
| k | ğ | sokak → sokağ**a** (street → to the street); ayak → ayağ**ım** (foot → my foot) |
| ç | c | ağaç → ağac**ı** (tree → the tree); güç → güc**ü** (strength → its strength) |

**Not all stems soften.** Single-syllable native words and many loanwords stay hard:

- ❌ ip → ib**i**? → ✅ ip**i** (stays p — single syllable native word)
- ❌ at → ad**ı**? → ✅ at**ı** (stays t — single syllable, distinguishes from "ad" name)
- ✅ saat → saat**i** (loanword, stays t)
- ✅ devlet → devlet**i** (loanword, stays t)

When in doubt, **check TDK dictionary** for the softening behavior. Misapplied softening is severity 1.5.

### Possessive Suffixes Instead of Pronouns (severity 1.5)

Turkish does NOT use separate possessive pronouns (like English "my", "your"). Instead, **possessive suffixes attach to the noun**:

| Person | Suffix | Example (ev "house") |
|---|---|---|
| 1sg (my) | -im / -ım / -um / -üm | ev**im** (my house) |
| 2sg informal (your) | -in / -ın / -un / -ün | ev**in** (your house) |
| 3sg (his/her/its) | -i / -ı / -u / -ü or -si / -sı / -su / -sü after vowel | ev**i** (his house); kapı**sı** (his door) |
| 1pl (our) | -imiz / -ımız / -umuz / -ümüz | ev**imiz** (our house) |
| 2pl / formal (your) | -iniz / -ınız / -unuz / -ünüz | ev**iniz** (your house [formal]) |
| 3pl (their) | -leri / -ları | ev**leri** (their house) |

**Optional possessive pronoun (for emphasis only):**

- benim evim (my house — emphatic)
- senin evin (your house — emphatic)
- sizin eviniz (your [formal] house — emphatic)

**In UI:** drop the pronoun, use only the suffix.

- ❌ "Senin ayarların" (your settings — pronoun + suffix) → for emphasis OK; for default UI use **"Ayarların"** (informal) or **"Ayarlarınız"** (formal).
- ❌ "Benim hesabım" → ✅ **"Hesabım"** in UI.

**Common error: using English-style pronoun without suffix:**

- ❌ "Sizin ayarlar" (just pronoun, no suffix) → ✅ **"Ayarlarınız"** (just suffix)

### SOV Word Order — Verb at the End (severity 2.0)

Turkish is **strictly SOV** (Subject-Object-Verb) in neutral sentences. The verb comes last.

| English (SVO) | Wrong (SVO calque) | Correct (SOV) |
|---|---|---|
| The user saved the file. | Kullanıcı kaydetti dosyayı. | **Kullanıcı dosyayı kaydetti.** |
| I am reading a book. | Okuyorum bir kitap. | **Bir kitap okuyorum.** |
| Click the button to save. | Tıkla butona kaydetmek için. | **Kaydetmek için butona tıkla.** (or **butona tıklayın** formal) |
| The system sent the email. | Sistem gönderdi e-postayı. | **Sistem e-postayı gönderdi.** |

**Question word order:** Same SOV, with question particle -mi/-mı/-mu/-mü after the questioned element:

- "Dosyayı kaydettin **mi**?" (Did you save the file? — informal)
- "Dosyayı kaydettiniz **mi**?" (formal/plural)
- "**Sen mi** dosyayı kaydettin?" (Was it YOU who saved the file? — focus shifted)
- "Sen dosyayı **mi** kaydettin?" (Did you save THE FILE? — focus on object)

### Singular Noun After Numbers (severity 2.0)

**Turkish nouns stay SINGULAR after numbers**, including in the ICU `other` branch.

- ❌ beş dosyalar (five files-plural) → ✅ **beş dosya** (five file-singular)
- ❌ üç kullanıcılar → ✅ **üç kullanıcı**
- ❌ 100 diller → ✅ **100 dil** (100 languages)
- ❌ 25 mesajlar → ✅ **25 mesaj**

The plural -ler/-lar is used ONLY when the quantity is non-numeric:

- "Dosyalar yüklendi." (The files were uploaded — collective, no number)
- "Kullanıcılar burada listelenmiştir." (The users are listed here — collective)

ICU pattern:

```icu
{count, plural,
  one {# dosya}
  other {# dosya}
}
```

**Both branches use the SINGULAR**. This is correct Turkish. Turkish has only 2 plural categories: `one` (=1) and `other` (everything else, but **still singular noun form**).

### Question Marker -mi/-mı/-mu/-mü (severity 2.0)

Yes/no questions in Turkish use the **separate-word question particle** -mi (with full vowel harmony) attached to (but **written separately from**) the questioned element:

| Statement | Question |
|---|---|
| Geliyor. (He/she is coming.) | Geliyor **mu**? (Is he/she coming?) |
| Gidiyorsun. (You are going.) | Gidiyor **musun**? (Are you going? — informal) |
| Kaydettiniz. (You [formal] saved.) | Kaydettiniz **mi**? (Did you save?) |
| Türk. (He/she is Turkish.) | Türk **mü**? (Is he/she Turkish?) |
| Açık. (It's open.) | Açık **mı**? (Is it open?) |

**Rules:**

1. -mi/-mı/-mu/-mü is a **separate word** in writing (with space before it).
2. Harmonizes with the previous vowel: i/ı/u/ü.
3. Person suffixes (-sin, -siniz) attach to **the question particle**, not to the verb: gidiyor **musun**, gidiyor **musunuz**.

Common errors:

- ❌ Geliyormu? (no space) → ✅ **Geliyor mu?**
- ❌ Geliyor mi? (wrong harmony — ge-li-yor ends in o, back rounded → mu) → ✅ **Geliyor mu?**

### Apostrophe with Proper Nouns and Abbreviations (severity 2.0)

When attaching suffixes to **proper nouns** (names, places, brands) or **abbreviations**, Turkish uses an **apostrophe** between the stem and the suffix.

| Wrong | Correct | Type |
|---|---|---|
| Türkiyede | **Türkiye'de** | place name + locative |
| Istanbulu | **İstanbul'u** | place name + accusative (note: İstanbul not Istanbul) |
| OneSkyı | **OneSky'ı** | brand + accusative |
| Googleda | **Google'da** | brand + locative |
| APIye | **API'ye** | abbreviation + dative (API pronounced [a-pe-i] → ends in front i → -ye) |
| USBye | **USB'ye** | abbreviation + dative (USB [u-es-be] → ends in front e → -ye) |
| PDFe | **PDF'e** | abbreviation + dative (PDF [pe-de-fe] → ends in e → -e) |
| GitHubda | **GitHub'da** | brand + locative |
| Aliye | **Ali'ye** | person name + dative |

**For abbreviations**, the harmony is based on **Turkish pronunciation** of the last letter:

| Abbrev | Turkish pronunciation | Last sound | Suffix |
|---|---|---|---|
| API | [a-pe-i] | i (front unrounded) | API'**ye**, API'**de** |
| USB | [u-es-be] | e (front unrounded) | USB'**ye**, USB'**de** |
| PDF | [pe-de-fe] | e | PDF'**e**, PDF'**de** |
| URL | [u-er-le] (or [yu-ar-el]) | e | URL'**ye** (or URL'**e**) |
| HTML | [ha-te-me-le] | e | HTML'**de** |
| CEO | [se-o] or [si-i-o] | o (back rounded) | CEO'**ya**, CEO'**dan** |
| TBMM | [te-be-me-me] | e | TBMM'**ye** |

When the abbreviation is read **as a word** (like NATO [na-to], UNESCO [u-nes-ko]), harmony follows that pronunciation.

### Verbal Suffixes — Person + Tense/Aspect (severity 1.5)

Turkish verbs agglutinate to express tense, aspect, mood, and person — all in one word.

**Person endings on verbs:**

| Person | Type 1 (after most tenses) | Type 2 (after -di past, -se conditional) |
|---|---|---|
| 1sg (I) | -im/-ım/-um/-üm | -m |
| 2sg informal (you) | -sin/-sın/-sun/-sün | -n |
| 3sg (he/she/it) | ∅ | ∅ |
| 1pl (we) | -iz/-ız/-uz/-üz | -k |
| 2pl / formal (you) | -siniz/-sınız/-sunuz/-sünüz | -niz/-nız/-nuz/-nüz |
| 3pl (they) | -ler/-lar | -ler/-lar |

**Tense/aspect suffixes (partial list, with vowel harmony):**

| Suffix | Meaning | Example (gel- "come") |
|---|---|---|
| -iyor / -ıyor / -uyor / -üyor | present continuous | gel**iyor**um (I am coming) |
| -er / -ar | aorist (habitual/general) | gel**ir**im (I [usually] come) |
| -di / -dı / -du / -dü | definite past (witnessed) | gel**di**m (I came) |
| -miş / -mış / -muş / -müş | evidential past (reported/inferred) | gel**miş**im (I [reportedly/apparently] came) |
| -ecek / -acak | future | gel**eceğ**im (I will come — note ğ before vowel) |
| -meli / -malı | necessity (must) | gel**meli**yim (I must come) |
| -ebil / -abil | ability | gel**ebil**irim (I can come) |
| -se / -sa | conditional | gel**se**m (if I come) |

**Example: "kullanabilirsiniz" = "you (formal/plural) can use"**

| Morpheme | Meaning |
|---|---|
| kullan- | use (stem) |
| -abil- | ability ("can") |
| -ir- | aorist (general/habitual) |
| -siniz | 2pl/formal person |

Five morphemes, one word.

**Negation:** -me / -ma immediately after the stem:

- gel**me**di (he/she did not come)
- gel**eme**di (he/she could not come — gel + e (ability) + me (neg) + di (past))
- gel**ip gel-me**diğini (whether he/she came or not — complex form)

### Existential Sentences Need a Predicate (severity 1.5)

Turkish doesn't use a copula in present-tense "X is Y" predicates (the suffix does it), but **existential statements** ("there is/are X") need the word **var** ("there is/exists") or **bulunuyor** ("is located/found"):

- ❌ "Ekibinizde # mevcut ad alanı" (just a noun phrase) → ✅ "Ekibinizde # mevcut ad alanı **var**." or "Ekibinizde # mevcut ad alanı **bulunuyor**."
- ❌ "# öğe listede" → ✅ "Listede # öğe **var**." / "Listede # öğe **bulunuyor**."
- ✅ Negative: "**yok**" is the negative existential. "Hata yok." (There's no error.)

**Copula in non-existential predicates:**

- "Bu dosya açık." (This file is open. — adjectival predicate, no overt copula in present)
- "Bu dosya açık**tır**." (More formal, with -dır copula — emphatic/written register)
- "Bu dosya açık**tı**." (This file was open. — past copula -dı)

## UI Conventions

### Button Labels — Imperative

Turkish UI buttons use the **imperative form** of the verb (unlike Hungarian which uses noun-form). Choose siz-form imperative for formal UI:

| English | Wrong | Correct (siz formal) | Informal (sen) |
|---|---|---|---|
| Save | Kaydetmek için tıklayın | **Kaydet** (or **Kaydedin** formal) | Kaydet |
| Delete | Silme işlemi | **Sil** (or **Silin** formal) | Sil |
| Cancel | İptal etmek | **İptal** (noun form, idiomatic for cancel) | İptal |
| Upload | Yüklemek | **Yükle** / **Yükleyin** | Yükle |
| Download | İndirmek | **İndir** / **İndirin** | İndir |
| Edit | Düzenlemek | **Düzenle** / **Düzenleyin** | Düzenle |
| Search | Aramak | **Ara** / **Arayın** | Ara |
| Close | Kapatmak | **Kapat** / **Kapatın** | Kapat |
| Open | Açmak | **Aç** / **Açın** | Aç |
| Log in | Giriş yapmak | **Giriş yap** / **Oturum aç** | Giriş yap |
| Log out | Çıkış yapmak | **Çıkış yap** / **Oturum kapat** | Çıkış yap |
| Copy | Kopyalamak | **Kopyala** / **Kopyalayın** | Kopyala |
| Paste | Yapıştırmak | **Yapıştır** / **Yapıştırın** | Yapıştır |
| Next | Sonraki | **İleri** / **Sonraki** | İleri |
| Back | Geri | **Geri** | Geri |

**Note:** for most modern Turkish apps, the **bare 2sg imperative** (Kaydet, Sil, Tıkla) is increasingly common even in formal contexts because of UI brevity — it's read as the bare verb stem rather than informal address. The **-in/-ın/-un/-ün siz form** (Kaydedin, Silin, Tıklayın) is more polite/explicit. Both are acceptable; **be consistent**.

### Status Messages — Present Continuous Passive or "-iyor"

Turkish loading/status messages use the **present continuous** form, often in passive voice or active 3sg:

```
✅ Yükleniyor...       (Loading... — passive present continuous)
✅ Kaydediliyor...     (Saving...)
✅ İşleniyor...        (Processing...)
✅ Aranıyor...         (Searching...)
✅ Bağlanıyor...       (Connecting...)
✅ İndiriliyor...      (Downloading...)
✅ Gönderiliyor...     (Sending...)
❌ Yükleniyor (no ellipsis — looks incomplete)
❌ Yüklendi (past tense — means "loaded", not "loading")
❌ Şu an yüklenme işlemi yapılıyor (verbose nominal)
```

**Confirmation messages** (action complete) use past tense:

- ✅ "Dosya kaydedildi." (The file was saved.)
- ✅ "Mesaj gönderildi." (The message was sent.)
- ✅ "Değişiklikler kaydedildi." (Changes saved.)

### Drag-and-Drop Vocabulary

| English | Turkish |
|---|---|
| drag | **sürükle / sürükleyin** |
| drop | **bırak / bırakın** |
| release | **bırak** (not "serbest bırak" — that means "set free / release prisoner") |
| Drag and drop files here | **Dosyaları buraya sürükleyip bırakın** (or **... sürükle bırak**) |

Anti-patterns:

- ❌ Draggla → ✅ **Sürükle**
- ❌ Droppla → ✅ **Bırak**
- ❌ "Dosyaları buraya sürükle, bırak veya tıkla" (comma before veya wrong) → ✅ "Dosyaları buraya sürükle bırak veya tıkla"
- ❌ "Serbest bırak" (set free) → ✅ "Bırak" / "Bırakın" (drop)

### Error Messages — Direct Predicate

Turkish error patterns are concrete and predicative, not nominalized:

- ❌ "Error: X" (English calque)
- ❌ "Dosya kaydetme işlemi sırasında hata oluştu" (verbose nominal)
- ✅ **"Dosya bulunamadı. Lütfen dosya yolunu kontrol edin."** (direct predicate + actionable advice)
- ✅ **"Dosya kaydedilemedi."** (file could not be saved — passive ability negative)
- ✅ **"Bağlantı kurulamadı. Lütfen internet bağlantınızı kontrol edin."**
- ✅ **"Geçersiz e-posta adresi."** (Invalid email address — bare predicate, concise)

### Sentence Case for UI Labels (severity 1.5)

Turkish does NOT use English Title Case in UI labels, headings, or button text. Only the first letter of the sentence and proper nouns are capitalized.

| Wrong (Title Case) | Correct (sentence case) |
|---|---|
| Dosyalara Göz At | **Dosyalara göz at** |
| Daha Fazla Ekle | **Daha fazla ekle** |
| Yeni Klasör Oluştur | **Yeni klasör oluştur** |
| Ayarları Değiştir | **Ayarları değiştir** |
| Kullanıcı Adı | **Kullanıcı adı** |

**Proper nouns stay capitalized:**

- ✅ "Türkiye'den dosyalar"
- ✅ "İstanbul ofisi"
- ✅ "Google Drive ile senkronize et"

**Acronym capitalization stays:**

- ✅ "API ayarları"
- ✅ "URL'yi kopyala"

### Honorific Titles — AFTER Name (severity 1.0)

Turkish puts titles **after the first name**, not before like English Mr./Ms.

| Wrong (English order) | Correct (Turkish order) |
|---|---|
| Bey Ali | **Ali Bey** (Mr. Ali) |
| Hanım Ayşe | **Ayşe Hanım** (Ms./Mrs. Ayşe) |
| Bay Ahmet (less common in formal) | **Ahmet Bey** (preferred) |
| Bayan Fatma | **Fatma Hanım** (preferred over Bayan) |
| Dr. Mehmet (this order is OK as loanword) | **Dr. Mehmet Bey** (combined) |

**Sayın (esteemed)** comes BEFORE the full name+title:

- ✅ **Sayın Ali Bey**
- ✅ **Sayın Ayşe Hanım**
- ✅ **Sayın Dr. Mehmet Yıldız**

In UI greetings:

- ✅ "Merhaba {firstName} Bey," — but only if you know the recipient is male
- Better: **"Merhaba {firstName},"** — gender-neutral, no title needed
- Even better in casual UI: **"Merhaba {firstName}!"** — friendly

## Punctuation, Numbers, Dates, Currency

### Quotation Marks

- **Primary: "..."** — straight double quotes are the standard in modern Turkish UI and writing.
- Secondary (less common, more literary): «...» guillemets, or 'single quotes' for nested.
- ❌ „..." (German low-high) → ✅ "..." (straight double)
- ❌ "..." curly typographic → either "..." straight or "..." curly is fine; be consistent.

### Numbers

- **Decimal separator: comma** — 1**,**5 (one and a half)
- **Thousands separator: period** — 1**.**234**,**56 (one thousand two hundred thirty-four point fifty-six)
- This is **European-style**, same as German/Italian/Spanish.

| Wrong (English) | Correct (Turkish) |
|---|---|
| 1,234.56 | **1.234,56** |
| 1234.56 | **1.234,56** |
| 99.99 (as ninety-nine point nine nine) | **99,99** |
| 1,000,000 | **1.000.000** |

### Dates

| Format | Example | Use |
|---|---|---|
| Numeric DD.MM.YYYY | **15.01.2024** | Default for forms, tables, technical contexts |
| Long with month name | **15 Ocak 2024** | Formal writing, headers, signatures |
| With day name | **15 Ocak 2024 Pazartesi** | Letterheads, schedules |
| Short DD.MM.YY | **15.01.24** | Compact contexts |

**Turkish months** (always capitalized as proper nouns):

| # | Month | Notes |
|---|---|---|
| 1 | **Ocak** | January |
| 2 | **Şubat** | February |
| 3 | **Mart** | March |
| 4 | **Nisan** | April |
| 5 | **Mayıs** | May |
| 6 | **Haziran** | June |
| 7 | **Temmuz** | July |
| 8 | **Ağustos** | August |
| 9 | **Eylül** | September |
| 10 | **Ekim** | October |
| 11 | **Kasım** | November |
| 12 | **Aralık** | December |

**Days of the week** (always capitalized):

| Day | Turkish |
|---|---|
| Monday | **Pazartesi** |
| Tuesday | **Salı** |
| Wednesday | **Çarşamba** |
| Thursday | **Perşembe** |
| Friday | **Cuma** |
| Saturday | **Cumartesi** |
| Sunday | **Pazar** |

**Common date errors:**

- ❌ 01/15/2024 (US MM/DD/YYYY) → ✅ **15.01.2024**
- ❌ 2024-01-15 (ISO — acceptable in technical contexts only) → ✅ **15.01.2024** for UI
- ❌ January 15, 2024 (English) → ✅ **15 Ocak 2024**

### Time

- **24-hour: 14:30** (default in Turkey — standard for transit, formal, official, UI)
- **12-hour: 2:30 ÖS** (öğleden sonra = "after noon" = PM) or 2:30 ÖÖ (öğleden önce = AM) — less common in software UI
- ❌ 14.30 with period (older typographic style, no longer standard) → ✅ **14:30**
- ❌ 2:30 PM → ✅ **14:30**

Word form: "saat **14:30**'da" (at 14:30 — note apostrophe before suffix on the time numeral).

### Currency — TRY Turkish Lira (₺)

- **Symbol: ₺** (Türk lirası işareti — adopted 2012)
- **Code: TRY** (ISO 4217)
- **Format: 1.234,56 ₺** — period thousands, comma decimal, symbol AFTER amount (most common in retail)
- Alternative: **₺1.234,56** — symbol before (financial/banking contexts)
- Older format: **1.234,56 TL** (lira abbreviation)
- Whole numbers: **1.500 ₺** (no decimals if exact)

**Northern Cyprus also uses TRY** — same formatting.

| Wrong | Correct |
|---|---|
| $1,234.56 (USD shown in TR UI) | Convert to **1.234,56 ₺** (or keep $ with TR number format: **1.234,56 $**) |
| 1234.56 TL | **1.234,56 ₺** |
| 99,99 TL | **99,99 ₺** (or **99,99 TL**) |
| TRY 1234 | **1.234 ₺** |

### Comma Rules

**Comma BEFORE subordinating conjunctions:**

- ki (that): "Görüyorum **ki**, çalışıyor."
- eğer (if): "**Eğer** istersen, kaydedebilirsin."
- çünkü (because): "Çalışmıyor**,** çünkü dosya eksik."
- ne zaman (when): "Hazır olduğunda**,** bildiririm."

**NO comma before coordinating conjunctions** (ve "and", veya "or", ya da "or"):

- ❌ "Dosyaları sürükleyin, veya tıklayın" → ✅ **"Dosyaları sürükleyin veya tıklayın"**
- ❌ "Kaydet, ve kapat" → ✅ **"Kaydet ve kapat"**
- ❌ "Hızlı, ve güvenli" → ✅ **"Hızlı ve güvenli"** (in tight phrases)
- Exception: comma DOES separate items in lists. "Hızlı, güvenli ve kolay" (fast, safe **and** easy) — comma between hızlı and güvenli, no comma before ve.

**Comma BEFORE contrast conjunctions:**

- ama (but): "Çalışıyor**, ama** yavaş."
- fakat (but/however, formal): "Denedik**, fakat** başaramadık."

### Apostrophe Rules

The apostrophe in Turkish has **one main job**: separating a suffix from a proper noun, abbreviation, or numeral.

| Context | Use apostrophe? | Example |
|---|---|---|
| Proper noun + suffix | YES | Türkiye'de, Ankara'dan, Atatürk'ün |
| Brand/foreign name + suffix | YES | Apple'dan, Google'a, OneSky'ı |
| Abbreviation + suffix | YES | API'ye, USB'de, TBMM'nin |
| Numeral + suffix | YES | 2024'te, 1453'te |
| Common noun + suffix | **NO** | evde (NOT ev'de), kitapta (NOT kitap'ta) |
| Acronym read as word + suffix | usually YES | NATO'ya, UNESCO'ya |

## Terminology

### Common UI Translations

| English | Preferred Turkish | Avoid |
|---|---|---|
| File | **dosya** | dokümentasyon (means documentation), file (anglicism) |
| Folder | **klasör** | dizin (more technical, "directory") |
| Save | **kaydet** | save-lemek, kayıt etmek (slightly less idiomatic) |
| Delete | **sil** / **silmek** | deletelemek, deletlemek |
| Cancel | **iptal** | kansel, vazgeçmek (means give up — too strong for cancel) |
| Upload | **yükle** / **yüklemek** | uploadlamak, ápplódlamak |
| Download | **indir** / **indirmek** | downloadlamak, daunlódlamak |
| Settings | **ayarlar** | setting'ler, konfigürasyon (anglicism — use only in tech docs) |
| Search | **ara** / **arama** | search, srcing |
| Edit | **düzenle** / **düzenlemek** | editelmek, editlemek |
| Copy | **kopyala** / **kopyalamak** | kopilemek |
| Paste | **yapıştır** / **yapıştırmak** | peyste |
| Close | **kapat** / **kapatmak** | close |
| Open | **aç** / **açmak** | open |
| Log in | **giriş yap** / **oturum aç** | log-inlemek, loginlemek |
| Log out | **çıkış yap** / **oturum kapat** | logoutlemek |
| Click | **tıkla** / **tıklamak** | klik yap, klikle |
| User | **kullanıcı** | user, ger |
| Account | **hesap** | account |
| Password | **parola** / **şifre** | (both standard; parola more modern, şifre slightly more formal) |
| Username | **kullanıcı adı** | username |
| Email | **e-posta** | mail (acceptable colloquial), email (anglicism — discouraged in formal) |
| Link | **bağlantı** | link (acceptable in casual contexts) |
| Browser | **tarayıcı** | browser |
| Dashboard | **gösterge paneli** / **kontrol paneli** | dashboard |
| Notification | **bildirim** | notification |
| Update | **güncelle** / **güncelleme** | apdeyt, update |
| Validation | **doğrulama** | validasyon (anglicism) |
| Configuration | **yapılandırma** | konfigürasyon (anglicism) |
| Implementation | **uygulama** / **gerçekleştirme** | implementasyon (anglicism) |
| Organization | **kuruluş** / **düzenleme** (depending on meaning) | organizasyon (anglicism for org/event) |
| Namespace | **ad alanı** | namespace |
| Drag | **sürükle** | dragla |
| Drop | **bırak** | droppla |
| Send | **gönder** / **göndermek** | sendla |
| Receive | **al** / **almak** | receive |
| Sign up | **kayıt ol** / **kaydol** | signupla |
| Submit | **gönder** | submitle |
| Next | **ileri** / **sonraki** | next |
| Back | **geri** | back |
| Skip | **atla** | skipple |
| Loading | **yükleniyor** | loading |
| Done | **tamam** / **bitti** | done |

### Anti-Anglicism: Türk Dil Kurumu (TDK) Preference (severity 1.5)

Turkey has an official **Türk Dil Kurumu (TDK, Turkish Language Society)** founded by Atatürk in 1932, which advocates native Turkish over foreign borrowings. **Established native forms must be preferred** in formal UI:

| English origin | Wrong (anglicism) | Correct (Turkish) |
|---|---|---|
| computer | kompüter | **bilgisayar** ("data counter") |
| software | softvér / software | **yazılım** |
| hardware | hardware / harduer | **donanım** |
| download | downloadlamak / daunlódlamak | **indirmek** |
| upload | uploadlamak / ápplódlamak | **yüklemek** |
| validation | validasyon | **doğrulama** |
| configuration | konfigürasyon | **yapılandırma** |
| implementation | implementasyon | **uygulama** / **gerçekleştirme** |
| organization (org) | organizasyon (event sense OK) | **kuruluş** (for institution) / **düzenleme** (for arrangement) |
| organization (event) | organizasyon | (acceptable for events) |
| user | yuzer / user | **kullanıcı** |
| login (verb) | login-lemek | **giriş yapmak** / **oturum açmak** |
| logout (verb) | logout-lamak | **çıkış yapmak** / **oturum kapatmak** |
| select | selektelemek / şeklemek | **seçmek** |
| edit (verb) | editelmek | **düzenlemek** |
| delete (verb) | deletelemek | **silmek** |
| save (verb) | save-lemek | **kaydetmek** |
| click (verb) | klikle / klik yap | **tıklamak** |
| browser | bravsır | **tarayıcı** |
| dashboard | daşbord | **gösterge paneli** / **kontrol paneli** |

**Acceptable loanwords** (no native equivalent, or fully integrated):

- internet ✅
- e-posta (← email, fully Turkified)
- online ✅ (acceptable, native "çevrimiçi" also exists and is preferred in formal docs)
- wifi ✅
- mobil ✅ (Turkified)
- telefon ✅ (long-integrated French loan)
- video ✅
- film ✅
- radyo ✅

### Brand Name Rules

**Brand names** stay in their original spelling. Take suffixes via apostrophe:

| Form | Result |
|---|---|
| Google | Google, Google'da (at Google), Google'dan (from Google), Google'ı (Google as object) |
| Apple | Apple, Apple'a, Apple'dan |
| Microsoft | Microsoft, Microsoft'a, Microsoft'tan (assimilated t after voiceless final) |
| OneSky | OneSky, OneSky'ı, OneSky'a |
| GitHub | GitHub, GitHub'da, GitHub'dan |

Don't translate brand names. Don't soften their final consonants.

### Proper Noun Naturalization in UI

Use **short native forms** for country/region names in compact UI:

| Full official form | UI short form |
|---|---|
| Amerika Birleşik Devletleri | **ABD** / **Amerika** |
| Büyük Britanya ve Kuzey İrlanda Birleşik Krallığı | **Birleşik Krallık** / **İngiltere** (colloquial) |
| Avrupa Birliği | **AB** |
| Birleşmiş Milletler | **BM** |
| Türkiye Cumhuriyeti | **Türkiye** |
| Almanya Federal Cumhuriyeti | **Almanya** |

## Calque / Anti-Pattern Blocklist

### Idiom Calques

| Wrong (calque) | Correct (idiomatic) | Source |
|---|---|---|
| Mantıklı geliyor | **Mantıklı** / **Anlaşılır** / **Makul** | "makes sense" |
| Günün sonunda | **Sonuçta** / **Özünde** / **Nihayetinde** | "at the end of the day" |
| Gerçekten değil | **Aslında hayır** / **Pek değil** / **Tam olarak değil** | "not really" |
| Aynı sayfada olmak | **Anlaşmak** / **Mutabık olmak** | "be on the same page" |
| Bacağını kır! | **Bol şans!** / **Başarılar!** | "break a leg" |
| Bir parça pasta | **Çocuk oyuncağı** / **Çok kolay** | "piece of cake" |
| Bir nevi | **Bir bakıma** / **Bir anlamda** / **Adeta** | awkward calque |
| Bir kerede (when meaning "all at once") | **Aynı anda** / **Tek seferde** | "at once" |
| Çok teşekkürler için | **... için çok teşekkürler** | English thank-you word order |
| Üstüne düşmek (work-context) | **Üzerinde çalışmak** | "to work on it" |

### Tech/Marketing Calques

| Wrong (calque) | Correct (idiomatic) | Source |
|---|---|---|
| X Destekli / X Güdümlü | **X ile çalışan** / **X teknolojisi ile** / **X tabanlı** | "X-powered / X-driven" |
| AI-destekli | **Yapay zeka ile çalışan** / **YZ tabanlı** | "AI-powered" |
| Veri-Güdümlü | **Veri odaklı** / **Veri tabanlı** | "data-driven" |
| Bulut-Tabanlı | **Bulut tabanlı** (no hyphen in TR) | "cloud-based" |
| Kullanıcı-Dostu | **Kullanıcı dostu** (no hyphen) | "user-friendly" |
| downloadlamak | **indirmek** | "to download" |
| uploadlamak | **yüklemek** | "to upload" |
| organizasyon (for nonprofit) | **kuruluş** | "organization" |
| validasyon | **doğrulama** | "validation" |
| implementasyon | **uygulama** | "implementation" |
| konfigürasyon | **yapılandırma** | "configuration" |

### False Friends

| Word | Looks like English | Actually means |
|---|---|---|
| **aktüel** | "actual" | **current / topical** (Aktüel haberler = current news) — for English "actual" use **gerçek**, **fiili**, **asıl** |
| **realize etmek** | "realize" | (anglicism, weak) — for English "realize" use **fark etmek** (notice) or **gerçekleştirmek** (make real) |
| **eventually** doesn't exist in TR | — | for English "eventually" use **sonunda** / **eninde sonunda** |
| **kontrol etmek** | "control" | **to check** (not "to control"). "Control" (as in remote control) = **kumanda** or **denetim** |
| **kontrol** (in chair sense) | "controller" | (varies by domain — see context) |

### Word Order Calques

| Wrong (SVO calque) | Correct (SOV) |
|---|---|
| Kullanıcı kaydetti dosyayı. | **Kullanıcı dosyayı kaydetti.** |
| Tıklayın butona kaydetmek için. | **Kaydetmek için butona tıklayın.** |
| Sistem gönderdi bildirimi. | **Sistem bildirimi gönderdi.** |
| Lütfen seçin bir seçenek. | **Lütfen bir seçenek seçin.** |

### Per vs For Distinction (severity 1.5)

Turkish distinguishes "per X" (rate) and "for X" (target):

| English meaning | Turkish | Example |
|---|---|---|
| Rate ("per language", "per user") | **X başına** (after amount) or **her X için** | {credits} kredi/dil başına / Her dil için {credits} kredi |
| Aggregate ("for 3 languages") | **# X için** or **# X'e** | 3 dil için {credits} kredi |

- ❌ "dil başına {credits} kredi" (amount AFTER "başına" — wrong order) → ✅ **"{credits} kredi/dil başına"** (amount BEFORE) or **"Her dil için {credits} kredi"**
- ❌ "Her dil başına {credits}" (mixed) → ✅ **"Her dil için {credits} kredi"**

Turkish natural word order: **[amount] + [unit] + [başına/için]**.

## Self-Check Checklist

Run BEFORE finalizing each translation:

**Accuracy (critical):**

- [ ] **Dotted vs dotless i:** İstanbul not Istanbul; capital İ stays dotted; capital I stays dotless; toLocaleUpperCase("tr-TR") used in code
- [ ] **29-letter alphabet only:** no Q/W/X in native Turkish words; Ç Ğ İ Ö Ş Ü present where required
- [ ] **Yumuşak ge:** ğ used where required (dağ, değer, doğru); never word-initial; never replaced with plain g
- [ ] **Vowel harmony (front-back):** suffix vowels a/e match stem (back a/ı/o/u → a; front e/i/ö/ü → e)
- [ ] **Vowel harmony (rounded-unrounded):** suffix high vowels i/ı/u/ü match stem's last vowel (a → ı, e → i, o → u, ö/ü → ü, etc.)
- [ ] **Case suffix correct:** -da/-de locative ("in/at"), -e/-a dative ("to/into"), -den/-dan ablative ("from"), -i/-ı/-u/-ü accusative (DEFINITE object), -in/-ın/-un/-ün genitive, -le/-la instrumental
- [ ] **Consonant assimilation:** voiceless final p/t/k/ç/ş/s/f/h → suffix d hardens to t (kitapta, sokaktan)
- [ ] **Consonant softening:** stem-final p/t/k/ç softens before vowel suffix when applicable (kitap → kitabı, sokak → sokağa)
- [ ] **Accusative only for definite objects:** "Dosyayı kaydet" (the file) vs "Bir dosya kaydet" (a file — no -ı)
- [ ] **Singular noun after numbers:** "5 dosya" not "5 dosyalar"; both ICU branches singular
- [ ] **Possessive suffixes used:** Ayarlarınız (your settings — formal), not "Sizin ayarlar"
- [ ] **SOV word order:** verb at end of sentence
- [ ] **Question particle:** -mi/-mı/-mu/-mü as separate word with vowel harmony; person suffix on particle (gidiyor musun)
- [ ] **Apostrophe before suffix on proper nouns:** Türkiye'de, OneSky'ı, API'ye, USB'ye, 2024'te
- [ ] **Loanword suffix harmony based on Turkish pronunciation:** API [a-pe-i] → API'ye (front), USB [u-es-be] → USB'ye (front)
- [ ] **Existential statements have predicates:** "Listede 5 öğe var/bulunuyor" not "Listede 5 öğe"
- [ ] **Number format:** 1.234,56 (period thousands, comma decimal)
- [ ] **Date format:** DD.MM.YYYY (15.01.2024) or "15 Ocak 2024"
- [ ] **Time format:** 24-hour 14:30 (colon) — not 14.30 in modern UI
- [ ] **Currency:** 1.234,56 ₺ (symbol after, period thousands, comma decimal)
- [ ] **Comma rules:** NO comma before veya/ya da/ve; YES comma before ki/eğer/çünkü/ama/fakat
- [ ] **Placeholders preserved exactly** ({name}, {count})
- [ ] **No suffix on placeholders without apostrophe:** {name}'ın not {name}nın

**Naturalness:**

- [ ] **siz/sen consistency** throughout entire file — possessives AND verb forms AND imperatives all match
- [ ] **Default register is siz** (formal) unless casual app context confirmed
- [ ] **Buttons in imperative:** Kaydet / Kaydedin, Sil / Silin (siz form preferred for formal)
- [ ] **Status in -iyor present continuous:** Yükleniyor..., Kaydediliyor..., Aranıyor...
- [ ] **Confirmation in passive past:** Dosya kaydedildi, Mesaj gönderildi
- [ ] **Drag-and-drop:** sürükle, bırak (not draggla, droppla, not "serbest bırak")
- [ ] **Error messages:** direct predicate (Dosya bulunamadı), not nominal (Hata oluştu)
- [ ] **Sentence case in UI** — not Title Case (Dosyalara göz at, not Dosyalara Göz At)
- [ ] **Titles after first name:** Ali Bey (not Bey Ali), Ayşe Hanım (not Hanım Ayşe), Sayın Ali Bey
- [ ] **Native verbs preferred:** indirmek not downloadlamak, doğrulama not validasyon, yapılandırma not konfigürasyon
- [ ] **Adjective + noun order:** modifier before noun (yeni dosya, büyük klasör)
- [ ] **`aktüel` not used for "actual":** use gerçek, fiili, asıl
- [ ] **Abbreviations in UI:** ABD (not full "Amerika Birleşik Devletleri"), AB, BM
- [ ] **Compound adjective restructure:** "X ile çalışan" / "X tabanlı" not "X Destekli/Güdümlü"
- [ ] **Per vs for distinction:** "X başına" for rate (amount BEFORE), "X için" for aggregate
- [ ] **No religious assumptions:** keep UI religiously neutral (Turkey is secular constitutionally, majority Sunni Muslim, but also Alevi, Christian, Jewish, secular communities)

## Worked Examples

### Example 1 — Save button + status + confirmation

**Source:**
> Save
> Saving your changes...
> Changes saved.

**Wrong:**
> Save-lemek (anglicism + infinitive)
> Save yapılıyor... (anglicism)
> Saved. (English)

**Correct:**
> **Kaydet** (or **Kaydedin** for explicit formal — both acceptable)
> **Değişiklikleriniz kaydediliyor...** (passive present continuous, formal possessive)
> **Değişiklikler kaydedildi.** (passive past, complete sentence)

### Example 2 — Files counter with ICU

**Source:**
> {count, plural, one {# file} other {# files}}

**Correct Turkish ICU:**

```icu
{count, plural,
  one {# dosya}
  other {# dosya}
}
```

Both branches use the SINGULAR (5 dosya, not 5 dosyalar). This is correct Turkish.

### Example 3 — Drag-and-drop area

**Source:**
> Drag and drop files here, or click to browse

**Wrong:**
> Drag ve dropla dosyaları buraya, veya tıkla browse'lamak için (full anglicism)
> Dosyaları buraya sürükleyin, veya göz atmak için tıklayın (comma before veya)

**Correct:**
> **Dosyaları buraya sürükleyip bırakın veya göz atmak için tıklayın** (formal, no comma before veya)
> **Dosyaları buraya sürükle bırak veya göz atmak için tıkla** (informal)

### Example 4 — Dotted vs Dotless i (CRITICAL)

**Source:**
> Welcome to Istanbul! Login below.

**Wrong:**
> Hoş geldiniz Istanbul! Login yap. (English I — should be İ; anglicism login)
> Hosgeldiniz Istanbula! (no Ş, no apostrophe before suffix)

**Correct:**
> **Hoş geldiniz, İstanbul'a! Aşağıdan giriş yapın.** (formal)
> **Hoş geldin, İstanbul'a! Aşağıdan giriş yap.** (informal)

Note:
- "İstanbul" — capital İ keeps the dot
- "İstanbul'a" — apostrophe before dative suffix on proper noun
- "giriş yap" — native Turkish for "login"
- "Aşağıdan" — capital A, then lowercase, with -dan ablative

### Example 5 — Vowel harmony in suffixes

**Source:**
> Saved in the system / Saved in the file / Saved in your folder

**Wrong:**
> Sistemda kaydedildi (back harmony on a front stem)
> Dosyade kaydedildi (front harmony on a back stem)
> Klasörünüzda kaydedildi (back harmony after front rounded)

**Correct:**
> **Sistemde kaydedildi.** (sistem ends in front e → -de)
> **Dosyada kaydedildi.** (dosya ends in back a → -da)
> **Klasörünüzde kaydedildi.** (klasör + -ünüz (formal possessive, front rounded) + -de (front))

### Example 6 — Question particle with harmony

**Source:**
> Did you save the file? / Did you (formal) save the file?

**Wrong:**
> Dosyayı kaydettin mi (no question mark)
> Dosyayı kaydettinmi? (no space before mi)
> Dosyayı kaydettiniz mu? (wrong harmony — kaydettiniz ends in i, front → mi not mu)

**Correct:**
> **Dosyayı kaydettin mi?** (informal — sen form)
> **Dosyayı kaydettiniz mi?** (formal — siz form)

### Example 7 — Definite vs indefinite object

**Source:**
> I saved the file. / I saved a file.

**Wrong:**
> Bir dosyayı kaydettim. (definite accusative + bir = inconsistent)
> Dosya kaydettim. (when meaning THE file — missing accusative)

**Correct:**
> **Dosyayı kaydettim.** (definite — the file, with accusative -ı)
> **Bir dosya kaydettim.** (indefinite — a file, no accusative)

### Example 8 — Apostrophe on proper nouns and abbreviations

**Source:**
> From Türkiye / In API / To the URL

**Wrong:**
> Türkiyeden (no apostrophe on proper noun)
> APIde (no apostrophe on abbreviation)
> URLye (no apostrophe + maybe wrong harmony)

**Correct:**
> **Türkiye'den** (apostrophe before ablative suffix)
> **API'de** (apostrophe before locative; API pronounced [a-pe-i] → front → -de)
> **URL'ye** (apostrophe before dative; URL pronounced [u-er-le] → ends in e/le → front → -ye)

### Example 9 — SOV word order

**Source:**
> The user uploaded 5 files yesterday.

**Wrong:**
> Kullanıcı yükledi 5 dosyayı dün. (SVO calque — verb in middle)
> Dün 5 dosyalar kullanıcı tarafından yüklendi. (plural after number)

**Correct:**
> **Kullanıcı dün 5 dosya yükledi.** (SOV, singular noun after number, time adverb before object — also valid)
> **Dün kullanıcı 5 dosya yükledi.** (time adverb at start, then SOV)

### Example 10 — Number + noun (singular!) + dotted i

**Source:**
> 5 users / 25 files / 100 languages

**Wrong:**
> 5 kullanıcılar / 25 dosyalar / 100 diller (plural after number — wrong!)

**Correct:**
> **5 kullanıcı** / **25 dosya** / **100 dil** (singular after number)

### Example 11 — Placeholder + suffix + apostrophe

**Source:**
> Sent to {name}

**Wrong:**
> {name}'a gönderildi (apostrophe + suffix on placeholder — but suffix harmony unknown at translation time)
> {name}nın dosyaları (no apostrophe, harmony invented)

**Correct (label-style, preferred for placeholders):**
> **Alıcı: {name}** (label-style — no suffix needed)
> **Şu kişiye gönderildi: {name}** (suffix on known word "kişiye")

**OR if forced to attach suffix:**
> **{name}'e gönderildi** (with apostrophe, but pick the most-likely harmony for your audience or restructure)

### Example 12 — Date and currency

**Source:**
> January 15, 2024 — Total: $1,234.56

**Wrong:**
> 01/15/2024 — Toplam: 1,234.56 ₺ (US date, English number format)
> January 15, 2024 — 1.234,56 $ (English month name)

**Correct:**
> **15 Ocak 2024 — Toplam: 1.234,56 ₺** (Turkish month, period thousands, comma decimal)
> **15.01.2024 — Toplam: 1.234,56 ₺** (numeric date, same number/currency)

### Example 13 — Error message — direct predicate

**Source:**
> Error: File not found. Please check the path.

**Wrong:**
> Hata: Dosya yok. Path check et. (anglicism)
> Bir hata oluştu dosya bulunmadığı için. (verbose nominal)

**Correct:**
> **Dosya bulunamadı. Lütfen dosya yolunu kontrol edin.** (direct predicate + actionable advice, formal)

### Example 14 — Honorific titles

**Source:**
> Dear Mr. Ahmet Yıldız, welcome.

**Wrong:**
> Sevgili Bay Ahmet Yıldız, hoş geldiniz. (Bay before name = English calque)

**Correct:**
> **Sayın Ahmet Yıldız Bey, hoş geldiniz.** (formal letter style)
> **Merhaba Ahmet Bey,** (UI greeting, less formal)
> **Merhaba {firstName},** (gender-neutral UI greeting — preferred)

### Example 15 — Compound adjective restructuring

**Source:**
> AI-powered translation engine

**Wrong:**
> AI-Destekli çeviri motoru (hyphenated calque + Title Case)
> Yapay-zeka-güdümlü çeviri motoru (hyphenated)

**Correct:**
> **Yapay zeka ile çalışan çeviri motoru** (verb-based natural Turkish)
> **YZ tabanlı çeviri motoru** (abbreviation + tabanlı "based")
> **Yapay zekalı çeviri motoru** (adjective form — natural Turkish)

## When in Doubt

1. **Capital İ or I?** Look at the lowercase. If the lowercase has a dot (i), the capital has a dot (İ). If the lowercase has no dot (ı), the capital has no dot (I). They never cross. İstanbul, NOT Istanbul.
2. **Vowel harmony unclear?** Look at the LAST vowel of the stem.
   - Back (a, ı, o, u) → a/ı/u suffixes (-da, -ım, -un)
   - Front unrounded (e, i) → e/i suffixes (-de, -im)
   - Front rounded (ö, ü) → e/ü suffixes (-de, -üm)
3. **Case unclear?** Identify the meaning:
   - "in" / "at" (location) → -de/-da (with consonant assimilation → -te/-ta after voiceless)
   - "into" / "to" (motion) → -e/-a
   - "from" / "out of" → -den/-dan (→ -ten/-tan after voiceless)
   - "of" / possessor → -in/-ın/-un/-ün
   - "the X" as definite object → -i/-ı/-u/-ü (only if definite)
   - "with" → -le/-la or `ile`
4. **Number + noun?** ALWAYS singular (5 dosya, 100 dil, üç kullanıcı).
5. **Placeholder + suffix?** Restructure to put the suffix on a known word. Use label-style "Alıcı: {name}" when possible.
6. **Brand or abbreviation + suffix?** Use apostrophe: Google'da, API'ye, USB'de.
7. **Verb from English?** Almost always wrong. Find the native Turkish verb: indirmek, yüklemek, kaydetmek, silmek, tıklamak.
8. **Adjective from English?** Many Anglicisms are tolerated as adjectives but native forms preferred in formal: kullanıcı dostu (user-friendly), yapay zeka tabanlı (AI-based), bulut tabanlı (cloud-based).
9. **Question?** Use the -mi/-mı/-mu/-mü particle, separated by space, with vowel harmony.
10. **Title case?** Never. Always sentence case in Turkish UI. Only first letter of sentence and proper nouns capitalized.
11. **24-hour or 12-hour time?** 24-hour (14:30) is standard in Turkey. Use 12-hour with ÖÖ/ÖS only if the source explicitly requires.
12. **Currency conversion?** TRY (₺) is the Turkish Lira; format as 1.234,56 ₺ (period thousands, comma decimal, symbol after).
13. **Religious or political content?** Stay neutral. Turkey is constitutionally secular; do not assume Islamic norms in default UI, do not insert religious references not in source.
14. **"Per X" vs "for X"?** "X başına" for per-unit rate (amount BEFORE başına). "X için" for total aggregate. Don't confuse — they have different meanings.
15. **Comma before "veya"/"ve"?** No. Only before subordinating conjunctions (ki, eğer, çünkü, ama, fakat).

Turkish's agglutinative structure means most translation errors are at the **suffix level** (wrong case, broken harmony, missing apostrophe on proper noun, wrong dot status on i/İ vs ı/I) rather than at the word-choice level. When the translation feels off, check (1) dotted/dotless i, (2) vowel harmony, (3) case selection, (4) apostrophe before suffixes on proper nouns/abbreviations — in that order.
