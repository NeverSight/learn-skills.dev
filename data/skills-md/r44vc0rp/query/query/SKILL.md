---
name: query
description: Ask the person for secrets and other private values (API keys, tokens, passwords, connection strings) through the local query CLI, which opens a floating prompt on their Mac, instead of asking them to paste values into chat. Use whenever a task needs a credential or environment variable the agent does not have, such as a missing API key, a failing command that reports an unset variable, a .env file that needs a value, or a test that needs live credentials.
---

# query

`query` opens a floating prompt on the person's screen that asks for named
values. Use it instead of asking for a secret in chat: anything pasted into
chat stays in the transcript, and `query` keeps the value out of it.

## Choose the command

Prefer the command that keeps the value away from you:

1. **`query run`**: the value is needed for one command. It runs the command
   with the values set as environment variables; they never reach your
   output.

   ```sh
   query run OPENAI_API_KEY -- npm test
   query run DATABASE_URL --reason "Run the migration against staging" -- bun run migrate
   ```

2. **`query write`**: the value belongs in a dotenv file the project already
   reads. The values are merged in (existing keys are replaced, other lines
   kept) and the file is written with mode 0600.

   ```sh
   query write .env.local STRIPE_SECRET_KEY "STRIPE_WEBHOOK_SECRET:From the Stripe dashboard, Webhooks"
   ```

   Before writing, make sure the file is ignored by git (`git check-ignore
   <file>`). If it is not, say so instead of writing a secret into a tracked
   file.

3. **`query get`**: only when a value must be read by you, such as a
   non-secret setting. It prints the values to stdout, so they enter the
   transcript. Never use it for secrets.

   ```sh
   query get AWS_REGION --format export
   ```

## Write a good request

- Use the exact variable names the code reads.
- Ask for everything a task needs in one prompt, not one prompt per key.
- Add a hint after a colon when the person may not know where to find the
  value: `"GITHUB_TOKEN:Fine-grained token with contents read"`.
- Add `--reason` with a short, plain sentence saying what the values are for.
  Keep it under about 80 characters.

## Wait for the answer

The prompt waits until the person answers. Run `query` in the foreground with
a long enough command timeout (several minutes), or pass `--timeout SECONDS`
so it gives up on its own.

Exit status:

| Status | Meaning | What to do |
| --- | --- | --- |
| 0 | Provided (for `run`, the command's own status) | Continue |
| 1 | The person cancelled | Stop and ask in chat whether to continue without it. Do not prompt again unasked. |
| 2 | Usage error | Fix the command; see `query --help` |
| 124 | Timed out | Tell the person the prompt expired |

## Limits

- It needs the person's logged-in Mac desktop. It does not work over SSH, in
  CI, in containers or in VMs. There, ask the person to set the variable
  themselves.
- Never print, echo, log or commit the values you receive, and never pass them
  as command-line arguments (`ps` shows arguments to every user). Inside the
  command, read them from the environment.
- If `query` is not installed, say so and point to `~/dev/query` instead of
  falling back to asking for the secret in chat.
