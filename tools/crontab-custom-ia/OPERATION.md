# Operación local — crontab-custom-ia

Este fichero describe los pasos operativos para usar y mantener la carpeta `~/data/crontab-custom-ia`.

Ubicación: `/home/user/data/crontab-custom-ia`

Contenido principal:
- `run_cron_meta.sh` — meta-runner que ejecuta todos los scripts ejecutables en `jobs/` y escribe logs en `logs/cron.log`.
- `jobs/` — scripts que se ejecutarán desde cron (pon aquí `run_weekly_planner.sh` u otros wrappers).
- `weekly_content_planner.py` — copia local del planner que extrae RSS y (opcionalmente) crea issues en GitHub.
- `install_crontab.sh` — instalador que añade la línea marcada `# crontab-custom-ia` al crontab del usuario.
- `README.md` — instrucciones de uso. `OPERATION.md` ofrece comandos rápidos.

Comandos útiles:

Hacer ejecutables (solo la primera vez o tras restaurar desde copia de seguridad):

```bash
chmod +x ~/data/crontab-custom-ia/*.sh
chmod +x ~/data/crontab-custom-ia/jobs/* || true
```

Probar el meta-runner manualmente (salida en logs):

```bash
/home/user/data/crontab-custom-ia/run_cron_meta.sh
tail -n 200 /home/user/data/crontab-custom-ia/logs/cron.log
```

Ejecutar solo el planner (sin cron):

```bash
python3 ~/data/crontab-custom-ia/weekly_content_planner.py
```

Instalar o actualizar la entrada del crontab (por defecto Lunes 09:00):

```bash
~/data/crontab-custom-ia/install_crontab.sh
```

Cambiar horario antes de instalar (ejemplo: Lunes 07:00):

```bash
export CRON_SCHEDULE_OVERRIDE="0 7 * * 1"
~/data/crontab-custom-ia/install_crontab.sh
```

Configurar para que el planner abra issues en GitHub:

- Añade `GITHUB_REPOSITORY` (p. ej. `javi-jimenez/jimenezgomez.org`) y `GITHUB_TOKEN` (token con permiso `repo`) en tu entorno (`~/.profile` o similar).

Ejemplo (agregar a `~/.profile`):

```bash
export GITHUB_REPOSITORY="javi-jimenez/jimenezgomez.org"
export GITHUB_TOKEN="ghp_..."
```

Backup:

Guarda la carpeta completa `~/data/crontab-custom-ia` en tu sistema de copia (git, rsync, etc.).

Seguridad:

- Nunca pongas tokens en archivos público sin protección.
- Preferible usar `pass`, `gpg` o el gestor que uses para exportar `GITHUB_TOKEN` al entorno antes de ejecutar el job.
