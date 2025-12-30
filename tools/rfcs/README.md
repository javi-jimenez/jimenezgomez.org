# RFC workflow — ASSISTANT_CONTEXT

This file documents the recommended local workflow to propose, discuss and merge edits to RFCs in `tools/rfcs/` using git branches and Pull Requests.

Principles
- Use topic branches per RFC (one change per branch).
- Use the provided `tools/rfcs/pr-body.md` as the PR body template.
- Discuss via Issues (template: `RFC comment`) or PR comments.

Branch & PR example

Commands (local):

```bash
# 1. Create and switch to a topic branch
git checkout -b rfc-0001-ajustes-campos

# 2. Edit the RFC file
editor tools/rfcs/RFC-0001-ASSISTANT_CONTEXT.md

# 3. Commit your changes (escribe un mensaje claro)
git add tools/rfcs/RFC-0001-ASSISTANT_CONTEXT.md
git commit -m "RFC-0001: Clarify files_changed as optional"

# 4. Push branch to remote
git push --set-upstream origin rfc-0001-ajustes-campos

# 5. Create PR using GitHub CLI and the provided body template
gh pr create --fill --title "RFC-0001: Ajustes a files_changed" --body-file tools/rfcs/pr-body.md
```

Notes on `gh pr create --fill`:
- `--fill` populates title/body from commit message; we provide `--body-file` to supply the RFC-specific structure.

Issue-driven discussion
- Alternatively open an Issue using the `RFC comment` template (`.github/ISSUE_TEMPLATE/rfc-comment.md`) and reference the RFC path.
- If an issue exists, reference it in the PR (e.g., `Closes #12` if appropriate).

Security and tokens
- Do NOT store your `GITHUB_TOKEN` in the repository.
- For local scripts we use `~/.config/crontab-custom-ia/env` (permissions `600`) as documented in the repo; do not commit that file.
- For `gh` CLI, prefer `gh auth login` which stores credentials securely per platform.

Review & merge
- Request reviews from collaborators via the PR UI.
- After consensus, merge using the project's merge policy (Squash, Merge, Rebase). Update the RFC version in the file if necessary.

Publishing and notifications
- Once merged, optionally create a short blog post or announcement linking to the merged RFC and summarizing the outcome.

Contact
- For procedural questions, open an issue titled `RFC process: question` and reference this README.
