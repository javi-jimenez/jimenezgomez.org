#!/usr/bin/env bash
#
# gitea-push-mirror.sh — configura un "push mirror" Gitea -> GitHub para todos
# los repositorios de una instancia Gitea (o los que casen con un filtro).
#
# Garantiza la copia en AMBOS sitios: el repo vive en Gitea y se empuja a GitHub
# en cada commit (sync_on_commit) y periódicamente.
#
# Requisitos:
#   - curl, jq
#   - GITEA_TOKEN: token de Gitea con permiso de escritura sobre los repos
#   - GITHUB_TOKEN: PAT de GitHub con scope `repo` (+ `workflow` si hay
#     .github/workflows). Si no se define, se intenta `gh auth token`.
#
# Uso:
#   GITEA_TOKEN=xxx GITHUB_TOKEN=yyy ./scripts/gitea-push-mirror.sh
#   ./scripts/gitea-push-mirror.sh --dry-run
#
# Variables (con defaults):
#   GITEA_URL     (https://gitea.app.brisecom.net)
#   GITHUB_OWNER  (javi-jimenez)   usuario u organización destino
#   REPO_FILTER   (vacío = todos)  regex sobre el nombre del repo, p. ej. '^cluster$'
#   PRIVATE_REPOS (true)           crear repos nuevos en GitHub como privados
#   MIRROR_INTERVAL (8h0m0s)
#
set -euo pipefail

GITEA_URL="${GITEA_URL:-https://gitea.app.brisecom.net}"
GITHUB_OWNER="${GITHUB_OWNER:-javi-jimenez}"
REPO_FILTER="${REPO_FILTER:-}"
PRIVATE_REPOS="${PRIVATE_REPOS:-true}"
MIRROR_INTERVAL="${MIRROR_INTERVAL:-8h0m0s}"
DRY_RUN=false

for arg in "$@"; do
  case "$arg" in
    --dry-run) DRY_RUN=true ;;
    -h|--help) sed -n '2,30p' "$0"; exit 0 ;;
  esac
done

command -v curl >/dev/null || { echo "Falta curl"; exit 1; }
command -v jq   >/dev/null || { echo "Falta jq";   exit 1; }

if [[ -z "${GITEA_TOKEN:-}" ]]; then
  echo "ERROR: define GITEA_TOKEN" >&2; exit 1
fi
if [[ -z "${GITHUB_TOKEN:-}" ]] && command -v gh >/dev/null; then
  GITHUB_TOKEN="$(gh auth token 2>/dev/null || true)"
fi
if [[ -z "${GITHUB_TOKEN:-}" ]]; then
  echo "ERROR: define GITHUB_TOKEN (o autentica gh)" >&2; exit 1
fi

api_gitea() { curl -fsS -H "Authorization: token ${GITEA_TOKEN}" "$@"; }
api_github() { curl -sS -H "Authorization: Bearer ${GITHUB_TOKEN}" \
                 -H "Accept: application/vnd.github+json" \
                 -H "X-GitHub-Api-Version: 2022-11-28" "$@"; }

echo "Gitea : ${GITEA_URL}"
echo "GitHub: ${GITHUB_OWNER}"
[[ -n "$REPO_FILTER" ]] && echo "Filtro: ${REPO_FILTER}"
$DRY_RUN && echo "*** DRY-RUN (no se cambia nada) ***"
echo

# ¿GITHUB_OWNER es el usuario autenticado o una organización?
me="$(api_github https://api.github.com/user | jq -r '.login // empty')"
if [[ "$me" == "$GITHUB_OWNER" ]]; then
  GH_CREATE_URL="https://api.github.com/user/repos"
else
  GH_CREATE_URL="https://api.github.com/orgs/${GITHUB_OWNER}/repos"
fi

# Lista de repos en Gitea (paginado)
repos="$(api_gitea "${GITEA_URL}/api/v1/user/repos?limit=50" \
         | jq -r '.[].full_name')"

ok=0; skipped=0; failed=0
while IFS= read -r full_name; do
  [[ -z "$full_name" ]] && continue
  owner="${full_name%%/*}"; repo="${full_name##*/}"

  if [[ -n "$REPO_FILTER" ]] && ! [[ "$repo" =~ $REPO_FILTER ]]; then
    continue
  fi

  gh_url="https://github.com/${GITHUB_OWNER}/${repo}.git"
  echo "== ${full_name}  ->  ${gh_url}"

  # 1) ¿Existe el repo en GitHub? Si no, crearlo.
  code="$(api_github -o /dev/null -w '%{http_code}' \
          "https://api.github.com/repos/${GITHUB_OWNER}/${repo}")"
  if [[ "$code" == "404" ]]; then
    echo "   GitHub: no existe -> crear (private=${PRIVATE_REPOS})"
    if ! $DRY_RUN; then
      api_github -X POST "$GH_CREATE_URL" \
        -d "$(jq -nc --arg n "$repo" --argjson p "$PRIVATE_REPOS" \
              '{name:$n, private:$p}')" >/dev/null
    fi
  elif [[ "$code" == "200" ]]; then
    echo "   GitHub: ya existe"
  else
    echo "   GitHub: respuesta inesperada ($code) -> salto"; failed=$((failed+1)); continue
  fi

  # 2) ¿Ya hay push mirror?
  existing="$(api_gitea "${GITEA_URL}/api/v1/repos/${full_name}/push_mirrors" \
              | jq -r --arg u "$gh_url" '.[] | select(.remote_address==$u) | .remote_address')"
  if [[ -n "$existing" ]]; then
    echo "   Gitea : push mirror ya configurado -> salto"; skipped=$((skipped+1)); continue
  fi

  # 3) Crear push mirror
  echo "   Gitea : crear push mirror (sync_on_commit, interval=${MIRROR_INTERVAL})"
  if ! $DRY_RUN; then
    api_gitea -X POST "${GITEA_URL}/api/v1/repos/${full_name}/push_mirrors" \
      -H 'Content-Type: application/json' \
      -d "$(jq -nc --arg a "$gh_url" --arg u "$GITHUB_OWNER" --arg p "$GITHUB_TOKEN" \
            --arg i "$MIRROR_INTERVAL" \
            '{remote_address:$a, remote_username:$u, remote_password:$p,
              sync_on_commit:true, interval:$i}')" >/dev/null
  fi
  ok=$((ok+1))
done <<< "$repos"

echo
echo "Resumen: configurados=${ok}  ya-estaban=${skipped}  fallos=${failed}"
