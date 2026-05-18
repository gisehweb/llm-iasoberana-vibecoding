## Instrucciones de Uso y Despliegue del Sistema

El script `resumidor.py` fue diseñado siguiendo principios de modularidad y configuración desacoplada. No requiere modificar ninguna línea de código para cambiar de entorno, ya que toda la configuración se realiza mediante argumentos de línea de comandos (CLI) o variables de entorno.

### Prerrequisitos del Entorno

#### Cliente
- Tener instalado **Python 3.10** o superior.
- El script utiliza únicamente librerías estándar de Python, sin dependencias externas.

#### Servidor
- Tener el motor de contenedores **Podman** en ejecución.
- Tener levantado el contenedor de **Ollama** con el puerto `11434` expuesto.
- Contar con el modelo `smollm` descargado.

#### Red
- Cliente y servidor deben encontrarse dentro de la misma red local (LAN/Wi-Fi) o dentro de la misma máquina física de laboratorio.

---

## Paso 1: Inicialización de la Infraestructura (Servidor)

### Iniciar el contenedor de Ollama

```bash
podman start ollama
```

### Verificar que el modelo responda correctamente

```bash
podman exec -it ollama ollama run smollm
```

Cuando aparezca el prompt interactivo `>>>`, escribir:

```text
/exit
```

para volver a la terminal.

### Obtener la IP local IPv4 del servidor

```bash
ip addr show | grep "inet " | grep -v "127.0.0.1"
```

Para los ejemplos de laboratorio se utilizará la siguiente IP:

```text
192.168.1.199
```

---

## Paso 2: Ejecución del Script Cliente

Antes de ejecutar cualquiera de los siguientes comandos, es necesario ubicarse en la carpeta donde se encuentra el archivo `resumidor.py`.

Por ejemplo:

```bash
cd ~/llm-iasoberana-vibecoding
```

El script soporta tres modalidades de configuración sin necesidad de modificar el código fuente.

### Modalidad 1: Parámetros explícitos por consola (CLI)

Permite indicar todos los parámetros directamente al ejecutar el script.

```bash
python3 resumidor.py licencia.txt --host 192.168.1.199 --port 11434 --model smollm
```

---

### Modalidad 2: Variables de Entorno

Permite definir la configuración una sola vez durante la sesión de terminal.

```bash
export OLLAMA_HOST=192.168.1.199
export OLLAMA_PORT=11434
export OLLAMA_MODEL=smollm
```

Luego, el script puede ejecutarse únicamente indicando el archivo:

```bash
python3 resumidor.py licencia.txt
```

---

### Modalidad 3: Configuración Mixta

Las variables de entorno funcionan como valores predeterminados, pero pueden sobrescribirse temporalmente mediante argumentos CLI.

```bash
export OLLAMA_PORT=11434
export OLLAMA_MODEL=smollm
```

Ejecución sobrescribiendo únicamente la IP del servidor:

```bash
python3 resumidor.py licencia.txt --host 192.168.1.45
```

---

## Sistema de Ayuda y Depuración Integrado

El script incorpora el módulo estándar `argparse`, permitiendo consultar automáticamente las opciones disponibles y habilitar herramientas de depuración sin necesidad de modificar el código fuente.

### Mostrar ayuda

```bash
python3 resumidor.py --help
```

### Salida esperada

```text
usage: resumidor.py [-h] [--host HOST] [--port PORT] [--model MODEL] [--debug] archivo

Genera un resumen de 3 líneas de un archivo de texto usando Ollama.

positional arguments:
  archivo        Ruta al archivo de texto que se desea resumir

options:
  -h, --help     show this help message and exit
  --host HOST    IP del servidor Ollama
  --port PORT    Puerto TCP donde escucha Ollama (default: 11434)
  --model MODEL  Nombre del modelo cargado en Ollama (default: smollm)
  --debug        Activa modo debug y muestra información detallada
```

---

## Modo Debug

Durante las etapas de prueba y depuración se incorporó un modo especial de diagnóstico utilizando el argumento `--debug`.

Este modo fue agregado mediante prompting como parte del proceso de Vibe Coding para facilitar el análisis del comportamiento interno del programa y de las respuestas generadas por Ollama.

### Ejecutar el script en modo debug

```bash
python3 resumidor.py licencia.txt --host 192.168.1.199 --port 11434 --model smollm --debug
```

Cuando el modo debug está activado, el programa muestra información adicional útil para diagnóstico y auditoría del proceso de inferencia.

### Información mostrada en modo debug

- contenido leído desde el archivo
- prompt completo enviado al modelo
- payload JSON generado para la API
- respuesta completa devuelta por Ollama
- respuesta cruda del modelo
- cantidad de líneas generadas
- estadísticas de palabras y caracteres
- advertencias cuando el modelo excede el límite esperado de líneas

### Objetivo del modo debug

La incorporación del sistema de debug permitió:

- comprender mejor cómo el modelo interpretaba los prompts
- analizar por qué el modelo no respetaba siempre las 3 líneas solicitadas
- verificar el contenido exacto enviado a la API
- depurar problemas relacionados con el formato de salida
- mejorar progresivamente el prompting mediante iteración

Este mecanismo fue especialmente útil durante las pruebas con el modelo `smollm`, ya que permitió observar cómo pequeños cambios en el prompt modificaban significativamente el comportamiento de la IA.