---
name: tweet
description: Generate 5 engaging tweet options based on a topic or description
user-invocable: true
argument-hint: "[topic or description]"
---

Generate 5 engaging and exciting tweet options based on the user's description. Each tweet must:

- Be exciting and attention-grabbing
- End with a question to engage readers
- Be between 190-210 characters
- Use `wc -c` to verify character count for each tweet
- Display the character count for each tweet

Format your response as:
1. [Tweet text] ([X] characters)
2. [Tweet text] ([X] characters)
3. [Tweet text] ([X] characters)
4. [Tweet text] ([X] characters)
5. [Tweet text] ([X] characters)

Ensure all tweets meet the character limit before displaying.

Note: Display the tweet options in chat only. Do not write to any file.
