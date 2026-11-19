# blog.jimenezgomez.org

Estado: **pendiente en el panel de OVH**. La parte del repositorio está hecha.

## Qué está resuelto

- **DNS**: `blog.jimenezgomez.org` ya resuelve a la misma IP que
  `jimenezgomez.org` (`2001:41d0:301:4::21`, OVH). No hay nada que tocar.
- **Redirección**: `static/.htaccess` la contiene, y Hugo la copia a
  `public/.htaccess` en cada `make deploy`:

  ```apache
  RewriteCond %{HTTP_HOST} ^blog\.jimenezgomez\.org$ [NC]
  RewriteRule ^/(.*)$ https://jimenezgomez.org/$1 [R=301,L]
  ```

  Destino: la **raíz**, sin anteponer `/blog`, para que el destino se pueda
  cambiar en el futuro sin tocar la regla y el enlace viejo quede archivado
  como redirección permanente. La ruta pedida se conserva:
  `blog.jimenezgomez.org/x` → `jimenezgomez.org/x`.

## Qué falta (panel de OVH)

Comprobado el 2026-11-19: el subdominio responde
`404 · Site not installed - OVHcloud`, así que **Apache no está mirando el
.htaccess de este sitio**: no existe el multisitio. En el dominio raíz sí se
procesa ( `jimenezgomez.org/posts/` → `301 /blog/` ).

1. **Multisitio** → añadir `blog.jimenezgomez.org` apuntando a la **misma
   carpeta** que `jimenezgomez.org`.
2. En esa misma pantalla, **activar el certificado SSL** para que el
   subdominio entre en el SAN. Hoy el certificado no lo cubre
   (`no alternative certificate subject name matches target hostname`).

## Cómo comprobar que está listo

```bash
curl -sSI https://blog.jimenezgomez.org/   # esperado: 301 -> https://jimenezgomez.org/
curl -sSI https://blog.jimenezgomez.org/x  # esperado: 301 -> https://jimenezgomez.org/x
```

Si devuelve `404 Site not installed`, el multisitio aún no está creado.
Si devuelve un error de certificado, falta el SSL del subdominio.
