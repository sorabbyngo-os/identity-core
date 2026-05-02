# ADR-001 — SUID Format Design

## Status: Accepted
## Date: 2026-04-30

## Context
Every entity in the Sorabbyngo ecosystem needs a unique, traceable identifier.
Requirements: human-readable, forensically useful without DB access, tamper-detectable,
Africa-region-aware, URL-safe.

## Decision
Format: `{PREFIX}-{YYYYMMDD}-{REGION}-{RANDOM6}-{CHECK2}`

- PREFIX: 3-char entity type code — permanent, never reused
- DATE: UTC creation date — forensically embedded
- REGION: African county/district code (KE001-KE047, UG001, etc.)
- RANDOM: 6-char cryptographically random suffix (secrets.choice)
- CHECK: 2-char weighted checksum — detects any single-component tampering

## Consequences
- IDs are self-describing — entity type, date, region readable without DB
- Checksum enables tamper detection in transit and storage
- 36^6 = 2.17 billion possible suffixes per prefix/date/region combination
- No sequential enumeration possible — secrets.choice provides CSPRNG
