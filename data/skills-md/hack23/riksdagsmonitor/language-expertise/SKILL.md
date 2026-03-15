---
name: language-expertise
description: Comprehensive linguistic and cultural expertise for all 14 languages supported by Riksdagsmonitor (EN, SV, DA, NO, FI, DE, FR, ES, NL, AR, HE, JA, KO, ZH)
license: Apache-2.0
---

# Language Expertise Skill

## Purpose

Comprehensive linguistic and cultural expertise for ensuring accurate, culturally appropriate, and engaging content across all 14 language versions of Riksdagsmonitor.

## Supported Languages

| Code | Language | Script | Direction | Native Speakers | Target Audience |
|------|----------|--------|-----------|-----------------|-----------------|
| **en** | English | Latin | LTR | 1.5B | International, default |
| **sv** | Swedish | Latin | LTR | 10M | Primary (Swedish citizens) |
| **da** | Danish | Latin | LTR | 6M | Nordic region |
| **no** | Norwegian | Latin | LTR | 5M | Nordic region |
| **fi** | Finnish | Latin | LTR | 5M | Nordic region |
| **de** | German | Latin | LTR | 130M | European, business |
| **fr** | French | Latin | LTR | 280M | European, diplomatic |
| **es** | Spanish | Latin | LTR | 550M | International, Latin America |
| **nl** | Dutch | Latin | LTR | 25M | Benelux region |
| **ar** | Arabic | Arabic | **RTL** | 420M | Middle East, North Africa |
| **he** | Hebrew | Hebrew | **RTL** | 9M | Israel, Jewish diaspora |
| **ja** | Japanese | Kanji/Kana | LTR | 125M | Japan, Asia |
| **ko** | Korean | Hangul | LTR | 80M | Korea, Asia |
| **zh** | Chinese | Hanzi | LTR | 1.3B | China, Asia |

## Core Principles

### 1. 🌍 Linguistic Accuracy
- **Native-Level Quality**: Professional translation, not machine translation
- **Domain Expertise**: Political/parliamentary terminology
- **Consistency**: Glossary of terms across all languages
- **Grammar Perfection**: No errors in grammar, spelling, punctuation

### 2. 🎭 Cultural Appropriateness
- **Cultural Sensitivity**: Respect local customs, values, taboos
- **Political Neutrality**: Avoid culturally biased framing
- **Localization**: Adapt examples, metaphors, idioms
- **Visual Elements**: Cultural considerations for colors, symbols

### 3. 📐 Technical Correctness
- **Character Encoding**: UTF-8 support for all scripts
- **RTL Layout**: Proper right-to-left rendering for Arabic, Hebrew
- **Typography**: Appropriate fonts for each script
- **Formatting**: Date, number, currency formats per locale

## Language-Specific Guidelines

### 🇬🇧 English (en) - Default/International

**Target Audience**: International users, journalists, researchers, diplomats

**Style Guidelines**:
- **Variety**: International English (prefer -ize over -ise, but consistent)
- **Tone**: Professional, authoritative, neutral
- **Complexity**: Accessible to non-native speakers (avoid idioms)
- **Structure**: Clear, concise sentences (15-20 words average)

**Political Terminology**:
```yaml
Riksdag: "Swedish Parliament" (explain in parentheses first use)
Ledamot: "Member of Parliament (MP)"
Utskott: "Parliamentary Committee"
Omröstning: "Parliamentary Vote"
```

**Date/Number Formats**:
- Dates: YYYY-MM-DD (ISO 8601) or "11 February 2026"
- Numbers: 1,000.00 (comma thousand separator, period decimal)
- Currency: SEK 1,000 or kr 1,000

### 🇸🇪 Swedish (sv) - Primary Language

**Target Audience**: Swedish citizens, primary stakeholder group

**Style Guidelines**:
- **Formality**: Du-form (informal) for general content, Ni-form (formal) for official documents
- **Compound Words**: Swedish compound word rules (sammansatta ord)
- **Gender**: Gender-neutral language where possible
- **Acronyms**: Explain Swedish political acronyms (S, M, SD, V, MP, C, L, KD)

**Political Terminology** (Use Swedish native terms):
```yaml
Riksdag: Riksdag (no translation)
Ledamot: Ledamot / Riksdagsledamot
Utskott: Utskott (e.g. Finansutskottet)
Omröstning: Votering / Omröstning
Regeringen: Regeringen (Government)
```

**Date/Number Formats**:
- Dates: 2026-02-11 or "11 februari 2026"
- Numbers: 1 000,00 (space thousand separator, comma decimal)
- Currency: 1 000 kr or 1 000 SEK

**Common Phrases**:
- Welcome: "Välkommen till Riksdagsmonitor"
- About: "Om Riksdagsmonitor"
- Contact: "Kontakta oss"

### 🇩🇰 Danish (da) - Nordic Region

**Target Audience**: Danish citizens, Nordic cooperation stakeholders

**Style Guidelines**:
- **Similarities**: Very similar to Norwegian, some mutual intelligibility with Swedish
- **Unique Features**: Stød (glottal stop), unique pronunciation
- **Compound Words**: Similar to Swedish, German
- **Formality**: Du-form standard for web content

**Political Terminology**:
```yaml
Riksdag: "Den svenske rigsdag" / "Sveriges riksdag"
Ledamot: "Medlem af rigsdagen"
Utskott: "Udvalg"
Omröstning: "Afstemning"
```

**Date/Number Formats**:
- Dates: 11. februar 2026 or 11-02-2026
- Numbers: 1.000,00 (period thousand, comma decimal)
- Currency: 1.000 kr (DKK)

### 🇳🇴 Norwegian (no) - Nordic Region

**Target Audience**: Norwegian citizens, Nordic cooperation

**Style Guidelines**:
- **Varieties**: Bokmål (used here) vs Nynorsk
- **Similarities**: Close to Danish written, distinct pronunciation
- **Compound Words**: German/Swedish-style compounding
- **Formality**: Du-form for web content

**Political Terminology**:
```yaml
Riksdag: "Det svenske Stortinget" / "Sveriges riksdag"
Ledamot: "Stortingsrepresentant" (Norwegian) / "Riksdagsmedlem" (Swedish)
Utskott: "Komité"
Omröstning: "Avstemning"
```

**Date/Number Formats**:
- Dates: 11. februar 2026
- Numbers: 1 000,00 (space thousand, comma decimal)
- Currency: 1 000 kr (NOK)

### 🇫🇮 Finnish (fi) - Nordic Region

**Target Audience**: Finnish citizens, Nordic cooperation

**Style Guidelines**:
- **Language Family**: Uralic (not Indo-European like others)
- **Cases**: 15 grammatical cases, complex morphology
- **Compound Words**: Extensive compounding
- **Formality**: Sinä (informal) for web, Te (formal) for official

**Political Terminology**:
```yaml
Riksdag: "Ruotsin valtiopäivät" / "Riksdag"
Ledamot: "Kansanedustaja" (Finnish) / "Riksdagsledamot" (Swedish)
Utskott: "Valiokunta"
Omröstning: "Äänestys"
```

**Date/Number Formats**:
- Dates: 11. helmikuuta 2026 or 11.2.2026
- Numbers: 1 000,00 (space thousand, comma decimal)
- Currency: 1 000 € (EUR)

### 🇩🇪 German (de) - European/Business

**Target Audience**: German-speaking Europe, business stakeholders

**Style Guidelines**:
- **Formality**: Sie-form (formal) for business content
- **Capitalization**: All nouns capitalized
- **Compound Words**: Extensive, longest in European languages
- **Precision**: German values precision, detail, thoroughness

**Political Terminology**:
```yaml
Riksdag: "Schwedischer Reichstag" / "Riksdag"
Ledamot: "Abgeordneter des Riksdags"
Utskott: "Ausschuss"
Omröstning: "Abstimmung"
Parlament: "Parlament"
```

**Date/Number Formats**:
- Dates: 11. Februar 2026 or 11.02.2026
- Numbers: 1.000,00 (period thousand, comma decimal)
- Currency: 1.000 € or 1.000 EUR

**Common Phrases**:
- Welcome: "Willkommen bei Riksdagsmonitor"
- About: "Über Riksdagsmonitor"
- Contact: "Kontakt"

### 🇫🇷 French (fr) - European/Diplomatic

**Target Audience**: French-speaking Europe, international organizations, diplomats

**Style Guidelines**:
- **Formality**: Vous-form (formal) for web content
- **Gender Agreement**: Adjectives must agree with noun gender
- **Accents**: Proper use of accents (é, è, ê, ç, etc.)
- **Elegance**: French values eloquence, avoiding anglicisms

**Political Terminology**:
```yaml
Riksdag: "Le Parlement suédois" / "Riksdag"
Ledamot: "Député du Riksdag"
Utskott: "Commission"
Omröstning: "Vote" / "Scrutin"
Gouvernement: "Gouvernement"
```

**Date/Number Formats**:
- Dates: 11 février 2026 or 11/02/2026
- Numbers: 1 000,00 (space thousand, comma decimal)
- Currency: 1 000 € or 1 000 EUR

**Common Phrases**:
- Welcome: "Bienvenue sur Riksdagsmonitor"
- About: "À propos de Riksdagsmonitor"
- Contact: "Nous contacter"

### 🇪🇸 Spanish (es) - International/Latin America

**Target Audience**: Spanish-speaking world (500M+), Latin America, Spain

**Style Guidelines**:
- **Variety**: International Spanish (neutral, avoid regional slang)
- **Formality**: Usted-form for professional content
- **Gender**: Use inclusive language (ciudadanos y ciudadanas → ciudadanía)
- **Punctuation**: Inverted question/exclamation marks (¿¡)

**Political Terminology**:
```yaml
Riksdag: "El Parlamento sueco" / "Riksdag"
Ledamot: "Diputado del Riksdag"
Utskott: "Comisión"
Omröstning: "Votación"
Gobierno: "Gobierno"
```

**Date/Number Formats**:
- Dates: 11 de febrero de 2026 or 11/02/2026
- Numbers: 1.000,00 (period thousand, comma decimal)
- Currency: 1.000 € or 1.000 EUR

**Common Phrases**:
- Welcome: "Bienvenido a Riksdagsmonitor"
- About: "Acerca de Riksdagsmonitor"
- Contact: "Contáctenos"

### 🇳🇱 Dutch (nl) - Benelux Region

**Target Audience**: Netherlands, Belgium (Flanders), Benelux business

**Style Guidelines**:
- **Formality**: U-form (formal) for business, je-form (informal) acceptable for web
- **Compound Words**: Like German, extensive compounding
- **Spelling**: Post-1990s spelling reforms
- **Directness**: Dutch culture values directness, clarity

**Political Terminology**:
```yaml
Riksdag: "Het Zweedse Parlement" / "Riksdag"
Ledamot: "Lid van de Riksdag"
Utskott: "Commissie"
Omröstning: "Stemming"
Regering: "Regering"
```

**Date/Number Formats**:
- Dates: 11 februari 2026 or 11-02-2026
- Numbers: 1.000,00 (period thousand, comma decimal)
- Currency: € 1.000 or EUR 1.000

### 🇸🇦 Arabic (ar) - Middle East/North Africa **[RTL]**

**Target Audience**: Arabic-speaking world (420M), Middle East, North Africa

**Style Guidelines**:
- **Script**: Arabic script (cursive, connected letters)
- **Direction**: **Right-to-left (RTL)** layout
- **Variety**: Modern Standard Arabic (MSA) for formal content
- **Formality**: Formal register for political content
- **Numerals**: Use Eastern Arabic numerals (٠١٢٣٤٥٦٧٨٩) or Western (0-9)

**Political Terminology**:
```yaml
Riksdag: "البرلمان السويدي" (al-Barlamān al-Suwaydī)
Ledamot: "عضو البرلمان" (ʿuḍw al-Barlamān)
Utskott: "لجنة" (lajnah)
Omröstning: "تصويت" (taṣwīt)
Government: "حكومة" (ḥukūmah)
```

**Date/Number Formats**:
- Dates: ١١ فبراير ٢٠٢٦ or 2026-02-11
- Numbers: ١٬٠٠٠٫٠٠ or 1,000.00 (depending on region)
- Currency: ١٬٠٠٠ ريال or 1,000 SAR

**RTL Considerations**:
```css
[dir="rtl"] {
  direction: rtl;
  text-align: right;
}

/* Mirror directional icons */
[dir="rtl"] .icon-arrow-right {
  transform: scaleX(-1);
}
```

### 🇮🇱 Hebrew (he) - Israel/Jewish Diaspora **[RTL]**

**Target Audience**: Israel, Jewish diaspora, Middle East

**Style Guidelines**:
- **Script**: Hebrew alphabet (אבגד)
- **Direction**: **Right-to-left (RTL)** layout
- **Vowels**: Usually omitted in modern Hebrew (נִקּוּד optional)
- **Formality**: Formal register for official content
- **Loanwords**: Many English loanwords in tech, politics

**Political Terminology**:
```yaml
Riksdag: "הפרלמנט השוודי" (ha-Parlament ha-Shvedi)
Ledamot: "חבר פרלמנט" (khaver Parlament)
Utskott: "ועדה" (va'adah)
Omröstning: "הצבעה" (hatsba'ah)
Government: "ממשלה" (memshalah)
```

**Date/Number Formats**:
- Dates: 11 בפברואר 2026 or 11.02.2026
- Numbers: 1,000.00 (comma thousand, period decimal)
- Currency: ₪1,000 or 1,000 ILS

**RTL Considerations**: Same as Arabic (mirroring, text-align: right)

### 🇯🇵 Japanese (ja) - Japan/Asia

**Target Audience**: Japan, Japanese business community, Asia

**Style Guidelines**:
- **Scripts**: Mix of Kanji (漢字), Hiragana (ひらがな), Katakana (カタカナ)
- **Honorifics**: Polite forms (です/ます) for web content
- **Formality**: Respectful language (敬語 keigo) for official contexts
- **Spacing**: No spaces between words, punctuation differs

**Political Terminology**:
```yaml
Riksdag: "スウェーデン議会" (Suwēden Gikai) / リクスダーグ (Rikusudāgu)
Ledamot: "国会議員" (Kokkai giin)
Utskott: "委員会" (Iinkai)
Omröstning: "投票" (Tōhyō)
Government: "政府" (Seifu)
```

**Date/Number Formats**:
- Dates: 2026年2月11日 (2026-nen 2-gatsu 11-nichi)
- Numbers: 1,000.00 (comma thousand, period decimal)
- Currency: ¥1,000 or 1,000円

**Common Phrases**:
- Welcome: "リクスダーグスモニターへようこそ" (Rikusudāgusumonitā e yōkoso)
- About: "リクスダーグスモニターについて" (Rikusudāgusumonitā ni tsuite)

### 🇰🇷 Korean (ko) - Korea/Asia

**Target Audience**: South Korea, Korean diaspora, Asia

**Style Guidelines**:
- **Script**: Hangul (한글), some Hanja (漢字) for formal terms
- **Honorifics**: Polite forms (요 yo-form, 습니다 sumnida-form)
- **Formality**: Respectful language for official content
- **Spacing**: Spaces between words (unlike Japanese)

**Political Terminology**:
```yaml
Riksdag: "스웨덴 의회" (Seuweden uihoe) / 릭스다그 (Rikseudag)
Ledamot: "국회의원" (Gukhoe uiwon)
Utskott: "위원회" (Wiwonhoe)
Omröstning: "투표" (Tupyo)
Government: "정부" (Jeongbu)
```

**Date/Number Formats**:
- Dates: 2026년 2월 11일 (2026-nyeon 2-wol 11-il)
- Numbers: 1,000.00 (comma thousand, period decimal)
- Currency: ₩1,000 or 1,000원

**Common Phrases**:
- Welcome: "릭스다그스모니터에 오신 것을 환영합니다" (Rikseudag-seumonitoeo osin geoseul hwanyeonghamnida)
- About: "릭스다그스모니터에 대해" (Rikseudag-seumonitoeo daehae)

### 🇨🇳 Chinese (zh) - China/Asia

**Target Audience**: China, Chinese diaspora, Asia (1.3B speakers)

**Style Guidelines**:
- **Variant**: Simplified Chinese (简体中文) for mainland China
- **Script**: Hanzi characters (汉字)
- **Tone**: Formal, respectful for official content
- **Translation Strategy**: Meaning-based, not word-for-word

**Political Terminology**:
```yaml
Riksdag: "瑞典议会" (Ruìdiǎn yìhuì) / 瑞典国会 (Ruìdiǎn guóhuì)
Ledamot: "议员" (Yìyuán)
Utskott: "委员会" (Wěiyuánhuì)
Omröstning: "投票" (Tóupiào)
Government: "政府" (Zhèngfǔ)
```

**Date/Number Formats**:
- Dates: 2026年2月11日 (2026 nián 2 yuè 11 rì)
- Numbers: 1,000.00 (comma thousand, period decimal)
- Currency: ¥1,000 or 1,000元

**Common Phrases**:
- Welcome: "欢迎访问瑞典议会监督平台" (Huānyíng fǎngwèn Ruìdiǎn yìhuì jiāndū píngtái)
- About: "关于我们" (Guānyú wǒmen)

## Translation Workflow

### 1. Terminology Glossary
```yaml
# Maintain consistent translations across all languages
Riksdag:
  en: Swedish Parliament
  sv: Riksdag
  de: Schwedischer Reichstag
  fr: Parlement suédois
  es: Parlamento sueco
  ar: البرلمان السويدي
  he: הפרלמנט השוודי
  ja: スウェーデン議会
  ko: 스웨덴 의회
  zh: 瑞典议会
```

### 2. Quality Assurance
- **Native Speaker Review**: All translations reviewed by native speakers
- **Back-Translation**: Translate back to English to verify accuracy
- **Consistency Check**: Use CAT tools (Trados, MemoQ) for term consistency
- **Cultural Review**: Local cultural expert reviews for appropriateness

### 3. Technical Validation
```bash
# Character encoding validation
file -bi index_*.html
# Should show: text/html; charset=utf-8

# HTML lang attribute validation
grep '<html lang=' index_*.html
# Should match: lang="en", lang="sv", lang="ar" dir="rtl", etc.

# RTL direction validation (Arabic, Hebrew)
grep 'dir="rtl"' index_ar.html index_he.html
# Should find: <html lang="ar" dir="rtl">
```

## Cultural Considerations

### Color Symbolism
| Color | Western | Middle East | Asia | Notes |
|-------|---------|-------------|------|-------|
| Red | Danger, alert | Luck, celebration (China) | Danger, celebration | Use cautiously |
| Green | Go, success | Islam, prosperity | Nature, growth | Generally safe |
| Blue | Trust, calm | Protection (Turkey) | Peace, immortality | Universally safe |
| Yellow | Caution | Prosperity, royalty | Sacred (Buddhism) | Context-dependent |
| White | Purity | Mourning (Middle East) | Mourning (Asia) | Avoid for somber topics |

### Political Sensitivities
- **China (zh)**: Avoid Taiwan, Tibet, Xinjiang political references
- **Arabic (ar)**: Neutral on Middle East conflicts, avoid Israel references in some contexts
- **Hebrew (he)**: Neutral on Palestinian conflict
- **All**: Strict political neutrality, no partisan language

## Accessibility (Multilingual)

### Screen Reader Support
```html
<!-- Language declaration for screen readers -->
<html lang="sv">

<!-- Language changes within page -->
<p>The Swedish Parliament, called <span lang="sv">Riksdag</span>, has 349 members.</p>

<!-- RTL languages -->
<html lang="ar" dir="rtl">
```

### Font Selection
```css
/* Language-specific font stacks */
:lang(en), :lang(sv), :lang(da), :lang(no), :lang(fi), :lang(de), :lang(fr), :lang(es), :lang(nl) {
  font-family: 'Inter', 'Helvetica Neue', Arial, sans-serif;
}

:lang(ar) {
  font-family: 'Noto Sans Arabic', 'Arial', sans-serif;
}

:lang(he) {
  font-family: 'Noto Sans Hebrew', 'Arial', sans-serif;
}

:lang(ja) {
  font-family: 'Noto Sans JP', 'Yu Gothic', 'Meiryo', sans-serif;
}

:lang(ko) {
  font-family: 'Noto Sans KR', 'Malgun Gothic', 'Apple SD Gothic Neo', sans-serif;
}

:lang(zh) {
  font-family: 'Noto Sans SC', 'Microsoft YaHei', 'PingFang SC', sans-serif;
}
```

## SEO (Multilingual)

### Hreflang Tags
```html
<link rel="alternate" hreflang="en" href="https://riksdagsmonitor.com/index.html">
<link rel="alternate" hreflang="sv" href="https://riksdagsmonitor.com/index_sv.html">
<link rel="alternate" hreflang="da" href="https://riksdagsmonitor.com/index_da.html">
<link rel="alternate" hreflang="no" href="https://riksdagsmonitor.com/index_no.html">
<link rel="alternate" hreflang="fi" href="https://riksdagsmonitor.com/index_fi.html">
<link rel="alternate" hreflang="de" href="https://riksdagsmonitor.com/index_de.html">
<link rel="alternate" hreflang="fr" href="https://riksdagsmonitor.com/index_fr.html">
<link rel="alternate" hreflang="es" href="https://riksdagsmonitor.com/index_es.html">
<link rel="alternate" hreflang="nl" href="https://riksdagsmonitor.com/index_nl.html">
<link rel="alternate" hreflang="ar" href="https://riksdagsmonitor.com/index_ar.html">
<link rel="alternate" hreflang="he" href="https://riksdagsmonitor.com/index_he.html">
<link rel="alternate" hreflang="ja" href="https://riksdagsmonitor.com/index_ja.html">
<link rel="alternate" hreflang="ko" href="https://riksdagsmonitor.com/index_ko.html">
<link rel="alternate" hreflang="zh" href="https://riksdagsmonitor.com/index_zh.html">
<link rel="alternate" hreflang="x-default" href="https://riksdagsmonitor.com/index.html">
```

## Remember

- 🌍 **14 Languages, 14 Cultures**: Each language requires cultural adaptation, not just translation
- 📐 **RTL Support**: Arabic and Hebrew require complete layout mirroring
- 🎯 **Terminology Consistency**: Maintain glossary for all political terms
- ♿ **Accessibility**: Proper lang attributes, font support for all scripts
- 📊 **Quality Assurance**: Native speaker review, back-translation, consistency checks
- 🔒 **Political Neutrality**: No partisan language, sensitive to cultural contexts
- 🎨 **Visual Localization**: Colors, images, symbols culturally appropriate

---

**Last Updated**: 2026-02-11  
**Maintained by**: Hack23 AB

---

## Political Intelligence Journalism Style (OSINT/INTOP-Driven)

### Formal Register Requirements

All political news articles use **formal register** across all languages. This is mandatory for political intelligence journalism.

**Pronouns (Second Person "You"):**
- 🇸🇪 Swedish: **"ni"** (not "du")
- 🇩🇪 German: **"Sie"** (not "du")
- 🇫🇷 French: **"vous"** (not "tu")
- 🇪🇸 Spanish: **"usted"** (not "tú")
- 🇳🇱 Dutch: **"u"** (not "je/jij")
- 🇩🇰 Danish: **"De"** (not "du")
- 🇳🇴 Norwegian: **"De"** (not "du")
- 🇫🇮 Finnish: **"Te"** (not "sinä")

**Note**: Most political articles use third-person perspective and avoid direct address, but when necessary, always use formal register.

### Political Intelligence Style Adaptation

**English (Master Style)**:
- Crisp, analytical prose
- Active voice preferred
- Short sentences (15-20 words average)
- Avoiding jargon unless necessary
- Data-driven assertions
- Understated wit acceptable

**Nordic Languages (SV, DA, NO, FI)**:
- Slightly longer sentences acceptable (compound sentences common)
- More formal tone than English
- Direct translation of wit may not work - adapt or omit
- Compound words common (especially Swedish/German) - maintain

**Germanic Languages (DE, NL)**:
- Longer, more complex sentences acceptable
- More structured paragraph organization
- Technical precision valued
- Compound nouns frequent - maintain accuracy

**Romance Languages (FR, ES)**:
- Elegant, flowing sentences
- Subjunctive mood for nuance
- More elaborate style than English
- Formal constructions preferred

**CJK Languages (JA, KO, ZH)**:
- Formal political register (敬語 in Japanese, 높임말 in Korean)
- Chinese: Maintain simplified characters (简体中文) not traditional
- Japanese: Use formal written style (です・ます体)
- Korean: Use formal endings (-습니다, -ㅂ니다)

**RTL Languages (AR, HE)**:
- Formal Modern Standard Arabic (not colloquial)
- Hebrew: Formal register with full vowel marking optional
- Maintain right-to-left flow in all elements

### Punctuation and Typography

**Quotation Marks**:
- 🇬🇧 English: "double quotes"
- 🇸🇪 Swedish: "dubbla citattecken" or »guillemets»
- 🇩🇪 German: „German quotes" or »Guillemets«
- 🇫🇷 French: « guillemets français »
- 🇪🇸 Spanish: «comillas españolas» or "comillas inglesas"
- 🇯🇵 Japanese: 「brackets」or『double brackets』
- 🇨🇳 Chinese: "中文引号" or 「书名号」
- 🇰🇷 Korean: "따옴표"
- 🇸🇦 Arabic: «علامات تنصيص»
- 🇮🇱 Hebrew: "מרכאות"

**Em Dashes and Hyphens**:
- English: Use em dash — sparingly
- German: Use Gedankenstrich – with spaces
- French: Use tiret long — with spaces
- Nordic: Use tankstreck – with spaces

**Ellipsis**:
- English: ... (three dots, no spaces)
- French: … (with non-breaking spaces: word…word)
- German: … (three dots or single ellipsis character)

### Real-World Style Examples

**Evening Analysis Opening (English)**:
> "Sweden's Riksdag enters its spring recess with mixed legislative accomplishments. The Tidö government has passed key reforms on immigration and energy policy, but falters on housing and healthcare. Coalition tensions simmer beneath parliamentary decorum."

**Evening Analysis Opening (German)**:
> "Schwedens Riksdag geht in die Frühjahrspause mit gemischten gesetzgeberischen Erfolgen. Die Tidö-Regierung hat wichtige Reformen in den Bereichen Einwanderung und Energiepolitik verabschiedet, scheitert jedoch bei Wohnungsbau und Gesundheitswesen. Koalitionsspannungen brodeln unter dem parlamentarischen Anstand."

**Evening Analysis Opening (French)**:
> "Le Riksdag suédois entre en pause de printemps avec des réalisations législatives mitigées. Le gouvernement Tidö a adopté des réformes clés sur l'immigration et la politique énergétique, mais échoue sur le logement et la santé. Les tensions au sein de la coalition couvent sous le décorum parlementaire."

### Tone and Voice Guidelines

**Analytical, Not Advocacy**:
- ✅ "The opposition criticized the proposal"
- ❌ "The opposition rightly pointed out flaws"

**Data-Driven**:
- ✅ "Support dropped 3 percentage points"
- ❌ "Support plummeted dramatically"

**Contextual Nuance**:
- ✅ "The vote revealed coalition fractures"
- ❌ "The vote showed the coalition is falling apart"

**Cultural Sensitivity**:
- Avoid idioms that don't translate (e.g., "kicked the can down the road")
- Be aware of cultural connotations (colors, numbers, symbols)
- Adapt metaphors to target culture

### Quality Checklist

For each translated article, verify:
- [ ] Formal register maintained throughout
- [ ] Political terminology consistent with swedish-political-system skill
- [ ] Punctuation matches target language conventions
- [ ] Quotation marks correct for language
- [ ] No machine translation artifacts
- [ ] Natural flow in target language
- [ ] Cultural references adapted or explained
- [ ] Political intelligence tone preserved (analytical, crisp, data-driven)

---

**Data Source**: Analysis of 81 translated news articles (Feb 2026)  
**Style Guide**: OSINT/INTOP political intelligence editorial standards (adapted for 14 languages)  
**Last Updated**: 2026-02-15
