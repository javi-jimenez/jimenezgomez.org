# Contributing to jimenezgomez.org

Gracias por ofrecerte a contribuir. Aquí tienes pasos rápidos para participar.

1) Lee el `ASSISTANT_CONTEXT`
- Revisa `tools/crontab-custom-ia/ASSISTANT_CONTEXT.md` para conocer el estado actual y los pasos para retomar.

2) Trabaja localmente
- Clona/usa el repo y crea una rama para tu cambio:

```bash
git checkout -b feat/my-change
```

3) Pruebas y ejecución
- Para cambios de contenido usa `hugo` para generar `public/`:

```bash
hugo
```

4) Crear Issues y PRs
- Para proponer cambios en el RFC o abrir discusión, usa `tools/rfcs/open_rfc_issue.sh` o abre una issue manualmente.
- Usa `gh` para crear PRs y la plantilla en `tools/rfcs/pr-body.md`.

5) Seguridad
- Nunca subas claves ni `~/.config/crontab-custom-ia/env`.

6) Etiquetas y tareas
- Marca issues con `help wanted` o `good first issue` para atraer colaboradores.

Contacto: `ASSISTANT_CONTEXT.md` y `content/authors`.
