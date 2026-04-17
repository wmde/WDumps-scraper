# ADR-001: Transaction Script Architecture

## Status

Accepted

## Context

This is a read-only scraper/ETL tool that fetches dump metadata from
[WDumper](https://wdumps.toolforge.org), enriches it with Wikidata labels, and outputs CSV rows
for analysis in a Jupyter notebook. The domain logic is a single linear pipeline: fetch a list of
dump IDs, fetch each dump's spec, resolve labels, render output columns.

The project needs a clear architectural style that keeps the codebase simple, testable, and easy
to follow.

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

## Consequences

**Benefits:**

- Simple to follow: data flows one direction through the pipeline.
- Easy to test: gateways can be mocked; pure functions tested in isolation with hand-crafted
  inputs; the Transaction Script tested end-to-end with stubbed collaborators.
- Low ceremony: no framework, no dependency injection container.

**Risks:**

- The Transaction Script (`DumpsInfoLoader`) can accumulate concerns over time and grow into a
  "God Class". Mitigated by keeping fetching in gateways, rendering in pure functions, and
  label-fetching behind a swappable interface.
- Not suitable if the project ever needs a rich domain model, event-driven flows, or multiple
  write paths. That is unlikely for a scraper.
