# ---------------------------------------------------------
# main.py
# ---------------------------------------------------------
#

from fastapi import FastAPI
from .routes import client_router, order_router # Importa los routers

app = FastAPI(
    title="Clients & Orders API",
    description="API para gestionar clientes y sus órdenes.",
    version="1.0.0",
)

@app.get("/", include_in_schema=False) # No incluir en la documentación
async def read_root():
    return {"message": "Welcome to Clients & Orders API. Visit /docs for API documentation."}

# Incluye los routers en la aplicación principal
app.include_router(client_router)
app.include_router(order_router)