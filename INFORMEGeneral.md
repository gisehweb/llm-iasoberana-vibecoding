## Arquitectura

El proyecto se desarrolló en un entorno GNU/Linux con Podman, utilizado como alternativa libre, daemonless y rootless a Docker.
## Integrante 1 - Henriquez Gisella
– Maintainer gestionó el repositorio en GitHub, organizando ramas (feature/infra, feature/scripting), resolviendo conflictos y realizando merges.
## Integrante 2 - Agustin Diumacan
– SysAdmin levantó la infraestructura con Podman, desplegando el contenedor de Ollama en el puerto 11434 y validando su funcionamiento con el modelo smollm
## Integrante 3 - Brenda Uichaques
– Vibe Coder generó el script resumidor.py mediante prompting con IA, asegurando que pudiera conectarse a la API de Ollama y procesar archivos de texto para devolver un resumen de 3 líneas.
La arquitectura combinó infraestructura local, automatización con Python y control de versiones en GitHub, garantizando soberanía tecnológica y trazabilidad del trabajo.

## Bitácora de Vibe Coding
El enfoque de Vibe Coding se aplicó en las tres ramas del proyecto:

- Maintainer (Integrante 1):

Cambió entre ramas para validar infraestructura y scripting.

Documentó pruebas de ejecución del script con prueba.txt.

Integró evidencias gráficas en el informe (img/git_log.PNG).

Aseguró la integración de los aportes mediante merges y resolución de conflictos.

- SysAdmin (Integrante 2):

Desplegó Ollama en Podman con comandos como podman run, podman ps y curl http://localhost:11434.

Validó que el modelo smollm estuviera corriendo en el contenedor.

Documentó la configuración de red y pruebas de conectividad.

- Vibe Coder (Integrante 3):

Usó asistentes de IA (Hugging Face Chat y DeepSeek) para generar y depurar el script.

Iteró sobre errores reales (timeouts, conexión rechazada, modelos inexistentes).

Ajustó parámetros (timeout=300, temperature=0.1, num_predict=200).

Incorporó funciones de limpieza y validación (extraer_primeras_oraciones(), limpiar_resumen_smollm()).

Añadió un modo --debug para visualizar payloads y respuestas completas.

## Reflexión Soberana
El trabajo conjunto mostró que:

Ventajas: control total de la infraestructura, soberanía sobre los datos, independencia de servicios privativos, trazabilidad en GitHub y aprendizaje práctico del paradigma Vibe Coding.

Desventajas: limitaciones de hardware (CPU/RAM), necesidad de configurar manualmente el entorno, resolver errores de conexión y enfrentar las limitaciones de modelos pequeños como smollm.

La experiencia evidenció que el desarrollo asistido por IA requiere supervisión humana, análisis crítico y decisiones arquitectónicas. El enfoque distribuido por roles permitió integrar infraestructura, scripting y documentación en un mismo repositorio, logrando un sistema funcional y educativo. Cada integrante redactó su propio INFORME.md en su rama, y posteriormente se realizó un resumen integrado en un único informe general, consolidando arquitectura, bitácora y reflexión soberana.