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
import re


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


def extraer_primeras_oraciones(texto, num_oraciones=3):
    """
    Extrae las primeras N oraciones completas de un texto.
    Esta función se usa cuando el modelo no responde correctamente.
    """
    # Limpiar el texto
    texto = texto.strip()
    
    # Dividir por puntuación que indica fin de oración
    # Patrón: punto, exclamación o interrogación seguido de espacio o fin de línea
    oraciones = re.split(r'(?<=[.!?])\s+(?=[A-ZÁÉÍÓÚÜÑ])', texto)
    
    oraciones_limpias = []
    for oracion in oraciones[:num_oraciones]:
        oracion = oracion.strip()
        # Asegurar que termine con puntuación
        if oracion and not oracion[-1] in '.!?':
            oracion += '.'
        if len(oracion) > 10:  # Ignorar oraciones muy cortas
            oraciones_limpias.append(oracion)
    
    # Si no encontramos suficientes oraciones, intentamos con un método más simple
    if len(oraciones_limpias) < num_oraciones:
        # Dividir por punto simple
        simple = [p.strip() + '.' for p in texto.split('.') if len(p.strip()) > 10]
        oraciones_limpias = simple[:num_oraciones]
    
    # Rellenar si faltan líneas
    while len(oraciones_limpias) < num_oraciones:
        oraciones_limpias.append("(Contenido no disponible)")
    
    return '\n'.join(oraciones_limpias[:num_oraciones])


def limpiar_resumen_smollm(resumen_crudo, texto_original, debug=False):
    """
    Limpieza específica para smollm.
    Si la respuesta es basura, extrae del texto original.
    """
    # Si la respuesta es demasiado larga o es igual al original
    if len(resumen_crudo) > len(texto_original) * 0.7:
        if debug:
            print("⚠️ El modelo devolvió texto demasiado largo, usando extracción local")
        return extraer_primeras_oraciones(texto_original, 3)
    
    # Eliminar frases comunes que smollm repite
    frases_prohibidas = [
        "Este es un resumen de",
        "Aquí tienes",
        "Here are",
        "Resume Text",
        "Introduction to",
        "Las cositas inteligentes",
    ]
    
    lineas = resumen_crudo.split('\n')
    lineas_limpias = []
    
    for linea in lineas:
        linea = linea.strip()
        # Verificar si la línea contiene frases prohibidas
        es_valida = True
        for frase in frases_prohibidas:
            if frase.lower() in linea.lower():
                es_valida = False
                break
        
        # Verificar que no sea una línea vacía o muy corta
        if es_valida and len(linea) > 20 and linea not in lineas_limpias:
            lineas_limpias.append(linea)
    
    if len(lineas_limpias) >= 3:
        if debug:
            print(f"✅ Se extrajeron {len(lineas_limpias)} líneas válidas")
        return '\n'.join(lineas_limpias[:3])
    elif len(lineas_limpias) == 2:
        if debug:
            print("⚠️ Solo 2 líneas válidas, duplicando la segunda")
        return '\n'.join(lineas_limpias + [lineas_limpias[-1]])
    elif len(lineas_limpias) == 1:
        if debug:
            print("⚠️ Solo 1 línea válida, extrayendo oraciones")
        return extraer_primeras_oraciones(lineas_limpias[0], 3)
    else:
        if debug:
            print("❌ No se encontraron líneas válidas, usando texto original")
        return extraer_primeras_oraciones(texto_original, 3)


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
    
    debug_print(cfg, "Contenido del archivo (primeros 500 chars)", 
                contenido[:500] + ("..." if len(contenido) > 500 else ""))

    # --- 4. Prompt MÍNIMO para smollm ---
    # Con smollm, menos es más. Solo pedimos "resume" sin formato complejo
    prompt = f"Resume this text in 3 short sentences:\n\n{contenido[:800]}\n\nSummary:"

    payload = {
        "model": cfg.model,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0.1,
            "num_predict": 200
        }
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
        respuesta_raw = urllib.request.urlopen(peticion, timeout=300)
    except TimeoutError:
        print(f"❌ Timeout: Ollama no respondió en 300 segundos.")
        print(f"   URL intentada: {url_ollama}")
        sys.exit(1)
    except ConnectionRefusedError:
        print(f"❌ Conexión rechazada en {url_ollama}.")
        print(f"   ¿Ollama está corriendo en el servidor?")
        sys.exit(1)
    except urllib.error.URLError as e:
        print(f"❌ Error de conexión con Ollama: {e.reason}")
        sys.exit(1)
    except urllib.error.HTTPError as e:
        if e.code == 404:
            print(f"❌ Error: El modelo '{cfg.model}' no existe en el servidor.")
            print(f"   Modelos disponibles: ejecuta 'curl {url_ollama.replace('/generate', '/tags')}'")
        else:
            print(f"❌ Error HTTP {e.code}: {e.reason}")
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
        sys.exit(1)

    resumen_crudo = datos["response"].strip()
    
    debug_print(cfg, "Respuesta cruda del modelo", resumen_crudo[:500])
    
    # --- 8. Limpieza inteligente para smollm ---
    resumen = limpiar_resumen_smollm(resumen_crudo, contenido, debug=cfg.debug)

    # --- 9. Mostrar resultado ---
    print("=" * 50)
    print("RESUMEN (3 líneas)")
    print("=" * 50)
    print(resumen)
    print("=" * 50)


if __name__ == "__main__":
    main()