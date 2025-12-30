---
Title: "RFC 0001: ASSISTANT_CONTEXT — Minimal file format for assistant-human session continuity"
Author: "Francisco Javier"
Date: 2025-12-30
Status: "Draft (Request for Comments)"
Version: "0.1"
---

Abstract
--------

This document specifies a minimal, machine-friendly file format, named `ASSISTANT_CONTEXT`, intended to persist the essential context required for automated assistants (AI agents) and human collaborators to resume work across sessions. The aim is to provide a small, interoperable payload that contains metadata, a concise action log, and next steps so that agents can continue tasks without re-discovering prior state.

Motivation
----------

Automated assistants increasingly interact with versioned repos and local workspaces. Without a standardized, explicit context artifact, subsequent sessions must re-scan repositories and infer intent, increasing latency and fragility. A small file with a structured frontmatter plus a human-readable body reduces ambiguity and enables simple tooling to continue previous tasks reliably.

Scope
-----

This RFC defines only a minimal format appropriate for per-workspace or per-task context. It does not attempt to standardize complex provenance systems, credential management, or full-task ontologies.

Specification
-------------

File name and placement
- Recommended filename: `ASSISTANT_CONTEXT.md` or `ASSISTANT_CONTEXT.yaml`.
- Location: co-located in the working folder or in a well-known folder such as `.assistant/` or `tools/assistant/`.

Frontmatter (YAML)
- `id` (string): unique identifier for the context instance.
- `created_at` (string, ISO 8601): creation timestamp.
- `updated_at` (string, ISO 8601): last updated timestamp.
- `user` (string): human owner (name or identifier).
- `location` (string, optional): human location context (city, country).
- `purpose` (string): short description of the context purpose.
- `files_changed` (list of strings): files created or modified by the assistant.
- `next_steps` (list of strings): actionable next items.
- `status` (enum): one of `active`, `paused`, `completed`.

Body (human-friendly)
- A brief chronological log of actions and decisions.
- Commands to verify or reproduce results.
- Pointers to logs or artifacts.

Examples
--------

See `tools/crontab-custom-ia/ASSISTANT_CONTEXT.md` in this repository for a concrete example.

Security Considerations
-----------------------

The format may reference secrets (e.g., tokens) or credentials; implementations MUST NOT store sensitive secrets in plaintext inside `ASSISTANT_CONTEXT` files. Any pointers to credentials MUST reference secure stores (environment variables, OS keyring, or secret managers).

Privacy Considerations
----------------------

The file may include identifiers or user metadata; treat it as repository data and apply the same privacy policies as other repository content.

Interoperability
-----------------

The format intentionally remains small and simple to enable diverse assistant implementations to read and update the file. Parsers should tolerate missing fields and preserve unknown fields.

Process for comments (Request for Comments)
-----------------------------------------

This document is published as RFC draft in this repository. To propose changes or discuss the standard:

1. Open a GitHub issue titled "RFC-0001: comment: <short subject>" and reference this file's path `tools/rfcs/RFC-0001-ASSISTANT_CONTEXT.md`.
2. Submit a pull request with suggested edits to the RFC file. Use the PR to discuss the change.
3. Major revisions may result in an incremented version (`0.2`, `1.0`, ...).

Acknowledgements
----------------

This document was produced collaboratively (AI-assisted drafting + human review) and first published by Francisco Javier on 2025-12-30.
