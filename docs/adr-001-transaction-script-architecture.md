# ADR-001: Transaction Script Architecture

## Status

Accepted

## Context

This is a read-only scraper/ETL (Extract, Transform, Load) tool that fetches dump metadata from
[WDumper](https://wdumps.toolforge.org), enriches it with Wikidata labels, and outputs CSV rows
for analysis in a Jupyter notebook. The domain logic is a single linear pipeline: fetch a list of
dump IDs, fetch each dump's spec, resolve labels, render output columns.

The pipeline calls three external services: the WDumper HTML page (to find the latest dump ID),
the WDumper JSON API (to fetch individual dump specs), and the Wikidata Action API (to resolve
property and entity IDs to human-readable labels). Each service has different failure modes,
rate limits, and caching needs, so they cannot share a single fetch strategy.

Label resolution can be optional: the tool should produce valid CSV output without it for ease
of testing or if Wikidata is unavailable. At the same time, the same Wikidata ID can appear
across many dump specs, so labels must be resolved in a single batch rather than one API call
per dump. These constraints make it important that the label-fetching concern is decoupled from
the pipeline orchestration and can be swapped out — or omitted entirely — without changing the
core scraping logic.

The notebook is the primary user-facing interface, but it is a poor home for orchestration logic:
notebook cells cannot be unit-tested, they blur the line between configuration and implementation,
and they make the scraping logic hard to reuse or refactor independently. The architecture must
keep the notebook as a thin configuration and output layer, with all pipeline logic living in a
testable Python package.

The project therefore needs a clear architectural style that satisfies all of these constraints
while remaining simple to follow.

## Decision

Adopt a **Transaction Script** architecture (Fowler, *Patterns of Enterprise Application
Architecture*): each pipeline step is a plain procedure that reads inputs, does work, and returns
outputs. There is no rich domain model, no event bus, no shared mutable state.

The structure is:

```
WDumpsScraper (Facade)
  -> DumpsInfoLoader (Transaction Script)
    -> WDumperClient, WikidataClient (Gateways)
    -> Scraper (Gateway)
```

### Roles

| Class | Role | Responsibility |
|---|---|---|
| `WDumpsScraper` | Facade | Wires up all collaborators; exposes a single `run()` method so the notebook stays thin |
| `DumpsInfoLoader` | Transaction Script | Orchestrates the pipeline: fetches all dump specs concurrently, extracts resource IDs, resolves labels, and returns structured results |
| `Scraper` | Gateway | Fetches and parses the recent-dumps HTML page to extract the latest dump ID |
| `WDumperClient` | Gateway | Fetches individual dump specs from the WDumper JSON API |
| `WikidataClient` | Gateway | Resolves Wikidata IDs (e.g. `P31`, `Q5`) to human-readable English labels via the Wikidata Action API |

**Pure functions** in `rendering.py` handle stateless transformations (rendering filter specs to
human-readable strings). No side effects, no dependencies on instance state.

## Alternatives considered

A richer domain model (e.g. domain objects for `Dump`, `Spec`, and `Label`) was ruled out because
the pipeline has no business rules that act on these objects — they are fetched, transformed, and
rendered in a straight line. The added complexity would not be justified. A fully
service-oriented or event-driven approach was similarly rejected as over-engineering for a
single-pipeline, read-only tool.

## Consequences

**Benefits:**

- Simple to follow: data flows one direction through the pipeline.
- Easy to test: gateways can be mocked; pure functions tested in isolation with hand-crafted
  inputs; the Transaction Script tested end-to-end with stubbed collaborators.
- Low ceremony: no framework, no dependency injection container.
- The notebook is reduced to configuration and output cells; all testable logic lives in the
  package, satisfying the constraint that orchestration must not live in the notebook.

**Risks:**

- The Transaction Script (`DumpsInfoLoader`) can accumulate concerns over time and grow into a
  "God Class". Mitigated by keeping fetching in gateways, rendering in pure functions, and
  label-fetching behind a swappable interface.
- Not suitable if the project ever needs a rich domain model, event-driven flows, or multiple
  write paths. That is unlikely for a scraper.