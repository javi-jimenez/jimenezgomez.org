---
title: Protocolo Unificado de Contexto para Asistentes (PUCA / ACS)
date: "2026-01-02T19:30:00+00:00"
draft: false
layout: post
image: og-image-1200x630.png
author: Gemini (AI Model)
description: Propuesta evolucionada del Assistant Context Standard para interoperabilidad entre asistentes.
tags: "["assistant-context","standard","AI","gemini"]"
og_image: og-image-1200x630.png
---

**Hora:** 20:30 UTC
**Creditos de Propuesta Original:** https://jimenezgomez.org/posts/2025-12-30-assistant-context-standard/

---

## 1. Introducción: El problema del "Efecto Amnesia"

A pesar de la potencia de los LLMs, el trabajo en entornos locales y distribuidos sufre de una desconexión crítica: la IA no sabe qué ocurrió en la sesión anterior si el motor o la interfaz cambian. Proponemos un estándar basado en archivos de manifiesto situados en la raíz de los proyectos para garantizar la continuidad del flujo de trabajo.

## 2. Estructura del Estándar Mejorado (Propuesta v2.0)

Para que un estándar sea efectivo, debe ser ligero y legible tanto para humanos como para máquinas. Sugerimos la creación de un archivo `.ai-context.json` o `.assistant.md` con la siguiente estructura mejorada:

### A. El Manifiesto de Tarea (`task_state`)

No basta con decir qué se está haciendo; hay que definir el "Estado de la Misión":

* **Current Goal:** El objetivo macro actual.
* **Sub-tasks:** Lista de verificación (Checklist) de tareas pendientes y completadas.
* **Blocking Issues:** Impedimentos técnicos encontrados en sesiones previas.

### B. Diccionario de Entidades (`knowledge_graph`)

Para evitar que la IA confunda términos en proyectos grandes:

* **Definitions:** Glosario de términos específicos del negocio o del código.
* **Key Files:** Mapeo de archivos críticos y su función (evita que la IA tenga que leer todo el repo para entender la arquitectura).

### C. Registro de Decisiones de Diseño (ADR - Architecture Decision Records)

El mayor fallo de contexto es cuando la IA sugiere cambiar algo que ya se decidió no hacer.

* **Decisions:** "Usamos UUID en lugar de ID incremental por X razón". Esto evita bucles de sugerencias erróneas.

## 3. Mejoras Agregadas (Aportación de la IA)

He añadido tres capas técnicas que tu estándar original puede adoptar para ser más robusto:

1. **Capa de Jerarquía de Herencia:** Si hay un archivo en `/root` y otro en `/root/module_A`, el asistente debe fusionarlos. El archivo de subdirectorio tiene prioridad sobre el global. Esto permite "Contexto por Módulo".
2. **Firma de Sesión (Hash de Estado):**
Incluir un `last_state_hash` que resuma el estado del código. Si el asistente detecta que el código cambió drásticamente desde la última lectura del contexto, debe alertar al usuario para actualizar el manifiesto.
3. **Token Budget Management:**
Instrucción explícita de "Priority Levels". Si el archivo de contexto crece mucho, el estándar define qué partes se pueden omitir (ej. el historial antiguo) y qué partes son obligatorias (el Goal actual).

## 4. Implementación Práctica (Ejemplo de Archivo)

```yaml
# .ai-context.yaml
standard_version: "2.0"
project_name: "Phoenix System"
author_context: "JimenezGomez"

current_sprint:
	task: "Refactorización de la capa de autenticación"
	status: "In_Progress (60%)"
	last_action: "Migración de JWT a cookies HttpOnly terminada"

rules:
	- "No usar librerías externas para el manejo de fechas"
	- "Mantener compatibilidad con Python 3.9"

knowledge_base:
	- "UserDB: Tabla principal en PostgreSQL"
	- "Legacy_Auth: No tocar hasta el sprint 4"

last_update: "2026-01-02 20:25"

```

---

## 5. Conclusión

El **Assistant Context Standard** propuesto por JimenezGomez y refinado en este documento elimina la fricción de entrada en cada nueva sesión de IA. Al tratar el contexto como **código persistente** y no como **memoria volátil**, permitimos que el desarrollo asistido por IA sea verdaderamente profesional y escalable.

---

**Nota del Asistente:** He redactado este artículo integrando tu visión de persistencia en directorios con mi capacidad de estructuración técnica. Si quieres que profundice en algún punto técnico (como la integración con el protocolo MCP), dímelo.
