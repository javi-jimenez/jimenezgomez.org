# Google Analytics (GA4) — Configuración y verificación

Este fichero explica cómo cambiar el Measurement ID y verificar la instalación localmente.

1) Dónde poner el Measurement ID

- Edita `hugo.toml` y actualiza la clave `googleAnalytics` con tu Measurement ID (ejemplo `G-XXXXXXXXX`).

2) Regenerar el sitio localmente

```bash
# Desde la raíz del repo
git pull origin main
hugo --cleanDestinationDir
# (o para desarrollo)
hugo server -D
```

3) Verificar que el script se ha inyectado

- Abre `public/index.html` y busca `gtag('config'` o tu ID `G-...`.
- Desde el navegador, en la página pública (ej. `http://localhost:1313/`) abre Herramientas de desarrollador → Network y filtra por `googletagmanager` o `gtag`.

4) Verificación en Google

- Entra en Google Analytics → Realtime → Live view y observa si hay actividad.
- Para comprobar que el sitio envía datos: usa el Google Tag Assistant o la extensión `GA Debug`.

5) Privacidad y recomendaciones

- El partial activa `anonymize_ip` por defecto en `gtag('config', ..., { 'anonymize_ip': true })`.
- Si prefieres no incluir analytics en entornos de desarrollo, puedes envolver la variable en el partial o añadir una condición en `hugo.toml`.

6) Revertir o cambiar ID

- Para cambiar, edita `hugo.toml`, vuelve a ejecutar `hugo --cleanDestinationDir`, y registra los cambios y súbelos al repositorio:

```bash
git add hugo.toml
git commit -m "Update Google Analytics Measurement ID"
git push
```

Si quieres, puedo añadir también comprobaciones automáticas en CI para asegurar que `googleAnalytics` está vacío en branches no-main.
