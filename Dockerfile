# Dockerfile para compilar y servir el blog Hugo

# Stage 1: Compilar con Hugo
FROM klakegg/hugo:latest as builder

WORKDIR /app

# Copiar contenido del blog
COPY . .

# Compilar el sitio
RUN hugo --minify

# Stage 2: Servir con Nginx
FROM nginx:alpine

# Copiar configuración de Nginx
COPY nginx.conf /etc/nginx/nginx.conf

# Copiar los archivos generados desde el stage anterior
COPY --from=builder /app/public /usr/share/nginx/html

# Exponer puerto
EXPOSE 80

# Iniciar Nginx
CMD ["nginx", "-g", "daemon off;"]
