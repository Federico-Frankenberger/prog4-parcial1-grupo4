from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field


class CategoriaResumen(BaseModel):
    id: int
    nombre: str
    es_principal: bool

    model_config = {"from_attributes": True}


class IngredienteResumen(BaseModel):
    id: int
    nombre: str
    es_removible: bool
    es_alergeno: bool

    model_config = {"from_attributes": True}


class CategoriaAsignacion(BaseModel):
    categoria_id: int = Field(..., gt=0)
    es_principal: bool = Field(default=False)


class IngredienteAsignacion(BaseModel):
    ingrediente_id: int = Field(..., gt=0)
    es_removible: bool = Field(default=False)


class ProductoBase(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=150, examples=["Hamburguesa clásica"])
    descripcion: Optional[str] = Field(default=None, examples=["Pan brioche, carne 200g, lechuga"])
    precio_base: float = Field(..., ge=0, examples=[1500.00])
    imagenes_url: Optional[List[str]] = Field(default=None, examples=[["https://ejemplo.com/img1.jpg"]])
    stock_cantidad: int = Field(default=0, ge=0, examples=[50])
    disponible: bool = Field(default=True)


class ProductoCreate(ProductoBase):
    categorias: List[CategoriaAsignacion] = Field(default_factory=list)
    ingredientes: List[IngredienteAsignacion] = Field(default_factory=list)


class ProductoUpdate(BaseModel):
    nombre: Optional[str] = Field(default=None, min_length=2, max_length=150)
    descripcion: Optional[str] = None
    precio_base: Optional[float] = Field(default=None, ge=0)
    imagenes_url: Optional[List[str]] = None
    stock_cantidad: Optional[int] = Field(default=None, ge=0)
    disponible: Optional[bool] = None


class ProductoRead(BaseModel):
    id: int
    nombre: str
    descripcion: Optional[str] = None
    precio_base: float
    imagenes_url: Optional[List[str]] = None
    stock_cantidad: int
    disponible: bool
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    categorias: List[CategoriaResumen] = []
    ingredientes: List[IngredienteResumen] = []

    model_config = {"from_attributes": True}


class ProductoCategoriaCreate(BaseModel):
    categoria_id: int = Field(..., gt=0)
    es_principal: bool = Field(default=False)


class ProductoIngredienteCreate(BaseModel):
    ingrediente_id: int = Field(..., gt=0)
    es_removible: bool = Field(default=False)
