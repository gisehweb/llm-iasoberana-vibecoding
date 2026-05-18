#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
resumidor.py
------------
Resume archivos de texto usando la API de Ollama.
Configuración 100% por CLI o variables de entorno.
"""

import sys
import os
import json
import argparse
import urllib.request
import urllib.error


DEFAULT_PORT = 11434
DEFAULT_MODEL = "llama3"


def obtener_config():
    """
    Lee argumentos de terminal y variables de entorno.
    """
    parser = argparse.ArgumentParser(
        description="Genera un resumen de 3 líneas de un archivo de texto usando Ollama."
    )

    parser.add_argument(
        "archivo",
        help="Ruta al archivo de texto que querés resumir (ej: log.txt)"
    )

    parser.add_argument(
        "--host",
        default=os.getenv("OLLAMA_HOST"),
        help="IP del servidor Ollama (también via env var OLLAMA_HOST)"
    )

    parser.add_argument(
        "--port",
        type=int,
        default=int(os.getenv("OLLAMA_PORT", str(DEFAULT_PORT))),
        help="Puerto TCP (default: 11434)"
    )

    parser.add_argument(
        "--model",
        default=os.getenv("OLLAMA_MODEL", DEFAULT_MODEL),
        help="Nombre del modelo en Ollama (default: llama3)"
    )

    parser.add_argument(
        "--debug",
        action="store_true",
        help="Activa modo debug: muestra prompt, payload y respuesta completa"
    )

    args = parser.parse_args()

    if not args.host:
        parser.error(
            "❌ Falta la IP del servidor Ollama.\n"
            "   Usá --host 192.168.x.x o definí la variable de entorno OLLAMA_HOST.\n"
            "   Ejemplo: python resumidor.py archivo.txt --host 192.168.1.45"
        )

    return args


def debug_print(cfg, titulo, contenido):
    """
    Muestra información de debug si el flag --debug está activado.
    """
    if cfg.debug:
        print("\n" + "=" * 50)
        print(f"🔍 DEBUG: {titulo}")
        print("=" * 50)
        print(contenido)
        print("=" * 50 + "\n")


def main():
    # --- 1. Configuración ---
    cfg = obtener_config()
    url_ollama = f"http://{cfg.host}:{cfg.port}/api/generate"

    print(f"🔗 Conectando a Ollama en {url_ollama} (modelo: {cfg.model})...\n")
    
    if cfg.debug:
        print("🐛 Modo debug activado - Se mostrará información detallada\n")

    # --- 2. Validar archivo ---
    if not os.path.isfile(cfg.archivo):
        print(f"❌ Error: no existe el archivo '{cfg.archivo}'.")
        sys.exit(1)

    # --- 3. Leer archivo ---
    try:
        with open(cfg.archivo, "r", encoding="utf-8") as f:
            contenido = f.read()
    except UnicodeDecodeError:
        print("❌ Error: el archivo no es texto plano válido (UTF-8).")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error leyendo el archivo: {e}")
        sys.exit(1)

    if not contenido.strip():
        print("⚠️  El archivo está vacío. Nada para resumir.")
        sys.exit(0)
    
    debug_print(cfg, "Contenido del archivo", contenido[:500] + ("..." if len(contenido) > 500 else ""))

    # --- 4. Armar prompt y payload ---
    prompt = (
        "IMPORTANTE: Tu respuesta DEBE tener EXACTAMENTE 3 líneas de texto, no más, no menos.\n"
        "NO escribas historias, NO agregues introducciones, NO pongas explicaciones.\n"
        "Solo escribe 3 líneas que resuman el siguiente texto de manera concisa.\n\n"
        "Texto a resumir:\n"
        f"{contenido}\n\n"
        "Resumen (exactamente 3 líneas):"
    )

    payload = {
        "model": cfg.model,
        "prompt": prompt,
        "stream": False
    }

    datos_json = json.dumps(payload).encode("utf-8")
    
    debug_print(cfg, "Prompt enviado a Ollama", prompt)
    debug_print(cfg, "Payload completo (JSON)", json.dumps(payload, indent=2))

    # --- 5. Crear petición HTTP POST ---
    peticion = urllib.request.Request(
        url=url_ollama,
        data=datos_json,
        method="POST",
        headers={"Content-Type": "application/json"}
    )

    # --- 6. Enviar y capturar TODOS los errores de red ---
    try:
        # timeout=300: si Ollama no responde en 300 segundos, cortamos
        respuesta_raw = urllib.request.urlopen(peticion, timeout=300)
    except TimeoutError:
        # ERROR PRINCIPAL QUE TE APARECIÓ:
        # El servidor no respondió dentro del tiempo límite.
        print(f"❌ Timeout: Ollama no respondió en 300 segundos.")
        print(f"   URL intentada: {url_ollama}")
        print(f"   ¿Ollama está levantado? ¿La IP y puerto son correctos?")
        print(f"   Si usás Podman, asegurate de que el contenedor tenga el puerto publicado.")
        sys.exit(1)
    except ConnectionRefusedError:
        # Llegamos a la IP, pero el puerto está cerrado o nadie escucha allí.
        print(f"❌ Conexión rechazada en {url_ollama}.")
        print(f"   Nadie está escuchando en ese puerto. Revisá si Ollama está corriendo.")
        sys.exit(1)
    except urllib.error.URLError as e:
        # Host inalcanzable, DNS fallido, sin ruta hacia la red, etc.
        print(f"❌ Error de conexión con Ollama:")
        print(f"   {e.reason}")
        sys.exit(1)
    except urllib.error.HTTPError as e:
        # Ollama respondió, pero con un código de error (404, 500, etc.)
        print(f"❌ Ollama respondió con error HTTP {e.code}: {e.reason}")
        sys.exit(1)

    # --- 7. Parsear respuesta JSON ---
    try:
        cuerpo = respuesta_raw.read().decode("utf-8")
        datos = json.loads(cuerpo)
    except json.JSONDecodeError:
        print("❌ Error: la respuesta de Ollama no es un JSON válido.")
        sys.exit(1)

    if "response" not in datos:
        print("❌ Error: la API no devolvió el campo 'response'.")
        print(f"   Campos recibidos: {list(datos.keys())}")
        sys.exit(1)

    resumen = datos["response"].strip()
    
    debug_print(cfg, "Respuesta completa de Ollama (JSON)", json.dumps(datos, indent=2))
    debug_print(cfg, "Respuesta cruda del modelo", resumen)
    
    # Mostrar estadísticas de la respuesta
    if cfg.debug:
        lineas_count = len(resumen.split('\n'))
        caracteres_count = len(resumen)
        palabras_count = len(resumen.split())
        print(f"📊 Estadísticas: {lineas_count} líneas, {palabras_count} palabras, {caracteres_count} caracteres\n")
    
    # Limitar a las primeras 3 líneas si el modelo se pasa
    lineas = resumen.split('\n')
    if len(lineas) > 3:
        if cfg.debug:
            print(f"⚠️  El modelo devolvió {len(lineas)} líneas. Recortando a las primeras 3.\n")
        resumen = '\n'.join(lineas[:3])

    # --- 8. Mostrar resultado ---
    print("=" * 50)
    print("RESUMEN (3 líneas)")
    print("=" * 50)
    print(resumen)
    print("=" * 50)


if __name__ == "__main__":
    main()