# ---------------------------------------------------------
# models.py
# ---------------------------------------------------------
#
from sqlalchemy import Column, DateTime, String, text, Boolean, Numeric
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import ForeignKey # Necesario para la relación

Base = declarative_base()
metadata = Base.metadata

class Client(Base):
    __tablename__  = 'clients'
    __table_args__ = {'schema': 'public'} # Especifica el esquema 'public'

    id          = Column(UUID, primary_key=True, server_default=text("gen_random_uuid()"))
    created_at  = Column(DateTime(True), server_default=text("now()"))
    email       = Column(String(255), nullable=False, unique=True)
    is_active   = Column(Boolean, default=True)
    user_id     = Column(UUID) # Asumiendo que user_id también es UUID
    client_name = Column(String(255)) 

    # Define la relación con la tabla de orders
    orders = relationship("Order", back_populates="client")

class Order(Base):
    __tablename__  = 'orders'
    __table_args__ = {'schema': 'public'} # Especifica el esquema 'public'

    id         = Column(UUID, primary_key=True, server_default=text("gen_random_uuid()"))
    created_at = Column(DateTime(True), server_default=text("now()"))
    client_id  = Column(UUID, ForeignKey('public.clients.id')) # Clave foránea

    name       = Column(String)
    address    = Column(String)
    zip_code   = Column(String)
    city       = Column(String)
    price      = Column(Numeric)

    # Define la relación con la tabla de clients
    client = relationship("Client", back_populates="orders")