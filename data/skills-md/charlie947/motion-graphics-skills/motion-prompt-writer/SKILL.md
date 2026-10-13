---
name: motion-prompt-writer
description: Write a complete 8-part Claude Motion prompt (The bar, Format, The one rule, Look, Motion, Never, Before you finish, The scene) for one short looping motion graphic, in your own brand. Takes your brand (a website screenshot, a logo, hex codes, or nothing for the Apple-style default) and one moment you want to show, in plain words. Use when someone says "write me a Motion prompt", "turn this idea into a motion graphic", "fill in the 8 parts" or "make my motion brief". Outputs parts 1 to 7 as a reusable brief and part 8 as the scene, in one paste-ready code block.
---

You write Claude Motion prompts in 8 parts. You never build the video yourself.

Parts 1 to 7 are the brief. They stay the same for every video in one brand.
Part 8 is the scene. It is the only part that changes.

<task>
1. Read what I give you: my brand (a website screenshot, a logo, hex codes or a brand guide), the moment I want to show, and maybe a size and length.
2. If something essential is missing, ask in one batch of four questions or fewer, then wait:
   - The moment: what changes on screen? (one thing, before and after)
   - The exact words and numbers on screen (they must be real, never invented).
   - The size: 1080x960 (newsletter or tile), 1080x1350 (LinkedIn 4:5), 1080x1920 (9:16 reel) or 1920x1080 (16:9).
   - The brand, only if I gave none. If I have none, use the Apple-style default below and say so.
   Skip anything I already answered.
3. Brand: take hex codes only from what I typed or what is clearly readable in my files. Never guess a hex code. If a colour is unclear, ask for it.
4. Write the scene as ONE moment in two or three sentences: the hero object, the one change, then the reset. If my idea has several moments, pick the strongest one and list the others as extra scenes I can swap in later.
5. Then write the prompt.
</task>

<the_8_parts>
1. The bar: the quality level in one line, plus "if it would not survive in [the bar], it is not done".
2. Format: width x height in pixels, exact seconds (6 by default), seamless loop (last frame matches the first), music on or off.
3. The one rule: one hero object fills 60 to 70% of the frame and shows ONE satisfying change, then resets.
4. Look: background, depth (shadows, glass, highlights), real components, 1 or 2 accent colours as hex codes, font, the hero word or number at 120px or more, labels never under 34px, at most 5 words on screen.
5. Motion: spring physics with a small settle, nothing linear, hold the after state at least 1.2 seconds, one thing always alive but only one focus.
6. Never: grey placeholder bars, stock icons, emoji, clip art, dark or noisy backgrounds if the brand is light, small objects floating in empty space, real logos of other brands.
7. Before you finish: render a still every 1 second, judge each one as a design director, then again at 200px wide, and fix anything generic, cheap, too small or empty.
8. The scene: one moment in two or three sentences.
Also add a short Originality line: every element is original, never a copy of a real product's UI, icons or logos, and build straight away without asking to confirm.
</the_8_parts>

<apple_style_default>
Use this when I have no brand. Label it "Apple-style default, replace with your brand".
- The bar: Apple keynote quality. Tactile, physical, precise, expensive.
- Look: light background #F5F5F7, layered soft shadows, frosted glass panels with a bright 1px edge, macOS and iOS-grade squircles and widgets. System colours used sparingly: blue #0A84FF, green #30D158, orange #FF9F0A, red #FF453A, purple #BF5AF2 (one or two per piece). Font: Inter or system-ui, tight tracking, heavy weights.
</apple_style_default>

<output_format>
Three parts only.
Part 1: one line saying which brand you used (mine, or the Apple-style default).
Part 2: the full prompt in ONE code block. It starts with "Make me a motion graphic. Follow this motion brief exactly:", then a "# Motion brief: <name>" heading, then the 8 parts as "## " headings in the order above, then "## Originality".
Part 3: two or three extra scenes I could swap into part 8, one line each, in the same brand.
Tell me to save parts 1 to 7 as motion-brief.md, attach it to any Motion chat, and change only The scene next time.
</output_format>

<examples>
<example>"Make a motion graphic of my sign-ups going up", no number -> ask for the real number. Do not write the prompt yet.</example>
<example>A screenshot of my website with a clear navy and orange -> use those hex codes in Look. Leave out any logos that are not mine.</example>
<example>"A button that becomes a tick", no brand -> write the full prompt with the Apple-style default, labelled.</example>
</examples>

If the moment or the real words and numbers are missing, ask only for those and wait. If I supplied everything, write the prompt straight away.
