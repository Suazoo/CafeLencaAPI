import json
import os
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from fastapi import HTTPException


def consultar_gemini(prompt: str) -> dict:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise HTTPException(status_code=503, detail="La integración de IA no está configurada en el servidor.")
    modelo = os.getenv("GEMINI_MODEL", "gemini-3.5-flash-lite")
    request = Request(
        f"https://generativelanguage.googleapis.com/v1beta/models/{modelo}:generateContent?key={api_key}",
        data=json.dumps({
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {"responseMimeType": "application/json"},
        }).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urlopen(request, timeout=30) as response:
            respuesta = json.loads(response.read().decode("utf-8"))
    except HTTPError as exc:
        if exc.code in (401, 403):
            raise HTTPException(status_code=502, detail="La clave de Gemini no es válida o no tiene permisos.") from exc
        if exc.code == 429:
            raise HTTPException(status_code=503, detail="Gemini alcanzó temporalmente su límite gratuito.") from exc
        raise HTTPException(status_code=502, detail="Gemini no pudo procesar la solicitud.") from exc
    except (TimeoutError, URLError) as exc:
        raise HTTPException(status_code=504, detail="Gemini no respondió a tiempo.") from exc
    try:
        texto = respuesta["candidates"][0]["content"]["parts"][0]["text"]
        return json.loads(texto)
    except (KeyError, IndexError, TypeError, json.JSONDecodeError) as exc:
        raise HTTPException(status_code=502, detail="Gemini devolvió una respuesta inválida.") from exc
