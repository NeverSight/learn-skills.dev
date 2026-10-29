---
name: cinematic-prompting
description: Rewrite naive image and video prompts with precise cinematography vocabulary. Triggers on "cinematic prompt", "film language", "camera movement", "make it cinematic", "shot from above", "enhance this image prompt", "enhance this video prompt", "cinematography vocabulary", "rewrite with camera terms".
license: MIT
metadata:
  author: genfeedai
  version: 1.0.0
---

# Cinematic Prompting

You rewrite image and video prompts so they use named cinematography techniques instead of vague spatial or mood language. Precision of vocabulary multiplies generation quality because the underlying models are language models.

Translate naive words into the closest lexicon term below. Never invent camera jargon that is not in this lexicon. Preserve the user's subject, characters, and named references verbatim.

## Rewriting rules

1. Identify the subject and any named characters. Copy them unchanged.
2. Replace naive spatial or mood phrases with the closest technique name.
3. Prefer one accurate term over a pile of synonyms.
4. Return only the enhanced prompt unless the user asked for feedback or a draft plan.

## Draft-resolution testing

Validate a prompt with 2–3 cheap waves at **low resolution on the full-quality model**. Do not switch to a "mini" or distilled variant for drafts — those models have different priors and will not predict the final look. After the wave looks right, render at final resolution.

## Corrective feedback grammar

When a generation misses, do not say "I don't like it." Structure the next request as:

- **Problem** — what is wrong in the current frame
- **Goal** — what the frame should communicate
- **Correction** — the lexicon terms and subject details that will get there

## Camera movement

| Technique | Definition | When to use |
| --- | --- | --- |
| dolly in | The camera physically travels toward the subject on a track or slider, keeping focal length fixed. | Intimacy or pressure should grow without changing perspective distortion. |
| dolly out | The camera physically retreats from the subject while the lens stays the same. | Reveal context around a character or drain intensity from a beat. |
| push-in | A short, deliberate advance toward the subject that lands on a tighter frame. | Underline a realization, threat, or emotional turn. |
| pull-out | A short retreat that widens the frame and reintroduces surrounding space. | After a close beat when the scene needs air or scale. |
| trucking left | The camera travels laterally left, parallel to the action, without rotating. | Keep pace with a walk-and-talk or a moving vehicle. |
| trucking right | The camera travels laterally right, parallel to the action, without rotating. | Follow a crossing subject while holding a consistent profile. |
| pedestal up | The camera rises vertically on a column or crane while remaining level. | Lift from a grounded detail to a standing figure or room. |
| pedestal down | The camera lowers vertically while staying level. | Drop from a face to hands, objects, or a floor-level clue. |
| pan | The camera rotates horizontally from a fixed position. | Survey a space or follow a subject that does not require a traveling camera. |
| tilt | The camera rotates vertically from a fixed position. | Reveal height, a body from shoes to face, or a building from street to sky. |
| whip pan | A pan so fast that frames smear into a directional blur. | Energetic connector between two related beats in the same location. |
| arc shot | The camera travels a curved path around the subject, usually at a constant radius. | Inspect a character or object from multiple sides without cutting. |
| orbit | A continuous 360-degree or near-360 path around the subject. | Hero reveals, product turnarounds, and hypnotic character moments. |
| crane shot | The camera rides a boom through a large vertical and horizontal path. | Open or close a scene with geography, crowd scale, or a descending arrival. |
| jib sweep | A shorter boom move that scoops or arcs across a compact set. | Aerial grace when a full crane is too large. |
| steadicam follow | A stabilized operator walk that floats behind, beside, or ahead of the subject. | Long takes through architecture or crowds without handheld shake. |
| tracking shot | The camera travels with the subject, matching speed and direction. | Motion itself is the story and cutting would break the line. |
| handheld | The camera is operator-held, admitting micro-shake and human weight shifts. | Urgency, documentary texture, or a character whose world is unstable. |
| locked-off | The camera is fixed on a tripod or mount with no pan, tilt, or travel. | Graphic compositions, comedy deadpan, and surveillance-like observation. |
| roll | The camera rotates on its lens axis so the horizon banks. | Disorientation, aircraft, or a world coming unmoored. |
| FPV drone | A first-person racing-drone path that weaves through tight architecture at speed. | The audience should feel like a projectile through a space. |
| snorricam | A body-mounted camera that keeps the subject locked while the world slides behind them. | Dissociation, panic, or a character sealed inside their own head. |
| speed ramp | Playback speed changes mid-shot, usually from real time into slow or back out. | Isolate a gesture, impact, or glance without cutting. |
| slow motion | Action is captured or played back well below real-time speed. | Ritualize violence, beauty, or a walk that should feel mythic. |
| time-lapse | Frames are captured at long intervals so hours compress into seconds. | Weather, crowds, construction, or the passage of a day over a place. |
| dolly zoom | The camera dollies while the lens zooms the opposite way, warping perspective around a still subject. | Vertigo, dread, or a sudden rewrite of how the character sees the world. |

## Framing and composition

| Technique | Definition | When to use |
| --- | --- | --- |
| extreme close-up | A frame that fills with one feature — an eye, a mouth, a ring, a trigger. | A tiny detail carries the scene’s meaning. |
| close-up | Head and shoulders, or an object large enough to read emotion or texture. | Dialogue beats, identity, and reaction. |
| medium close-up | Chest-up framing that keeps face and a hint of gesture. | Default interview and conversation size. |
| medium shot | Waist-up framing that balances body language with environment. | Blocking, props in hand, and two-person exchanges. |
| cowboy shot | Mid-thigh up, historically so a holster stays in frame. | Armed or swaggering figures who need stance as well as face. |
| full shot | The entire body from head to toe with a modest amount of ground and headroom. | Costume, gait, or full-body silhouette matters. |
| wide shot | The subject is small enough that architecture and geography share the frame. | Locate people in a place before tightening. |
| extreme wide shot | A landscape-scale frame where figures are tiny or absent. | Establishing image that sells climate, city, or isolation. |
| ultra wide | An extremely short focal length that stretches space and exaggerates near objects. | Immersive interiors, skate, or a slightly unhinged point of view. |
| two shot | Two people share the frame at roughly equal weight. | Relationships, arguments, and paired presence. |
| over-the-shoulder | The camera looks past one person’s shoulder and cheek onto the facing subject. | Conversation coverage that keeps both parties connected. |
| point of view | The frame is what a character sees, including blink, height, and obstruction. | Lock the audience into one person’s perception. |
| dutch angle | The horizon is canted so verticals lean. | Unease, intoxication, or a world whose rules have slipped. |
| high-angle shot | The camera looks down at the subject from above eye level. | Shrink a character, survey a table, or read a floor plan of action. |
| low-angle shot | The camera looks up at the subject from below eye level. | Enlarge power, monumentality, or menace. |
| worm's-eye | An extreme low angle from ground level, often with sky or ceiling dominating. | The world should tower over the viewer. |
| overhead shot | A top-down frame perpendicular to the floor, sometimes called bird’s-eye. | Maps of movement, ritual layouts, and graphic tableaus. |
| central framing | The subject sits on the optical center, often with symmetry around them. | Portraits of control, ceremony, and ordered tableau. |
| rule of thirds | Key masses sit on the intersections of a three-by-three grid. | Default for landscapes and talking heads that should feel natural. |
| leading lines | Architecture, roads, or light beams steer the eye to the subject. | A location can point at the character without extra camera work. |
| negative space | A large empty field around a small subject. | Loneliness, waiting, or a title-safe graphic beat. |
| frame within a frame | Doorways, windows, mirrors, or screens crop a second picture inside the shot. | Trap a character, spy on them, or stack two story worlds. |
| profile shot | The subject is seen from the side, silhouetting nose, brow, and posture. | Confrontations, cameos against windows, and non-humanoid identity sheets. |
| three-quarter view | The face or body is turned about 45 degrees from the camera. | Most dimensional default for portraits and product heroes. |
| insert shot | A brief close view of a relevant object or action detail. | Plant a clue, a text, a button press, or a ticking clock. |
| cutaway | A shot of something other than the main action, used to bridge or comment. | Hide an edit, show reaction in the room, or add documentary evidence. |

## Lighting

| Technique | Definition | When to use |
| --- | --- | --- |
| hard light | A small, sharp source that throws crisp shadows and specular hits. | Noon sun, interrogation, and graphic contrast. |
| soft light | A large, diffused source that wraps the subject and melts shadow edges. | Beauty, overcast days, and gentle interiors. |
| high-key | A bright, low-contrast scheme with open shadows and pale backgrounds. | Comedy, retail, wellness, and optimistic advertising. |
| low-key | A dark scheme that withholds fill so most of the frame falls toward black. | Mystery, night, and anything described as moody or dramatic. |
| Rembrandt lighting | Key light at 45 degrees that leaves a triangle of light on the shadowed cheek. | Classical portraits that need both shape and dignity. |
| butterfly lighting | A key placed on axis above the lens, dropping a butterfly-shaped shadow under the nose. | Glamour portraits and beauty campaigns. |
| split lighting | The key hits one half of the face; the other half falls into shadow. | Duality, moral conflict, and severe character studies. |
| rim light | A backlight that traces the subject’s edge with a thin highlight. | Separate dark hair or clothing from a dark background. |
| backlight | The primary source sits behind the subject, toward the camera. | Halos, rain sparkle, and subjects defined by silhouette plus glow. |
| silhouette | The subject is underexposed against a brighter background so only the outline reads. | Identity-as-shape, sunsets, and anonymous figures. |
| practicals | Lamps, neon, screens, and other sources that exist in the set and are photographed on. | Motivate night interiors and keep light grounded in the world. |
| motivated lighting | Off-camera units that pretend to be a visible source such as a window or sign. | The audience should believe the light belongs to the location. |
| golden hour | The low, warm sun shortly after dawn or before dusk. | Romance, travel, and any prompt that mentions sunset or sunrise. |
| blue hour | The cool, even skylight just before sunrise or after sunset. | City lights mixing with residual daylight and quiet melancholy. |
| overcast | Cloud-diffused daylight that acts like a giant softbox. | Even skin, documentary honesty, and outdoor product shots. |
| spotlight | A focused cone that isolates one subject from a darker surround. | Stages, interrogations, and single-object hero moments. |
| chiaroscuro | Painting-like contrast of a few lit planes against deep shadow. | When “dramatic” should mean sculpted light, not just darkness. |
| bounce fill | Light redirected from a wall, card, or ceiling to lift shadows without a second hard source. | Keep a key dramatic while still reading eyes and wardrobe. |
| haze | Airborne scatter that makes beams visible and softens distant contrast. | Shafts through windows, clubs, forests, and dream distance. |
| halation | Highlights bloom and bleed, as if the emulsion cannot contain them. | Analog warmth, night neon, and memory. |
| neon practicals | Colored tube or LED signage that both keys the scene and paints the set. | Nightlife, rain streets, and cyber or retro-future looks. |
| window light | A single large opening that keys the subject from one side. | Interiors that should feel observed rather than lit. |
| top light | A source directly above, pooling on shoulders and burying the eyes. | Menace, factory floors, and interrogation rooms. |
| underlighting | A source from below the face, inverting the usual daylight pattern. | Campfire stories, horror, and unnatural presence. |
| volumetric light | Visible beams carved through haze, dust, or smoke. | When the air itself should feel thick and directional. |

## Editing and transitions

| Technique | Definition | When to use |
| --- | --- | --- |
| match cut | Two shots join because shape, motion, or idea continues across the cut. | Rhyme images and collapse time without a dissolve. |
| jump cut | A cut within the same setup that skips time and makes the subject pop. | Restlessness, montage of process, or a narrator talking to camera. |
| smash cut | An abrupt join between two shots of maximally different energy or volume. | Jolt from quiet to loud or from dream to alarm. |
| crash cut | A violent, almost colliding join used as a rhythmic punch. | Action and music video when the beat itself is the cut. |
| cross dissolve | One image fades in as the other fades out, overlapping in time. | Memory, elapsed time, or a gentle change of place. |
| fade to black | The image decays to black, ending a chapter. | Act breaks and deaths, never between ordinary coverage. |
| fade from black | The image is born out of black. | Open a new chapter or a morning after. |
| whip-pan transition | A whip pan’s blur is used as the join to another whip pan. | Stitch two locations that share momentum. |
| L-cut | Picture cuts away while the outgoing audio continues. | Dialogue or score can pull the viewer into the next image. |
| J-cut | Incoming audio arrives before the picture of the next shot. | Pre-lap a new space, a voice, or a threat. |
| montage | A designed sequence of short shots that compresses process or argument. | Training, travel, and any “time passed” that needs rhythm. |
| parallel action | Two or more lines of action intercut so they feel simultaneous. | Chases, countdowns, and destinies that are about to collide. |
| cross cut | Alternating shots from two scenes to build comparison or suspense. | The audience should hold two places in mind at once. |
| freeze frame | Motion stops on a still that is held as a graphic. | Endings, evidence, or a joke that needs a button. |
| iris | A circular mask closes or opens on a point of interest. | Period pastiche and to single out a clue. |
| wipe | A traveling edge replaces one shot with another. | Serial adventure, chaptering, and graphic play. |
| cut on action | The join happens during a continuous gesture so the motion hides the cut. | Default invisible way to change size or angle. |
| axial cut | A cut along the lens axis, jumping closer or farther without changing angle. | Emphasis that still feels like the same point of view. |
| smash cut to silence | A loud or busy shot cuts to a still, quiet image. | After an explosion, a scream, or a party to make absence felt. |
| match on motion | The direction and speed of movement continue across a cut into a new space. | Teleport a character while keeping kinetic logic. |

## Stylistic effects

| Technique | Definition | When to use |
| --- | --- | --- |
| bullet time | Time appears frozen or slowed while the camera still travels around the subject. | Iconic action punctuation, not as a default look. |
| double exposure | Two images occupy the same frame, stacked by opacity or blend. | Memory, haunting, and interior states. |
| tilt-shift | Selective focus and often a miniature-like perspective. | Make a city look like a model or isolate a thin plane of sharpness. |
| thermal | A false-color heat map instead of reflected light. | Night search, science fiction sensors, and animal vision. |
| anamorphic flare | Horizontal streaks from a bright source, characteristic of anamorphic glass. | Widescreen cinema texture and night headlights. |
| film grain | Visible silver or digital grain structure over the image. | Age a picture, hide digital smoothness, or match analog references. |
| teal-and-orange grade | Shadows push cyan-teal while skin and practicals hold orange. | Contemporary blockbuster color contrast, not a default for every scene. |
| bleach bypass | A desaturated, silver-heavy look with crushed blacks and retained density. | War, crime, and moral exhaustion. |
| lens flare | Internal glass reflections from a source in or near the frame. | When the sun or headlights should invade the lens, sparingly. |
| bokeh | Out-of-focus highlights rendered as discs or polygons. | Romanticize night cities and isolate a subject from sparkle. |
| shallow depth of field | Only a thin plane is sharp; foreground and background fall off quickly. | Portraits, product heroes, and any “blurry background” request. |
| deep focus | Near and far planes are simultaneously sharp. | Blocking in depth is the composition, from foreground prop to distant door. |
| rack focus | Focus travels from one plane to another during the shot. | Hand attention from a face to a clue, or from a gun to a reaction. |
| glitch | Digital tearing, channel offset, and compression wounds used as style. | Hacked feeds, broken memory, and electronic unease. |
| vignette | The corners darken or desaturate, pooling attention in the center. | Age a lens, hide edges, or intensify a portrait. |
| motion blur | Moving masses streak according to shutter angle. | Sell speed; avoid it when the brief wants razor-frozen action. |
| light leak | Streaks and veils of unexposed-looking color invading the frame. | Analog accident, summer memory, and super-8 pastiche. |
| infrared | Foliage goes pale, skies go dark, and skin tones shift into an otherworldly register. | Dream forests, surveillance, and uncanny daylight. |
| chromatic aberration | Color channels misregister at high-contrast edges. | Cheap optics, VR, or a world slightly out of calibration. |
| split diopter | A half-lens that holds two different focus distances sharp in one frame. | Two-plane tension without racking focus. |
| day for night | Daylight is underexposed and cooled to stand in for night. | True night capture is impractical; keep skies dark and highlights restrained. |

## Naive to technical examples

| Naive | Technical |
| --- | --- |
| shot from above looking down, moody | high-angle shot, low-key |
| camera moves toward him slowly | push-in on him |
| close on her face in the dark | close-up of her face, low-key |
| sunset light on Anna | golden hour on Anna |
| spin around the car | arc shot around the car |
| blurry background | shallow depth of field |
| cut quickly between shots | jump cut |
| make it look dramatic | chiaroscuro |
| like a dream | haze |
| two people talking, wide | two shot, wide shot, two people talking |

## Output

Return the rewritten prompt as a single block of natural language that a generation model can ingest. Do not explain the lexicon unless asked.
