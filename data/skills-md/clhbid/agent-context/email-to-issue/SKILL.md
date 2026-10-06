---
name: email-to-issue
description: Sweep flagged Outlook threads, or threads named by subject, into GitHub issues or comments.
disable-model-invocation: true
---

# Email to issue

One run is a **sweep**: read the chosen Outlook threads, propose one table for all of them, and file
only the rows the user approves, by `issue-tracker`. New issues stop at `Backlog`; triage routes
them and writes any agent brief.

Find the Microsoft 365 connector's mail tools by capability — read, search, reply, move, flag —
since their names change between connector versions.

## Mail permissions

Every mail action in the sweep falls inside this list. For anything else, tell the user it is theirs
to do by hand.

- **Allowed:**
  - Read and search mail.
  - Send [the reply](#the-reply) in a thread filed this sweep.
  - Clear the flag on, and move to Archive, a thread filed this sweep, once the user confirms in
    [step 6](#6-close-the-loop).
- **Never:**
  - Delete mail, drafts included.
  - Send, forward or draft mail to anyone but the signed-in user.
  - Write to calendar, files or Teams.

## The sweep

### 1. Gather

Read every **flagged** Inbox thread, or the threads the user names by subject. When a subject
matches several threads, list them with sender and date and ask which.

Skip a thread that already holds [the reply](#the-reply): it is **processed**. Leave attachments in
the mail, and note on the row that the thread has one.

**Done when:** a list of threads to process, each with sender, date and subject, plus a count of
those skipped as processed.

### 2. Check permissions

Writing to mail needs two capabilities:

- **Reply**, taking its recipients as an argument. A reply that only pre-fills the sender does not
  count.
- **Move and flag**: move to Archive and clear a flag.

Without them, the sweep still files issues and [step 6](#6-close-the-loop) ends in a manual list.

**Done when:** the user has one line saying whether this sweep can reply, and whether it can unflag
and archive.

### 3. Match

Search open issues across the org for one that already covers each thread:

```bash
gh search issues "<key terms>" --owner clhbid --state open --json repository,number,title,url
```

Try two or three phrasings, and read a candidate before calling it a match. A match becomes a
**comment** carrying only what the thread adds — new evidence or a clarification. No match becomes
a **new issue** in the repo the thread is about.

**Done when:** every thread has a proposed action and target.

### 4. Propose

Read each target's visibility, then draft its title by [Confidentiality](#confidentiality):

```bash
gh repo view clhbid/<repo> --json visibility --jq .visibility
```

Show one table for the whole sweep:

| #   | Source                                 | Action    | Target              | Visibility | Title                         | Label |
| --- | -------------------------------------- | --------- | ------------------- | ---------- | ----------------------------- | ----- |
| 1   | Pat Example (`pat@example.com`), 2 Mar | New issue | `clhbid/<repo>`     | PRIVATE    | Bid export drops the last lot | `bug` |
| 2   | Sam Sample (`sam@example.org`), 3 Mar  | Comment   | `clhbid/<repo>#123` | PUBLIC     | Second report of the timeout  | —     |

The user approves, edits or skips each row. GitHub stays untouched until then.

**Done when:** every row is approved or skipped.

### 5. File

For each approved row, write by [Confidentiality](#confidentiality):

- **New issue**: by
  [`issue-tracker` § Creating an issue from the org form](../issue-tracker/SKILL.md#creating-an-issue-from-the-org-form),
  then confirm it landed in `Backlog`.
- **Comment**: `gh issue comment <number> --repo clhbid/<repo>`, as a `writing-lean` thread comment.

**Done when:** every approved row has a link, and every new issue reads back as `Backlog`.

### 6. Close the loop

Send [the reply](#the-reply) in each filed thread. Then list the filed threads and ask which to
unflag and archive; approving the table in step 4 is not that confirmation. Move only the threads
the user confirms.

**Without write tools**, list each filed thread with sender, date, subject and issue link, for the
user to reply, unflag and archive by hand. The reply is what lets the next sweep skip the thread.

**Done when:** a sweep summary gives each thread's issue link and outcome — replied, unflagged,
archived, or left to the user, with the reason for every skipped reply.

## The reply

It marks a thread processed and links it to its issue.

1. Take the user's address from the connector's signed-in profile. Ask when it is missing or
   ambiguous.
2. Write the body, marker first:

   ```text
   Filed by /email-to-issue: clhbid/<repo>#<number>
   https://github.com/clhbid/<repo>/issues/<number>
   ```

3. **Replace the recipients**: `To` the user alone, `Cc` and `Bcc` empty.
4. **Read every recipient field back** from the built message. Send only when the user is the one
   recipient.
5. **On any doubt, skip** the reply and put the link in the sweep summary. Name any draft left
   behind so the user can remove it.

## Confidentiality

Titles, bodies and comments follow the target's visibility:

- **`PRIVATE`**: the thread's details in full, confidential ones included.
- **`PUBLIC`**: a paraphrase. Name the sender by role ("a seller", "a bidder"), and leave out
  customer names, contact details, pricing and other proprietary detail.
- **Anything else, or unsure about a detail**: ask.
