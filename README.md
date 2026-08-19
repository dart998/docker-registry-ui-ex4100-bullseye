# docker-registry-ui-ex4100-bullseye

Joxit Docker Registry UI 2.6.0 adapted for the WD My Cloud EX4100 (ARMv7 / My Cloud OS 5) with a Debian Bullseye runtime.

This repository contains the working UI build used on OsCrisCloud, including branding, automatic light/dark theme support, favicon, and a retry patch for transient `/tags/list` failures seen on the EX4100.

## Docker image

```text
ovelayos/docker-registry-ui-wd-ex4100:2.6.0-bullseye-r2
```

## Build and push

From Windows PowerShell with Docker Desktop / Buildx:

```powershell
.\build-and-push.ps1
```

The script publishes:

```text
ovelayos/docker-registry-ui-wd-ex4100:2.6.0-bullseye-r2
ovelayos/docker-registry-ui-wd-ex4100:latest
```

## Portainer

Deploy the complete `portainer-stack.yml`. It runs both:

```text
Registry API: http://192.168.178.130:5000
Registry UI:  http://192.168.178.130:5005
```

Registry data is persisted at:

```text
/mnt/HD/HD_a2/docker/registry
```

The backend image is maintained separately in:

```text
dart998/docker-registry-ex4100
```

## Included patches

- Debian Bullseye runtime for ARMv7 compatibility.
- Uses Joxit's official `90-docker-registry-ui.sh` initializer.
- OsCrisCloud logo in the navigation bar.
- Simplified favicon without text.
- `THEME=auto` with working light/dark switch.
- Retry of transient tag-count requests before showing `Server not found`.

## Upstream

The UI is built from Joxit Docker Registry UI 2.6.0 and remains subject to the upstream AGPL-3.0 license.
