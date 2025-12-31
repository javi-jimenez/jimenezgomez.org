---
title: "Propuesta: Estándar ASSISTANT_CONTEXT para continuidad entre sesiones"
date: 2025-12-30T12:30:00+01:00
draft: false
layout: post
author: "Francisco Javier"
---

Enlace al borrador formal (RFC): [RFC-0001: ASSISTANT_CONTEXT](../../tools/rfcs/RFC-0001-ASSISTANT_CONTEXT.md)

Proceso para comentarios (Request for Comments):

- Abre un issue en el repositorio con el título "RFC-0001: comment: <resumen>" o ejecuta `tools/rfcs/open_rfc_issue.sh` localmente con `GITHUB_REPOSITORY` y `GITHUB_TOKEN` en tu entorno para crear la issue automáticamente.
- También puedes enviar un Pull Request con la propuesta de cambio sobre `tools/rfcs/RFC-0001-ASSISTANT_CONTEXT.md`.

Este es un borrador de propuesta para un pequeño estándar que permita a asistentes automatizados (IA) y a sus usuarios mantener continuidad entre sesiones.

Motivación
- Cuando un asistente y un humano trabajan iterativamente en un repositorio o en tareas locales, es útil que exista un archivo estándar, legible por humanos y máquinas, que contenga el contexto mínimo necesario para reanudar trabajo.

Propuesta mínima (frontmatter YAML):
- `id`, `created_at`, `updated_at`, `user`, `location`, `purpose`, `files_changed`, `next_steps`, `status`.

Uso
- El asistente crea o actualiza `ASSISTANT_CONTEXT.md` en la carpeta de trabajo.
- El archivo incluye un breve historial, comandos de verificación y enlaces a archivos clave.

Ventajas
- Facilita que distintos agentes (humanos o automáticos) retomen el trabajo sin perder pasos.
- Sirve como contrato mínimo para colaboraciones asistidas por IA.

Invitación
- Comentad sugerencias, campos adicionales o formatos alternativos (JSON-LD, TOML). Si os gusta, puedo convertir esto en un PR y publicarlo como propuesta en este repositorio.
