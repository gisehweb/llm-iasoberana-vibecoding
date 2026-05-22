# INFORME

## Arquitectura
Entorno: GNU/Linux con Podman (alternativa libre, daemonless y rootless a Docker).

Comandos utilizados:

bash
podman run -d -v ollama:/root/.ollama -p 11434:11434 --name ollama docker.io/ollama/ollama
podman ps
curl http://localhost:11434
podman exec -it ollama ollama run smollm
Modelo elegido: smollm (ultraligero, optimizado para CPU y poca RAM).

Infraestructura validada: El contenedor Ollama quedó corriendo en el puerto 11434, accesible desde localhost

## Bitácora de Vibe Coding
Como main realice el cambio de rama a infraestructura:

bash
git checkout feature/infra
podman start ollama
curl http://localhost:11434
podman exec -it ollama ollama run smollm
 Validación de que el contenedor Ollama estaba corriendo y el modelo smollm funcionaba.

Luego cambie de main a la rama scripting:

bash
git checkout feature/scripting
git pull origin feature/scripting
 Descarga de resumidor.py y archivos asociados.

Prueba del script:

bash
echo "Este es un texto de prueba para verificar el resumen automático." > prueba.txt
python3 resumidor.py prueba.txt --host localhost --model smollm
 Resultado: el script se conectó a Ollama y generó un resumen de 3 líneas.

En la siguiente imagen se puede observar parte del proceso:
![Historial de commits y archivos](img/git_log.PNG)

## Reflexión Soberana
El trabajo en equipo nos permitió comprobar que la soberanía tecnológica no es solo un concepto, sino una práctica concreta. Cada integrante tuvo que asumir un rol distinto y complementario: levantar la infraestructura con Podman y Ollama, generar el script mediante prompting con IA, y mantener el repositorio integrado y ordenado. Esto nos obligó a coordinar ramas, resolver conflictos cada uno de nosotros creo un informe.md que detallara lo que hizo cada uno, tambien creamos uno general resumiendo nuestras partes en el proyecto.

La experiencia mostró que la ventaja principal fue aprender a construir un sistema completo sin depender de servicios externos, controlando cada paso desde la instalación hasta la automatización. También nos dio independencia para experimentar con distintos modelos y validar resultados en nuestro propio entorno.

Las dificultades estuvieron en la práctica: hardware limitado, errores de conexión, modelos que no cumplían con las instrucciones, y la necesidad de iterar varias veces con la IA para lograr un script estable. Resolver estos problemas nos obligó a trabajar de manera colaborativa, documentar cada paso y apoyarnos mutuamente en las ramas de GitHub.
