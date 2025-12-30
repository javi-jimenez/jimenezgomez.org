# Issues for Contributors

If you want to help, here are small, well-scoped tasks you can pick.

How to open an issue (example using `gh`):

```bash
gh issue create --title "task: Improve planner sources - add more feeds" \
  --body-file tools/crontab-custom-ia/ISSUES_FOR_CONTRIBUTORS.md \
  --label "help wanted" --label "good first issue"
```

Suggested tasks

- Improve weekly planner feed sources
  - Add more RSS sources (Hacker News, arXiv categories, relevant blogs)
  - File: `tools/crontab-custom-ia/weekly_content_planner.py`

- Add unit tests for planner
  - Add small tests that validate feed parsing and scoring
  - Suggested path: `tests/test_planner.py`

- Make installer idempotent
  - Ensure `install_crontab.sh` can be run multiple times safely

- Add CI linting for Python scripts
  - Add `requirements.txt` and GitHub Action to run `flake8`/`pytest`

- Translate `tools/crontab-custom-ia/README.md` to Spanish and English versions

Notes
- If you don't have `GITHUB_TOKEN` locally, open the issue via the web UI and use labels `help wanted` / `good first issue`.
- See `CONTRIBUTING.md` for local setup and `ASSISTANT_CONTEXT.md` for the current snapshot.
