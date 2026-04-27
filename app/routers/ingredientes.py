from typing import Annotated, List, Optional

from fastapi import APIRouter, HTTPException, Path, Query, status

from app.schemas.ingrediente import IngredienteCreate, IngredienteRead, IngredienteUpdate
from app.services import ingrediente_service

router = APIRouter(prefix="/ingredientes", tags=["Ingredientes"])

IdIngrediente = Annotated[int, Path(gt=0, description="ID del ingrediente")]


@router.post("/", response_model=IngredienteRead, status_code=status.HTTP_201_CREATED)
def crear_ingrediente(datos: IngredienteCreate):
    try:
        return ingrediente_service.crear_ingrediente(datos)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


@router.get("/", response_model=List[IngredienteRead])
def listar_ingredientes(
    skip: Annotated[int, Query(ge=0, description="Registros a omitir")] = 0,
    limit: Annotated[int, Query(ge=1, le=100, description="Máximo de resultados")] = 10,
    nombre: Annotated[Optional[str], Query(description="Filtrar por nombre")] = None,
):
    return ingrediente_service.obtener_ingredientes(skip, limit, nombre)


@router.get("/{id}", response_model=IngredienteRead)
def detalle_ingrediente(id: IdIngrediente):
    ingrediente = ingrediente_service.obtener_ingrediente(id)
    if not ingrediente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ingrediente no encontrado",
        )
    return ingrediente


@router.patch("/{id}", response_model=IngredienteRead)
def actualizar_ingrediente(id: IdIngrediente, datos: IngredienteUpdate):
    ingrediente = ingrediente_service.actualizar_ingrediente(id, datos)
    if not ingrediente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ingrediente no encontrado",
        )
    return ingrediente


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_ingrediente(id: IdIngrediente):
    try:
        encontrado = ingrediente_service.eliminar_ingrediente(id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    if not encontrado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ingrediente no encontrado",
        )
