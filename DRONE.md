Using Drone locally and manual alternative

This project includes a `.drone.yml` pipeline that builds the Hugo site and deploys the generated `public/` folder to your FTP host. To avoid GitHub Actions billing you can: run the steps manually locally, or run the `.drone.yml` pipeline with `drone exec` locally.

Manual (recommended):

1. Build the site locally (requires Hugo installed):

hugo --minify

2. Upload `public/` to your FTP host (example using `lftp`):

# install lftp if missing: apt install lftp   # or apk add lftp on Alpine
lftp -u "$FTP_USER","$FTP_PASSWORD" "$FTP_HOST" -e "mirror -R public $FTP_REMOTE_PATH --delete --verbose; bye"

Using Drone locally (optional):

- Install the Drone CLI (https://docs.drone.io/cli/install/). Then run:

# export secrets in your shell (do NOT commit them)
export FTP_HOST="ftp.example.com"
export FTP_USER="me"
export FTP_PASSWORD="secret"
export FTP_REMOTE_PATH="/path/on/server"

# run the pipeline locally (requires docker)
drone exec --trusted

Notes:
- The `.drone.yml` intentionally reads FTP credentials from secrets. Never commit credentials.
- The pipeline will skip deployment if FTP secrets are missing, so you can test builds without deploying.
- If you want full CI in Drone (server + runners), see https://docs.drone.io for setup. For local pre-flight checks the manual steps above are simplest.
