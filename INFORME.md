# Informe de Desarrollo y Depuración del Script `resumidor.py`

# Conversaciones con las IA:

https://huggingface.co/chat/r/ftJhSr0?leafId=da4bfee8-6a6d-4747-bf18-4a7096684d61

https://chat.deepseek.com/share/sxkodlxhyw8kdkkbie


## Introducción

Durante esta actividad se trabajó utilizando el enfoque de Vibe Coding, donde la inteligencia artificial fue utilizada como asistente para diseñar, mejorar y depurar un script en Python capaz de comunicarse con una instancia local de Ollama mediante HTTP.

El objetivo principal fue desarrollar una herramienta simple y flexible que permitiera:

- Leer un archivo de texto desde la terminal.
- Enviar su contenido a una API de Ollama en la red local.
- Solicitar un resumen automático de exactamente 3 líneas.
- Mostrar el resultado por pantalla.
- Manejar errores comunes de ejecución y conectividad.

La interacción con la IA permitió iterar progresivamente sobre el código, agregando mejoras de configuración, manejo de errores y diagnóstico de red.

## Desarrollo del Script

La primera versión del programa fue diseñada utilizando únicamente librerías estándar de Python:

- `sys`
- `os`
- `json`
- `urllib`

El script realizaba las siguientes tareas:

1. Validación del argumento recibido desde terminal.
2. Verificación de existencia del archivo.
3. Lectura del contenido en UTF-8.
4. Construcción del prompt para Ollama.
5. Envío de una petición HTTP POST hacia `/api/generate`.
6. Recepción y parseo de la respuesta JSON.
7. Impresión del resumen generado.

Además, incluía manejo básico de errores:

- Archivo inexistente.
- Error de lectura.
- Respuesta JSON inválida.
- Fallos de conexión HTTP.

## Mejora de Configuración (Vibe Coding)

Inicialmente, la IP del servidor Ollama, el puerto y el modelo estaban escritos directamente dentro del código:

```python
OLLAMA_IP = "192.168.1.45"
OLLAMA_PORT = 11434
MODEL_NAME = "llama3"
```

Esto obligaba a editar el archivo `.py` cada vez que cambiaba la máquina o el modelo utilizado.

Para resolver este problema, la IA propuso migrar la configuración hacia:

- argumentos de terminal (`--host`, `--port`, `--model`)
- variables de entorno (`OLLAMA_HOST`, `OLLAMA_PORT`, `OLLAMA_MODEL`)

Para ello se incorporó la librería estándar `argparse`.

El nuevo diseño permitió ejecutar el programa de distintas maneras.

### Ejemplo usando argumentos

```bash
python3 resumidor.py licencia.txt --host 192.168.1.45 --port 11434 --model smollm
```

### Ejemplo usando variables de entorno

```bash
export OLLAMA_HOST=192.168.1.45
export OLLAMA_PORT=11434
export OLLAMA_MODEL=smollm

python3 resumidor.py licencia.txt
```

## Problemas Encontrados Durante las Pruebas

Durante la primera ejecución apareció el siguiente error:

```text
TimeoutError: timed out
```

El script esperaba 30 segundos la respuesta de Ollama y luego finalizaba abruptamente porque el `TimeoutError` no estaba siendo capturado correctamente.

Para solucionarlo, la IA sugirió agregar manejo específico para:

```python
except TimeoutError:
```

y también:

```python
except ConnectionRefusedError:
```

De esta manera el programa dejó de finalizar con un traceback completo y comenzó a mostrar mensajes de error más amigables para el usuario.

## Diagnóstico de Red

Inicialmente se utilizó:

```bash
--host localhost
```

Sin embargo, esto generaba timeout.

La IA explicó que:

- `localhost` puede resolver a IPv6 (`::1`)
- mientras que Podman estaba publicando el puerto únicamente en IPv4 (`0.0.0.0`)

Por ello recomendó utilizar directamente:

```bash
127.0.0.1
```

o una IP de red local.

Luego se intentó utilizar:

```bash
192.168.1.45
```

pero apareció:

```text
No route to host
```

La IA ayudó a interpretar correctamente el error indicando que:

- la IP no existía en la red local
- o el servidor no estaba encendido
- o pertenecía a otra subred

Posteriormente se verificó que el contenedor de Ollama estaba ejecutándose localmente mediante:

```bash
podman ps
```

La salida observada fue:

```text
0.0.0.0:11434->11434/tcp
```

Esto confirmó que:

- el contenedor estaba activo
- el puerto estaba correctamente publicado

## Identificación de la IP Correcta

La IA indicó que el servidor Ollama estaba ejecutándose en la misma máquina del usuario y sugirió utilizar la IP local real del equipo.

La IP detectada fue:

```text
192.168.1.199
```

Entonces se probó:

```bash
python3 resumidor.py licencia.txt --host 192.168.1.199 --port 11434 --model smollm
```

## Persistencia del Timeout

Aun utilizando la IP correcta, el modelo continuó respondiendo lentamente y el programa agotó el timeout de 30 segundos.

Esto permitió identificar otro posible problema:

- el modelo `smollm` podía estar tardando demasiado en cargar
- o el contenedor estaba demorando la inferencia inicial

En esta etapa se decidió modificar manualmente el timeout del código para permitir más tiempo de respuesta.

## Aprendizajes Obtenidos

Durante la actividad se trabajaron varios conceptos importantes.

### Python

- manejo de archivos
- uso de `argparse`
- consumo de APIs HTTP
- parseo JSON
- manejo de excepciones

### Redes

- diferencias entre `localhost`, `127.0.0.1` e IPs LAN
- diagnóstico de conectividad
- uso de `ping`
- uso de `nc`
- publicación de puertos con Podman

### IA y Vibe Coding

Se aplicó el paradigma de Vibe Coding:

- construir rápidamente
- iterar mediante prompting
- mejorar gradualmente
- separar configuración de lógica
- utilizar prompts como mecanismo principal de experimentación

## Conclusión

La interacción con la IA permitió desarrollar un script funcional y modular utilizando únicamente herramientas estándar de Python.

Además del desarrollo del programa, la experiencia permitió comprender:

- cómo se comunica un cliente Python con una API de IA local
- cómo diagnosticar errores reales de red
- cómo adaptar una aplicación a entornos distribuidos
- cómo utilizar prompting iterativo para evolucionar un sistema

La actividad también mostró que muchos errores inicialmente atribuidos al código en realidad provenían de problemas de infraestructura, configuración de red o tiempos de respuesta del modelo.

# Prompts Utilizados Durante el Desarrollo

A continuación se incluyen algunos de los principales prompts utilizados durante la interacción con la IA para desarrollar y mejorar el script `resumidor.py`.

## Prompt Inicial

```text
Quiero que generes un script en Python utilizando únicamente librerías estándar o de código abierto.

El objetivo del script es:

* Leer cualquier archivo de texto indicado por el usuario mediante argumento de terminal.
* Enviar el contenido de ese archivo a una API local de Ollama que está ejecutándose en una IP y puerto específicos de la red local.
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
* No uses frameworks complejos.
* Explicá también cómo ejecutar el script y cómo instalar las dependencias necesarias.
* Agregá un ejemplo de uso.

Además:

* La URL de Ollama NO debe ser localhost. Debe quedar preparada para usar una IP de red local y puerto configurable.
* La API de Ollama ya está levantada por otro integrante usando Podman.
* El código debe seguir el enfoque de “Vibe Coding”: claro, simple y fácil de iterar mediante prompting.

Finalmente:

* Explicá brevemente cómo funciona cada parte del código.
```

## Prompt para Mejorar la Configuración

```text
la verdad no me gustaria tener que entrar al archivo y cambiar la ollama ip, el puerto y el modelo de nombre
```

A partir de este prompt, la IA propuso utilizar:

- argumentos de terminal
- variables de entorno
- argparse

para evitar modificar el código manualmente.

## Prompt Relacionado con los Errores

Luego de probar el script se obtuvieron errores de timeout y conectividad, por lo que se enviaron mensajes mostrando la salida de la terminal:

```text
python3 resumidor.py licencia.txt --host localhost --port 11434 --model smollm
```

y posteriormente:

```text
python3 resumidor.py licencia.txt --host 192.168.1.45 --port 11434 --model smollm
```

La IA analizó los mensajes de error y propuso mejoras en el manejo de excepciones y diagnóstico de red.

## Uso de Distintas IA Durante el Desarrollo

Durante el desarrollo del script se utilizaron distintas herramientas de inteligencia artificial generativa.

La mayor parte del código y del proceso de depuración fue realizada utilizando un modelo accesible desde Hugging Face, el cual fue utilizado para:

- generar la estructura inicial del script
- mejorar el manejo de errores
- implementar configuración mediante argumentos y variables de entorno
- diagnosticar problemas de red y conectividad
- explicar el funcionamiento del código

Sin embargo, durante la actividad se alcanzó el límite de mensajes disponibles en dicha plataforma, por lo que fue necesario continuar el trabajo utilizando otra IA.

Para el ajuste final del programa se utilizó DeepSeek, específicamente para modificar el tiempo de espera (`timeout`) de la conexión HTTP hacia Ollama.

El prompt enviado a DeepSeek fue:

```text
¿Podrías darle más de 30 segundos al código para que responda? unos 300 estarian bien

en si lo codigo esta bien, y funciona solo esa modificacion estaria bien, dame todo el codigo, modificando eso, en esta actividad no puedo modificar nada a mano, asi que solo modifica eso, no cambies nada mas del codigo quiero los comentarios exactamente iguales
```

El cambio solicitado fue aumentar el tiempo de espera desde:

```python
timeout=30
```

hasta aproximadamente:

```python
timeout=300
```

Esto permitió darle más tiempo al modelo para responder, especialmente durante la primera inferencia o cuando el contenedor demoraba en procesar solicitudes.

Posteriormente, una vez corregido el problema de timeout y lograda la conexión correcta con la API de Ollama, el script consiguió generar correctamente un resumen del archivo enviado.

Durante una de las pruebas exitosas se ejecutó:

```bash
python3 resumidor.py /home/brendauichaques/Documentos/cuento.txt
```

La salida obtenida fue:

```text
🔗 Conectando a Ollama en http://192.168.1.199:11434/api/generate (modelo: smollm)...

==================================================
RESUMEN (3 líneas)
==================================================
Había una vez un pequeño zorro llamado Milo que vivía en un bosque cerca de un río. Aunque todos los animales lo consideraban muy inteligente, Milo tenía un gran problema: nunca terminaba lo que empezaba. Un día quería aprender a pescar, al siguiente intentaba trepar árboles, y después abandonaba todo para perseguir mariposas.

Una mañana, mientras caminaba por el bosque, encontró a una vieja tortuga llamada Alba que llevaba una semilla en el caparazón. Milo se rió y le preguntó por qué caminaba tan lento solo para llevar una pequeña semilla de un lugar a otro. Alba respondió que quería plantarla junto al río para que algún día creciera un árbol que diera sombra a todos los animales.

Milo comprende que era una pérdida de tiempo. Sin embargo, durante las semanas siguientes observó cómo Alba regresaba cada día para regar la semilla. Pasaron las estaciones y, poco a poco, comenzó a crecer un árbol fuerte y alto. En verano, los animales descansaban bajo su sombra y los pájaros hacieron nidos en sus ramas.

Entonces Milo comprendió algo importante: las cosas valiosas necesitan paciencia y constancia. Desde ese día decidió terminar al menor a tarea antes de comenzar otra. Con el tiempo aprendió a pescar y también a construir refugios para el invierno. Aunque seguía siendo curioso y aventurero, ya no abandonaba todo a mitad de camino.
==================================================
```

Aunque el script funcionó correctamente y la IA respondió al pedido realizado, durante las pruebas se observó que el modelo `smollm` no siempre respetaba exactamente la restricción de generar únicamente 3 líneas.

A partir de este comportamiento, se continuó iterando mediante prompting para mejorar el resultado del resumen. Entre las mejoras propuestas por la IA se incluyeron:

- prompts más estrictos y específicos
- instrucciones explícitas indicando “EXACTAMENTE 3 líneas”
- reducción de creatividad usando parámetros como `temperature`
- limitación automática de líneas en la salida

También se incorporó un sistema de depuración (`--debug`) solicitado mediante prompting, con el objetivo de visualizar información interna del programa durante la ejecución.

El modo debug permitió mostrar:

- el contenido leído desde el archivo
- el prompt completo enviado a Ollama
- el payload JSON generado
- la respuesta cruda devuelta por el modelo
- estadísticas de la respuesta (líneas, palabras y caracteres)
- advertencias cuando el modelo excedía el límite esperado de líneas

El nuevo modo podía ejecutarse de la siguiente manera:

```bash
python3 resumidor.py licencia.txt --host 192.168.1.199 --port 11434 --model smollm --debug
```

La incorporación de este sistema de depuración facilitó enormemente el análisis del comportamiento del modelo y permitió comprender con mayor claridad cómo Ollama interpretaba los prompts enviados.

Estas pruebas permitieron comprender mejor cómo pequeños cambios en el prompting afectan directamente el comportamiento del modelo y la calidad de la salida generada.

De esta manera, el desarrollo final del script fue resultado de un proceso iterativo utilizando múltiples asistentes de IA, manteniendo siempre el enfoque de Vibe Coding y experimentación progresiva mediante prompting.