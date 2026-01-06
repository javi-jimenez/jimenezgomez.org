---
og_image: og-image-1200x630.png
image: og-image-1200x630.png
---

---title: "Costo computacional y afinidad a la verdad: lenguajes formales vs ML (Borrador)"
date: 2025-12-30T10:00:00+01:00
draft: true
layout: post
tags: [ia, formal-methods, machine-learning, research]
image: "og-image.svg"
---

Este artículo compara, en modo borrador, el coste computacional y la afinidad a la verdad de dos enfoques para construir sistemas de IA: los métodos basados en lenguajes formales (especificación, verificación, síntesis) y las aproximaciones del aprendizaje automático (ML) dominantes en la actualidad.

Introducción
----------
En las próximas generaciones veremos dos paradigmas competir y complementarse: los métodos formales (modelado lógico, verificación, síntesis por especificación) y las aproximaciones estadísticas actuales (redes neuronales, transformers). Aquí comparo su coste computacional esperado a corto y medio plazo, su escalabilidad y lo que llamo "afinidad a la verdad": la propensión del sistema a producir salidas correctas, justificables y verificables.

Definiciones rápidas
--------------------
- Lenguajes formales: sistemas construidos sobre lógica matemática, gramáticas y autómatas; incluyen verificación por modelo, pruebas formales y síntesis programática.
- Aprendizaje automático (ML): modelos estadísticos que aproximan funciones a partir de datos; sus garantías son probabilísticas.

Coste computacional según horizonte temporal
-------------------------------------------
Usamos tres ejes: coste de desarrollo inicial, coste de cómputo para entrenamiento/compilación/verificación y coste de mantenimiento/adaptación.

- Corto plazo (1–3 años): ML domina tareas de lenguaje/visión; métodos formales permanecen en nichos críticos.
- Medio plazo (3–7 años): mejoras en síntesis y verificación reducirán costes en dominios estructurados; ML mejora en eficiencia (distillation, sparsity, hardware dedicado).
- Largo plazo (>7 años): aparecen híbridos (especificaciones que guían ML; ML que sugiere invariantes formales); la relación coste/beneficio dependerá mucho del hardware disponible.

Estimaciones orientativas (resumen)
----------------------------------

- Métodos formales: coste humano alto para especificar; verificación puede ser intensiva (desde 10^2 a 10^4 core-segundos para módulos no triviales, según abstracción y herramienta). Mantenimiento eficiente si hay buena modularidad.
- ML: entrenamiento de grandes modelos modernos puede usar 10^6–10^9 GPU-segundos a escala máxima; inferencia optimizada baja el coste por petición.

Factores que cambian la relación coste
-------------------------------------

- Hardware especializado (TPU, NPU, aceleradores de SMT) y avances algorítmicos pueden reducir costes en ambos bandos.
- Datos vs. especificaciones: obtener datos etiquetados es costoso; especificar formalmente propiedades también lo es.

Afinidad a la verdad (definición y comparación)
--------------------------------------------

Definimos "afinidad a la verdad" como la capacidad del sistema para producir salidas que correspondan a hechos, invariantes o requisitos verificables, y para justificar por qué la salida es correcta.

- Lenguajes formales: alta afinidad a la verdad cuando la especificación es correcta y completa; la verificación ofrece pruebas dentro del modelo formal. Riesgo: si la especificación es pobre, las garantías son engañosas (GIGO).
- ML: afinidad probabilística dependiente de la calidad y cobertura de los datos; puede alucinar o mostrar sesgos; explicabilidad limitada salvo empleando técnicas XAI.

Híbridos
--------

Los enfoques híbridos (ML que sugiere candidatos, métodos formales que verifican) ofrecen un equilibrio: reducción del espacio de búsqueda gracias a ML y garantía de corrección proporcionada por verificación. En muchos dominios este patrón ofrece mejor coste/verdad que cualquiera de los enfoques por separado.

Aplicaciones por dominio
------------------------

- Críticos (médico, aeroespacial): preferible formal; coste mayor pero la afinidad a la verdad y trazabilidad justifican la inversión.
- NLP creativo y generación: ML domina; garantías formales costosas y difíciles.
- Sistemas mixtos (negocio+reglas): combinación práctica: reglas formales + ML para ranking.

Economía práctica
-----------------

- Proyecto formal crítico: mayor coste humano y herramientas; alta amortización si el fallo tiene coste elevado.
- Proyecto ML grande: costes de infra (GPU/TPU), datos y operación; escalabilidad reduce coste por usuario.

Conclusión (BORRADOR — revisión pendiente)
-----------------------------------------

ADVERTENCIA: esta conclusión se deja como borrador por petición del autor. El equilibrio entre coste computacional y afinidad a la verdad no es una elección binaria; sin embargo, la afirmación de que "la convergencia será la norma" requiere matices: depende fuertemente del dominio, del coste social del error y de las mejoras en técnicas formales y de ML.

Puntos abiertos (para revisar):

- ¿Qué peso dar a la verificación probabilística frente a la verificación clásica en sistemas mixtos?
- ¿Cómo cuantificar correctamente el coste humano de especificar sistemas complejos frente al coste de obtención y curación de datos? (necesario para ROI real)
- ¿Cuál es el horizonte realista para que la síntesis guiada por ML reduzca el coste de verificación en la práctica?

Indícame cómo quieres modificar la conclusión y la dejo actualizada. El post está marcado `draft: true` y no lo subiré a git salvo que me lo indiques.
