---
name: test-proof-debt-audit
description: Audit one named behavioral claim and the test, validator, benchmark, or gate cited as proof, or audit a named set of existing tests for redundant or low-value tests. Do not use for ordinary implementation, writing new tests, failing tests, weak coverage, or the presence of mocks.
---

# Test Proof Debt Audit

Audit only the claim and proof route, or the test set, named by the user. Do not
turn ordinary implementation, a failing test, weak coverage, or the presence of
mocks into a repository-wide proof audit.

1. Name the claim and production behavior that makes it true.
2. Identify the cited proof.
3. State what the proof actually observes: behavior, machine-readable contract, performance, or proxy text/metadata.
4. Apply deletion sensitivity: would it still pass if the claimed behavior disappeared?
5. Check whether expected values come from independent truth.
6. Choose `keep`, `replace`, `demote`, `closeout-only`, `delete`, or `escalate`.

Treat history-only expected values as proof debt. A current test must not name
or pin a retired width, tag, field, version, byte sequence, or identifier merely
to prove its rejection. Ask whether the test could be derived from the current
contract without repository history. Replace it with current-boundary cases,
demote it to closeout-only evidence, or delete it unless the historical value
is itself a current public machine/security contract.

For a redundancy audit of a named test set, map each contract to the one test
that owns it at the strongest boundary. A second test of that contract stays only
if it can fail where the owner cannot, for example across a process, network, or
lifecycle boundary the owner never crosses. Any other second test is a duplicate:
merge its case into the owner's table or fixture, or delete it.

Before choosing `delete`, apply the retention bar. Keep a test that independently
enforces a current public API, protocol, config, storage, security, or
architecture contract (a history-only value stays under the rule above),
observable call ordering, or a regression with a credible failure mode, even when
it looks like the implementation. Being static or slow never justifies a delete.
A retained test that is red on the baseline may be exposing a product bug:
reproduce it and route the owner fix rather than removing the test.

A `delete` needs a filled record; any gap turns it into `keep` or `escalate`:

- where the test lives and what it is called;
- the regression it would catch, stated concretely;
- the production callers, if any, of the seam it exercises;
- which remaining test at the owner boundary still catches that regression, or why nothing needs to;
- why the test was written, from its commit history;
- what else can go once it is gone, in production or test support;
- the risk, and the narrow command that validates the removal.

Proxy evidence can support lint or closeout but cannot prove runtime behavior. Mocks and replicas prove only their own boundary unless the claim is explicitly about that boundary.

Report location, claimed behavior, actual observation, disconfirming scenario, and
smallest replacement. Weak proof does not authorize an architecture redesign. If
the user requested assessment only, report and stop; modify proof or production code
only when requested.

Read [references/catalog.md](references/catalog.md) only for a broad user-requested audit, a redundancy audit, or when concrete replacement examples are needed.
