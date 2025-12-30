# Notas del asistente — crontab-custom-ia

Fecha de creación: 2025-12-30
Usuario: Francisco Javier (Valencia, España)

Propósito:
- Proveer un meta-runner local para ejecutar scripts de apoyo editorial/IA sin usar GitHub Actions.
- Mantener los scripts y logs en `~/data/crontab-custom-ia/` para copia de seguridad y control local.

Contenido relevante y dónde buscarlo:
- Meta-runner: `/home/user/data/crontab-custom-ia/run_cron_meta.sh`
- Jobs (wrappers): `/home/user/data/crontab-custom-ia/jobs/`
  - `run_weekly_planner.sh` — ejecuta `weekly_content_planner.py` con variables por defecto.
- Planner Python (copia local): `/home/user/data/crontab-custom-ia/weekly_content_planner.py`
- Instalador de crontab: `/home/user/data/crontab-custom-ia/install_crontab.sh`
- Logs: `/home/user/data/crontab-custom-ia/logs/cron.log`
- Documentación: `/home/user/data/crontab-custom-ia/README.md` y `/home/user/data/crontab-custom-ia/OPERATION.md`

Comportamiento del cron (actual):
- Línea añadida al crontab del usuario (marcada con `# crontab-custom-ia`) que ejecuta `run_cron_meta.sh` los lunes a las 09:00.

Variables importantes (pueden definirse en `~/.profile`):
- `GITHUB_REPOSITORY` — repositorio objetivo para crear issues (por ejemplo: `javi-jimenez/jimenezgomez.org`).
- `GITHUB_TOKEN` — token personal con permisos `repo` para crear issues.
- `CRON_SCHEDULE_OVERRIDE` — usar antes de ejecutar `install_crontab.sh` para cambiar horario.

Notas operativas para futuras sesiones del asistente:
- Si el usuario pide cambiar horario: recuérdales `install_crontab.sh` con `CRON_SCHEDULE_OVERRIDE`.
- Si el planner necesita más fuentes, añade URLs a la lista `FEEDS` en `weekly_content_planner.py`.
- Para que el planner cree issues, el usuario debe exportar `GITHUB_REPOSITORY` y `GITHUB_TOKEN` en su entorno; de lo contrario el script sólo genera el cuerpo y lo muestra/registrará.
- Para añadir nuevos jobs: crea un script ejecutable en `jobs/` que sea seguro e idempotente.

Comandos rápidos para debugging (desde la sesión):

```bash
# Ver crontab actual y ubicación de la línea marcada
crontab -l | sed -n '1,200p'

# Ejecutar meta-runner en foreground
/home/user/data/crontab-custom-ia/run_cron_meta.sh

# Ver logs
tail -n 200 ~/data/crontab-custom-ia/logs/cron.log

# Ejecutar planner manualmente
python3 ~/data/crontab-custom-ia/weekly_content_planner.py
```

Si el usuario pide que actualice o expanda la funcionalidad, seguir este patrón:
1. Modificar `weekly_content_planner.py` o añadir un wrapper en `jobs/`.
2. Probar localmente con `python3` o ejecutando el wrapper.
3. Comprobar `logs/cron.log` y corregir errores.

Fin de la nota.
