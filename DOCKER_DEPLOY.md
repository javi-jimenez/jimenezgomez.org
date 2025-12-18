# Despliegue de Blog Hugo con Docker y Drone CI

## 📋 Opciones de despliegue

### Opción 1: Docker Compose (Local/VPS)
```bash
docker-compose up -d
```

Acceso: `http://localhost`

### Opción 2: Drone CI + Docker Registry

1. **Configurar Drone CI en tu Gitea:**
   - Ir a `https://tu-gitea.com/admin/packages`
   - Habilitar Docker Registry
   - Crear token de acceso personal

2. **Configurar secretos en Drone:**
   ```
   - ftp_server: tu-servidor-ftp.ovh.net
   - ftp_username: tu-usuario
   - ftp_password: tu-contraseña
   ```

3. **Push activa automáticamente:**
   - El archivo `.drone.yml` define el pipeline
   - Drone compila, construye la imagen Docker
   - Despliega a OVH via FTP

### Opción 3: Gitea Runners + Drone

```bash
# En tu servidor con Gitea:
docker run -d \
  -e GITEA_RPC_CLIENT="http://gitea:3000" \
  -e GITEA_INSTANCE_URL="https://tu-gitea.com" \
  -e GITEA_RUN_UID=1000 \
  -e GITEA_RUN_GID=1000 \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v /data/runner:/data/runner \
  gitea/act_runner:latest
```

## 🏗️ Estructura

```
├── Dockerfile           # Build multi-stage: Hugo + Nginx
├── nginx.conf          # Configuración de Nginx
├── docker-compose.yml  # Para desarrollo local
├── .drone.yml          # Pipeline de CI/CD
└── build.sh            # Script para compilar localmente
```

## 🚀 Flujo de despliegue con Drone

1. Haces `git push` a main
2. Gitea notifica a Drone
3. Drone ejecuta `.drone.yml`:
   - Compila el sitio con Hugo
   - Construye imagen Docker
   - Sube vía FTP a OVH
4. Tu sitio se actualiza automáticamente

## 📝 Variables de entorno

En Drone, configura como secretos:
- `ftp_server` - Servidor FTP de OVH
- `ftp_username` - Usuario FTP
- `ftp_password` - Contraseña FTP
- `docker_registry_server` (opcional)
- `docker_registry_username` (opcional)
- `docker_registry_password` (opcional)

## 🔒 Seguridad

- Los secretos se encriptan en Drone
- El Dockerfile usa multi-stage para reducir tamaño
- Nginx con gzip y cache headers
- No expongas credenciales en `.drone.yml`

## 💡 Próximos pasos

1. Elige la opción que más te guste (Docker Compose es la más simple)
2. Configura los secretos en Drone si usas CI/CD
3. Prueba localmente con `docker-compose up`
4. Confirma y sube los cambios a Git
