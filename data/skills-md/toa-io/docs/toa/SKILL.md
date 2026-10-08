---
name: toa
description: >-
  How to build an application on Toa, the runtime for distributed systems: components, state,
  operations, events, tasks, the HTTP API, identities and access, tests, configuration and
  deployment. Use when working on an application built with Toa.
---

# Building Applications on Toa

How to turn business requirements into a working application on Toa: what to write, which files
to create, how to run and test it. Why the runtime behaves the way it does, and what it
guarantees, is in the [mental model](https://toa.io/model/).

Every article answers "how do I do X?", stands on its own, and links to what it relies on. Find
the one the task needs by its summary below and read that file. Every example comes from the
same application — a small shop with orders and customer accounts.

## Chapter I. First Steps

*From one command to a tested, configured component behind an HTTP API, one small step at a time.*

1. **[Create an Application](start/1.application.md)**
   — summary: what the machine needs; creating an application with one command; starting it;
   the two processes; the first requests; running its tests; the commands of every day; what
   was created and where each file is explained.
2. **[Run It and Make a Change](start/2.running.md)**
   — summary: an operation and its file; restarting after a change; calling an operation from
   the command line; the manifest; an entity and the operations a component inherits; adding a
   property; what a restart generates.
3. **[Create a Component](start/3.component.md)**
   — summary: a manifest with an entity; creating objects by forwarding to `transit`; an
   operation with a business rule; returning and declaring an error; calling it; what a reply,
   an error and an exception look like.
4. **[Expose It over HTTP](start/4.api.md)**
   — summary: the smallest exposition for listing, reading, creating and approving; where routes
   are mounted; the gateway; requests with curl; how a returned error and other failures are
   answered.
5. **[Write a Test](start/5.testing.md)**
   — summary: a scenario that sends http requests and matches responses; the steps the
   application came with; what a scenario runs against; running scenarios; calling an operation
   directly; the stage api; the agent's request text, captures, pipelines and matching.
6. **[Add Configuration](start/6.configuration.md)**
   — summary: declaring a configuration schema and defaults; reading `context.configuration`;
   setting values in the context; one value per environment with the `@environment` suffix;
   where secrets and runtime changes are described.

## Chapter II. Business Logic

*What a component is made of, one requirement at a time: state, operations, refusals, calls, events, and what follows from them.*

1. **[Describe State](logic/1.state.md)**
   — summary: the entity schema, required properties and blank; system properties; associated
   entities and identifiers of your own; moments; storage; every manifest key.
2. **[Write Operations](logic/2.operations.md)**
   — summary: a file is an operation; choosing a type and a scope; declaring input, output,
   concurrency and query; classes and factories; shared code; rules for operation code.
3. **[Refuse a Request](logic/3.errors.md)**
   — summary: returning and declaring an error; handling an error from a call; exceptions and
   their http statuses; deciding not to write with discard; the four outcomes.
4. **[Call Operations and Select State](logic/4.calls.md)**
   — summary: local and remote calls; input and query; criteria, sorting and paging; creating an
   object; versions; deleted objects; trimming the reply; every request property.
5. **[Use the Inherited Operations](logic/5.prototype.md)**
   — summary: transit, observe, enumerate, assign, terminate and the rest; narrowing and
   forwarding them; replacing one; inherited events; a prototype of your own.
6. **[Protect an Invariant](logic/6.guards.md)**
   — summary: a guard file that every write must pass; what a refused write looks like; choosing
   between a guard, the schema and an operation.
7. **[Announce a Change](logic/7.events.md)**
   — summary: an event file with a condition; a payload of your own; trailers; inherited events;
   naming events for consumers outside the application; rules for conditions.
8. **[React to an Event](logic/8.receivers.md)**
   — summary: binding an event to an operation; building the request; skipping events; shared
   operations with arguments; own events; events from other systems; what the operation must
   expect.
9. **[Do Work in the Background](logic/9.tasks.md)**
   — summary: handing a call over with `task: true`; tasks to your own component; getting the
   result; what a task's operation must handle; calls that cannot be tasks.
10. **[Handle Repeated Calls](logic/10.repeats.md)**
   — summary: why an operation can run again; setting instead of adding; skipping by `VERSION`;
   keying a change by what it is for; declaring `once`, how long a call is remembered and why a
   transition that retries does not call it; the `idempotency-key` header; keys for external
   services.
11. **[Call an External Service](logic/11.external.md)**
   — summary: requests with `context.fetch`; address and key from configuration; stubbing the
   provider locally and in tests; retries and timeouts; what a repeated operation means for a
   provider; traces and metrics.
12. **[Write a Multi-Step Workflow](logic/12.workflows.md)**
   — summary: an effect under `continuity` that goes on from the step that failed; starting it as
   a task or from a receiver; what counts as a step; time, randomness and ids from the context;
   what can still repeat; what it needs to run.
13. **[Run Work on a Schedule](logic/13.schedules.md)**
   — summary: pulses at a regular interval and cron schedules under `cadence`; what must be
   configured and run; writing for missed and repeated calls; spreading work over a cycle; per-
   replica pulses; several entries; regions.
14. **[Do Something Later](logic/14.delays.md)**
   — summary: arming a call with `context.delay` and cancelling it; choosing `overdue`; timing
   and discreteness; calls that re-arm themselves; where a delay is refused; the `cadence`
   settings of the Context.
15. **[Read a Large Collection](logic/15.collections.md)**
   — summary: reading a collection as a stream of parts; operations with the `stream` scope;
   tokens and reading only what changed; windows, order and `stop`; what a reader handles;
   turning changes on with images.
16. **[Stream a Reply or an Input](logic/16.streams.md)**
   — summary: answering with a generator or a `Readable` and reading it; operations that take a
   stream with `stream` and the `http` binding; how to call them; what such a call lacks;
   addresses for a local run.
17. **[Keep Something in a Process](logic/17.processes.md)**
   — summary: run commands in `rc/`; `context.state`; releasing in `dispose`; `pause` and
   `resume`; stateful operations called by process name, their failures, timeouts and limits.
18. **[Loops and Read-Only Calls](logic/18.chains.md)**
   — summary: reading and fixing a `LoopException`; `unchained` operations and delays; the trail
   limits; `SafetyException` from a safe operation and under `GET` and `HEAD`; `io:readonly`.
19. **[Use TypeScript](logic/19.typescript.md)**
   — summary: operations in typescript without a build step; generating types from manifests;
   type checking with tsc; the three rules of erased types.
20. **[Indexes and Data Migrations](logic/20.migrations.md)**
   — summary: declaring indexes, unique values and expiry; changing stored data; the rules a
   migration must follow.
21. **[The Operation Context](logic/21.context.md)**
   — summary: everything on the context argument and the article that teaches each member: calls,
   ids and time, where it runs, what extensions add.

## Chapter III. The API

*Serving the application over HTTP: routes, what they accept and return, files, live updates, and tools for AI assistants.*

1. **[Build an API for a Component](api/1.exposing.md)**
   — summary: more routes and methods; the two defaults, no body and no access; where a component
   is mounted and the trailing slash; a scenario that creates and reads; the host; routes of the
   context; the long form.
2. **[Lay Out the Routes](api/2.routes.md)**
   — summary: nested and flat routes; route variables and wildcards; which route answers;
   forwarding; intermediate nodes; how directives are inherited and how to avoid it; shortcuts;
   sharing declarations.
3. **[Map Methods to Operations](api/3.methods.md)**
   — summary: short and long form of a method; which operation suits which method; changing only
   some fields with patch; the body as input; route variables; read-only get; statuses of
   replies; retrying with an idempotency key.
4. **[List with Filters, Sorting and Paging](api/4.queries.md)**
   — summary: the standard parameters; criteria, fixed and open; sort; omit and limit with
   bounds; fixed queries; identifier; text search; projection; parameters of the operation;
   queries of collection streams.
5. **[What a Client Sends and Receives](api/5.protocol.md)**
   — summary: formats and content negotiation; every status; the three kinds of failure; debug;
   headers on every reply and the ray; multipart responses; browsers on other origins; a halted
   deployment; a client's checklist.
6. **[Choose What a Route Accepts and Returns](api/6.io.md)**
   — summary: naming the properties a route returns; narrowing the input; choosing the status
   from the output; throttling by address, route or identity; read-only calls.
7. **[Pass Headers, Language and Host to an Operation](api/7.mapping.md)**
   — summary: headers, route variables, the language, the host, token claims and the raw body as
   input properties; requiring headers.
8. **[Cache Replies and Prevent Lost Updates](api/8.caching.md)**
   — summary: declaring how long a reply is kept; what authenticated requests get; an exact
   value; etag and not modified; writing only if unchanged with the version; a checklist.
9. **[Stream Through the API](api/9.streams.md)**
   — summary: reply streams; keeping a client's copy of a collection current; one value composed
   from a stream; request bodies streamed into an operation and bytes answered; calling one
   particular process; answering with content fetched elsewhere.
10. **[Keep Files in a Storage](api/10.storages.md)**
   — summary: declaring a storage and using it from an operation; entries; put, head, get and
   delete; providers and their options; a storage per environment; secrets; installing a
   provider's sdk.
11. **[Upload and Download Files](api/11.files.md)**
   — summary: a file resource in three declarations; where a file is stored; accepted types and
   the size limit; naming and describing an upload; uploading by url; downloads, ranges and
   variants; the entry; deleting.
12. **[Process an Uploaded File](api/12.workflows.md)**
   — summary: operations called with a reference to a stored file; parallel and sequential steps;
   the multipart reply and one composed reply; steps as tasks; workflows on delete and without
   storing; a scenario that uploads.
13. **[Push Changes to the Browser](api/13.realtime.md)**
   — summary: routing events to keys; serving the stream of a key; an identity's own stream;
   literal keys; reading a stream and reconnecting with a token; rules for the client; redis and
   expiry.
14. **[Call the API as Procedures](api/14.procedures.md)**
   — summary: turning json-rpc on; how a route names a procedure; parameters and results; batches
   and notifications; errors; the rules shared with http.
15. **[Let an AI Assistant Call the API](api/15.tools.md)**
   — summary: turning mcp on and publishing a method as a tool; describing tools; what a tool
   takes and answers; hints; instructions; credentials, anonymous access and browser origins; a
   host of its own; icons; the protocol in brief.
16. **[Describe the API](api/16.discovery.md)**
   — summary: asking a resource with options; the whole tree and its page; what a caller is
   shown; describing resources, methods and parameters; hiding a method.
17. **[Run and Configure the Gateway](api/17.running.md)**
   — summary: running the gateway locally; ports; authorities; ingress, resources and http/2 in a
   deployment; readiness; the client address; the censor; stubs, delays and faults for
   development; every key of the context's exposition.

## Chapter IV. Users and Access

*Signing users up and in, keeping them signed in, and deciding who may call what: owners, staff, other applications.*

1. **[Sign Users Up and In](access/1.identities.md)**
   — summary: the token key; a sign-up route that creates an account and its identity; signing in
   with a username and password; reaching the caller's own account by path or by delegation;
   guests; sign in or up with one request; a scenario that signs up and in; where to go next;
   refusals of a sign-up.
2. **[Manage Passwords](access/2.credentials.md)**
   — summary: rules for usernames and passwords; whether a username is free; changing, adding and
   removing a password; listing the ways to sign in; limiting password guessing; an identity
   without an account; the first administrator; hashing settings; the authentication schemes.
3. **[Keep Users Signed In](access/3.tokens.md)**
   — summary: what a client does with the token; how long a sign-in lasts; signing a user out
   everywhere; token keys and replacing them; custom tokens for scripts limited to roles and
   paths; acting for another identity; listing and revoking custom tokens.
4. **[Sign In with Google or Apple](access/4.federation.md)**
   — summary: trusting a provider; signing in with its token; creating the account together with
   the identity; reading claims into the input; several client ids; exchanging an authorization
   code; adding, listing and removing providers of an account; a provider's account as the first
   administrator; why a token was refused.
5. **[Sign In with an Emailed Code or a Passkey](access/5.passwordless.md)**
   — summary: an operation that gets a code and emails it; signing in with the code; making an
   address a way into an account; moving a sign-in to another device; limits on codes; adding a
   passkey, signing up and signing in with one; listing and removing passkeys; passkey settings
   and refusals.
6. **[Restrict Who Can Call a Route](access/6.access.md)**
   — summary: routes are closed until they say who; a customer reaches only their own orders; a
   scenario with the refusals; several ways in and why nesting cannot narrow; public routes; any
   signed-in user; roles; several conditions at once; who may send a property; asking for the
   password again; recording who called; admitting by a provider's token; access for the whole
   application; what a caller is shown; all directives.
7. **[Give Staff Wider Access](access/7.roles.md)**
   — summary: requiring a role on a route; the first administrator; granting a role; when a
   change reaches a signed-in user; a scenario with the principal; naming roles from general to
   specific; roles per resource; reading roles; letting staff pass roles on; revoking; banning a
   user; the system roles.
8. **[Serve Several Domains and Screen Requests](access/8.authorities.md)**
   — summary: authorities and hosts per environment; users belong to an authority; telling an
   operation which domain was asked; the header that holds the client address; refusing requests
   by country; requiring a header; scenarios for the refusals.
9. **[Let Another App Act for a User](access/9.oauth.md)**
   — summary: turning the authorization server on; which programs are known; the four steps of
   the consent page; what the program gets; limiting a token to roles and to one entry;
   connecting an AI assistant over MCP; showing and revoking what a user allowed; a scenario of
   the whole exchange; the requests a program makes; settings.
10. **[Users and Access Reference](access/10.reference.md)**
   — summary: every identity resource with its access; operations an application calls;
   directives; annotation keys; configuration of the identity components; secrets; statuses a
   client handles.

## Chapter V. Platform Features

*Features the platform brings and a component switches on: settings, a cache, coordination, telemetry, a map of itself.*

1. **[Turn On a Platform Feature](platform/1.extensions.md)**
   — summary: declaring an extension in the manifest; setting it up in the context; values per
   environment; the full form; supplied extensions and connectors; ports that are taken.
2. **[Keep Settings and Secrets out of the Code](platform/2.configuration.md)**
   — summary: secret values and `$NAME` references; `unwrap`; supplying secrets locally and to a
   deployment; schema, defaults, nested values, prototypes; values in the context; resources of
   the values service; trying a component with other values.
3. **[Change a Setting without Redeploying](platform/3.configuration-values.md)**
   — summary: creating, reading and resetting configuration over http; roles; the configuration
   page; changing values from an operation; the change event; what happens on the next deployment
   and after a schema change.
4. **[Cache Something All Replicas Share](platform/4.stash.md)**
   — summary: turning the stash on; redis commands on `context.stash`; storing objects; keys
   private to a component; a redis per component; behaviour when redis is away.
5. **[Coordinate Replicas](platform/5.shared-decisions.md)**
   — summary: letting only one replica do something at a time; splitting work between replicas;
   limiting calls across replicas; the `atomicity` annotation; behaviour without redis.
6. **[Write Logs](platform/6.logs.md)**
   — summary: writing entries with `context.logs`; reading them on the console; finding
   everything about one request; levels per environment and per component; sending entries to a
   backend; finding why a process failed; writing good entries.
7. **[Follow a Request through the Application](platform/7.traces.md)**
   — summary: seeing spans on the console; what is traced without code; adding spans with
   `context.span`; sending traces to a backend; sampling; tracing the start of a process.
8. **[Count Things and Alert on Them](platform/8.metrics.md)**
   — summary: declaring and recording a counter; turning metrics on; labels; histograms and
   gauges; declaration reference; choosing intervals, buckets and labels; the metrics recorded
   for every application.
9. **[Send Telemetry to Grafana](platform/9.exporting-telemetry.md)**
   — summary: wiring logs, traces and metrics to tempo, prometheus and loki; linking traces and
   logs; the whole `telemetry` annotation; `otlp` exporter options; loss and outages; resource
   attributes; the readiness probe.
10. **[See What Is Deployed and How Components Talk](platform/10.introspection.md)**
   — summary: the topology page and api; nodes and observed edges; leaving a component out; the
   `introspection` annotation; what to use the graph for.
11. **[Change the Storage, the Transport or the Language](platform/11.connectors.md)**
   — summary: the default storage and what it asks of you; storing nothing; the broker and
   brokers of other systems; the http binding for streamed calls; shell scripts as operations.
12. **[Point the Application at Its Database, Broker and Cache](platform/12.addresses-and-credentials.md)**
   — summary: one address for everything; addresses per environment, namespace and component;
   several addresses under one key; credentials locally and as deployed secrets; secret names.
13. **[Write an Extension of Your Own](platform/13.own-extensions.md)**
   — summary: an aspect of your own; declaring and calling it; annotations and deployment
   variables; validating declarations; tenants, services and residents; pausing; a storage of
   your own.

## Chapter VI. Shipping

*From "it works on my machine" to production: describe the application, deploy it, release new versions safely and look after it.*

1. **[Describe the Application](shipping/1.context.md)**
   — summary: the context file; name and version; addresses of the broker and the database; keys
   of connectors and extensions; events another application reads; runtime settings; every top-
   level key.
2. **[Give Each Environment Its Values](shipping/2.environments.md)**
   — summary: the `@environment` suffix at any depth; the local environment and `.env`; several
   local environments; derived environments as a chain; default environment of each command.
3. **[Decide What Runs Together](shipping/3.compositions.md)**
   — summary: grouping components into compositions; replicas; cpu and memory; extension services
   inside a composition; ports; leaving components out of a deployment; one process for
   everything; how to group.
4. **[Deploy](shipping/4.deployment.md)**
   — summary: what must exist before the first deploy; the keys a deploy needs; `toa deploy` and
   what you see; checking the result; options; what gets deployed; start and stop limits;
   ingress; single-image deployment; pipelines; running without kubernetes.
5. **[Build Images](shipping/5.images.md)**
   — summary: the registry; building and pushing; tags; what goes into an image; platforms;
   private registries; base images; extra build steps and arguments; private npm registry;
   published service images; registry retention.
6. **[Supply Secrets](shipping/6.secrets.md)**
   — summary: what is a secret; listing what a deployment needs; putting secrets in the cluster;
   the check before a deploy; changing a value; secrets for a local run; names of credential
   secrets; checklist for a new environment.
7. **[Release a New Version](shipping/7.upgrades.md)**
   — summary: what to do when you change code, add an operation, add a required input, remove or
   rename an input, change the entity, add a migration or change an event; changes that cannot be
   rolled; going back; the component map and versions.
8. **[Run in More Than One Region](shipping/8.regions.md)**
   — summary: declaring regions and ranks; requirements; concurrent writes in two regions;
   writing components for several regions; adding a region step by step; adding a component
   later; removing a region.
9. **[Stop Everything for Maintenance](shipping/9.halt.md)**
   — summary: turning halt on and its limits; requesting a halt over the gateway; what you and
   clients see; `pause` and `resume` run commands; choosing the numbers; deploying a release that
   cannot be rolled; rehearsing.
10. **[Look After a Running Application](shipping/10.operating.md)**
   — summary: what is running and at which version; a pod that does not become ready; a message
   that keeps failing and the parked queue; events that are not published and outbox settings;
   rolling back; changes without a release; an isolated second copy; alerts to have.
11. **[The CLI](shipping/11.cli.md)**
   — summary: installing; common options; every command with its arguments and options, grouped
   as preparing, running, inspecting, building and deploying, secrets and the cluster; variables
   the cli reads; exit codes.

## Chapter VII. Patterns

*How typical problems are solved: when to call and when to announce, what repeats, races and late messages ask of the code, and how to say no.*

1. **[Call, Event, or Task](patterns/1.call-event-task.md)**
   — summary: the one rule for choosing; what goes wrong with calls only; what a call, an event
   and a task each give; a table of situations; the same operation called on one path and
   received on another.
2. **[Reply Before the Work Is Done](patterns/2.reply-first.md)**
   — summary: storing what is wanted and replying; an event of your own that starts the slow
   part; writing the result and the failure into state; telling the client; why not a task from
   the operation.
3. **[Events Worth Subscribing To](patterns/3.events.md)**
   — summary: conditions that fire when a fact becomes true; trailers for what the states cannot
   say; payloads as contracts; receivers that filter and translate; why not subscribe to
   `updated`.
4. **[The Same Message Twice](patterns/4.repeats.md)**
   — summary: why messages repeat; setting and looking before writing, by itself or under a
   key; `once` for what accumulates and how long it remembers; a record under the other
   system's id; deduplicating where the effect is.
5. **[Two Writers at Once](patterns/5.concurrency.md)**
   — summary: the read-check-write race; one transition with `concurrency: retry`; keeping the
   fact in one object; what a second run repeats; forms edited by people; when a lock is the
   answer.
6. **[Messages Out of Order](patterns/6.order.md)**
   — summary: why arrival order means nothing; carrying the version and skipping older messages;
   treating an event as a signal and asking the owner; values that only move forward; not
   creating the dependency.
7. **[Saying No](patterns/7.refusing.md)**
   — summary: five ways to refuse and what each answers; schema and route, guard, returned error,
   success without a write, exception; refusals nobody hears; passing a refusal on; refusing
   before the work and settling after.
8. **[Ask the Owner, or Keep a Copy](patterns/8.ownership.md)**
   — summary: using a fact another component owns; a call to the owner that keeps the rule;
   freezing an answer; a copy kept current by a receiver; entities that need no creation; a limit
   checked where its counter lives.
9. **[Keep Data About a Customer without Creating It](patterns/9.associated.md)**
   — summary: why records made at sign-up do not hold; an entity identified by the customer's
   id; a blank that says what is true before anything happened; what disappears; what a list
   and an assignment do not do; when existence means something.
10. **[A Process Across Components](patterns/10.processes.md)**
   — summary: a business process of several steps without a transaction; a status for every
   stage; steps that react to events and report back; the owner of the process decides; failure
   as one more step, with compensation; steps that repeat, race, refuse or never finish.
11. **[Reservations](patterns/11.reservations.md)**
   — summary: setting money aside now and taking or releasing it later; `hold`, `settle` and
   `release` keyed by the order; asking before the work and settling after it; the late hold; a
   guard for the sum; when a debit with a refund or charging afterwards is enough.
12. **[Work on the Clock](patterns/12.time.md)**
   — summary: expiry as a stored moment compared on use; counters that renew at their next use;
   sweeps on a pulse that select by state; a delay per object; reconciling a copy with an outside
   truth; finding work that stopped.
13. **[A Gateway to an External Service](patterns/13.gateways.md)**
   — summary: one entity-less component that alone holds a provider's keys; operations and errors
   in the application's words; an error for "ask again later"; a stub when the key is empty; a
   composition so secrets reach one process.
14. **[Receiving Webhooks](patterns/14.webhooks.md)**
   — summary: an anonymous route with the raw body; verifying the signature by a call; storing
   every notification and announcing it; one record per provider object under a derived id; why
   `once` is not enough; refusing so the provider sends again.
15. **[Mirroring a Provider's Object](patterns/15.mirrors.md)**
   — summary: a notification as a signal to read again; an associated mirror merged by a retried
   transition; signalling from the webhook, the customer's return and the shop's own change;
   announcing only what changed; a copy that refuses older reads; expiry as a date.
16. **[A Wallet and Its Ledger](patterns/16.wallet.md)**
   — summary: a stored balance in an associated entity; `credit` as a `once` transition and
   `debit` keyed by what it is for, both with `concurrency: retry`; a guard; trailers that say
   what moved; ledger lines derived from the wallet's event under `id:VERSION`; a unique index;
   corrections as new lines.
17. **[Taking a Payment, End to End](patterns/17.payments.md)**
   — summary: a checkout started by a call; the result by webhook, by the customer's return and
   by a sweep, all ending in one record; consequences fanned out by events to the wallet, the
   ledger, the receipt and the page; which mechanism at each step; failures walked through;
   limits.
