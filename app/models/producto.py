from datetime import datetime
from typing import TYPE_CHECKING, List, Optional
from sqlalchemy import Column, DateTime, String
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.sql import func
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from .producto_categoria import ProductoCategoria
    from .producto_ingrediente import ProductoIngrediente


class Producto(SQLModel, table=True):
    __tablename__ = "producto"

    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str = Field(max_length=150)
    descripcion: Optional[str] = Field(default=None)
    precio_base: float = Field(ge=0)
    imagenes_url: Optional[List[str]] = Field(
        default=None,
        sa_column=Column(ARRAY(String), nullable=True),
    )
    stock_cantidad: int = Field(default=0, ge=0)
    disponible: bool = Field(default=True)

    created_at: Optional[datetime] = Field(
        default=None,
        sa_column=Column(DateTime(timezone=True), nullable=False, server_default=func.now()),
    )
    updated_at: Optional[datetime] = Field(
        default=None,
        sa_column=Column(
            DateTime(timezone=True),
            nullable=False,
            server_default=func.now(),
            onupdate=func.now(),
        ),
    )
    deleted_at: Optional[datetime] = Field(
        default=None,
        sa_column=Column(DateTime(timezone=True), nullable=True),
    )

    categorias_link: List["ProductoCategoria"] = Relationship(
        back_populates="producto",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )
    ingredientes_link: List["ProductoIngrediente"] = Relationship(
        back_populates="producto",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )
