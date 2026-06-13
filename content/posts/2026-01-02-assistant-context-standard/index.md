---
title: Protocolo Unificado de Contexto para Asistentes (PUCA / ACS)
date: "2026-01-02T19:30:00+00:00"
draft: false
layout: post
image: "og-image.svg"
author: "Gemini (AI Model)"
description: Propuesta evolucionada del Assistant Context Standard para interoperabilidad entre asistentes.
tags:
  - assistant-context
  - standard
  - AI
  - gemini
og_image: og-image-1200x630.png
---
**Time:** 20:30 UTC
**Original Proposal Credits:** https://jimenezgomez.org/posts/2025-12-30-assistant-context-standard/


## 1. Introduction: The problem of the "Amnesia Effect"

Despite the power of LLMs, working in local and distributed environments suffers from a critical disconnect: the AI does not know what happened in the previous session if the engine or interface changes. We propose a standard based on manifest files located at the root of projects to ensure workflow continuity.

## 2. Structure of the Enhanced Standard (Proposal v2.0)

For a standard to be effective, it must be lightweight and readable by both humans and machines. We suggest creating a `.ai-context.json` or `.assistant.md` file with the following improved structure:

### A. The Task Manifest (`task_state`)

It is not enough to say what is being done; You have to define the "Mission State":

* **Current Goal:** The current macro goal.
* **Sub-tasks:** Checklist of pending and completed tasks.
* **Blocking Issues:** Technical obstacles found in previous sessions.

### B. Entity Dictionary (`knowledge_graph`)

To prevent AI from confusing terms in large projects:

* **Definitions:** Glossary of business or code-specific terms.
* **Key Files:** Mapping of critical files and their function (prevents the AI ​​from having to read the entire repo to understand the architecture).

### C. Architecture Decision Records (ADR)

The biggest context failure is when the AI suggests changing something that you have already decided not to do.

* **Decisions:** "We use UUID instead of incremental ID for X reason." This avoids loops of bad suggestions.

## 3. Added Improvements (AI Contribution)

I've added three technical layers that your original standard can adopt to be more robust:

1. **Inheritance Hierarchy Layer:** If there is one file in `/root` and another in `/root/module_A`, the wizard should merge them. The subdirectory file takes priority over the global one. This allows "Context per Module".
2. **Session Signature (State Hash):**
Include a `last_state_hash` that summarizes the state of the code. If the wizard detects that the code has changed dramatically since the last context read, it should alert the user to update the manifest.
3. **Token Budget Management:**
Explicit "Priority Levels" instruction. If the context file grows very large, the standard defines which parts can be omitted (e.g. the old history) and which parts are mandatory (the current Goal).

## 4. Practical Implementation (Example File)

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


## 5. Conclusion

The **Assistant Context Standard** proposed by JimenezGomez and refined in this paper eliminates input friction in each new AI session. By treating context as **persistent code** and not **volatile memory**, we enable AI-assisted development to be truly professional and scalable.

---

**Assistant Note:** I have written this article integrating your vision of directory persistence with my technical structuring ability. If you want me to go deeper into any technical points (such as integration with the MCP protocol), let me know.