# Primer Parcial — Programación IV

Backend REST API desarrollado con **FastAPI**, **SQLModel** y **PostgreSQL** como parte del primer parcial de Programación IV.

## Descripción

API para gestión de un menú de productos con categorías e ingredientes. Implementa:

- CRUD completo de Categorías, Ingredientes y Productos
- Relaciones N:N entre Producto–Categoría y Producto–Ingrediente 
- Jerarquía de categorías con detección de ciclos
- Borrado lógico (soft delete) en entidades principales
- Arquitectura en capas: Modelos → Repositorios → Servicios → Routers

## Integrantes

- Federico Frankenberger
- Emilia Barros
- Miguel Barrera
- Guadalupe Maricchiolo

## Video de presentación

<!-- Reemplazá este link con el link real del video una vez subido -->
[Ver video de presentación](https://youtu.be/IWFji0xzQcM)


## Instalación y ejecución

```bash
# 1. Clonar el repositorio
git clone <url-del-repositorio>
cd Primer_Parcial_Prog4

# 2. Crear entorno virtual e instalar dependencias
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # Linux/Mac

pip install -r requirements.txt

# 3. Configurar variables de entorno
cp .env.example .env
# Editar .env con los datos de tu base de datos PostgreSQL

# 4. Levantar la base de datos con Docker (opcional)
cd ..
docker-compose up -d

# 5. Iniciar el servidor
fastapi dev app/main.py
```

## Estructura del proyecto

```
backend/
├── app/
│   ├── main.py              # Entrada de la aplicación
│   ├── database.py          # Configuración de la base de datos
│   ├── models/              # Modelos SQLModel 
│   ├── schemas/             # Esquemas Pydantic
│   ├── repositories/        # Capa de acceso a datos
│   ├── services/            # Lógica de negocio
│   ├── routers/             # Endpoints HTTP
│   └── uow/                 # Unit of Work
```

