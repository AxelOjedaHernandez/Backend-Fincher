from fastapi import APIRouter, Query
from services.pubchem_service import search_pubchem_compounds
from models.response_models import SearchResponse

router = APIRouter()

@router.get("/search/", response_model=SearchResponse)
async def search(
    compound_name: str = Query(None, description="Nombre del compuesto"),
    formula: str = Query(None, description="Fórmula química"),
    exact_mass: float = Query(None, description="Masa exacta")
):
    params = {}
    if compound_name:
        params["compound_name"] = compound_name
    if formula:
        params["formula"] = formula
    if exact_mass:
        params["exact_mass"] = exact_mass

    return await search_pubchem_compounds(params)
