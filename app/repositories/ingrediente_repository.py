from datetime import datetime, timezone
from typing import List, Optional

from sqlmodel import Session, select

from app.models.ingrediente import Ingrediente
from app.models.producto import Producto
from app.models.producto_ingrediente import ProductoIngrediente
from app.schemas.ingrediente import IngredienteCreate


class IngredienteRepository:
    def __init__(self, sesion: Session):
        self.sesion = sesion

    def crear(self, datos: IngredienteCreate) -> Ingrediente:
        ingrediente = Ingrediente(**datos.model_dump())
        self.sesion.add(ingrediente)
        self.sesion.flush()
        self.sesion.refresh(ingrediente)
        return ingrediente

    def obtener_por_id(self, id: int) -> Optional[Ingrediente]:
        ingrediente = self.sesion.get(Ingrediente, id)
        if ingrediente is None or ingrediente.deleted_at is not None:
            return None
        return ingrediente

    def obtener_todos(
        self,
        skip: int = 0,
        limit: int = 10,
        nombre: Optional[str] = None,
    ) -> List[Ingrediente]:
        consulta = select(Ingrediente).where(Ingrediente.deleted_at == None)
        if nombre:
            consulta = consulta.where(Ingrediente.nombre.icontains(nombre))
        consulta = consulta.offset(skip).limit(limit)
        return self.sesion.exec(consulta).all()

    def tiene_productos_activos(self, id: int) -> bool:
        resultado = self.sesion.exec(
            select(ProductoIngrediente.ingrediente_id)
            .join(Producto, ProductoIngrediente.producto_id == Producto.id)
            .where(
                ProductoIngrediente.ingrediente_id == id,
                Producto.deleted_at == None,
            )
            .limit(1)
        ).first()
        return resultado is not None

    def actualizar(self, ingrediente: Ingrediente, campos: dict) -> Ingrediente:
        for campo, valor in campos.items():
            setattr(ingrediente, campo, valor)
        self.sesion.add(ingrediente)
        self.sesion.flush()
        self.sesion.refresh(ingrediente)
        return ingrediente

    def eliminar(self, ingrediente: Ingrediente) -> None:
        ingrediente.deleted_at = datetime.now(timezone.utc)
        self.sesion.add(ingrediente)
        self.sesion.flush()
