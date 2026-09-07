# Dockerfile para compilar y servir el blog Hugo

# Stage 1: Compilar con Hugo (imagen oficial de gohugoio)
# klakegg/hugo está descontinuado; usamos la imagen oficial.
FROM ghcr.io/gohugoio/hugo:latest as builder

WORKDIR /app

# Copiar contenido del blog
COPY . .

# Compilar el sitio (la imagen usa hugo como entrypoint)
RUN hugo --minify

# Stage 2: Servir con Nginx
FROM nginx:alpine

# Puerto por defecto (se sobreescribe con PORT en el despliegue, ej. 8081 en cluster)
ENV PORT=80

# Plantilla nginx: el puerto se configura con la env var PORT.
# nginx:alpine procesa /etc/nginx/templates/*.template con envsubst en el arranque.
COPY nginx.template.conf /etc/nginx/templates/default.conf.template

# Copiar los archivos generados desde el stage anterior
COPY --from=builder /app/public /usr/share/nginx/html

# Exponer puerto (se sobreescribe con PORT en el despliegue)
EXPOSE 80

# Iniciar Nginx
CMD ["nginx", "-g", "daemon off;"]
