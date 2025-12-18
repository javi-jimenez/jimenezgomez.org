# Laia Brand Assets - Reference Index

Este archivo mantiene el control de todos los recursos de la identidad visual de Laia y dónde se mencionan/utilizan.

## Ubicaciones de los Recursos

### 1. Recursos Originales (Fuente)
**Ubicación:** `content/posts/2025-12-18-laia-brand-identity/`

Archivos creados:
- laia-brand-showcase.svg (miniatura del post)
- laia-brand-hero.svg (hero del artículo)
- laia-logo-main.svg
- laia-logo-light.svg
- laia-logo-dark.svg
- laia-logo-mono.svg
- laia-icon-compact.svg
- laia-avatar-github.svg
- laia-avatar-twitter.svg
- laia-avatar-linkedin.svg
- laia-banner-github.svg
- laia-social-instagram.svg
- laia-social-twitter-card.svg

**Total:** 13 archivos SVG

### 2. Recursos Copiados (Distribución)
**Ubicación:** `brand/`

Estructura:
```
brand/
├── README.md                        # Documentación básica
├── brand-guidelines.pdf             # Manual completo (Markdown)
├── logo/
│   ├── laia-logo-main.svg
│   ├── laia-logo-light.svg
│   ├── laia-logo-dark.svg
│   └── laia-logo-mono.svg
├── icons/
│   └── laia-icon-compact.svg
├── avatars/
│   ├── laia-avatar-github.svg
│   ├── laia-avatar-twitter.svg
│   └── laia-avatar-linkedin.svg
├── banners/
│   └── laia-banner-github.svg
└── social/
    ├── laia-social-instagram.svg
    └── laia-social-twitter-card.svg
```

**Total:** 11 archivos SVG + 2 documentos

## Referencias en Artículos del Blog

### Artículo 1: Laia - Inteligencia Artificial Ética
**Ubicación:** `content/posts/2025-12-18-laia-intelligent-agent/index.md`

**Imágenes utilizadas:**
- `image: "laia-thumbnail.svg"` (frontmatter - miniatura)
- `![Laia - Ethical AI Research](laia-header.svg)` (línea 20 - header)

**Archivos en la carpeta:**
- laia-ai.jpg
- laia-ai.svg (no usado actualmente)
- laia-header.svg
- laia-thumbnail.svg

### Artículo 2: Identidad Visual de Laia
**Ubicación:** `content/posts/2025-12-18-laia-brand-identity/index.md`

**Imágenes utilizadas en el artículo:**
1. Frontmatter: `image: "laia-brand-showcase.svg"`
2. Hero: `![Laia Brand Identity](laia-brand-hero.svg)`
3. Logo Principal: `![Logo Principal Laia](laia-logo-main.svg)`
4. Icono: `![Icono Compacto](laia-icon-compact.svg)`
5. GitHub Avatar: `![GitHub Avatar](laia-avatar-github.svg)`
6. Twitter Avatar: `![Twitter Avatar](laia-avatar-twitter.svg)`
7. LinkedIn Avatar: `![LinkedIn Avatar](laia-avatar-linkedin.svg)`
8. Banner GitHub: `![GitHub Banner](laia-banner-github.svg)`
9. Logo Light: `![Logo Light](laia-logo-light.svg)`
10. Logo Dark: `![Logo Dark](laia-logo-dark.svg)`
11. Logo Mono: `![Logo Mono](laia-logo-mono.svg)`
12. Instagram: `![Instagram Template](laia-social-instagram.svg)`
13. Twitter Card: `![Twitter Card](laia-social-twitter-card.svg)`

**Sección de recursos:** Documenta la ubicación en `content/posts/2025-12-18-laia-brand-identity/` y propone estructura futura en `brand/`

## Documentación

### brand/README.md
- Descripción de la estructura de carpetas
- Referencia al blog y al PDF
- Información de licencia CC BY 4.0
- Contacto

### brand/brand-guidelines.pdf (Markdown)
Secciones:
1. Introducción (proyecto y propósito)
2. Filosofía del diseño (estrellas, azul, red neuronal)
3. Paleta de colores (primarios, neutros, acento)
4. Logotipo (versiones y usos)
5. Espaciado y área de seguridad
6. Tipografía (Segoe UI, Inter, Arial)
7. Usos permitidos (fondos, aplicaciones)
8. Usos prohibidos
9. Avatares para redes sociales
10. Banners y headers
11. Accesibilidad (WCAG AAA, daltonismo)
12. Archivos de recursos (ubicaciones)
13. Licencia (CC BY 4.0)
14. Control de versiones
15. Créditos

## Sincronización

### Si se modifica un SVG en el post original:
```bash
# Copiar desde post a brand/
cp content/posts/2025-12-18-laia-brand-identity/[archivo].svg brand/[subcarpeta]/
```

### Si se crea un nuevo recurso:
1. Crear en `content/posts/2025-12-18-laia-brand-identity/`
2. Añadirlo al artículo del blog con `![](nombre.svg)`
3. Copiarlo a `brand/[subcarpeta-apropiada]/`
4. Actualizar este archivo de referencia
5. Actualizar `brand/brand-guidelines.pdf` si aplica

## Paleta de Colores (Referencia Rápida)

```css
/* Primarios */
--laia-blue-deep:    #0c4a6e  /* Azul profundo */
--laia-blue-primary: #0369a1  /* Azul principal */
--laia-blue-light:   #60a5fa  /* Azul claro */
--laia-blue-pale:    #bfdbfe  /* Azul pálido */

/* Neutros */
--laia-dark:         #0f172a  /* Fondo oscuro */
--laia-slate:        #1e293b  /* Gris pizarra */
--laia-gray:         #94a3b8  /* Gris medio */
--laia-light:        #f0f9ff  /* Casi blanco */

/* Acento */
--laia-accent-cyan:  #06b6d4  /* Cyan */
--laia-accent-sky:   #38bdf8  /* Cielo */
```

## Tipografía (Referencia Rápida)

- **Principal:** Segoe UI (weight 300 títulos, 400 texto)
- **Web/Apps:** Inter
- **Fallback:** Arial
- **Letter-spacing:** 12-20px (logos), 3-8px (títulos)

## Notas

- Los archivos SVG son la fuente principal (vectoriales, escalables)
- El post del blog es la ubicación canónica de los archivos originales
- La carpeta `brand/` es para distribución y uso externo
- Cualquier cambio debe reflejarse en ambas ubicaciones
- El artículo del blog sirve como documentación visual interactiva
- El PDF sirve como documentación formal para imprimir/compartir

## Última actualización
**Fecha:** 2025-12-18  
**Versión:** 1.0  
**Cambios:** Creación inicial del sistema de identidad visual Laia
