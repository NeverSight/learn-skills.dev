---
name: silent-product-demo
description: Produce a designed, silent product demo from real UI with camera moves and concise on-screen words. Use for feature launches, announcements, and social clips that should work without narration.
---

# Silent product demo

Show one feature being used and the result it creates. The interface, cursor, and camera carry the story. On-screen text may name a beat or clarify an outcome, but it should not narrate every click.

## Plan the sequence

Identify the real starting state, the user's decision, the app's response, and the final outcome. Make a short storyboard with time, screen state, pointer action, camera focus, and any text. Start with something legible and meaningful on frame one.

Use the real app as the authority. Capture it directly, or build a frame-accurate port from its UI source when a designed camera or extreme zoom requires one. Preserve actual labels, layout, and interaction states. Do not invent controls, results, or supported integrations.

## Direct the motion

- Move the camera to make the current action easier to see, then let it settle before the next action.
- Place a cursor only for a decision. Confirm its tip touches the target when the pressed state appears.
- Keep each beat focused on one subject. Remove old props or text when the story moves on.
- Use the product's motion timing and visual tokens. In frame-based rendering, calculate animation from frame or time explicitly so every render is deterministic.
- Let transitions connect related states. A direct cut is fine when continuity adds no information.

Render stills at the first frame, each action, every transition midpoint, and the final frame before committing to full exports. Then watch the rendered files muted. Check that the feature is understandable, text remains readable at phone size, no interaction misses, and each aspect ratio preserves the outcome. Make a cover for each requested format.
