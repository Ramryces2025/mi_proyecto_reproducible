# Mi Proyecto Reproducible

Breve descripcion:
Este proyecto entrena un modelo `RandomForestClassifier` usando un CSV con las columnas
`age`, `income`, `years_experience`, `gender` y `target`. El script prepara los datos,
entrena el modelo y guarda el artefacto en la carpeta `models/`.

## Requisitos
- Python 3.10+ recomendado

## Instalacion
1) Crear entorno virtual (opcional pero recomendado):
   - Windows PowerShell:
     python -m venv .venv
     .\.venv\Scripts\Activate.ps1

2) Instalar dependencias:
   pip install -r requirements.txt

O usando Makefile:
   make install

## Ejecucion
Desde la carpeta del proyecto:

python src/train.py

O usando Makefile:
   make train

Opciones:
- --data: ruta al CSV (default: data/raw/data_export.csv)
- --model-out: ruta del modelo (default: models/modelo_final_v2.pkl)
- --test-size: porcentaje de test (default: 0.2)
- --seed: semilla (default: 42)

Ejemplo:
python src/train.py --data data/raw/data_export.csv --model-out models/modelo.pkl --test-size 0.25 --seed 123

## Comandos utiles (Makefile)
- make install: instala dependencias
- make data: valida que el dataset exista
- make train: entrena el modelo con rutas por defecto
- make clean: elimina modelos en `models/*.pkl`
- make help: muestra ayuda

## Flujo rapido
make install
make data
make train

## Estructura del proyecto
mi_proyecto_reproducible/
+- data/
¦  +- raw/
¦  ¦  +- data_export.csv
¦  +- processed/
+- models/
+- notebooks/
+- reports/
+- src/
¦  +- train.py
+- requirements.txt
+- .gitignore

Notas:
- `notebooks/`: exploracion, pruebas y prototipos (Jupyter).
- `reports/`: resultados, graficos y entregables (imagenes, PDFs).
