# Magic-Number
Challenge Data Engineer

## Resumen
Este repositorio contiene un sencillo pipeline ETL que descarga archivos ZIP públicos, extrae CSVs y los carga en una base de datos SQLite (`Annies.db`). Está pensado como una solución de ejemplo para procesar conjuntos de datos tipo transaccional.

## Estructura del repositorio
- `ETL/` : scripts de extracción y carga (`config.py`, `extract.py`, `load.py`).
- `Data/` : ubicación local para los CSV descargados (generada por `extract.py`).
- `Analyze/` : consultas y análisis (por ejemplo `queries.sql`).
- `Annies.db` : base de datos SQLite (se crea al ejecutar `load.py`).
- `requirements.txt` : dependencias Python.

## Requisitos
- Python 3.9+ recomendado
- Paquetes (ver `requirements.txt`): `pandas`, `requests`

## Instalación rápida
1. Crear y activar un entorno virtual (opcional pero recomendado):

```bash
python -m venv venv
# Windows PowerShell
venv\Scripts\Activate.ps1
# o cmd
venv\Scripts\activate.bat
```

2. Instalar dependencias:

```bash
pip install -r requirements.txt
```

## Uso
1. Ejecutar extracción y carga (desde la raíz del repo):

```bash
python ETL/load.py
```

Esto ejecuta `ETL/extract.py` (descarga y extrae los CSV en `Data/`) y luego carga los CSV listados en `ETL/config.py` dentro de `Annies.db`.

## Detalles ETL
- `ETL/config.py`: lista las URLs fuente, nombres de tablas y rutas locales.
- `ETL/extract.py`: descarga los ZIP, extrae el CSV y renombra el archivo según `config.URLS`.
- `ETL/load.py`: ejecuta `extract.py` y carga los CSV en SQLite con `pandas.DataFrame.to_sql`.

## Herramientas de inspección

Se incluye un script de utilidad para inspeccionar rápidamente la base de datos generada `Annies.db`:

```bash
python scripts/inspect_db.py --db Annies.db --samples 5
```

El script lista las tablas, muestra el conteo de filas por tabla y presenta hasta `--samples` filas de ejemplo por tabla.

## Tests y CI

Se incluyen suites de prueba basadas en `pytest` en la carpeta `tests/`. El test principal `tests/test_validate_schemas.py` valida que los CSV que se cargarán contienen las columnas esperadas (usa `ETL/schemas.py`).

Para ejecutar localmente:

```bash
pip install -r requirements.txt
# extraer CSVs antes de ejecutar los tests (si es necesario):
python ETL/extract.py
pytest -q
```

El pipeline de CI (`.github/workflows/ci.yml`) ejecuta `pytest` primero; después usa `Annies.db` incluido en el repo si existe, y sólo en su defecto ejecuta `ETL/load.py` (evita descargas innecesarias en CI).

## Cambios recientes

- `ETL/extract.py`: migrado a una implementación con `requests.Session` que incluye reintentos y backoff; ahora registra actividad y errores con `logging`.
- `ETL/schemas.py`: mapa `EXPECTED_COLUMNS` con columnas mínimas esperadas por tabla.
- Tests: añadido `tests/test_validate_schemas.py` que valida encabezados de CSV antes de la carga.
- CI: añadido workflow `.github/workflows/ci.yml` que ejecuta `pytest`, usa `Annies.db` incluido si está disponible y ejecuta `scripts/inspect_db.py` para comprobaciones finales.
- Utilidades: `scripts/inspect_db.py` muestra tablas, conteos y ejemplos de filas.

Estos cambios mejoran la robustez del pipeline y permiten validar la integridad de los CSV antes de cargar en la base de datos.

## Despliegue en AWS (guía rápida)

Resumen: se recomienda contenerizar la aplicación y desplegarla en AWS usando ECR + ECS (Fargate) o un scheduler (EventBridge) para ejecutar periódicamente el pipeline. La base de datos en producción debería ser `Postgres` (RDS). Use `Secrets Manager` para credenciales y `CloudWatch` para logs.

Pasos mínimos (resumen):

1. Preparar `Dockerfile` en la raíz del repo (ejemplo mínimo):

```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
ENV PYTHONUNBUFFERED=1
CMD ["python","ETL/load.py"]
```

2. Crear repo en ECR y subir la imagen:

```bash
# crear repo (una vez)
aws ecr create-repository --repository-name magic-number --region us-east-1

# log in y push
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <AWS_ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com
docker build -t magic-number:latest .
docker tag magic-number:latest <AWS_ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com/magic-number:latest
docker push <AWS_ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com/magic-number:latest
```

3. Preparar base de datos (RDS Postgres) o usar un servicio gestionado. Anotar endpoint y credenciales.

4. Guardar credenciales en Secrets Manager (ej. `magic-number/db`), por ejemplo una JSON con `DATABASE_URL`:

```bash
aws secretsmanager create-secret --name magic-number/db --secret-string '{"DATABASE_URL":"postgres://user:pass@host:5432/dbname"}'
```

5. Crear cluster ECS Fargate y una Task Definition que use la imagen ECR. Configure variables de entorno en la task: `DATABASE_URL`, `LOCAL_PATH` (si usa S3, configurar credenciales y bucket), y habilite CloudWatch Logs.

6. Schedule: crear una regla EventBridge (cron) que invoque `RunTask` en ECS para ejecutar la Task Definition en el horario deseado (p. ej. diario). Alternativa: usar AWS Batch o Step Functions si el pipeline crece.

7. Observabilidad y permisos:
- Configure la Task IAM Role con permisos mínimos para acceder a Secrets Manager, S3 (si se usa), y CloudWatch Logs.
- Asegure backups automáticos para RDS y configure alertas de CloudWatch para errores/tiempos altos.

Notas y recomendaciones:
- Parametrizar `ETL/load.py` para leer `DATABASE_URL` desde `os.environ` en lugar de usar `Annies.db` local.
- Considerar subir/leer datos desde S3 en lugar de montar `Data/` en el contenedor. Esto permite escalado y persistencia.
- Para despliegues rápidos, también es posible usar AWS Lambda con container image (si la ejecución cabe en los límites de Lambda).

