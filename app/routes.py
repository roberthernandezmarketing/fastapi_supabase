from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from typing import List, Optional
from uuid import UUID

from .database import get_db
from .models import Client, Order
from .schemas import ClientWithOrders, ClientCreate, ClientInDB, OrderCreate, OrderInDB

# Crea un router para clientes
client_router = APIRouter(
    prefix="/clients",
    tags=["Clients"], # Esto crea la sección "Clients" en la documentación de Swagger UI
    responses={404: {"description": "Not found"}},
)

# Crea un router para órdenes
order_router = APIRouter(
    prefix="/orders", # Prefijo para todas las rutas de órdenes (e.g., /orders/by_client)
    tags=["Orders"], # Esto crea la sección "Orders" en la documentación de Swagger UI
    responses={404: {"description": "Not found"}},
)

# --- Endpoints de Clientes ---

@client_router.post("/", response_model=ClientInDB, status_code=status.HTTP_201_CREATED)
async def create_client(client: ClientCreate, db: AsyncSession = Depends(get_db)):
    """
    Crea un nuevo cliente en la base de datos.
    """
    db_client = Client(email=client.email, is_active=client.is_active, client_name=client.client_name, user_id=client.user_id)
    db.add(db_client)
    await db.commit()
    await db.refresh(db_client)
    return db_client

@client_router.get("/", response_model=List[ClientInDB])
async def get_all_clients(db: AsyncSession = Depends(get_db)):
    """
    Obtiene una lista de todos los clientes.
    """
    stmt = select(Client).order_by(Client.created_at.desc())
    result = await db.execute(stmt)
    clients = result.scalars().all()
    return clients

@client_router.get("/{client_id}", response_model=ClientInDB)
async def get_client_by_id(client_id: UUID, db: AsyncSession = Depends(get_db)):
    """
    Obtiene un cliente específico por su ID.
    """
    stmt = select(Client).filter(Client.id == client_id)
    result = await db.execute(stmt)
    client = result.scalar_one_or_none()
    if client is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Client not found")
    return client

@client_router.get("/with_orders/", response_model=List[ClientWithOrders])
async def get_clients_with_orders(db: AsyncSession = Depends(get_db)):
    """
    Obtiene una lista de todos los clientes junto con sus órdenes asociadas.
    """
    stmt = select(Client).options(selectinload(Client.orders)).order_by(Client.created_at.desc())
    result = await db.execute(stmt)
    clients = result.scalars().unique().all()
    return clients


# --- Endpoints de Órdenes ---

@order_router.post("/", response_model=OrderInDB, status_code=status.HTTP_201_CREATED)
async def create_order(order: OrderCreate, db: AsyncSession = Depends(get_db)):
    """
    Crea una nueva orden asociada a un cliente.
    """
    # Verificar si el client_id existe
    client_exists = await db.execute(select(Client).filter(Client.id == order.client_id))
    if not client_exists.scalar_one_or_none():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Client not found")

    db_order = Order(**order.model_dump()) # Usar model_dump() para Pydantic v2
    db.add(db_order)
    await db.commit()
    await db.refresh(db_order)
    return db_order

@order_router.get("/by_client/{client_id}", response_model=List[OrderInDB])
async def get_orders_by_client(client_id: UUID, db: AsyncSession = Depends(get_db)):
    """
    Obtiene todas las órdenes de un cliente específico por su ID.
    """
    # Verificar si el cliente existe
    client_exists = await db.execute(select(Client.id).filter(Client.id == client_id))
    if client_exists.scalar_one_or_none() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Client not found")

    # Obtener las órdenes para el cliente
    stmt = select(Order).filter(Order.client_id == client_id).order_by(Order.created_at.desc())
    result = await db.execute(stmt)
    orders = result.scalars().all()
    return orders