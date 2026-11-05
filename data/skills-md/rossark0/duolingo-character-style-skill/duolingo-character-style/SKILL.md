---
name: duolingo-character-style
description: Draws people and characters in Duolingo's flat illustration style, using rules and proportions measured from the vector drawings in Duolingo's own brand guide. Covers the three rounded shapes, tombstone head and torso, thick capsule arms with the shoulder hidden, big circle hands, fingers only when a gesture needs them, pill eyes, posing, layer order and flat color with at most one shade. Use when asked to draw, generate, review or fix a Duolingo-style person, avatar, mascot or illustrated scene (SVG, React Native SVG, Skia, canvas, Figma specs), or when someone says the arms, hands or fingers look wrong for this style.
---

# Duolingo-style characters

Draw original characters the way Duolingo's illustrators draw theirs. Every rule here comes from Duolingo's public brand guide ("Shape language", design.duolingo.com/illustration) or from measuring the vector drawings published in it (raw numbers in `reference/measurements.md`).

Make new characters in this style. Never copy Duolingo's own characters (Duo, Lily, Zari, Bea, Vikram and the rest) or its logo: they are trademarks.

## The frame

Draw every character in one frame: **the head is 100 units wide and its center is (0, 0)**, with y growing downward. All numbers below use that unit, so the proportions survive any size. To place the character in a scene, translate and scale the whole group.

## 1. Shape language (always)

- **Three shapes only:** the rounded rectangle (the one you use most), the circle and the rounded triangle. Every corner is rounded, because pointy shapes are off-brand. A capsule is a fully rounded rectangle.
- **Few shapes:** use the fewest shapes that tell the story, and make every shape matter.
- **Rhythm:** put big and small shapes side by side (big head, short neck, round hands). Shapes of the same weight next to each other look dull.
- **No outlines:** parts are separated by flat color only.
- **One shade step at most per color:** no gradients and no textures. Never use transparency to fake a darker tone; pick a solid darker color.
- **Flat perspective:** a floor shadow is a pill, never an oval (an oval implies perspective).
- **Few colors:** too many colors hurt legibility at small sizes.
- **Never gray:** not for skin, clothes or a "sad / before" version of a character. Use cool pastels instead.

## 2. Proportions (head width = 100)

| Part | Shape | Size | Value in the kit |
|---|---|---|---|
| Head | Tall capsule, or a tombstone (half-circle top, straight sides, rounded bottom corners) | 100 wide, 115 to 125 tall | 100 x 122, y -66 to 56 |
| Neck | Rounded rectangle | About 1/3 of the head width. 12 to 25 of it shows between chin and torso | 28 wide |
| Torso of a bust | Tombstone: the top is a half circle (radius = half the width), straight sides, small bottom radius | 1.4 to 1.55 x the head width | 144 wide, top at y 68 |
| Torso of a short full body | Rounded square with very round corners (radius about 0.45 of the width), or a circle | About 1.45 x the head | n/a |
| Arm or sleeve | Capsule, same thickness from shoulder to wrist | 36 to 40: about the neck's width, a quarter of the torso's width | 38 |
| Shoulder (the arm's round end) | Fully inside the torso outline | About 0.7 x arm thickness in from the torso side, about 1/3 of the torso width below its top | (±46, 118) |
| Hand | Circle | Diameter about half the head width (1.3 x the arm thickness) | Radius 25 |
| Hanging arm | One straight capsule, 9 to 15 degrees out from vertical | About 145 from the shoulder to the hand center | Hand at (±80, 252) |
| Bent arm | Two capsules sharing one round elbow | 55 to 80 each (most poses 65 to 80), within 25% of each other | n/a |
| Raised straight arm | One capsule | Can stretch to about 2 x the head width | n/a |
| Finger or thumb | Capsule | Width = 1/3 of the hand diameter | 16 |

## 3. Arms

- **An arm is a thick capsule:** the same thickness from shoulder to wrist, about as wide as the neck. A thin "stick" arm is the most common way to break this style.
- **The socket is always hidden behind the torso.** The guide says: "Ensure that the arm socket is always concealed behind the torso." Put the arm's round shoulder end fully inside the torso outline and draw the arm before the torso. If the round end reaches the torso's top corner, a ball shows on the shoulder; move the shoulder lower and further in.
- **Straight, or one bend.** A bent arm is two capsules that share the same round elbow. An SVG polyline with round caps and round joins draws exactly this.
  - Never draw a continuous curve (a "banana" arm).
  - Never draw a separate ball for the elbow or shoulder. The guide: "Avoid too many shapes. It complicates the overall silhouette."
- **Segment length:** when both the upper arm and the forearm show, keep them about the same length. A straight arm can stretch (a raised arm can reach twice the head width); a cartoon length is fine, but unequal segments are not.
- **Let the elbow break the silhouette.** When a forearm crosses the body, the elbow sticking out of the torso outline is what tells the viewer the arm is bent.
- **Hanging arms** fall almost straight down, 9 to 15 degrees outward, with the hand at hip height. On a bust, the torso hides most of the arm and only a sliver along the side and the hand show. That is correct.

## 4. Hands and fingers

The guide: "Try to keep hands as abstract as you can by keeping them as circles in most places. If you need to show fingers, display the bare minimum needed for the pose."

- **Size:** the hand is a circle about half the head width (1.3 x the arm thickness). Hands a third of the head wide look like beads.
- **Clothed arm:** draw the hand first and the sleeve over it, so the sleeve's round end covers the top of the hand a little. The hand center sits about 38 units past the center of the sleeve's round end. **Bare arm:** the hand can go on top of the arm's end.
- **Fingers:** each finger is a capsule 1/3 as wide as the hand diameter, never a thin line. Use at most four digits, counting the thumb.
- **The minimum per gesture:**

  | Gesture | Hand |
  |---|---|
  | Fist, holding something, cheering, hand on the face or knee | Circle only |
  | Thumbs up | Fist circle plus a thumb capsule (width 1/3 of the hand diameter). The thumb runs from the fist center to 0.63 x the radius past the top of the fist, shifted toward the body |
  | Pointing | Fist circle plus an index capsule along the top of the fist, reaching about 1.6 x the fist radius past it |
  | Wave or spread hand | Four short capsules fanned out from the end of the arm, from up-left round to the right, with no extra palm shape. Each is about 0.46 x the arm thickness wide and 0.9 to 1.3 x the arm thickness long. Use it only when the wave is the point of the image |
  | Flat open palm (a shrug) | A thin horizontal pill, about half the arm thickness tall and 1.6 x it long |

- **Avoid the "fork":** three thin parallel fingers plus a thumb. It is the second most common way to break the style.

## 5. Same-color overlaps and shading

- **Sleeve in front of the torso:** when the torso is the same color, the sleeve merges with it, with no outline and no extra shade. The pose reads from the elbow sticking out of the silhouette and from the hand. Duolingo draws it this way for arms crossed over a sweater and for a forearm holding a bowl. Do not draw a darker forearm across the chest; it reads as a separate stick.
- **Where the hand lands:** the forearm disappears into the body, so design poses where the hand lands somewhere readable:
  - on the face or head;
  - at the edge of the silhouette (gripping the other arm);
  - on an object;
  - in the air.

  A lone hand in the middle of the chest reads as a stray dot.
- **Hand over the face** (skin on skin): use the skin's one-step-darker shade.
- **Same-color part behind** (a body behind a head, a second blueberry): the one behind can go one step darker.
- **Holding an object:** draw the sleeve, then the object, then the hand on top. Otherwise the merged sleeve covers the object.
- **Holding an edge** (a blanket, table or wall): put the hands behind the edge so only their top half shows. Two full circles side by side read as something else.

## 6. Face (inside the 100-wide head)

- **Eyes:** white pills standing up (fully rounded rectangles), never ovals. They are big and close together: each about 30 x 40, with centers about 39 apart, a little above the middle of the head (y about -8).
- **Pupil:** a dark pill (13 x 20) in the upper part of the eye, never centered vertically. Add a small white shine dot on the same side in both eyes.
- **Emotion:** it comes from cutting the white of the eye and from the pupil size. There are no eyebrows. A cut is a skin-colored shape over the top of the white (the lid) or the bottom (the cheek).

  | Expression | How |
  |---|---|
  | Tired | Flat lid across the top |
  | Sad | Lid slanting down toward the outside |
  | Worried | Steeper lid plus a cheek cut |
  | Happy | Cheek cut pushing up from below |
  | Wide-eyed | Smaller pupil |

- **Closed eye:** one stroke in the dark skin tone, never black.
  - Happy: an upward arc.
  - Calm: a line with the outer end drooping.
  - Squeezed: ">" and "<" with a flat stroke along the bottom.
- **Nose:** one or two rounded rectangles between the eyes, in the "feature" color (a darker, more saturated skin tone).
- **Mouth:** the least geometric shape. It is usually pulled to one side and can break the face outline.

  | Mouth | How |
  |---|---|
  | Smile | A stroke |
  | Big smile | Only a white tooth shape |
  | Open | Dark shape with the teeth at the top and the tongue in the middle |
  | Gritted teeth | A white rounded bar |

- **Extras:**
  - Tear: a light-blue rounded triangle plus a circle under the outer corner of the eye.
  - Tired bags: short curved strokes in the skin shade.
  - Facial hair: keep the nose the same color as the skin (guide).

## 7. Head and hair

- **Hair:** simple, one or two big shapes. Too many irregular shapes make the head hard to turn.
- **Above the ear:** always put some hair above the ear or sideburn, or the character looks like it got a bad haircut (guide).
- **Two hair recipes:**
  - A bob is one tombstone behind the head plus straight bangs in front, in the same color so they read as one shape.
  - Curls are a few circles of different sizes (rhythm) over a close-cropped base.
- **Ears** (optional): small circles at eye height.
- **Variety:** vary head width and height, eye style (round, glasses, almond, linear, dots), nose and hair between characters. The construction stays the same.

## 8. Posing

- **Tell the story:** posing adds personality. Avoid static, expressionless characters.
- **Silhouette test:** fill the character in one color; the gesture must still read.
- **Size test:** check at the smallest size the image will ship (for example 60 px tall). Hands, elbows and the expression must still read.
- **Prefer readable hand spots:** hands on the face or head, at the silhouette edge, on an object, or in the air.
- **Tested poses in the kit:**
  - hand on the forehead (sigh);
  - both arms up in a V (cheer);
  - thumbs up;
  - self hug (sad and cold);
  - hands on the temples with elbows on a desk (stress);
  - holding a phone with both hands;
  - phone at the ear with a coffee in the other hand;
  - cross-legged with the hands on the knees (calm);
  - lying in bed holding the blanket.
- **Floating accents** (hearts, notes, drops) are fine when they serve the illustration (the idea comes from Duo's floating feet). Keep them few.

## 9. Layer order (back to front)

1. Back hair (a bob behind the head)
2. Arms that go behind the torso (shoulder hidden)
3. Neck
4. Torso, collar, prints
5. Head, face, front hair, accessories
6. Things a hand goes over (a phone at the ear)
7. Sleeves of the arms in front (merged with the torso)
8. Objects being held (a cup)
9. Hands that grip (on top)
10. Things in front of the hands (a phone held with both hands)

## 10. Color

**Official palette** (names and hex values from the guide):

| Color family | Names and hex values |
|---|---|
| Neutrals | Snow #FFFFFF, Polar #F7F7F7, Swan #E5E5E5, Hare #AFAFAF, Wolf #777777, Eel #4B4B4B |
| Reds | Squid #EBE3E3, Walking Fish #FFDFE0, Flamingo #FFB2B2, Pig #F5A4A4, Crab #FF7878, Cardinal #FF4B4B, Fire Ant #EA2B2B |
| Yellows and oranges | Canary #FFF5D3, Duck #FBE56D, Bee #FFC800, Lion #FFB100, Fox #FF9600, Cheetah #FFCE8E, Monkey #E5A259, Camel #E7A601, Guinea Pig #CD7900, Grizzly #A56644 |
| Greens | Sea Sponge #D7FFB8, Turtle #A5ED6E, Feather Green #58CC02, Mask Green #89E219, Tree Frog #58A700 |
| Blues | Iguana #DDF4FF, Anchovy #D2E4E8, Beluga #BBF2FF, Moon Jelly #7AF0F2, Blue Jay #84D8FF, Macaw #1CB0F6, Whale #1899D6, Humpback #2B70C9, Narwhal #1453A3 |
| Pinks and purples | Starfish #FFAADE, Beetle #CE82FF, Betta #9069CD, Butterfly #6F4EA1 |

**Each character has:**
- skin;
- skin shade, one step darker (hands over the face, tired bags);
- feature, darker and more saturated (nose, closed eyes, closed mouth);
- hair;
- clothes, plus one clothes shade.

**Example skin trios** (skin, shade, feature):
- light: #FFCBA3, #F5B585, #E99B5F;
- warm: #F5B092, #E8946F, #D97856.

**Face colors:**
- eye white #FFFFFF;
- pupil #3C3C3C;
- open mouth #B03A3A;
- tongue #F15A5A.

**Muted "before" version:**
- Map every color by its lightness onto a cool pastel ramp (from #4A4680 dark to #DEDAFF light). Never use gray.
- Keep the eye whites and teeth white.
- Push the clothes about one step darker than the skin. Skin and a pastel sweater have the same lightness, so without this the hands in front of the clothes vanish.

## 11. Workflow

1. **Read the request:** who the character is, the mood, where it appears and at what size, and the output (SVG, React Native SVG, Skia, Figma spec).
2. **Pick the parts:** head shape, eye style, nose, hair (one or two shapes), clothes, and the palette (skin trio plus clothes pair).
3. **Build in the 100-unit frame** using the proportions table. When code is wanted, start from `reference/kit.mjs`.
4. **Pose:** pick the gesture, then place the shoulder (inside the torso), the elbow (breaking the silhouette) and the hand center. Keep arm segments similar in length.
5. **Face:** set the expression (section 6).
6. **Render and check:** compare against the numbers, run the checklist, and view it at the final display size.
7. **Fix what reads poorly:** change the pose before adding shapes.

## 12. Checklist before showing anything

- [ ] Only rounded rectangles, circles and rounded triangles. No outlines, gradients or transparency shading.
- [ ] Arm thickness about the neck's width (about 38 for a 100-wide head).
- [ ] No ball showing at the shoulder: the arm's round end is inside the torso.
- [ ] Each arm is straight or has one bend, with similar segments. The elbow breaks the silhouette when the forearm crosses the body.
- [ ] Hands are circles about half the head wide. Fingers appear only where the gesture needs them: capsules 1/3 of the hand wide, at most 4 digits.
- [ ] The torso has round shoulders (half-circle top on a bust).
- [ ] Eyes are white pills with the pupil in the upper half. No eyebrows. Closed eyes use the dark skin tone.
- [ ] At most one shade step. Same-color sleeves merge with the torso. A hand on the face is one shade darker.
- [ ] Hair is one or two shapes and covers above the ear.
- [ ] It reads at the final size, and the silhouette alone tells the pose.

## 13. Mistakes already made, and the fix

| What it looked like | Why | Fix |
|---|---|---|
| Stick arms | Arm 1/6 of the torso width | Arm as thick as the neck (0.38 of the head) |
| A ball on the shoulder | Round end of the arm at the torso's top corner | Shoulder lower and further in, fully inside the torso |
| Beads for hands | Hand a third of the head | Hand diameter half the head |
| Fork fingers | Three thin fingers plus a thumb on every hand | Circles; fingers only for the gesture, as thick capsules |
| A body like a sack | Box torso with small corner radius | Tombstone torso with a half-circle top |
| Two-tone stick across the chest | Forearm drawn one shade darker over the same-color sweater | Merge the sleeve; let the elbow and the hand tell the pose |
| "Hand on chest" read as a stray dot | Merged forearm, hand alone in the middle of the body | A pose whose hands land at the silhouette edge (self hug) or on the face or head |
| A flipper sticking out | Elbow pushed far out on a diagonal with nothing after it | Upper arm closer to the body; elbow as a short bump at the side |
| Swollen cheeks | Two big shaded hands on the cheeks | Hands on the temples (stress) or over a clear gesture |
| Cup hidden by the arm | Front sleeve drawn over the held object | Sleeve, then object, then hand |
| Two balls under the chin | Full hand circles on top of a blanket edge | Hands behind the edge, only the top half showing |
| Hands vanish in the muted version | Skin and pastel clothes map to the same tone | Clothes one step darker in the muted ramp |
| A mascot floating next to the head | It used to sit on a square shoulder; round shoulders have no seat | Stand it beside the character on the ground line |

## Reference files

- `reference/measurements.md` has the raw numbers taken from the guide's own drawings, with which drawing each number came from.
- `reference/kit.mjs` is a dependency-free JavaScript kit (Node 18+). It draws two example characters in nine poses, following every rule above. Each function returns plain shape data, and `toSvg()` turns it into SVG. Port the geometry to React Native SVG, Skia or canvas unchanged: it is plain path data.
- `reference/render-sheet.mjs` writes a contact sheet. Run `node reference/render-sheet.mjs out` and open `out/sheet.svg`. Run it after any change to the kit and look at the result before showing anyone.
