# Google Analytics (GA4) — Configuration and Verification

This file explains how to change the Measurement ID and verify the setup locally.

1) Where to set the Measurement ID

- Edit `hugo.toml` and update the `googleAnalytics` key with your Measurement ID (for example `G-XXXXXXXXX`).

2) Rebuild the site locally

```bash
# From the repository root
git pull origin main
hugo --cleanDestinationDir
# (or for development)
hugo server -D
```

3) Verify that the script was injected

- Open `public/index.html` and search for `gtag('config'` or your `G-...` ID.
- In the browser, on the public page (for example `http://localhost:1313/`), open Developer Tools → Network and filter by `googletagmanager` or `gtag`.

4) Verify in Google Analytics

- Go to Google Analytics → Realtime → Live view and check whether activity appears.
- To confirm that the site is sending data, use Google Tag Assistant or the `GA Debug` extension.

5) Privacy and recommendations

- The partial enables `anonymize_ip` by default in `gtag('config', ..., { 'anonymize_ip': true })`.
- If you prefer not to include analytics in development environments, wrap the variable in the partial or add a condition in `hugo.toml`.

6) Revert or change the ID

- To change it, edit `hugo.toml`, run `hugo --cleanDestinationDir` again, then commit and push the changes:

```bash
git add hugo.toml
git commit -m "Update Google Analytics Measurement ID"
git push
```

If you want, I can also add automatic CI checks to ensure `googleAnalytics` is empty on non-main branches.
