---
og_image: og-image-1200x630.png
image: "og-image.svg"
tags:
title: "Proposal: ASSISTANT_CONTEXT standard for continuity between sessions"
date: 2025-12-30T12:30:00+01:00
draft: false
layout: post
author: "Francisco Javier"
---
---
Link to formal draft (RFC): [RFC-0001: ASSISTANT_CONTEXT](../../tools/rfcs/RFC-0001-ASSISTANT_CONTEXT.md)

Process for comments (Request for Comments):

- Open an issue in the repository with the title "RFC-0001: comment: <summary>" or run `tools/rfcs/open_rfc_issue.sh` locally with `GITHUB_REPOSITORY` and `GITHUB_TOKEN` in your environment to create the issue automatically.
- You can also send a Pull Request with the change proposal on `tools/rfcs/RFC-0001-ASSISTANT_CONTEXT.md`.

This is a draft proposal for a small standard that allows automated assistants (AI) and their users to maintain continuity between sessions.

Motivation
- When an assistant and a human work iteratively on a repository or on local tasks, it is useful for a standard file, human- and machine-readable, to exist that contains the minimum context necessary to resume work.

Minimum proposal (YAML frontmatter):
- `id`, `created_at`, `updated_at`, `user`, `location`, `purpose`, `files_changed`, `next_steps`, `status`.

Use
- The assistant creates or updates `ASSISTANT_CONTEXT.md` in the working folder.
- The file includes a brief history, verification commands and links to key files.

Advantages
- Makes it easier for different agents (human or automatic) to resume work without losing steps.
- Serves as a minimum contract for AI-assisted collaborations.

Invitation
- Comment suggestions, additional fields or alternative formats (JSON-LD, TOML). If you like it, I can turn this into a PR and publish it as a proposal in this repository.