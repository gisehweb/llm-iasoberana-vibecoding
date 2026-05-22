## Bitácora de Vibe Coding

Durante el desarrollo de la actividad se trabajó utilizando asistentes de IA de pesos abiertos bajo el enfoque de *Vibe Coding*. La lógica del sistema y los requisitos fueron definidos manualmente, mientras que la generación y corrección del código se realizó mediante prompting e iteración continua.

Inicialmente se utilizó Hugging Face Chat para generar la primera versión del script. Posteriormente, debido a las limitaciones del plan gratuito, se continuó el desarrollo utilizando DeepSeek.

### Prompt inicial utilizado

```text
Quiero que genere un script en Python utilizando únicamente librerías estándar o de código abierto.

El objetivo del script es:

* Leer cualquier archivo de texto indicado por el usuario mediante argumento de terminal.
* Enviar el contenido de ese archivo a una API local de Ollama que está ejecutándose en una IP y puerto específico de la red local.
* Pedirle al modelo que genere un resumen de exactamente 3 líneas.
* Mostrar el resumen por pantalla.

Requisitos importantes:

* El script debe funcionar con cualquier archivo de texto plano.
* La conexión debe hacerse usando HTTP hacia la API local de Ollama.
* El modelo debe poder definirse fácilmente en una variable.
* Debe incluir manejo básico de errores.
* Debe ejecutarse desde terminal.
* La URL de Ollama NO debe ser localhost.
* La API ya está levantada por otro integrante usando Podman.
```

### Iteraciones y errores encontrados

A medida que el script fue siendo probado, aparecieron distintos problemas que fueron reenviados a la IA junto con los mensajes de error obtenidos desde la terminal.

Uno de los primeros inconvenientes fue un problema de conectividad y timeout al intentar comunicarse con Ollama. El script agotaba el tiempo de espera antes de recibir respuesta del modelo. Para solucionarlo, se le indicó a la IA que mantuviera la estructura original del código pero aumentara el tiempo de espera de:

```python
timeout=30
```

a:

```python
timeout=300
```

También surgieron errores relacionados con:

* uso incorrecto de `localhost`,
* errores HTTP,
* modelos inexistentes en el servidor,
* y problemas de conexión hacia la instancia remota de Ollama.

Todos estos errores fueron copiados desde la terminal y reenviados directamente a la IA para que propusiera nuevas versiones del código o mejoras en el manejo de excepciones.

Posteriormente aparecieron problemas relacionados con la calidad de los resúmenes generados por el modelo `smollm`. En muchos casos el modelo:

* generaba respuestas demasiado largas,
* repetía líneas,
* agregaba frases como:
  
```text
"Este es un resumen de..."
```

* o devolvía respuestas fuera de contexto.

Para intentar solucionarlo, se realizaron nuevas iteraciones sobre el prompt enviado a Ollama, agregando instrucciones más estrictas para obligar al modelo a responder únicamente con tres líneas.

Además, la IA propuso incorporar funciones de limpieza y validación para:

* eliminar frases introductorias,
* detectar líneas duplicadas,
* filtrar respuestas inválidas,
* y reconstruir automáticamente el resumen cuando el modelo fallaba.

También se agregó un modo `--debug` que permitía visualizar:

* el contenido leído,
* el prompt enviado,
* el payload JSON,
* y la respuesta completa devuelta por Ollama.

Finalmente, durante las pruebas se observó que el sistema funcionaba mejor utilizando textos cortos o información relativamente pequeña, especialmente al trabajar con modelos livianos como `smollm`.

La experiencia permitió comprender cómo utilizar prompting e iteración continua para desarrollar y depurar software asistido por IA sin modificar manualmente el código generado.
