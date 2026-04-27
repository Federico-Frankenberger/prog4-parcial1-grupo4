from typing import List, Optional

from sqlalchemy.exc import IntegrityError

from app.models.producto import Producto
from app.schemas.producto import (
    CategoriaResumen,
    IngredienteResumen,
    ProductoCategoriaCreate,
    ProductoCreate,
    ProductoIngredienteCreate,
    ProductoRead,
    ProductoUpdate,
)
from app.uow.uow import UnidadDeTrabajo


def _construir_producto_read(producto: Producto) -> ProductoRead:
    categorias = [
        CategoriaResumen(
            id=link.categoria_id,
            nombre=link.categoria.nombre,
            es_principal=link.es_principal,
        )
        for link in producto.categorias_link
    ]
    ingredientes = [
        IngredienteResumen(
            id=link.ingrediente_id,
            nombre=link.ingrediente.nombre,
            es_removible=link.es_removible,
            es_alergeno=link.ingrediente.es_alergeno,
        )
        for link in producto.ingredientes_link
    ]
    return ProductoRead(
        id=producto.id,
        nombre=producto.nombre,
        descripcion=producto.descripcion,
        precio_base=producto.precio_base,
        imagenes_url=producto.imagenes_url,
        stock_cantidad=producto.stock_cantidad,
        disponible=producto.disponible,
        created_at=producto.created_at,
        updated_at=producto.updated_at,
        categorias=categorias,
        ingredientes=ingredientes,
    )


def crear_producto(datos: ProductoCreate) -> ProductoRead:
    with UnidadDeTrabajo() as uow:
        for asignacion in datos.categorias:
            if not uow.categorias.obtener_por_id(asignacion.categoria_id):
                raise ValueError(f"Categoría con id={asignacion.categoria_id} no encontrada")
        for asignacion in datos.ingredientes:
            if not uow.ingredientes.obtener_por_id(asignacion.ingrediente_id):
                raise ValueError(f"Ingrediente con id={asignacion.ingrediente_id} no encontrado")
        producto = uow.productos.crear(datos)
        return _construir_producto_read(producto)


def obtener_productos(
    skip: int = 0,
    limit: int = 10,
    nombre: Optional[str] = None,
    disponible: Optional[bool] = None,
) -> List[ProductoRead]:
    with UnidadDeTrabajo() as uow:
        productos = uow.productos.obtener_todos(skip, limit, nombre, disponible)
        return [_construir_producto_read(p) for p in productos]


def obtener_producto(id: int) -> Optional[ProductoRead]:
    with UnidadDeTrabajo() as uow:
        producto = uow.productos.obtener_por_id(id)
        if not producto:
            return None
        return _construir_producto_read(producto)


def actualizar_producto(id: int, datos: ProductoUpdate) -> Optional[ProductoRead]:
    with UnidadDeTrabajo() as uow:
        producto = uow.productos.obtener_por_id(id)
        if not producto:
            return None
        producto = uow.productos.actualizar(producto, datos.model_dump(exclude_unset=True))
        return _construir_producto_read(producto)


def eliminar_producto(id: int) -> bool:
    with UnidadDeTrabajo() as uow:
        producto = uow.productos.obtener_por_id(id)
        if not producto:
            return False
        uow.productos.eliminar(producto)
        return True


def agregar_categoria(id_producto: int, datos: ProductoCategoriaCreate) -> Optional[ProductoRead]:
    try:
        with UnidadDeTrabajo() as uow:
            if not uow.productos.obtener_por_id(id_producto):
                return None
            if not uow.categorias.obtener_por_id(datos.categoria_id):
                return None
            producto = uow.productos.agregar_categoria(id_producto, datos.categoria_id, datos.es_principal)
            return _construir_producto_read(producto)
    except IntegrityError:
        raise ValueError("La categoría ya está asignada al producto")


def quitar_categoria(id_producto: int, id_categoria: int) -> bool:
    with UnidadDeTrabajo() as uow:
        return uow.productos.quitar_categoria(id_producto, id_categoria)


def agregar_ingrediente(
    id_producto: int, datos: ProductoIngredienteCreate
) -> Optional[ProductoRead]:
    try:
        with UnidadDeTrabajo() as uow:
            if not uow.productos.obtener_por_id(id_producto):
                return None
            if not uow.ingredientes.obtener_por_id(datos.ingrediente_id):
                return None
            producto = uow.productos.agregar_ingrediente(
                id_producto, datos.ingrediente_id, datos.es_removible
            )
            return _construir_producto_read(producto)
    except IntegrityError:
        raise ValueError("El ingrediente ya está asignado al producto")


def quitar_ingrediente(id_producto: int, id_ingrediente: int) -> bool:
    with UnidadDeTrabajo() as uow:
        return uow.productos.quitar_ingrediente(id_producto, id_ingrediente)
