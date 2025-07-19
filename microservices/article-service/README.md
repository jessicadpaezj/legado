# Microservicio de Article

Este microservicio implementa las funcionalidades relacionadas con `article` del monolito original. Utiliza Python, Flask, SQLAlchemy y PostgreSQL como base de datos.

## Estructura del proyecto

- `app/`: Contiene la lógica principal del microservicio.
- `tests/`: Contiene las pruebas unitarias y de integración.
- `requirements.txt`: Lista de dependencias del proyecto.
- `Dockerfile`: Configuración para construir la imagen del contenedor.

## Instalación

1. Instalar las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

2. Configurar las variables de entorno necesarias para la conexión a la base de datos PostgreSQL.

## Ejecución

Para ejecutar el microservicio localmente:
```bash
python app/main.py
```
