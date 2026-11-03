#!/usr/bin/env python3
"""
Genera reporte HTML (+ PDF si weasyprint/pdfkit disponible) dentro de reporte/.
Ejecuta las 25 consultas contra MongoDB y embebe código + resultados.
"""

from __future__ import annotations

import html
import json
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "app"))

from bson import json_util  # noqa: E402
from db import get_db  # noqa: E402
from queries import QUERIES  # noqa: E402

OUT_DIR = ROOT / "reporte"
HTML_PATH = OUT_DIR / "reporte_proyecto2a.html"
PDF_PATH = OUT_DIR / "reporte_proyecto2a.pdf"


def dumps(obj) -> str:
    return json.dumps(json.loads(json_util.dumps(obj)), indent=2, ensure_ascii=False)


def build_html(sections: list[str]) -> str:
    body = "\n".join(sections)
    return f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8"/>
<title>Proyecto 2a — BDAutos MongoDB</title>
<style>
  body {{ font-family: Georgia, 'Times New Roman', serif; margin: 2rem auto; max-width: 960px; color: #1a1a1a; line-height: 1.45; }}
  h1, h2, h3 {{ font-family: 'Helvetica Neue', Arial, sans-serif; }}
  .meta {{ color: #444; margin-bottom: 2rem; }}
  pre {{ background: #f4f4f4; border: 1px solid #ddd; padding: 0.75rem; overflow-x: auto; font-size: 0.85rem; }}
  .query {{ page-break-inside: avoid; margin-bottom: 2rem; border-top: 1px solid #ccc; padding-top: 1rem; }}
  code {{ font-family: Menlo, Consolas, monospace; }}
  ul {{ padding-left: 1.2rem; }}
</style>
</head>
<body>
{body}
</body>
</html>
"""


def try_pdf(html_path: Path, pdf_path: Path) -> bool:
    import subprocess
    from urllib.parse import urljoin
    from urllib.request import pathname2url

    # Intento 1: Chrome / Edge headless
    browsers = [
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
        "/Applications/Chromium.app/Contents/MacOS/Chromium",
    ]
    file_url = urljoin("file:", pathname2url(str(html_path.resolve())))
    for browser in browsers:
        if not Path(browser).exists():
            continue
        try:
            subprocess.run(
                [
                    browser,
                    "--headless",
                    "--disable-gpu",
                    "--no-pdf-header-footer",
                    f"--print-to-pdf={pdf_path}",
                    file_url,
                ],
                check=True,
                capture_output=True,
                timeout=120,
            )
            if pdf_path.exists() and pdf_path.stat().st_size > 0:
                return True
        except Exception:
            continue

    # Intento 2: weasyprint
    try:
        from weasyprint import HTML  # type: ignore

        HTML(filename=str(html_path)).write_pdf(str(pdf_path))
        return True
    except Exception:
        pass

    # Intento 3: pdfkit
    try:
        import pdfkit  # type: ignore

        pdfkit.from_file(str(html_path), str(pdf_path))
        return True
    except Exception:
        pass
    return False


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    try:
        db = get_db()
    except Exception as exc:  # noqa: BLE001
        print(f"Sin MongoDB: {exc}", file=sys.stderr)
        return 1

    sections: list[str] = []
    sections.append("<h1>Proyecto 2a. Evaluación — BDAutos en MongoDB</h1>")
    sections.append(
        "<div class='meta'>"
        "<p><strong>Universidad Autónoma de Chihuahua</strong> — Bases de Datos Avanzado</p>"
        f"<p>Generado: {html.escape(datetime.now().strftime('%Y-%m-%d %H:%M'))}</p>"
        "<p>Base: <code>bdautos</code> — colecciones: continents, countries, makers, cars</p>"
        "</div>"
    )
    sections.append("<h2>1. Objetivo</h2>")
    sections.append(
        "<p>Aplicar Aggregation Framework: diseñar BD Autos con embedding y linking, "
        "migrar desde el modelo relacional, resolver 25 consultas y exponerlas con una "
        "aplicación Python que muestra el código y el resultado.</p>"
    )
    sections.append("<h2>2. Modelo documental</h2>")
    sections.append(
        "<ul>"
        "<li><strong>continents</strong>: catálogo (linking target).</li>"
        "<li><strong>countries</strong>: linking <code>continentId</code> + snapshot embebido.</li>"
        "<li><strong>makers</strong>: embedding de <code>models[]</code> + linking <code>countryId</code>.</li>"
        "<li><strong>cars</strong>: embedding Names+Details + snapshots + linking makerId/modelId.</li>"
        "</ul>"
        "<p>Detalle en <code>docs/01_modelo_y_migracion.md</code>.</p>"
    )
    sections.append("<h2>3. Migración</h2>")
    sections.append(
        "<p>Script <code>scripts/migrate.py</code> parsea <code>data/BDAutosU2.sql</code> "
        "e inserta documentos. Conteos esperados: 5 / 17 / 20 / 42 modelos / 138 autos.</p>"
    )
    counts = {
        "continents": db.continents.count_documents({}),
        "countries": db.countries.count_documents({}),
        "makers": db.makers.count_documents({}),
        "cars": db.cars.count_documents({}),
    }
    sections.append(f"<pre>{html.escape(json.dumps(counts, indent=2))}</pre>")

    sections.append("<h2>4. Consultas (código + resultado)</h2>")
    for q in QUERIES:
        results = list(db[q["collection"]].aggregate(q["pipeline"]))
        sections.append("<div class='query'>")
        sections.append(f"<h3>Consulta {q['id']}: {html.escape(q['title'])}</h3>")
        sections.append(f"<p>{html.escape(q['description'])}</p>")
        sections.append(f"<p>Colección: <code>{html.escape(q['collection'])}</code></p>")
        sections.append("<p><strong>Pipeline</strong></p>")
        sections.append(f"<pre>{html.escape(dumps(q['pipeline']))}</pre>")
        sections.append(
            f"<p><strong>Resultado</strong> ({len(results)} documentos)</p>"
        )
        # Truncar resultados muy largos en el PDF
        shown = results if len(results) <= 40 else results[:40]
        note = "" if len(results) <= 40 else f"\n... ({len(results) - 40} más omitidos en el reporte)"
        sections.append(f"<pre>{html.escape(dumps(shown) + note)}</pre>")
        sections.append("</div>")

    sections.append("<h2>5. Aplicación Python (GUI)</h2>")
    sections.append(
        "<p>Interfaz gráfica CustomTkinter en <code>app/gui.py</code> "
        "(lanzada con <code>app/main.py</code>). Muestra pipeline + resultado. "
        "Ver <code>docs/03_aplicacion_python.md</code>.</p>"
        "<pre>.venv/bin/python app/main.py</pre>"
    )
    sections.append("<h2>6. Bitácora de decisiones</h2>")
    sections.append(
        "<p>Documentación incremental en <code>docs/</code> "
        "(00_bitacora, 01_modelo, 02_consultas, 03_app, 04_entrega).</p>"
    )

    html_doc = build_html(sections)
    HTML_PATH.write_text(html_doc, encoding="utf-8")
    print(f"HTML: {HTML_PATH}")

    if try_pdf(HTML_PATH, PDF_PATH):
        print(f"PDF: {PDF_PATH}")
    else:
        # Fallback: PDF mínimo vía reportlab si está instalado
        try:
            from reportlab.lib.pagesizes import letter  # type: ignore
            from reportlab.pdfgen import canvas  # type: ignore

            c = canvas.Canvas(str(PDF_PATH), pagesize=letter)
            width, height = letter
            y = height - 50
            c.setFont("Helvetica-Bold", 14)
            c.drawString(50, y, "Proyecto 2a — BDAutos MongoDB")
            y -= 24
            c.setFont("Helvetica", 10)
            c.drawString(50, y, "Ver reporte HTML completo: reporte_proyecto2a.html")
            y -= 18
            c.drawString(50, y, "Las 25 consultas con código y resultados están en el HTML.")
            y -= 30
            for q in QUERIES:
                if y < 60:
                    c.showPage()
                    y = height - 50
                    c.setFont("Helvetica", 10)
                c.drawString(50, y, f"Q{q['id']}: {q['title'][:80]}")
                y -= 14
            c.save()
            print(f"PDF resumen: {PDF_PATH}")
        except Exception as exc:  # noqa: BLE001
            print(f"No se pudo generar PDF automáticamente ({exc}).")
            print("Entrega el HTML o convierte reporte_proyecto2a.html a PDF manualmente.")
            return 0
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
