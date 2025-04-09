from fastapi import APIRouter, Query
from services.masbank_service import search_compounds
from models.response_models import SearchResponse

router = APIRouter()

@router.get("/search/", response_model=SearchResponse)
def search(
    compound_name: str = Query(None, description="Nombre del compuesto"),
    exact_mass: str = Query(None, description="Masa exacta"),
    mass_tolerance: float = Query(0.01, description="Tolerancia de masa"),
    formula: str = Query(None, description="Fórmula química")
):
    params = {}
    if compound_name:
        params["compound_name"] = compound_name
    if exact_mass:
        params["exact_mass"] = exact_mass
        params["mass_tolerance"] = mass_tolerance
    if formula:
        params["formula"] = formula

    return search_compounds(params)
