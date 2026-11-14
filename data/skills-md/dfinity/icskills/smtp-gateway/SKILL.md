---
name: smtp-gateway
description: "Receive email in an Internet Computer canister through the SMTP Gateway Protocol. Covers implementing smtp_request and smtp_request_validate, addressing (user@<canister-id>.icp0.io, custom domains, handing mail to another canister with /.well-known/ic-smtp-canister-id), how the gateway turns reply codes into SMTP (5xx bounces, everything else retries, 550 rejects one recipient), what actually arrives (raw headers, raw MIME body, a per-attempt message_id, no sender authentication), the ic-smtp-gateway-protocol Rust crate, and the optional chunked upload for messages over 2 MiB. Use when a canister must receive or process inbound email, when implementing the SMTP gateway Candid interface, or when mail to a canister bounces, is retried, or never arrives. Do NOT use for sending email from a canister (the gateway is inbound only; call an email API with https-outcalls) or for serving HTTP from a canister."
license: Apache-2.0
compatibility: "icp-cli >= 0.2.2; Rust examples: ic-cdk 0.20 with ic-smtp-gateway-protocol 0.1 (plus sha2 0.11 for chunked upload); Motoko examples: moc >= 1.11.0 with core >= 2.5.0"
metadata:
  title: SMTP Gateway (Inbound Email)
  category: Integration
---

# SMTP Gateway (Inbound Email)

## What This Is

An SMTP gateway is an off-chain mail server that accepts email addressed to a canister and delivers it by calling the canister's `smtp_request` method, the way the HTTP gateway calls `http_request`. DFINITY operates the gateways that mail for `<canister-id>.icp0.io` reaches, alongside its HTTP gateways; others can run their own, since the gateway is part of `ic-gateway`. The limits and sender checks in this skill are those of DFINITY's gateways. A canister opts in by implementing two methods. There is nothing to register for `<canister-id>.icp0.io` addresses. Mail flows **in** only: a canister cannot send email through the gateway, and it never receives bounce messages either, because the gateway rejects the null sender (`MAIL FROM:<>`).

The protocol is specified in `candid/smtp_gateway.did` in `dfinity/ic-smtp-gateway-protocol`, and the gateway that implements it is the `smtp` module of `dfinity/ic-bn-lib`.

## Addressing

| Address | Setup |
|---|---|
| `anything@<canister-id>.icp0.io` | None. Every `<canister-id>.icp0.io` already has MX records pointing at the gateway. |
| `anything@<custom-domain>` | The domain must be registered as an IC custom domain (`custom-domains` skill): the gateway resolves it in the same registry as the HTTP gateway. Its MX records must also point at the gateway. A subdomain set up the standard way (`CNAME` to `<domain>.icp1.io`) inherits the gateway's MX records through the CNAME. An apex domain cannot be a CNAME, and ALIAS or CNAME flattening only produces A/AAAA records, so publish the hosts that `dig +short MX boundary.dfinity.network` lists as your MX records, and keep them in sync. Do **not** publish `MX boundary.dfinity.network` itself: mail servers would connect to that name's own addresses, which do not accept mail. |

How the gateway routes a recipient:

- If the first DNS label of the recipient's domain parses as a principal, that is the canister. Otherwise the exact domain is looked up among registered custom domains. No match: `550 5.1.1 Unknown recipient domain.`
- The domain arrives lowercased. The local part (`user`) arrives **verbatim**: case, `+tag` suffixes and quotes are kept. Match it case-insensitively unless you have a reason not to. The gateway rejects non-ASCII local parts itself.
- **Handing mail to another canister.** Before calling the addressed canister, the gateway fetches `https://<canister-id>.icp0.io/.well-known/ic-smtp-canister-id`. If that returns a 2xx response whose body (whitespace-trimmed) is a principal, every SMTP call goes to that principal instead. Any failure falls back to the addressed canister, and either result is cached for 10 minutes. Use this when a frontend canister owns the domain and a backend canister handles mail: with the `static-site` recipe, add a file `.well-known/ic-smtp-canister-id` containing only the backend's canister ID to the uploaded directory (`.well-known/` is uploaded without extra configuration).

## The Protocol

| Method | Required | When the gateway calls it |
|---|---|---|
| `smtp_request_validate : (SmtpRequest) -> (SmtpResponse) query` | **Yes** (see Pitfall 4) | Once per `RCPT TO`, before the message is transferred |
| `smtp_request : (SmtpRequest) -> (SmtpResponse)` | Yes | After `DATA`, once per destination canister, listing all recipients that resolved to it |
| `smtp_capabilities`, `smtp_upload_chunk`, `smtp_upload_commit`, `smtp_upload_status`, `smtp_upload_abort` | No | Chunked upload for messages over the ~2 MiB ingress limit. Read `references/chunked-upload.md` before implementing these. |

What each call carries:

| Field | `smtp_request_validate` | `smtp_request` |
|---|---|---|
| `envelope` | `MAIL FROM` address and exactly one recipient | `MAIL FROM` address and every recipient for this canister (at most 10 per session) |
| `message` | `null` | Headers and raw body |
| `message_id` | `null` | A new UUIDv7 for every SMTP transaction |

The wire types are defined in `candid/smtp_gateway.did`. The Rust crate exports them, and the Motoko example below declares them field for field. `code` is `nat64` (a `nat32` does not decode), the variant labels are exactly `Ok` and `Err`, and `Ok` carries an empty record, not `null`.

## Reply Codes Are the Interface

The gateway acts on the **class** of `SmtpRequestError.code`: 500–599 is permanent and anything else is temporary. Traps and call failures are temporary too, except two that are permanent: the method is not exported, or the request is too large for one ingress message.

During `RCPT TO`, from `smtp_request_validate`:

| Canister result | The sending server sees |
|---|---|
| `Ok` | `250 2.1.5 OK` |
| `Err` with code 550 | `550 5.1.2 Mailbox does not exist.` for that recipient only (your `message` is dropped) |
| `Err` with another 500–599 code | `550 5.1.3 Permanent error: <message>` |
| `Err` with any other code | `451 4.4.3 Temporary error: <message>` |
| Method not exported | `550 5.1.3 Permanent error: Canister <id> does not support SMTP protocol` |
| Trap or call failure | `451 4.4.3 Temporary error: ...` |

After `DATA`, from `smtp_request`:

| Canister result | The sending server sees | Then |
|---|---|---|
| `Ok` | `250` | Delivered |
| `Err` with a 500–599 code | `550 5.5.0 Permanent delivery error: <message>` | The sender gets a bounce |
| `Err` with any other code | `450 4.5.0 Temporary delivery error: <message>` | The sending server retries later |
| Trap, call failure, or no reply within 90 s | `450 ...` | Retried |

Codes to use. Permanent: **550** no such mailbox (reserved, never for anything else), **501** a required field is missing, **552** message, headers or recipient list too large, **554** content rejected, **530** caller not authorized. Temporary: **450** try again later, **452** out of storage.

## Mistakes That Break Mail Delivery

1. **Trapping instead of returning `Err`.** A trap is reported as a *temporary* failure, so the sending server retries for days before it gives up with an unhelpful error. Every rejection must be a returned `Err`. Traps hide in `unwrap()`, `expect()`, out-of-range slicing, `String::truncate` inside a multi-byte character, a nested `RefCell` borrow, and in Motoko in `Nat` underflow and array indexing.

2. **Reporting a permanent problem with a non-5xx code.** Only 500–599 bounces. A deterministic rejection sent as 4xx, or as any code outside 400–599, is retried until the sender's server gives up, and the sender never learns why.

3. **Using 550 for anything except "unknown mailbox".** From `smtp_request_validate`, 550 becomes `550 5.1.2 Mailbox does not exist.` and your text is dropped. Use another 5xx code (552, 554) for policy rejections so that your message reaches the sender.

4. **Skipping `smtp_request_validate`.** The gateway calls it on every `RCPT TO` and treats a missing method as a permanent "does not support SMTP protocol" rejection of every recipient. Implement both methods. (`smtp_capabilities` is genuinely optional: a missing method just means no chunked upload.)

5. **Requiring `message` or `message_id` in `smtp_request_validate`.** It receives only `envelope`, with exactly one recipient. Requiring the other fields rejects every recipient.

6. **Trusting Candid to validate the request.** Every `SmtpRequest` field is `opt`, so *any* record argument decodes into it, with all fields `null`. Check each field you need and return 501 when it is missing.

7. **Forgetting that anyone can call the SMTP methods.** They are public: any principal can call them directly with any envelope, headers and body, bypassing every check a gateway makes. To restrict who delivers mail, check the caller's principal. For example, to accept mail only through the DFINITY-operated gateway, allow only `ttvgm-eefjs-h2pqz-huxqk-ld2c3-rcwbm-a2tik-35hex-pm2jn-l6glo-oae` (plus controllers, for testing), as both examples do. For another gateway, ask its operator for its principal, or don't restrict callers. Reject with 530, never by trapping, because the gateway would retry. Either way, bound every input (Internet Identity allows 100 headers, 8 KiB per header value, 64 bytes per local part) and cap stored mail.

8. **Trusting the sender's address.** DFINITY's gateways reject mail that fails SPF for the envelope sender's domain, and mail whose DKIM signatures all fail. They do accept senders without an SPF record and unsigned mail, they do not check that the signing domain matches `From` (no DMARC), and no result reaches the canister (`gateway_flags` is always `null`). So `From`, and `envelope.from` for domains without SPF, is still whatever the client claimed. If the sender's identity matters, verify DKIM inside the canister, as Internet Identity does: relaxed header canonicalization (names arrive normalized, so `simple` cannot be verified); the public key fetched with DNS-over-HTTPS outcalls (`https-outcalls` skill) and accepted only when several resolvers agree; the signing domain `d=` aligned with `From`; duplicate `From`, `Subject` or `DKIM-Signature` headers rejected, since a duplicate header can smuggle content past the signature.

9. **Expecting clean, decoded header values.** Each value is the raw text after the colon: the leading space, the trailing `\r\n` or `\n`, folded continuation lines and `=?UTF-8?B?...?=` encoded words are all left in. Trim before comparing, decode encoded words yourself if you display them, and match header names case-insensitively: names the gateway recognizes arrive in canonical case (`fRoM` as `From`). Order and duplicates are preserved; a header whose value is not valid UTF-8 is dropped.

10. **Expecting a parsed body.** `body` holds the raw bytes after the header block, with CRLF line endings, and no MIME processing. Mail from a normal client is usually `multipart/alternative` with base64 or quoted-printable parts: you receive the boundaries and encoded parts, not plain text.

11. **Deduplicating on `message_id`.** It identifies one SMTP transaction, not one email: when the sending server retries, the retry gets a new `message_id`. Delivery is at-least-once. A lost reply after you stored the mail, the 90-second delivery timeout, or a failure at *another* canister receiving the same message (the gateway fails the whole message and the sender retries for every recipient) all lead to redelivery. If duplicates matter, deduplicate on the RFC 5322 `Message-ID` header (chosen by the sender, so scope it per sender) or make processing idempotent.

12. **Awaiting inside `smtp_request`.** The gateway keeps the SMTP session open while it waits and gives up after 90 seconds. That is reported as temporary and retried, so if your call did finish, the mail arrives twice. Every `await` is also an interleaving point (`canister-security` skill). Accept synchronously and defer slow work, for example to a timer. Internet Identity stores the message and finishes its DKIM key lookups after it has replied.

13. **Long or multi-line error messages.** The `message` is copied into the SMTP reply line: on `RCPT TO` it is cut at about 224 bytes without stripping CR or LF, and a delivery reply over about 220 bytes can be dropped. Use short, single-line ASCII and never echo request content.

14. **Leaking secrets through error codes.** Every `Err` tells the caller something, and a 5xx also sends a bounce to the claimed sender. If mail carries secrets such as verification codes, return `Ok` for unknown or invalid content and record the outcome internally. Internet Identity returns `Err` only for malformed requests, more than one recipient, and unknown mailboxes.

15. **Keeping mail on the heap, or configuration in stable variables.** Heap state is lost on upgrade, so store mail in stable memory (`stable-memory` skill). In a Motoko `persistent actor` the opposite applies: a plain `let` is stable and keeps its first-install value, so a mailbox list or limit you change in code has no effect after an upgrade. Declare configuration `transient let`.

## Implementation

Both examples accept mail for `support@` and `hello@` only through the DFINITY-operated gateway (and from controllers, for testing; this restriction is optional, see Pitfall 7), store each message, and apply the pitfalls above. `smtp_request_validate` and `smtp_request` share one envelope check because the query may be stale by the time the update runs.

### Rust

The `ic-smtp-gateway-protocol` crate provides the protocol types. It builds for `wasm32-unknown-unknown`.

```toml
[package]
name = "backend"
version = "0.1.0"
edition = "2021"

[lib]
crate-type = ["cdylib"]

[dependencies]
candid = "0.10"
ic-cdk = "0.20"
ic-smtp-gateway-protocol = "0.1"
```

Deploy it with the `@dfinity/rust@v3.3.0` recipe as canister `backend` (`icp-cli` skill).

```rust
use std::{cell::RefCell, collections::BTreeMap};

use ic_cdk::{
    api::{is_controller, msg_caller, time},
    query, update,
};
use ic_smtp_gateway_protocol::{
    Envelope, Header, SmtpOk, SmtpRequest, SmtpRequestError, SmtpResponse,
};

/// Principal of DFINITY's SMTP gateways; gateways run by others have their own.
const SMTP_GATEWAY: &str = "ttvgm-eefjs-h2pqz-huxqk-ld2c3-rcwbm-a2tik-35hex-pm2jn-l6glo-oae";

/// Local parts this canister accepts mail for.
const MAILBOXES: &[&str] = &["support", "hello"];

// Bounds on what one request may cost this canister.
const MAX_RECIPIENTS: usize = 10;
const MAX_HEADERS: usize = 100;
const MAX_BODY_BYTES: usize = 100_000;
const MAX_STORED: usize = 10_000;

#[allow(dead_code)] // read by your application logic
struct Mail {
    envelope_from: String, // unauthenticated: see pitfalls
    subject: String,
    headers: Vec<Header>,
    body: Vec<u8>, // raw RFC 5322 body bytes, MIME not decoded
    received_at: u64,
}

thread_local! {
    // Heap only for brevity: use stable structures in production.
    static INBOX: RefCell<BTreeMap<String, Mail>> = RefCell::default();
}

/// Keep `message` short, single-line ASCII: the gateway copies it into the
/// SMTP reply line.
fn err(code: u64, message: &str) -> SmtpResponse {
    SmtpResponse::Err(SmtpRequestError {
        code,
        message: message.to_string(),
    })
}

/// Optional: accept mail only through DFINITY's gateways (plus
/// controllers, for testing). Drop this check to accept any gateway. Return
/// 530 rather than trapping, which would read as a temporary failure.
fn check_caller() -> Result<(), SmtpResponse> {
    let caller = msg_caller();
    if caller.to_text() == SMTP_GATEWAY || is_controller(&caller) {
        Ok(())
    } else {
        Err(err(530, "unauthorized caller"))
    }
}

/// Header names are case-insensitive. Values arrive as the raw text after the
/// colon: leading space and line ending included, RFC 2047 not decoded.
fn header<'a>(headers: &'a [Header], name: &str) -> Option<&'a str> {
    headers
        .iter()
        .find(|h| h.name.eq_ignore_ascii_case(name))
        .map(|h| h.value.trim())
}

fn is_mailbox(user: &str) -> bool {
    MAILBOXES.iter().any(|m| m.eq_ignore_ascii_case(user))
}

/// Shared by both entry points: smtp_request must re-check everything
/// smtp_request_validate checked, because the state may have changed since.
fn check_envelope(env: &Envelope) -> Result<(), SmtpResponse> {
    if env.to.is_empty() {
        return Err(err(501, "no recipients"));
    }
    if env.to.len() > MAX_RECIPIENTS {
        return Err(err(552, "too many recipients"));
    }
    if env.to.iter().any(|rcpt| !is_mailbox(&rcpt.user)) {
        return Err(err(550, "no such mailbox"));
    }
    Ok(())
}

/// Called once per RCPT TO, with only `envelope` set (exactly one recipient).
/// Never require `message` or `message_id` here.
#[query]
fn smtp_request_validate(req: SmtpRequest) -> SmtpResponse {
    if let Err(rejected) = check_caller() {
        return rejected;
    }
    let Some(env) = req.envelope else {
        return err(501, "envelope is required");
    };
    match check_envelope(&env) {
        Ok(()) => SmtpResponse::Ok(SmtpOk {}),
        Err(rejected) => rejected,
    }
}

/// Delivery. Synchronous on purpose: no `.await`, so no interleaving and no
/// risk of running into the gateway's delivery timeout.
#[update]
fn smtp_request(req: SmtpRequest) -> SmtpResponse {
    if let Err(rejected) = check_caller() {
        return rejected;
    }
    // Every SmtpRequest field is `opt`, so ANY record decodes into this type.
    // Check presence yourself and never unwrap: a trap reads as a temporary
    // failure, and the sending server retries it until it gives up.
    let (Some(env), Some(msg), Some(id)) = (req.envelope, req.message, req.message_id) else {
        return err(501, "envelope, message and message_id are required");
    };
    if let Err(rejected) = check_envelope(&env) {
        return rejected;
    }
    if msg.headers.len() > MAX_HEADERS {
        return err(552, "too many headers");
    }
    if msg.body.len() > MAX_BODY_BYTES {
        return err(552, "message too large");
    }

    INBOX.with_borrow_mut(|inbox| {
        if inbox.len() >= MAX_STORED {
            return err(452, "mailbox full"); // transient: the sender retries later
        }
        // `message_id` is unique per SMTP transaction, NOT per email: a retry
        // by the sending server arrives with a new one. Storing under it
        // avoids overwrites; it does not deduplicate.
        inbox.entry(id).or_insert_with(|| Mail {
            envelope_from: format!("{}@{}", env.from.user, env.from.domain),
            subject: header(&msg.headers, "Subject")
                .unwrap_or_default()
                .to_string(),
            headers: msg.headers,
            body: msg.body,
            received_at: time(),
        });
        SmtpResponse::Ok(SmtpOk {})
    })
}

#[query]
fn inbox_size() -> u64 {
    INBOX.with_borrow(|inbox| inbox.len() as u64)
}

ic_cdk::export_candid!();
```

### Motoko

There is no Motoko package for the protocol: declare the types yourself, field for field, as below. `mops.toml` needs `core = "2.5.0"` under `[dependencies]`.

```motoko
import Char "mo:core/Char";
import Map "mo:core/Map";
import Principal "mo:core/Principal";
import Text "mo:core/Text";
import Time "mo:core/Time";

persistent actor Inbox {

  // --- Protocol types: a field-for-field projection of candid/smtp_gateway.did ---
  // Names and labels are the wire format: keep `#Ok`/`#Err` capitalised,
  // `code : Nat64`, and `#Ok` carrying the empty record `{}`.

  public type Header = { name : Text; value : Text };
  public type Message = { headers : [Header]; body : Blob };
  public type Address = { user : Text; domain : Text };
  public type Envelope = { from : Address; to : [Address] };
  public type SmtpRequest = {
    message : ?Message;
    envelope : ?Envelope;
    gateway_flags : ?[Text];
    message_id : ?Text;
  };
  public type SmtpRequestError = { code : Nat64; message : Text };
  public type SmtpResponse = { #Ok : {}; #Err : SmtpRequestError };

  // --- Application state ---

  type Mail = {
    envelopeFrom : Address; // unauthenticated: see pitfalls
    subject : Text;
    headers : [Header];
    body : Blob; // raw RFC 5322 body bytes, MIME not decoded
    receivedAt : Int;
  };

  // Configuration is `transient`: a plain `let` in a persistent actor is
  // stable and would keep its first-install value across upgrades.

  // Principal of DFINITY's SMTP gateways; gateways run by others have their own.
  transient let smtpGateway = Principal.fromText("ttvgm-eefjs-h2pqz-huxqk-ld2c3-rcwbm-a2tik-35hex-pm2jn-l6glo-oae");

  // Local parts this canister accepts mail for.
  transient let mailboxes : [Text] = ["support", "hello"];

  // Bounds on what one request may cost this canister.
  transient let maxRecipients = 10;
  transient let maxHeaders = 100;
  transient let maxBodyBytes = 100_000;
  transient let maxStored = 10_000;

  let inbox = Map.empty<Text, Mail>(); // stable: survives upgrades

  // Keep `message` short, single-line ASCII: the gateway copies it into the
  // SMTP reply line.
  func err(code : Nat64, message : Text) : SmtpResponse {
    #Err({ code; message });
  };

  // Optional: accept mail only through DFINITY's gateways (plus
  // controllers, for testing). Drop this check to accept any gateway. Return
  // 530 rather than trapping, which would read as a temporary failure.
  func checkCaller(caller : Principal) : ?SmtpResponse {
    if (caller == smtpGateway or Principal.isController(caller)) null else ?err(530, "unauthorized caller");
  };

  // Header names are case-insensitive. Values arrive as the raw text after the
  // colon: leading space and line ending included, RFC 2047 not decoded.
  func header(headers : [Header], name : Text) : ?Text {
    let wanted = name.toLower();
    for (h in headers.vals()) {
      if (h.name.toLower() == wanted) return ?h.value.trim(#predicate(Char.isWhitespace));
    };
    null;
  };

  func isMailbox(user : Text) : Bool {
    let u = user.toLower();
    for (m in mailboxes.vals()) { if (m == u) return true };
    false;
  };

  // Shared by both entry points: smtp_request must re-check everything
  // smtp_request_validate checked, because the state may have changed since.
  func checkEnvelope(env : Envelope) : ?SmtpResponse {
    if (env.to.size() == 0) return ?err(501, "no recipients");
    if (env.to.size() > maxRecipients) return ?err(552, "too many recipients");
    for (rcpt in env.to.vals()) {
      if (not isMailbox(rcpt.user)) return ?err(550, "no such mailbox");
    };
    null;
  };

  // Called once per RCPT TO, with only `envelope` set (exactly one recipient).
  // Never require `message` or `message_id` here.
  public shared query ({ caller }) func smtp_request_validate(req : SmtpRequest) : async SmtpResponse {
    switch (checkCaller(caller)) { case (?rejected) return rejected; case null {} };
    let ?env = req.envelope else return err(501, "envelope is required");
    switch (checkEnvelope(env)) {
      case (?rejected) rejected;
      case null #Ok({});
    };
  };

  // Delivery. No `await` in here: no interleaving, and no risk of running
  // into the gateway's delivery timeout.
  public shared ({ caller }) func smtp_request(req : SmtpRequest) : async SmtpResponse {
    switch (checkCaller(caller)) { case (?rejected) return rejected; case null {} };
    // Every SmtpRequest field is `opt`, so ANY record decodes into this type.
    // Check presence yourself and never trap: a trap reads as a temporary
    // failure, and the sending server retries it until it gives up.
    let (?env, ?msg, ?id) = (req.envelope, req.message, req.message_id) else {
      return err(501, "envelope, message and message_id are required");
    };
    switch (checkEnvelope(env)) {
      case (?rejected) return rejected;
      case null {};
    };
    if (msg.headers.size() > maxHeaders) return err(552, "too many headers");
    if (msg.body.size() > maxBodyBytes) return err(552, "message too large");
    if (Map.size(inbox) >= maxStored) return err(452, "mailbox full"); // transient

    // `message_id` is unique per SMTP transaction, NOT per email: a retry by
    // the sending server arrives with a new one. Storing under it avoids
    // overwrites; it does not deduplicate.
    if (not Map.containsKey(inbox, Text.compare, id)) {
      Map.add(
        inbox,
        Text.compare,
        id,
        {
          envelopeFrom = env.from;
          subject = switch (header(msg.headers, "Subject")) {
            case (?s) s;
            case null "";
          };
          headers = msg.headers;
          body = msg.body;
          receivedAt = Time.now();
        },
      );
    };
    #Ok({});
  };

  public query func inboxSize() : async Nat { Map.size(inbox) };
};
```

## Chunked Upload (Optional)

A message whose encoded `SmtpRequest` exceeds 2 MiB cannot be delivered with one ingress call. The gateway then uploads it with `smtp_upload_chunk` and finalizes it with `smtp_upload_commit`, but **only** when `smtp_capabilities` returns both `upload_protocol_version >= 1` and `max_message_size > 0`. Otherwise the sender gets a permanent `550 5.5.0 ... does not support chunked upload` error, and your canister is unaffected. DFINITY's gateways accept at most 1,996,800 bytes per message (header block and body) and rejects larger mail with `552 5.3.4`, so nearly everything it accepts fits one `smtp_request`: implement chunked upload only if you need it. The obligations are strict: verify each chunk's SHA-256 before storing it, bound the layout before allocating, derive the commit digest from the bytes you stored (SHA-256 over the concatenated per-chunk SHA-256 digests in index order, not over the body: the crate's `body_sha256()`; a mismatch is 554), and keep the commit verdict so a repeated commit or a status query returns it. Read `references/chunked-upload.md` for the checklist, the gateway's behavior, and where to find the reference implementation.

## Deploy & Test

There is no local SMTP gateway. Test by making the gateway's two calls yourself. Your identity deployed the canister, so it is a controller and passes the caller check:

```bash
icp network start -d
icp deploy backend

# 1. RCPT TO for a known mailbox. Expected: (variant { Ok = record {} })
icp canister call backend smtp_request_validate '(record { envelope = opt record { from = record { user = "alice"; domain = "example.com" }; to = vec { record { user = "support"; domain = "example.icp0.io" } } } })'

# 2. RCPT TO for an unknown mailbox. Expected: Err with code = 550 : nat64
icp canister call backend smtp_request_validate '(record { envelope = opt record { from = record { user = "alice"; domain = "example.com" }; to = vec { record { user = "nobody"; domain = "example.icp0.io" } } } })'

# 3. Delivery, with header values as raw as the gateway sends them.
# Expected: (variant { Ok = record {} })
icp canister call backend smtp_request '(record {
  envelope = opt record { from = record { user = "alice"; domain = "example.com" }; to = vec { record { user = "support"; domain = "example.icp0.io" } } };
  message = opt record {
    headers = vec { record { name = "From"; value = " Alice <alice@example.com>\r\n" }; record { name = "Subject"; value = " Hello\r\n" } };
    body = blob "Hi there!\r\n";
  };
  message_id = opt "0193f0a1-2b3c-7d4e-8f90-a1b2c3d4e5f6";
})'

# 4. Delivery without message_id. Expected: Err with code = 501 : nat64, not a trap
icp canister call backend smtp_request '(record { envelope = opt record { from = record { user = "a"; domain = "b.c" }; to = vec { record { user = "support"; domain = "x" } } }; message = opt record { headers = vec {}; body = blob "" } })'

# 5. Expected: (1 : nat64). The Motoko example names this inboxSize and returns nat.
icp canister call backend inbox_size '()'

# 6. A caller that is neither the gateway nor a controller. Expected: Err with code = 530 : nat64
icp canister call --identity anonymous backend smtp_request_validate '(record {})'
```

## Verify It Works on Mainnet

```bash
icp deploy -e ic backend
CANISTER_ID=$(icp canister status backend -e ic --id-only)

# 1. Mail for the canister routes to the gateway. Expected: one or more MX hosts.
dig +short MX "$CANISTER_ID.icp0.io"

# 2. Send a mail to support@<CANISTER_ID>.icp0.io from any mail account, then:
icp canister call -e ic backend inbox_size '()'
```

| Symptom at the sender | Cause |
|---|---|
| `550 5.1.3 Permanent error: Canister <id> does not support SMTP protocol` | `smtp_request_validate` is not exported, misnamed, or not a query, or the `.well-known/ic-smtp-canister-id` handoff names a canister without it |
| `550 5.1.2 Mailbox does not exist.` | `smtp_request_validate` returned 550. Check the local-part match, including case. |
| `550 5.1.3 Permanent error: unauthorized caller` | The caller check does not accept the gateway principal (Pitfall 7) |
| `550 5.1.1 Unknown recipient domain.` | The custom domain is not registered, or the address is not `<canister-id>.icp0.io` |
| Delivery delayed, then a bounce after days | The canister traps, or returns a code outside 500–599, or takes longer than 90 s. Call it directly to see which. |
| `552 5.3.4 Message too big` | The message exceeds the gateway's size limit (see Chunked Upload) |
