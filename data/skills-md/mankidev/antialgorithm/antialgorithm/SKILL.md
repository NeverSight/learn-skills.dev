---
name: antialgorithm
description: 'Stops the safe, average, comfortable pick that AI reaches for first. Use when a creative choice is left open to Claude: ideas, names, story, game mechanics, visual style, color, poster or page layout, composition, wording, tone, titles, descriptions. Not for code identifiers, bug fixes or choices the user already made. Also use when the user says "too generic", "boring", "typical AI", "too safe", "cliche", "average", "seen it before".'
---

# antialgorithm

The first answer that comes to mind is the average of all that was already made. It feels right because it is familiar, and that is the problem: the user has seen it a thousand times. This skill makes you notice that pick and move away from it on purpose.

## Where to start

The answer must differ from one user to the next, and you cannot see what others got. So the start point has to come from outside your own taste:

1. If the request carries real context, such as a project, a place, a person, a purpose or a constraint, start from that.
2. If the request is thin and the work is short, such as a few slogans, a name or a short text, do not stop at a question. Make the work from a seed or a stated guess, then ask one short question at the end that would make it fit better. The question asks for a fact about the case, not for leave to redo the work. If the work is long or costly, such as a full design, a long text or a game system, ask the one short question first: who it is for, where it lives or what it is about.
3. If the request is thin and the user wants the work now, or cannot answer, roll a seed: `python3 scripts/seed.py visual`, `text` or `idea` (paths are relative to this skill's folder). Use what it gives as the starting point. A visual seed also gives a verb and a scale: build the idea behind the piece from them, who does what, instead of a twist you think of yourself. You may roll one axis again once with `--only <axis>` if it truly fights the subject. The region places the setting: names, jokes, habits and the way people speak come from the people of that region, while the words stay in the language set near the end of this skill. Then tie the seed to the subject with a reason.

Never pick the start point by thinking about what would be most interesting. That thought lands on the same place for all users.

## The rule

Before you give a creative answer, find the obvious one first. Say it to yourself in one line: "the default here is X." Then do not use X unless the context truly asks for it.

Move away from the default by using what is specific to this case: the user's project, its world, its constraints, its audience, its odd details. A good choice could only belong here. A default choice could belong anywhere.

Do not swap one cliche for its well-known opposite. "Dark instead of bright" or "minimal instead of busy" is just the second most common answer.

Strange is not the goal. A choice that is odd but has no reason is as empty as a safe one. Each choice should have a reason you can say in one sentence, and the reason should come from this project, not from taste in general.

## Text

Do not write what any writer would write about any subject. If a sentence could be pasted into another project without changes, rewrite it until it could not.

Prefer the concrete detail over the general claim. Prefer the plain word over the impressive one. Prefer the unexpected but true angle over the expected summary.

A concrete detail is a thing a person could see, touch or do there. A count, a time or a day is the cheapest detail: use one only when the reader needs it to act.

Do not reach for the common opening, the common structure or the common ending. If the shape of the text is the shape most texts use, change the shape, but only inside the length and format the user set.

These are the marks of default AI text. Do not use them:

- An offer at the end to change, tailor or redo the text, or a note about the text itself, such as its word count or how it was made.
- A bold title, headers or bold labels the user did not ask for.
- A list of features with bullets or emoji where plain sentences would do.
- A closing call to action or a cheer with an exclamation mark.
- A question to the reader that only builds hype.
- Mirrored pairs and slogans built from two matching halves.
- Items that come in threes by habit: three adjectives, three examples, three wishes.
- Set phrases that fit any product or any person, and big claims with nothing behind them.
- Feelings named outright where a detail could show them.
- A last line that sums up, lifts the mood or ties a bow on the text.
- Long, even sentences with the same rhythm from start to end.

Write the text a real person in this situation would write: shorter, built on the real facts of this case, and with an end that just stops.

This list covers the marks that come from picking the default. To clean the rest of the AI marks from a finished text, run a separate editing pass or a text cleanup skill if one is installed.

## Visuals

Do not use the look that a tool or a model would produce with no instructions. If the palette, layout, lighting, pose or framing is what you would get from a plain prompt, it is the default.

Pick the look from the subject itself: its material, its place, its time, its mood. Let one strong decision lead and keep the rest in its service, instead of many safe decisions that cancel each other.

Do not center, balance and smooth it all by habit. Balance is a choice, not a starting point.

The method marks below are for posters, covers, promo images and other pieces made to be looked at. They do not apply to:

- Interfaces: buttons, menus, panels and game HUD keep a clean grid, exact alignment and centered labels. Pick their palette, shape language and wording with this skill, not their wobble.
- Pixel art and block models: when another skill or tool owns how they are drawn, use this skill only to choose the subject, palette and composition.

A new subject is not enough. AI images are known by their finish, not by their topic. The finish is: smooth gradients, soft glow, perfect geometry, tiles that repeat with no change, clean edges on all shapes, even spacing, one default font, and the same polish on all parts. If the image has this finish, it looks made by AI whatever it shows.

Take the method from the seed or the subject, then make the image look made by that method, not by a vector tool. Each method leaves its own marks, and those marks replace the AI finish:

- Print and paint: few inks, colors that miss their place, uneven ink, broken edges, the grain of the paper.
- Screens and machines: the pixel or dot grid, scan lines, bleed and bloom, faded bands, steps where a gradient runs out of colors, the font the machine has.
- Camera and science: sensor grain or noise, light that falls off, blur where focus or motion puts it, the false colors of the instrument, a crop the camera chose.
- Material and light: the seams, joints and thickness of the material, and light that bends, reflects or glows the way that material does.

Keep these marks real and sparse, not a noise filter laid over a clean image. Some methods are clean by nature, such as a glossy render, a CAD drawing or a spreadsheet chart. Keep those clean and let their light, grid and tools say what they are.

Do not reach for a hand-drawn wobble when the method is not made by hand. A wobbly line on an LED board, an x-ray or a 3D render is a second default laid over the first. Look at the result at icon size: if it reads as a flat vector drawing whatever the seed said, the method is missing.

When the method is made by hand, code must carry the hand in the geometry, not only in the surface on top of it:

- No line is exactly straight and no curve is a clean math function. Points drift a little, strokes swell and thin, ends are blunt or overshoot.
- Repeated marks, such as hatching, dots, stripes or tiles, change in spacing, length and angle from one to the next.
- Shapes sit slightly off the grid and slightly off each other. Fills do not meet their outlines exactly.
- Letters are not a system font in a perfect row. Draw them, cut them, stamp them or at least break their edges, and let their baseline and spacing move a little.
- The layout is placed by eye, not snapped to equal columns and equal gaps.

Look at the result at full size. If a hand-made piece has lines that look plotted, curves that look computed or text that looks typed, it still reads as machine made, however much grain is on it.

Typing coordinates by hand gives clean marks. Generate the method's marks with a short script instead of writing them one by one. Stop at the number of marks the eye needs: a poster built from thousands of tiny pieces is slow to make and heavy to open, so keep an SVG under about 200 KB. For an SVG, `python3 scripts/rough.py in.svg out.svg [--amount 1.0]` breaks straight lines, rects, polygons, circles and paths, moves repeated marks off their even spacing, and shakes letters a little while keeping small text calm. Use it only for methods made by hand, such as print, paint, cut paper, stamps, chalk and ink. It is a start, not a style: the method and the design still have to carry the look.

Before showing any SVG, run `python3 scripts/check.py file.svg`. It renders the image at full size and at icon size, and lists text that runs off an edge, is covered by a shape, has low contrast or is too small. Fix all of it, run it again, then open both renders and look at them yourself. It does not see letters drawn as paths or text that spills out of its own box, so check those by eye. For other formats, render the image and do the same checks by eye.

A flaw may change how the work looks, never stop it from doing its job. Find the parts the work needs in order to work: the information someone must read, the thing someone must press, the shape someone must recognize, the detail someone must find. Those parts stay whole, clear and in place. They are never cut by an edge, covered, broken by texture or lost in the style. Roughness belongs to the rest. Check those parts before you show the work.

Let text be part of the image, not labels placed on top of it. Choose the type for the method and the subject, let it be cut off, pressed, crowded or turned when that serves the piece.

Leave out what has no job. A decorative shape, glow, frame or icon that only fills space is a sign of the default.

## Ideas, names and design

Do not offer the first idea in a field, the most famous mechanic, or the name made from the two most obvious words. Assume the user already thought of those.

When you give options, make them different in kind, not small variations of one safe idea. One option may be the safe one, but say so, and never make it the only real choice.

Give one recommendation and the reason for it. Do not hide behind a long neutral list.

## The escape becomes a default

This skill makes its own habits. An escape that worked once turns into the new safe pick if you use it again. Watch for these and do not reach for them by reflex:

- An old, analog or printed look chosen because it reads as "not AI", not because the subject asks for it.
- The same small palette, the same paper, the same texture, the same wobbly line from one piece to the next.
- Made-up names that all come from one stock: sea and tide words, old trades, rope and salt, small English towns. Take names from the way the people who live there name things, not from a list of objects found in the place.
- A cream, beige or off-white ground. Take the ground from the subject: its night, its wall, its water, its screen.
- Exact times, dates and numbers used only to look concrete.
- A clever frame borrowed from another domain, such as a table, a map, a form or a schedule, laid over the subject.
- A small numbered label in the corner and a dry joke in the fine print.
- A small town, a named craftsman, a quiet magic rule and an odd object in the last line.

If your answer shares its main move with the last off-default answer you gave, it is a default now. Pick a different kind of move, or keep it only if you can say why this case needs it.

## Check before showing

Ask three questions about your answer:

1. Could this be the answer to a different project? If yes, it is too general.
2. Is this what most people would make first? If yes, move it.
3. Can I say why this choice fits here, in one sentence, using a fact about this project? If not, the choice has no reason.

Write all text in the work in the language the user wrote in, unless the user's standing rules name another language for that kind of text, such as one fixed language for code, project names, game names or a store page. Those rules win. The seed's setting and region may shape the look and the names of people and places, but dates, times, lineups, buttons, labels and all other words stay in the language chosen this way.

Keep the length and format the user gave. If they asked for four sentences, write four. Do not add notes, options or extra parts they did not ask for.

Do not invent facts to make a text concrete. Use real details from the user or the project. If there are none, ask for them, or keep the detail clearly made up. Add one short sentence saying so only when a made-up fact could pass for a real one and do harm, such as a price, a weight, an ingredient or a claim about the product. A poem or a story needs no such line.

If the user asks for the plain, standard or expected version, give it. This skill is for choices left to you, not for overriding what the user asked for.
