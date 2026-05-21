# Fase 2: Vibe Coding y Automatización

## Introducción

El objetivo de esta actividad fue desarrollar un script en Python capaz de leer un archivo de texto local, enviar su contenido a una instancia remota de Ollama mediante HTTP y obtener como respuesta un resumen automático de exactamente tres líneas.

La práctica estuvo centrada en el paradigma de *Vibe Coding*, donde el rol del desarrollador consiste en definir objetivos, restricciones y comportamiento esperado, mientras que la implementación técnica es generada y refinada mediante asistentes de IA.

Una condición importante de la actividad fue que el código no debía corregirse manualmente: todos los errores detectados durante las pruebas debían reenviarse a la IA para que propusiera nuevas versiones o soluciones.


# Objetivo de la actividad

El script debía:

* leer un archivo de texto local,
* conectarse a una API de Ollama accesible por red local,
* enviar el contenido del archivo,
* solicitar un resumen de 3 líneas,
* y mostrar el resultado por pantalla.

Además, el sistema debía:

* funcionar con distintos tipos de archivos de texto,
* utilizar únicamente librerías estándar o abiertas,
* permitir configurar IP, puerto y modelo,
* incluir manejo de errores,
* y ejecutarse desde terminal.

# Desarrollo del proceso

El desarrollo se realizó de manera iterativa en distintos días y sesiones, retomando progresivamente el trabajo a medida que aparecían nuevos problemas o necesidades de mejora.

El enfoque utilizado consistió en:

1. generar código mediante prompting,
2. ejecutar el script,
3. capturar errores reales desde terminal,
4. reenviar esos errores a la IA,
5. solicitar correcciones o mejoras,
6. volver a probar el sistema.

A lo largo del proceso se trabajó tanto sobre la generación inicial del código como sobre optimizaciones relacionadas con:

* conectividad,
* manejo de errores,
* calidad de los resúmenes,
* depuración,
* limpieza de respuestas,
* y adaptación a las limitaciones del modelo utilizado.

# Prompt inicial utilizado

```text
Quiero que genere un script en Python utilizando únicamente librerías estándar o de código abierto.

El objetivo del script es:

* Leer cualquier archivo de texto indicado por el usuario mediante argumento de terminal.
* Enviar el contenido de ese archivo a una API local de Ollama que está ejecutándose en una IP y puerto específico de la red local.
* Pedirle al modelo que genere un resumen de exactamente 3 líneas.
* Mostrar el resumen por pantalla.

Requisitos importantes:

* El script debe funcionar con cualquier archivo de texto plano (logs, licencias, archivos .txt, etc.).
* La conexión debe hacerse usando HTTP hacia la API local de Ollama.
* El modelo debe poder definirse fácilmente en una variable.
* El código debe estar comentado y explicado de forma clara porque es para una actividad educativa.
* Debe incluir manejo básico de errores:
  * archivo inexistente
  * error de conexión con Ollama
  * respuesta inválida de la API
* Debe ejecutarse desde terminal con una sintaxis similar a:
  python resumen.py archivo.txt
* No utiliza frameworks complejos.
* Explique también cómo ejecutar el script y cómo instalar las dependencias necesarias.
* Agregue un ejemplo de uso.

Además:

* La URL de Ollama NO debe ser localhost.
* Debe quedar preparado para usar una IP de red local y puerto configurable.
* La API de Ollama ya está levantada por otro integrante usando Podman.
* El código debe seguir el enfoque de “Vibe Coding”: claro, simple y fácil de iterar mediante indicaciones.

Finalmente:

* Explique brevemente cómo funciona cada parte del código.
```

# Uso de asistentes de IA

Durante el desarrollo se utilizaron distintos asistentes de IA de pesos abiertos.

Inicialmente se trabajó con Hugging Face Chat para generar la primera versión del script y realizar las primeras pruebas.

Posteriormente, debido a las limitaciones del plan gratuito, el desarrollo continuó utilizando DeepSeek para seguir iterando sobre:

* errores de conexión,
* manejo de excepciones,
* mejoras del prompt,
* depuración,
* y validación de resultados.

Las conversaciones no ocurrieron en una única sesión continua, sino en distintos momentos del proceso de desarrollo.

# Iteración y corrección de errores

Toda la depuración del proyecto se realizó mediante prompting, respetando la consigna de no modificar manualmente el código.

Entre los principales problemas detectados y corregidos se encontraron:

## Problemas de conectividad

Durante las primeras pruebas aparecieron errores relacionados con:

* `TimeoutError`
* `ConnectionRefusedError`
* uso incorrecto de `localhost`
* errores HTTP al consultar modelos inexistentes

Para resolverlos, la IA propuso:

* configuración flexible mediante argumentos CLI y variables de entorno,
* validaciones de red,
* manejo explícito de excepciones,
* y mejoras en los mensajes de error.

También se incrementó el tiempo de espera:

```python
timeout=30
```

a:

```python
timeout=300
```

para permitir que modelos más lentos pudieran responder correctamente.

## Mejora del prompt

Uno de los principales problemas detectados fue que algunos modelos devolvían respuestas demasiado largas o ignoraban el formato solicitado.

Para mejorar esto se realizaron varias iteraciones sobre el prompt enviado a Ollama, buscando:

* forzar exactamente 3 líneas,
* evitar introducciones innecesarias,
* mejorar la coherencia,
* y conservar el desenlace del texto original.

La IA propuso:

* instrucciones más estrictas,
* ejemplos de formato esperado,
* reducción de complejidad del prompt,
* y ajustes de parámetros como:

```python
temperature: 0.1
num_predict: 200
```

## Problemas con el modelo `smollm`

Durante las pruebas se detectó que el modelo `smollm` tenía dificultades para seguir instrucciones estrictas.

Entre los problemas observados aparecieron:

* respuestas incoherentes,
* repeticiones,
* líneas duplicadas,
* pérdida del desenlace,
* generación de texto fuera de contexto,
* e introducciones no deseadas como:

```text
Este es un resumen de...
```

o

```text
Here are three possible resume texts...
```

Luego de varias iteraciones, se concluyó que las limitaciones provenían principalmente del modelo y no del script.

La IA sugirió utilizar modelos más robustos como:

* `llama3`
* `phi3:mini`
* `mistral`

Sin embargo, algunos de ellos no estaban instalados en el servidor remoto de Ollama, produciendo errores como:

```text
❌ Error de conexión con Ollama:
Not Found
```

## Adaptación del script

Frente a las limitaciones del modelo, se modificó la estrategia del sistema.

En lugar de depender completamente de la respuesta generada por la IA, se incorporaron mecanismos locales de validación y limpieza del resumen.

Se agregaron funciones para:

* eliminar frases introductorias,
* detectar líneas inválidas,
* evitar duplicados,
* reconstruir resúmenes,
* y extraer oraciones directamente desde el texto original cuando el modelo fallaba.

Entre las funciones implementadas se encuentran:

```python
extraer_primeras_oraciones()
```

```python
limpiar_resumen_smollm()
```

También se incorporó un modo `--debug` que permitía visualizar:

* contenido leído,
* prompt enviado,
* payload JSON,
* respuesta completa de Ollama,
* y estadísticas de salida.

# Resultado final

El resultado fue un script funcional llamado `resumidor.py`, desarrollado íntegramente mediante iteración asistida por IA.

El sistema permite:

* resumir archivos de texto utilizando Ollama,
* conectarse a servidores remotos mediante IP configurable,
* seleccionar modelos dinámicamente,
* utilizar modo debug,
* manejar errores de red y parsing,
* y limpiar automáticamente respuestas defectuosas.

El proyecto utilizó únicamente librerías estándar de Python, principalmente:

```python
urllib.request
urllib.error
```

para realizar las peticiones HTTP.

Además, durante las pruebas se observó que el sistema funciona mejor con textos cortos o información relativamente pequeña, especialmente cuando se utilizan modelos livianos como `smollm`.

# Enlaces a conversaciones

## Hugging Face Chat

https://huggingface.co/chat/r/FGHv8AK?leafId=a8930567-e6db-432a-8074-d98145681e73

## DeepSeek

https://chat.deepseek.com/share/0k7661gri9xep0zsc3

# Conclusión

La actividad permitió experimentar de forma práctica el paradigma de *Vibe Coding*, utilizando asistentes de IA no solo para generar código, sino también para iterar, depurar y adaptar el sistema frente a errores reales.

El proceso mostró que:

* la calidad del modelo impacta directamente en los resultados,
* el prompting es una herramienta central pero no suficiente por sí sola,
* los modelos pequeños pueden tener limitaciones importantes,
* y los sistemas robustos necesitan validaciones adicionales más allá de la salida generada por IA.

También permitió comprender mejor conceptos relacionados con:

* APIs locales,
* comunicación HTTP,
* configuración por red,
* manejo de excepciones,
* y automatización mediante Python utilizando únicamente librerías estándar.

feature/scripting
Más allá del resultado técnico, la experiencia sirvió para entender que el desarrollo asistido por IA sigue requiriendo supervisión humana, análisis crítico y toma de decisiones arquitectónicas durante todo el proceso.

De esta manera, el desarrollo final del script fue resultado de un proceso iterativo utilizando múltiples asistentes de IA, manteniendo siempre el enfoque de Vibe Coding y experimentación progresiva mediante prompting.


main
