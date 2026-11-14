# AGENTS.md

Hard rules for agents working in this repo. Gates enforce them.

## Discipline

1. **Numbers come from measurement only**; keep the reproduction command next to each
   assertion. A sentence without a reproduction command is history, never current state.
   Ledger `cmd` entries in `build/FACTS.json` are executed verbatim by
   `zreflect/check_facts_replay.py` (stdout must equal the bare value).
2. **Each number is produced once**. In documents, cite `[[key]]`; never hand-copy a
   number. `zreflect/check_facts.py` blocks bare numbers and broken references in
   live-state prose.
3. **Readable ≠ usable**. `verified` here comes from `--probe` (inspecting tar
   contents for m/oct); it does not mean "runs when installed". Anything about real
   usability must be tested in the real environment.
   - **"Probe found nothing" ≠ "it does not exist"**: before claiming something is
     missing or broken, first show a positive control proving the probe can detect
     existence when present. Otherwise you are reporting a probe defect, not a product
     defect.
   - **Verify call surfaces against the artifact's exports**: when auditing tools or
     adapters, check the artifact's `.d.ts` or runtime `typeof`, not just the source
     code.
   - **A declared injection seam is not wiring**: every "declared injection surface"
     change needs an assertion that reads the real composition-root source. Unit
     tests, type checks, and builds cannot catch a missing injection — their fakes
     are always reachable.
   - **One counterexample does not condemn a class**: before judging "all members of
     class X cannot do Y", list every member and check each one.
4. **Assertions must be falsifiable**: every new contract ships at least one negative
   assertion (the error case must error). Every gate ships a `--selftest` with three
   case classes: normal passes / violations fail / empty input fails.
5. **Assertions have a lifecycle** (measured / inferred / retracted):
   - live-state documents contain measured facts only;
   - inferences go to `questions/` as open questions with a runnable settling command;
   - retracted claims go to `build/retractions.json` (`zreflect/check_retractions.py`
     fails when they reappear in declared live-state docs; the scan surface is bounded
     to declared docs — a known gap, stated here).
6. **Know what "live state" means** before editing documents (`zreflect/living.py`):
   numbers inside history sections declared via `REFLECT_HISTORY_SECS` describe the
   past; lines carrying history/retired/retracted markers describe the past;
   everything else is live state and is reconciled against the ledger by gates.
7. **Read the collector contract** (`zreflect/collect.py`) before writing `measure()`:
   read persistent disk only, never introduce self-changing inputs (wall clock, HEAD
   sha ⇒ `--check` never converges), report unavailable instead of fabricating 0,
   cache expensive measurements.

## Repo-specific red lines

- **Role = production adapter**: package dossiers (`packages/`), supply recipes
  (`recipes/`), port copy (`port/`), facts-system operation, and the content-contract
  edge toward the UI (state semantics: four-state meanings, `content` honesty, version
  policy, license ledger). Do not touch the engine contract (host's), do not define
  distribution-contract semantics (Static-Contract's), do not run runtime endpoints
  (the only same-origin endpoint is the host site).
- **The two protocols are fully disjoint**:
  - **Distribution protocol** (release contract: `manifest.json`, chunks,
    `catalogue.json` `base`): how bytes are published and fetched.
  - **Market protocol** (content contract `content-list`: `name`/`version`/`deps`/
    `content`/`consumer`/`role`/`form`): what the market offers, what works, for whom.
  - Rule: no field of the market table may come from a distribution-side unique id
    (`tag`/`base`/`manifest_sha256`); the distribution contract must not reference
    `name`/`version`/`deps`/`consumer`.
  - **`product` in a release manifest is a delivery coordinate** ("which byte group
    within this release"), never a lane/product identity source. Consumer-side
    hand-written maps from lane names to `product` are the same disease. Lane
    identity is declared by the **engine contract** (host ↔ UI); this repo does not
    touch it and does not assign an existing content-contract field to that job.
    The `arch` of `kind:"engine"` entries (`w64`/`omc` lane index keys) and the
    distribution-side `arch` (`wasm64`) are homonyms with different meanings — no
    unification, no new fields (the authority is the host's
    `validate-content-list.py`, which widens the enum per kind: "index key, not a
    version axis").
- **Port origin = host**: schema + validator live in the host repo
  `build/extra-content/`; `port/` here is a copy, kept in sync, host wins.
- **Ownership ≠ delivery**: ownership (who defines semantics) = this repo; delivery
  (what the UI actually receives) = host (assembled site tables); deep-semantics
  conversation goes through `mail/`.
- **No bytes in git**: this repo stores metadata and recipes (URL + sha256) only.
  "No bytes" = no content bytes in git history; GitHub Release assets are fine (they
  are the publication surface, and immutable tags keep bytes reachable). Red lines
  that still hold: never `git add` tar/zip/wasm/whl into this repo; never provide a
  runtime endpoint; never reassign another repo's artifact ownership in the name of
  being an origin.
- **Never modify the host repo** (path iron rule); the host maintains its own
  consumption surface.
- **Whitelist .gitignore**: every new file/directory needs a matching `!path` line,
  otherwise it stays invisible to git. `!pattern` does not support trailing comments.
- **If upstream bytes are not on this machine, the fact is not written** (never
  fabricate 0 as "measured").
- **The repo tip never enters the ledger** (it changes every commit ⇒ `--check`
  never converges).

## Cross-agent mail (`mail/`)

- `mail/` is the inbox (letters addressed to this repo), append-only; rules in
  `mail/README.md`.
- Answer point by point (`A1`/`A2` aligned to `Q1`/`Q2`); state changed paths
  explicitly in replies.
- Disagreement is never silent: state "disagree" plus the criterion.
- Conclusions from letters that change this repo's role or contracts go into the
  live-state docs (`README.md` / `AGENTS.md` / `STATE.md`) — only live state is
  gate-reconciled.

## Defect reports to Einfacht go through GitHub issues

Upstream Einfacht is outside the Octave cluster mail system; report via its GitHub
issues using its downstream-feedback issue shape (title prefixed with the reporting
repo and what was measured). The delivery channel is chosen by the receiver, never
inferred by the sender.

## Reproduction commands (facts-system health)

```bash
python3 build/facts.py --render-doc STATE.md --check     # machine blocks fresh (run via the wrapper)
set -a; source reflect-hooks/Einfacht.env; set +a        # gate knobs (bare registry runs = false reds)
python3 zreflect/registry.py --run commit                  # ran/off/failed counts
# Run gates-selftest with both knobs unset (see CI notes) and in a clean shell:
# sourcing the env file in the same command chain leaks host knobs into harness
# fixtures (false rename_failed reds).
env -u REFLECT_NAKED_MIN -u REFLECT_MEASURE_MODULE sh gates-selftest.sh  # platform selftest
REFLECT_FACTS=build/FACTS.json python3 zreflect/check_facts_replay.py
# Repo-level "next round" shell (never registered in user-level hook config):
printf '%s' '{"cwd":"'"$PWD"'"}' | .kimi-code/hooks/kimi-hook
```

## Tool and contract behaviors

- **Test git hooks the way git runs them** (`./reflect-hooks/pre-commit`, not
  `sh reflect-hooks/pre-commit`): under `sh` the `$0` derivation fails and
  `Einfacht.env` is silently skipped, so the replay gate reports a missing ledger.
- **CLIs that mutate live state require explicit flags**: a script whose default
  action rewrites published releases must refuse with usage and a non-zero exit
  when its guard flags are absent.
- **`tools/` here is shared**: other repos' CI clones this repo's main to run the
  validators, so changing a tool is changing someone else's build — verify against
  real artifacts before landing, keep the two-step split (generator never touches
  licenses; the upgrade tool is a separate verified step), and after any change run
  the tool against another repo's real published data, not just local fixtures.
- **The catalogue has a dead-link window by design**: it is derived on a timer, so
  after an upstream deletes an old tag the catalogue points at the missing tag until
  the next run. Consumers must fall back to the next entry when a manifest fetch
  fails; never start from the first entry unconditionally.
- **`license.url` must point at a page with substantive terms**: an HTTPS URL that
  returns an empty page passes a shape check, so the criterion is license keywords in
  the page body. When an upstream package has no central license text, state that
  fact instead of pointing at a placeholder.
- **Strings used for matching come only from the side being matched**: never trim,
  beautify, or prefix keys (e.g. `entry.name` stays exactly as the manifest
  declares), and never fabricate normalization examples — a wrong example gets
  copied.
- **For `form:"tree"`, `url` / `sha256` / `size` point at three different objects**
  (the unpacked entry file / its hash / the whole directory's bytes), and a tree
  hits a release only when its entry file is also a standalone entry; otherwise fall
  back to the site path and log why. Check every member of a class before generalizing.
- **Comparing two payloads: sort, then compare sets** — entry order is not content.
  Report codec-shape differences separately.
- **Selftests must catch hollowed assertions**: meta-tests, mutation checks, and
  fail counters all miss a `t(label, True)` rewrite; the effective defense is a
  static audit of source (an assertion's condition may not be a literal bool), and
  that audit is itself covered by the selftest.
- **Syncing shared upstream tools is a release**: run the selftest, regress against
  real published data, and prove the new criterion rejects what it should — a stale
  tool pinned on main blocks downstream repos that gate on the selftest count.



## Push and read path

- The remote is **split**: `fetch` = `https://github.com/ArchivalEra/Octave-Extra-Content.git`
  (read-only PAT via the gh keyring — silent, no approval); `push` =
  `ssh://git@github-ArchivalEra/ArchivalEra/Octave-Extra-Content.git` (SK key via the
  akr FIDO2 agent + phone MFA approval).
- **Never point a fetch URL at an ssh:// URL** — every ssh fetch fires a phone
  approval and is forbidden. Reconciliation prefers `gh api`; plain `git fetch` over
  HTTPS is the fallback; `gh repo sync` is never used (it needs write scope and
  returns 403 under a read-only PAT). The SSH aliases (`github-ArchivalEra` /
  `github-PlumHelper`) exist for push only.
- The push gate is the push itself: the SK key is signed via the akr FIDO2 agent and
  the owner approves on the phone. Approval does not flow through the cross-repo
  coordination channel (`wo-u` carries task assignments and rulings only) — instead,
  run the code-review skill on your own changes, write the change description plus
  the review conclusion into your session's final output (the commit message carries
  them too), then stop; the owner patrols session outputs and replies with approval.
- Configure remotes and proxy per this repo's own Einfacht env; do not copy another
  repo's config.

## CI notes

- `.github/workflows/quality-assessment.yml` runs the same existing checks
  (no new lint rules); the replay gate is **skipped honestly** there — several
  ledger cmds hash local byte caches and one needs gh auth. Locally it always runs.
- `gates-selftest` must always run with
  `-u REFLECT_NAKED_MIN -u REFLECT_MEASURE_MODULE` (locally and in CI): the data
  layer lives at repo root, so harness fixtures with renamed files fail to resolve
  the host measure module when that knob is set.
- `REFLECT_REPLAY_TIMEOUT` is raised above its default because one ledger cmd
  (`releases_published`) calls the GitHub API; the short default produces flaky
  false reds.
- shellcheck runs with the allowlist in `.github/shellcheck-allowlist.md` (every
  excluded rule has a written criterion; do not add `-e` codes without updating it).
