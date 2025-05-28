# ---------------------------------------------------------
# schemas.py
# ---------------------------------------------------------
#
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List
from uuid import UUID

# Esquemas para Cliente
class ClientBase(BaseModel):
    email      : str = Field(..., description="Email del cliente")
    is_active  : bool = Field(True, description="Estado activo del cliente")
    client_name: Optional[str] = Field(None, description="Nombre completo del cliente")
    user_id    : Optional[UUID] = Field(None, description="ID del usuario de Supabase Auth (opcional)")

class ClientCreate(ClientBase):
    pass # Por ahora, crear cliente usa los mismos campos que ClientBase

class ClientInDB(ClientBase):
    id: UUID
    created_at: datetime

    class Config:
        from_attributes = True # Equivalente a orm_mode = True en Pydantic v1.x

# Esquemas para Órdenes
class OrderBase(BaseModel):
    name     : str = Field(..., description="Nombre o descripción de la orden")
    address  : Optional[str] = Field(None, description="Dirección de envío")
    zip_code : Optional[str] = Field(None, description="Código postal")
    city     : Optional[str] = Field(None, description="Ciudad de envío")
    price    : float = Field(..., ge=0, description="Precio total de la orden") # Pydantic convierte Numeric a float

class OrderCreate(OrderBase):
    client_id: UUID # Necesario para crear una orden asociada a un cliente

class OrderInDB(OrderBase):
    id: UUID
    created_at: datetime
    client_id : UUID # Mantener client_id para referencia

    class Config:
        from_attributes = True

# Esquema para Clientes con sus Órdenes (para la respuesta de la API)
class ClientWithOrders(ClientInDB):
    orders: List[OrderInDB] = [] # Una lista de objetos OrderInDB

    class Config:
        from_attributes = True