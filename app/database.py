# ---------------------------------------------------------
# database.py
# ---------------------------------------------------------
#
import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Cargar variables de entorno del archivo .env
load_dotenv()

# Obtener la URL de la base de datos desde las variables de entorno
DATABASE_URL = os.getenv("DATABASE_URL")

# Asegúrate de que la URL de la base de datos esté configurada
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set.")

# Configuración de SQLAlchemy para una conexión asíncrona
# El echo=True es útil para depuración, muestra las queries SQL ejecutadas
engine = create_async_engine(DATABASE_URL, echo=False)

print(f"DEBUG: DATABASE_URL loaded: {DATABASE_URL}")

# Crea una sesión asíncrona
AsyncSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=AsyncSession # Usar AsyncSession para operaciones asíncronas
)

# Dependencia para obtener una sesión de base de datos
async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()