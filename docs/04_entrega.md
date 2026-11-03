# 04 — Entrega y checklist final

## Checklist vs enunciado

| # | Requisito | Evidencia | Estado |
|---|-----------|-----------|--------|
| 1 | Diseñar BD Autos (embedding + linking) | `docs/01_modelo_y_migracion.md`, colecciones `bdautos` | Cumple |
| 2 | Migrar modelo relacional → documental | `data/BDAutosU2.sql` + `scripts/migrate.py` (5/17/20/42/138) | Cumple |
| 3 | 25 consultas Aggregation | `app/queries.py`, `scripts/02_consultas.js`, `docs/02_consultas.md` | Cumple |
| 4 | App Python GUI (código + resultado) | `app/main.py` → `app/gui.py` (CustomTkinter) | Cumple |
| 5 | Repo con PDF, consultas y código | Todo bajo `proyecto2doParcial/`; PDF en `reporte/` | Cumple |
| 6 | Bitácora `.md` incremental | `docs/00`–`04` | Cumple |
| 7 | Todo dentro de `proyecto2doParcial/` | Sin artefactos del parcial en raíz `BDA/` | Cumple |

## Cómo preparar el GitHub

Desde esta carpeta (o subiendo `proyecto2doParcial` como raíz del repo):

```bash
cd proyecto2doParcial
git init   # si aún no es repo
git add data scripts app docs reporte README.md .gitignore
git commit -m "Proyecto 2a: BDAutos MongoDB aggregation + app Python"
# crear repo remoto y push
```

Incluir en el remoto: PDF (`reporte/reporte_proyecto2a.pdf`), HTML de respaldo, consultas JS/Python y docs.

## Verificación rápida hecha en construcción

- Migración: conteos OK.
- `app/main.py all`: exit 0, 25 consultas.
- Spot-checks: Q3 (11 turbos JP), Q14 (dacia/bentley/lamborghini sin autos), Q13 (20 makers), Q23 (`$facet`), Q24 (top 5 Alemania).

## Por qué esta forma de entrega

Se separó evidencia ejecutable (`scripts/`, `app/`) de la narrativa académica (`docs/`, `reporte/`) para que el revisor pueda **correr** las consultas y a la vez leer las decisiones de diseño sin mezclar ambos en un solo archivo monolítico.
