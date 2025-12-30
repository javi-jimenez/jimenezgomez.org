# crontab-custom-ia — Quick Start

Propósito
- Carpeta local para ejecutar y versionar herramientas de automatización editorial (weekly planner, comprobador de borradores, instalador de crontab). Esta copia en `tools/` es un backup; la ejecución principal está en `~/data/crontab-custom-ia/`.

Resumen rápido
- Archivo de contexto: `tools/crontab-custom-ia/ASSISTANT_CONTEXT.md` (snapshot y pasos para retomar).
- Env local (NO commitear): `~/.config/crontab-custom-ia/env` (usar el `env.example` como plantilla).

Preparar entorno
1. Copia el ejemplo de env y ajusta valores (no subir al repo):

```bash
cp tools/crontab-custom-ia/env.example ~/.config/crontab-custom-ia/env
chmod 600 ~/.config/crontab-custom-ia/env
```

2. Contenido mínimo (`~/.config/crontab-custom-ia/env`):

- GITHUB_TOKEN=ghp_xxx
- GITHUB_REPOSITORY=owner/repo
- MAINTAINER_EMAIL=tu@correo

Ejecutar manualmente (pruebas)

```bash
# Cargar variables
export $(cat ~/.config/crontab-custom-ia/env | xargs)

# Ejecutar wrapper probado
bash ~/data/crontab-custom-ia/jobs/run_weekly_planner.sh

# O ejecutar el planner directamente (debug)
python3 ~/data/crontab-custom-ia/weekly_content_planner.py
```

Instalar crontab (si falta)

```bash
# Esto añade un bloque marcado en el crontab del usuario
bash tools/crontab-custom-ia/install_crontab.sh

# Verificar
crontab -l | sed -n '1,160p'
```

Logs
- Por defecto `~/data/crontab-custom-ia/logs/cron.log` (si se habilitó). Si no existe, la salida irrá a stdout del job; ejecuta manualmente para depuración.

Publicar cambios en el sitio
- El repositorio contiene `public/` preparado para deploy; si editas contenido fuente, genera el sitio localmente con `hugo` y commitea `public/` (si sigues usando el mismo flujo):

```bash
hugo
git add public/ && git commit -m "chore(public): site build" && git push origin HEAD
```

RFC y discusión
- Draft RFC: `tools/rfcs/RFC-0001-ASSISTANT_CONTEXT.md`.
- Abrir issue automático (requiere token en env):

```bash
bash tools/rfcs/open_rfc_issue.sh
```

Notas de seguridad
- Nunca commitees `~/.config/crontab-custom-ia/env` ni claves en texto.
- Asegura permisos: `chmod 600 ~/.config/crontab-custom-ia/env`.

Handoff rápido
- Archivo de contexto para retomar: `tools/crontab-custom-ia/ASSISTANT_CONTEXT.md`.
- Para que otra IA/ingeniero retome: confirme crontab instalado, env seguro, y ejecutar el wrapper manualmente.

Contacto
- Responsable: Francisco Javier (ver `content/authors` o `ASSISTANT_CONTEXT.md`).
# crontab-custom-ia

This folder contains a simple meta-runner and job scaffolding to run local IA-related scripts via the user's `crontab`.

Structure:
- `run_cron_meta.sh` - executes every executable script in `jobs/` and logs to `logs/cron.log`.
- `jobs/` - place executable job scripts here (e.g., `run_weekly_planner.sh`).
- `weekly_content_planner.py` - local copy of the planner (can be executed from `jobs/` via a wrapper).
- `run_weekly_planner.sh` - wrapper to run `weekly_content_planner.py` with sane defaults.
- `install_crontab.sh` - adds a marked crontab entry for the current user.

Quick install (local):

1. Make scripts executable:

```bash
chmod +x ~/data/crontab-custom-ia/*.sh
chmod +x ~/data/crontab-custom-ia/jobs/* || true
```

2. Move wrappers to `jobs/` so the meta-runner executes them:

```bash
mkdir -p ~/data/crontab-custom-ia/jobs
mv ~/data/crontab-custom-ia/run_weekly_planner.sh ~/data/crontab-custom-ia/jobs/
```

3. Optional: set `GITHUB_REPOSITORY` and `GITHUB_TOKEN` in your environment if you want the planner to open issues on GitHub.

4. Install crontab entry (defaults to Mondays 09:00):

```bash
~/data/crontab-custom-ia/install_crontab.sh
```

Customize schedule via `CRON_SCHEDULE_OVERRIDE` env var before running installer, e.g.: 

```bash
export CRON_SCHEDULE_OVERRIDE="0 7 * * 1" # Mondays 07:00
~/data/crontab-custom-ia/install_crontab.sh
```

Notes:
- Scripts and logs live in `~/data/crontab-custom-ia/` for easy backup.
- `run_cron_meta.sh` will run any executable file in `jobs/` — ensure wrappers are safe and idempotent.
