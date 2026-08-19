# docker-registry-ui-ex4100-bullseye

Docker Registry + Docker Registry UI adaptados para WD My Cloud EX4100 ARMv7 / My Cloud OS 5.

## Incluye

- Docker Distribution Registry 3.1.1 sobre Debian Bullseye
- Joxit Docker Registry UI 2.6.0 sobre Debian Bullseye
- Branding OsCrisCloud (logo y favicon)
- Tema claro/oscuro automático
- Parche de reintento para fallos transitorios de `/tags/list`
- Stack completo para Portainer CE
- Script PowerShell para compilar y publicar ambas imágenes ARMv7

## Estructura

```text
registry/
  Dockerfile
  config.yml

ui/
  Dockerfile
  apply-branding.py
  entrypoint.sh
  favicon.ico
  oscriscloud-registry-favicon.png
  oscriscloud-registry-logo.png

build-images.ps1
portainer-stack.yml
README.md
```

## Construir y publicar las imágenes

Desde Windows PowerShell:

```powershell
.\build-images.ps1
```

Publica:

```text
ovelayos/docker-registry-wd-ex4100:3.1.1-bullseye
ovelayos/docker-registry-wd-ex4100:latest
ovelayos/docker-registry-ui-wd-ex4100:2.6.0-bullseye-r2
ovelayos/docker-registry-ui-wd-ex4100:latest
```

## Portainer

Despliega el contenido completo de `portainer-stack.yml`.

Endpoints predeterminados:

```text
Registry API: http://192.168.178.130:5000
Registry UI:  http://192.168.178.130:5005
```

Datos persistentes del Registry:

```text
/mnt/HD/HD_a2/docker/registry
```

## Registry local por HTTP

El Docker daemon del EX4100 debe incluir:

```json
{
  "insecure-registries": [
    "192.168.178.130:5000"
  ]
}
```

Puedes recargar esa configuración sin reiniciar el NAS:

```sh
kill -HUP $(pidof dockerd)
```

## Upstream

La UI está basada en Joxit Docker Registry UI y mantiene la licencia AGPL-3.0 del proyecto upstream.
