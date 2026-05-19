# INFORME

# Arquitectura

Utilizamos Podman como herramienta de contenedorizaciòn, debido a que es una alternativa libre, daemonless y rootless a Docker.

El modelo elegido fue "smollm", ya que es un modelo ultraligero optimizado para funcionar en equipos con pocos recursos de 
hardware, bajo consumo de RAM y ejecuciòn en CPU.

El servicio de IA se ejecutò localmente mediante Ollama dentro de un contenedor Podman, exponiendo la API en el puerto "11434".

## Instalaciòn de Podman

```bash
sudo apt update
sudo apt install podman
```
## Despliegue del contenedor Ollama

```bash
podman run -d -v ollama:/root/.ollama -p 11434:11434 --name ollama docker.io/ollama/ollama
```

### Explicaciòn de paràmetros

- `-d`: ejecuta el contenedor en segundo plano.
- `-v`: crea un volumen persistente para almacenar los modelos descargados.
- `-p 11434:11434`: expone el puerto de la API de Ollama.
- `--name ollama`: asigna un nombre al contenedor. 

## Descarga del modelo

```bash
podman exec -it ollama ollama run smollm
```

## Verificaciòn de la API

```bash
curl http://localhost:11434
```

Respuesta obtenida:

```text
Ollama is running
```

## Verificaciòn de modelos instalados

```bash
curl http://localhost:11434/api/tags
```

## Bitácora de Vibe Coding

Se verificó el funcionamiento de la infraestructura local utilizando Podman y Ollama.

Comandos utilizados:

```bash
podman start ollama
curl http://localhost:11434
podman exec -it ollama ollama run smollm
```

Durante las pruebas se comprobó el funcionamiento del contenedor y la disponibilidad de la API local.

## Reflexión Soberana

Trabajar con herramientas libres y procesamiento local permitió mantener el control de los datos utilizados durante el desarrollo del trabajo, evitando enviarlos a servicios externos o nubes privativas. Esto representa una ventaja en términos de privacidad, independencia tecnológica y transparencia. Como desventaja, observamos que el rendimiento depende directamente del hardware disponible y que la configuración inicial requiere más tiempo y conocimientos técnicos que utilizar plataformas ya configuradas en la nube.
