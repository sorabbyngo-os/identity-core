# ADR-002 — Audit Logger Chain Integration

## Status: Accepted
## Date: 2026-04-30

## Context
AuditLogger previously only wrote to Python logging. Kenya DPA 2019 Section 41
requires tamper-evident audit records. The sorabbyngo-security repo provides
a SHA-256 hash-chained JSONL audit writer.

## Decision
AuditLogger now writes to the hash-chained ledger when sorabbyngo-security
is available on the Python path. Falls back to Python logging gracefully.

Every audit entry still generates its own SUID (AUD- prefix) — audit IDs
are themselves first-class traceable entities in the system.

## Consequences
- All entity lifecycle events are now hash-chain protected
- Chain integrity verifiable via `python3 audit/verify_chain.py --all`
- Graceful degradation — works without security repo (dev mode)
