---
title: "Propuesta: Estándar ASSISTANT_CONTEXT para continuidad entre sesiones"
date: 2025-12-30T12:30:00+01:00
draft: true
layout: post
author: "Francisco Javier"
---

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
