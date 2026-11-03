# 03 — Aplicación Python (interfaz gráfica)

## Qué

Aplicación con **interfaz gráfica** (CustomTkinter) que conecta a MongoDB `bdautos` y permite:

1. Elegir cualquiera de las 25 consultas en un menú lateral
2. Ver el **código del pipeline** (JSON)
3. Pulsar **Ejecutar consulta** y ver los **datos resultantes**

## Cómo está armada

| Archivo | Rol |
|---------|-----|
| `app/gui.py` | Ventana CustomTkinter (lista + código + resultado) |
| `app/main.py` | Punto de entrada → lanza la GUI |
| `app/queries.py` | Definición de las 25 consultas |
| `app/db.py` | Conexión MongoDB |
| `app/requirements.txt` | `pymongo`, `customtkinter` |

### Uso

```bash
cd proyecto2doParcial
/opt/homebrew/bin/python3.12 -m venv .venv
.venv/bin/pip install -r app/requirements.txt
.venv/bin/python scripts/migrate.py   # si hace falta
./iniciar.sh
# o: .venv/bin/python app/main.py
```

En macOS usar Python 3.12 de Homebrew + `python-tk@3.12` (el Python del sistema no muestra bien la ventana).

## Por qué GUI

El enunciado pide una aplicación Python que muestre código + resultado. CustomTkinter cumple eso con una ventana simple (sidebar + paneles).
