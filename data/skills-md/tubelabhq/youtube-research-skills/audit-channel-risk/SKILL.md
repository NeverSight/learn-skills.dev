---
name: audit-channel-risk
description: Use when the user wants to know whether a YouTube channel is at risk of being demonetized or terminated, with a score for each, the proof and what to fix first. Requires the TubeLab MCP.
license: MIT
metadata:
  author: tubelab
  version: "1.0"
  requires: tubelab-mcp
---

# Audit Channel Risk

## Overview

YouTube's [channel monetization policies](https://support.google.com/youtube/answer/1311392?hl=en) decide which channels keep monetization, and they change often. Read the page on every run and check the channel against it, never against memory.

## Workflow

1. Read the policy page and list the sections that set a rule for what videos contain. Skip those about the review, the creator's behaviour or another page. If it will not open, ask for a paste.
2. Read each channel for free: its top and newest videos and About text.
3. Check the channel against each section, across titles, descriptions, thumbnails and three to five transcripts. View the thumbnails of the videos you cite. For the section on repetitive content, a video counts when:
   - its script could swap names and places with an earlier video's and still work, or repeats its entries. A shared intro or outro does not count.
   - its title has the shape used on over half the videos. Count shapes, not words.
4. Note what already shows real people behind the channel: a real presenter on camera, and an About text naming who makes the videos.
5. Run both searches below per channel, seeded with it, without the quality filter. Lost AdSense means `monetization.adsense` is false with a `monetizationChangedAt` date. False alone only means not monetized.
6. Rate every hit but the channel itself from 0 to 100: titles first, then thumbnails for title matches, then scripts if still unsure. A close one, 60 or more, shares the title formula and subject, and the thumbnail style. A terminated channel's thumbnails load from `https://cdn.tubelab.net/vi/<id>.jpeg`.
7. Score two risks from 0 to 100, where higher is riskier. Take the highest signal, never a sum. Under 30 is low 🟢, 30 to 59 is medium 🟡, and 60 or more is high 🔴.
   - Termination: 15 points per close similar channel terminated, up to 100.
   - Demonetization: the higher of two signals.
     - Similar channels: 15 points per close one terminated or demonetized, up to 100.
     - Guidelines: its worst section. A section scores 0 when at most two videos, or under a tenth, run into it, 60 when more do, and 100 when over half do. Drop it one level, 100 to 60 or 60 to 30, when the newest ten videos run into it at under half the older ones' rate.
8. With several channels, compare them. A shared template, presenter or description block, or uploads minutes apart, link channels as one network.

Terminated, then lost AdSense:

```json
{ "relatedChannelId": ["<channelId>"], "terminated": true, "publishedAtFrom": "year", "size": 40 }
{ "relatedChannelId": ["<channelId>"], "monetizationChanged": true, "monetizationAdsense": false, "publishedAtFrom": "year", "size": 40 }
```

## Output Format

One HTML page, from this template. Change nothing in the style block.

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Channel Risk Audit: {channel}</title>
<style>
:root{--bg:#fff;--fg:#1c1c1c;--mut:#666;--line:#e3e3e3;--low:#0c8a4d;--med:#c26a00;--high:#d42a2a}
@media(prefers-color-scheme:dark){:root{--bg:#0f0f0f;--fg:#f1f1f1;--mut:#9a9a9a;--line:#2b2b2b;--low:#3ddc97;--med:#ffa400;--high:#ff4e42}}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--fg);font:16px/1.5 system-ui,sans-serif}
main{max-width:920px;margin:auto;padding:32px 16px 72px}
a{color:inherit}
h1{font-size:24px;margin:0}
h2{font-size:19px;margin:44px 0 6px}
h3{font-size:13px;margin:16px 0 0;color:var(--mut);text-transform:uppercase;letter-spacing:.06em}
.mut{color:var(--mut)}
.center{text-align:center}
.low{--c:var(--low)}.med{--c:var(--med)}.high{--c:var(--high)}
.gauges{display:flex;justify-content:center;gap:40px;flex-wrap:wrap;margin:40px 0 24px;text-align:center}
.gauge{position:relative;width:200px;font-weight:600}
.gauge svg{display:block;width:132px;margin:0 auto 8px;transform:rotate(-90deg)}
.gauge circle{fill:none;stroke:var(--line);stroke-width:8}
.gauge .arc{stroke:var(--c);fill:color-mix(in srgb,var(--c) 12%,transparent)}
.gauge b{position:absolute;top:0;left:0;width:100%;line-height:132px;font-size:44px;color:var(--c)}
.legend{display:flex;justify-content:center;gap:20px;flex-wrap:wrap;font-size:13px}
.legend i,.row i{flex:none;display:inline-block;width:10px;height:10px;border-radius:50%;background:var(--c)}
.big{font-size:19px;max-width:660px;margin:24px auto 8px}
.cols{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:0 44px}
.row{border-bottom:1px solid var(--line)}
div.row,.row>summary{display:flex;align-items:center;gap:12px;padding:13px 0}
.row>summary{cursor:pointer;list-style:none}
.row>summary::-webkit-details-marker{display:none}
.row>summary::after{content:"+";color:var(--mut);width:12px;text-align:center}
.row[open]>summary::after{content:"\2212"}
.row span{flex:1}
.row b{color:var(--c)}
.row small{display:block;font-size:13px;color:var(--mut)}
.proof{padding:0 24px 18px 22px}
.proof p{margin:6px 0}
.vids{display:flex;gap:14px;flex-wrap:wrap;margin:10px 0}
.vids a{width:200px;font-size:13px;line-height:1.35;text-decoration:none}
.vids img{display:block;width:100%;aspect-ratio:16/9;object-fit:cover;border-radius:8px;margin-bottom:6px;background:var(--line)}
blockquote{margin:10px 0;padding-left:12px;border-left:3px solid var(--line);color:var(--mut)}
ol{padding-left:22px}
li{margin:12px 0}
table{border-collapse:collapse;width:100%;margin-top:24px}
td,th{text-align:left;padding:10px 12px 10px 0;border-bottom:1px solid var(--line)}
</style>
</head>
<body>
<main>
{With several channels, one page: first a table of channel, both scores and biggest risk, then one line on what links the channels (a shared template, presenter, description block or upload times), then everything below once per channel, riskiest first.}

<h1>Channel Risk Audit: <a href="{url}">{channel}</a></h1>
<p class="mut">{run date} · checked against <a href="{policy page url}">YouTube's channel monetization policies</a></p>

<div class="gauges">
  <div class="gauge {low, med or high}"><svg viewBox="0 0 120 120"><circle cx="60" cy="60" r="54"/><circle class="arc" cx="60" cy="60" r="54" pathLength="100" stroke-dasharray="{n} 100"/></svg><b>{n}</b>Demonetization risk</div>
  <div class="gauge {band}"><svg viewBox="0 0 120 120"><circle cx="60" cy="60" r="54"/><circle class="arc" cx="60" cy="60" r="54" pathLength="100" stroke-dasharray="{n} 100"/></svg><b>{n}</b>Termination risk</div>
</div>
<div class="legend"><span class="low"><i></i> 0–29 low</span><span class="med"><i></i> 30–59 medium</span><span class="high"><i></i> 60–100 high</span></div>
<p class="big center">{biggest risk, one sentence with numbers}</p>
<p class="mut center">Higher is riskier. The highest signal sets each score. A low score means no signal was found, not that the channel is safe.</p>

<h2>Signals</h2>
<div class="cols">
  <div>
    <h3>Demonetization</h3>
    <div class="row {band}"><i></i><span>Similar channels terminated or demonetized<small>{n} close of {n} checked</small></span><b>{n}</b></div>
    <div class="row {band}"><i></i><span>Guidelines<small>{n} of {n} sections failed {a section fails when it scores above 0}</small></span><b>{n}</b></div>
  </div>
  <div>
    <h3>Termination</h3>
    <div class="row {band}"><i></i><span>Similar channels terminated<small>{n} of the {n} close ones</small></span><b>{n}</b></div>
  </div>
</div>

<h2>Guidelines check</h2>
{One block per section checked, failed ones first.}
<details class="row {band}">
  <summary><i></i><span>{section name as the page words it}</span><b>{n}</b></summary>
  <div class="proof">
    <p>{what was found, one or two sentences, then how many of the newest ten videos still do it against the older ones, and whether that lowered the score}</p>
    {The next three only for a failed section.}
    <div class="vids">
      <a href="{video url}"><img src="{thumbnail: the 320px mqdefault.jpg, or the TubeLab one for a terminated channel}" alt="">{title} · {views, ratio, date}</a> {up to three videos}
    </div>
    <blockquote>{the policy line it runs into, quoted from the page}</blockquote>
    <p><strong>Fix:</strong> {one sentence per thing to change}</p>
  </div>
</details>

<h2>What happened to similar channels</h2>
{One block per close one, closest first, up to ten. The band is high for terminated, med for lost AdSense. If none is close, one line saying so and naming the nearest.}
<details class="row {band}">
  <summary><i></i><span><a href="{url}">{channel}</a> · {terminated, last upload {date} | lost AdSense {date}}</span><span class="mut" style="flex:none">closeness {n}</span></summary>
  <div class="proof">
    <p>{what matched: the title formula, the thumbnail style or the script structure}</p>
    <div class="vids">
      <a href="{video url}"><img src="{thumbnail}" alt="">{title}</a> {one or two of its videos that match}
    </div>
  </div>
</details>
<p class="mut">{Only if a close one is not counted: which one and why, in one line.}</p>

<h2>Actions to reduce risk</h2>
{One action per fix in a failed section first, biggest first. Then one action for what step 4 found missing: a real presenter on camera, in a video presenting the channel and how its videos are made, an About text naming who makes them, or both. Never an action the channel already does. Word each action as one plain thing to try, clear without its reason, like "Try new title formulas" or "Add a real presenter on camera". Up to four.}
<ol>
  <li><strong>{Action}</strong><br><span class="mut">{why, one sentence}</span></li>
</ol>
</main>
</body>
</html>
```

- File: save it as `channel-risk-{handle}.html` and open it, or make it an artifact.
- Chat: reply with only the two scores, the biggest risk and the file.
- Language: plain words and short sentences. Say "similar channels" and "terminated".
- Proof: every claim has its videos or channels under it.
- Links: link every video and channel you cite, from IDs in the data.

## Common Pitfalls

- Do not say why a similar channel was terminated. The data does not show why.
- Do not rate closeness by topic alone.
- Do not count a later clone of the channel's own videos. Other channels in the same format count.
- Do not flag AI use or upload pace alone.
- Do not score the channel's own AdSense status. Off can mean it was never monetized.
- A score is not a probability, and a low one does not mean safe.
- Never suggest hiding from detection. Every action changes the videos or shows who makes them.
