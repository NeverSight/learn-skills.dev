---
name: broll
description: The creator's own B-roll (their clips, screen recordings, photos) turned into a library any agent can search in one grep - scanned once with ffprobe and ffmpeg (length, orientation, date, GPS, one contact sheet per clip), tagged by cheap Haiku sub-agents (title, description, mood, keywords, creator on screen), then placed full screen in a short by short-editing. Use for /broll setup, /broll add, /broll use, /broll search, or when the user says "my B-roll", "add these clips", "put my B-roll on this short", "find me a sunset shot".
argument-hint: "[setup|add|use|search|reject] [folder|files|slug|words]"
allowed-tools: Bash(ffmpeg *) Bash(ffprobe *) Bash(node -e *) Bash(grep *) Bash(mkdir *) Bash(cp *)
---

# B-roll

B-roll = the images shown over the creator's voice: their own footage (street, desk at night, sunset, gym, phone in hand), screen recordings, photos. The library is read ONCE, then every edit finds "me at my desk at night" with one grep, without opening a single video.

```text
<their clips folder>/            the files, never moved or edited
video-agent/broll/
├── library.json                 one entry per clip: file, length, orientation, date, GPS, tags, used in
├── library.md                   the same, one line per clip, newest first: what agents grep
├── sheets/<id>.jpg              6 frames of the clip in a 3x2 grid (what the taggers and you look at)
└── tags/batch-NN.json           what each Haiku tagger wrote
```

Talk to the creator in their language, short messages, no jargon ("ta bibliothèque de B-roll", never "JSON"). Run every command from the project folder (the one holding `video-agent/`). Preflight: `ffmpeg -version && node -v`; missing: `/studio-setup tools`.

## /broll setup

1. **The folder.** Ask in one line where their clips are. Their own folder stays where it is (an external drive works). Clips spread everywhere: `mkdir -p video-agent/broll/clips` and copy them in.
2. **Photos of them** (to know which clips show them): their face, well lit, as `video-agent/broll/me.jpg`, plus 1 to 3 more as `me-2.jpg`, `me-3.jpg` (a close-up, another cap or glasses, a frame of a clip where they surely are): with one photo alone, Haiku misses most of their clips. No photo: `is_self` stays false.
3. **The scan** (about 1 s per clip). Only new files are read, so the same command adds clips later:

```bash
node -e '
const fs=require("fs"),path=require("path"),{execFileSync:x}=require("child_process");
const B="video-agent/broll",L=B+"/library.json",ext=/\.(mp4|mov|m4v|mkv|webm|jpe?g|png)$/i;
fs.mkdirSync(B+"/sheets",{recursive:true});
const lib=fs.existsSync(L)?JSON.parse(fs.readFileSync(L,"utf8")):[],known=new Set(lib.map(c=>c.file));
const walk=d=>fs.readdirSync(d,{withFileTypes:true}).flatMap(e=>e.name.startsWith(".")?[]:e.isDirectory()?walk(path.join(d,e.name)):ext.test(e.name)?[path.resolve(d,e.name)]:[]);
let n=0;
for(const f of process.argv.slice(1).flatMap(a=>fs.statSync(a).isDirectory()?walk(a):[path.resolve(a)])){
  if(known.has(f))continue;
  try{
    const p=JSON.parse(x("ffprobe",["-v","error","-print_format","json","-show_format","-show_streams",f]).toString());
    const v=p.streams.find(s=>s.codec_type==="video")||{},t=p.format.tags||{},photo=/\.(jpe?g|png)$/i.test(f);
    const turn=Math.abs(+(v.tags?.rotate||(v.side_data_list||[]).find(s=>s.rotation!=null)?.rotation||0))%180===90;
    const w=turn?v.height:v.width,h=turn?v.width:v.height,dur=photo?0:+p.format.duration||0;
    let id=path.basename(f).replace(/\.[^.]+$/,"").toLowerCase().replace(/[^a-z0-9]+/g,"-").replace(/^-|-$/g,"")||"clip";
    while(lib.some(c=>c.id===id))id+="-2";
    const sheet=B+"/sheets/"+id+".jpg";
    x("ffmpeg",["-v","error","-y","-i",f,"-vf",photo?"scale=720:-2":"fps=6/"+Math.max(dur,1)+",scale=360:-2,tile=3x2","-frames:v","1",sheet]);
    const g=(t["com.apple.quicktime.location.ISO6709"]||t.location||"").match(/([+-][\d.]+)([+-][\d.]+)/);
    lib.push({id,file:f,sheet,duration:Math.round(dur*10)/10,width:w,height:h,orientation:w<h?"portrait":w>h?"landscape":"square",
      date:t["com.apple.quicktime.creationdate"]||t.creation_time||null,lat:g?+g[1]:null,lon:g?+g[2]:null,place:null,tags:null,used:[],status:"active"});
    if(++n%20===0)fs.writeFileSync(L,JSON.stringify(lib,null,1));
  }catch(e){console.log("skipped "+f+": "+e.message.split("\n")[0])}
}
fs.writeFileSync(L,JSON.stringify(lib,null,1));
console.log(n+" new, "+lib.length+" in the library, "+lib.filter(c=>!c.tags&&c.status==="active").length+" to tag");
' "<their clips folder>"
```

   Clips with GPS: name the places, one request per distinct spot (rounded to 2 decimals), one per second, then set `place` ("Lisbon, Portugal") in `library.json`: `curl -s "https://nominatim.openstreetmap.org/reverse?format=json&zoom=10&lat=<lat>&lon=<lon>" -H "User-Agent: video-agent-skills"`. No GPS = no place, never a guess.
4. **The tagging, by Haiku** (cheap and fast). Batches of 5 untagged clips; one sub-agent per batch, all launched in ONE message so they run together, 10 at a time (Claude Code: the Agent tool with `model: "haiku"`). No sub-agents in this tool: tag the batches yourself, same rules. Prompt of each tagger, filled in:

```text
You tag B-roll clips for a video creator's library. Read each contact sheet below (6 frames of one clip, left to right then top to bottom, spread evenly over the clip) and video-agent/broll/me.jpg, me-2.jpg, me-3.jpg (the creator; skip the missing ones). Then Write ONE file, video-agent/broll/tags/batch-<NN>.json, then answer "done". Nothing else.
Clips: <id> (<duration> s) video-agent/broll/sheets/<id>.jpg ; ... (5 of them)
The file is one JSON object keyed by clip id, every id present, this shape:
{"<id>": {"title": "4 to 8 words", "description": "3 plain sentences: what is on screen, what moves, the light",
 "setting": "desk|bedroom|kitchen|street|beach|car|gym|cafe|office|city|nature|screen|studio|...",
 "subjects": [], "actions": [], "emotions": [{"name": "serenity", "intensity": 0.6}],
 "mood": "calm|joyful|melancholic|tense|energetic|contemplative|neutral",
 "time_of_day": "dawn|day|golden hour|sunset|evening|night|unknown",
 "shot_type": "close-up|medium|wide|screen|aerial", "keywords": ["8 to 15 words someone would search"],
 "has_people": true, "is_self": false, "quality_flags": ["blur|shaky|dark|overexposed|watermark"], "best_start": 0}}
Rules: only what is visible, never a place, brand or name you cannot read on screen. Everything in English. emotions 0 to 2, only when the image clearly carries one. is_self: compare every face with the creator photos (face shape, nose, eyebrows, hair, glasses); same person = true, even with another cap, glasses or clothes, in a mirror selfie or small in the frame; an arm's-length selfie is usually them, look twice; hands or back only = false. best_start = the second where the clean part starts (frame k of 6 is at about k/6 of the length), 0 when clean from the start. Valid JSON, no comment.
```

   Then merge every batch and rebuild `library.md` (also after any change by hand to `library.json`):

```bash
node -e '
const fs=require("fs"),B="video-agent/broll",L=B+"/library.json",lib=JSON.parse(fs.readFileSync(L,"utf8"));
fs.mkdirSync(B+"/tags",{recursive:true});
const T=Object.assign({},...fs.readdirSync(B+"/tags").filter(f=>f.endsWith(".json")).map(f=>JSON.parse(fs.readFileSync(B+"/tags/"+f,"utf8"))));
for(const c of lib)if(T[c.id])c.tags={...(c.tags||{}),...T[c.id]};
fs.writeFileSync(L,JSON.stringify(lib,null,1));
const k=c=>c.tags||{},row=c=>[c.id,c.duration+"s",c.orientation,(c.date||"").slice(0,10),c.place||"",k(c).title||"(untagged)",k(c).mood||"",k(c).time_of_day||"",
  [...(k(c).keywords||[]),...(k(c).emotions||[]).map(e=>e.name),k(c).setting||""].join(" "),k(c).is_self?"me":"",(k(c).quality_flags||[]).join(" "),c.used.length?"used "+c.used.length:""].join(" | ");
const on=lib.filter(c=>c.status==="active").sort((a,b)=>(b.date||"").localeCompare(a.date||""));
fs.writeFileSync(B+"/library.md","# B-roll library\n\nid | length | orientation | date | place | title | mood | time | keywords | me | flags | used\n"+on.map(row).join("\n")+"\n");
console.log(on.length+" clips, "+on.filter(c=>!c.tags).length+" untagged, "+on.filter(c=>k(c).is_self).length+" with the creator");
'
```

   A batch file that is not valid JSON or misses an id: run its tagger again. A big library (300+ clips): tag 100 now, say so, the rest in the background or the first time a video needs B-roll.
5. **Check, with the creator**: 3 searches from their real topics (below), Read the sheets of the hits, show what you found ("pour « bureau la nuit » j'ai ces 3 plans"). A wrong tag: fix it in `library.json` and rebuild. A clip they never want: reject it.
6. One line to them: "ta bibliothèque est prête : N clips. Dis « ajoute ces vidéos » pour en mettre d'autres, « mets mes B-roll » sur un short."

## /broll add

Their files or a folder: copy them into their clips folder (or scan them where they are), then steps 3 and 4 on the new ones only (the scan skips known files, the taggers get only `tags: null`). Say what came in: "12 clips ajoutés : 4 à Lisbonne en août, 8 au bureau".

## /broll search

```bash
grep -i -E "sunset|dusk|golden" video-agent/broll/library.md
grep -i "desk" video-agent/broll/library.md | grep -i "night" | grep "| me |"
```

English words of what the image should show; synonyms joined with `|`, a second filter with a second `grep`. Rank the hits yourself: matches the line, then unused, then recent, then the right orientation (portrait for a short; a landscape clip is cropped to fill). Then Read the sheets of the 3 best: the tags help you find, only your eyes validate.

## /broll use

The short in progress (`video-agent/edits/<slug>/` or named): its B-roll from its words.

1. Read the transcript (`public/<slug>.json` in the studio, source ms). Mark the lines that show a moment or a place ("I moved to Lisbon"), a feeling ("I was exhausted"), the creator doing something ("I code at night"), a thing they use. Numbers, ideas and proof stay as callouts.
2. One search per line; Read the sheets. A clip goes in only if the image fits the sentence (a calm line over a calm image), the clean part from `best_start` lasts the whole stretch, and nothing is wrong on screen (blur, a stranger's face, a private screen). At most one B-roll every 8 to 15 s, 2 to 5 s each, 5 s of the creator between two.
3. Copy each picked clip into the studio: `mkdir -p video-agent/studio/public/broll && cp "<file>" video-agent/studio/public/broll/<id>.<ext>`.
4. Add them to `public/<slug>.edit.json`: `"broll": [{ "src": "broll/<id>.mp4", "atMs": <startMs of the first word>, "toMs": <endMs of the last word>, "startSec": <best_start> }]`. The composition needs the `broll` layer of `short-editing` (its `references/remotion-short.md`, section 2): a studio made before it lacks it, add it once.
5. Render a still in the middle of each stretch, Read it, then the full render (`short-editing` steps 6 to 8).
6. The creator keeps the short: add the slug to each clip's `used` in `library.json` and rebuild `library.md`, so the next shorts prefer fresh clips.

No good hit = the library lacks that image: keep the creator on screen or a callout, never a random clip.

## /broll reject

`"status": "rejected"` on that clip in `library.json` (`"active"` brings it back), then rebuild `library.md`: it never comes up again. The file itself is never deleted: it is the creator's footage.
