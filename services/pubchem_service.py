import asyncio
import time
import logging
from config import BASE_URL_PUBCHEM
from utils.http_client import fetch_data_pubchem

async def fetch_pubchem_details(cid: str):
    """Obtiene los detalles de un compuesto dado su CID en PubChem."""
    detail_url = f"{BASE_URL_PUBCHEM}/compound/cid/{cid}/property/MolecularFormula,MolecularWeight,IUPACName/JSON"
    detail_data = await fetch_data_pubchem(detail_url)

    if "error" in detail_data:
        logging.error(f"Error obteniendo detalles de CID {cid}")
        return None

    properties = detail_data.get("PropertyTable", {}).get("Properties", [{}])[0]

    return {
        "nombre": properties.get("IUPACName", "No disponible"),
        "formula": properties.get("MolecularFormula", "No disponible"),
        "masa_exacta": properties.get("MolecularWeight", "No disponible"),
        "imagen": f"https://pubchem.ncbi.nlm.nih.gov/image/imgsrv.fcgi?cid={cid}&t=l",
        "url": f"https://pubchem.ncbi.nlm.nih.gov/compound/{cid}"
    }

async def search_pubchem_compounds(params: dict):
    """Busca compuestos en PubChem y obtiene los detalles de los CIDs comunes en todas las búsquedas."""
    start_time = time.perf_counter()
    search_urls = []
    
    # Generar URLs de búsqueda según los parámetros proporcionados
    if "compound_name" in params:
        search_urls.append(f"{BASE_URL_PUBCHEM}/compound/name/{params['compound_name']}/cids/JSON")
    if "formula" in params:
        search_urls.append(f"{BASE_URL_PUBCHEM}/compound/formula/{params['formula']}/cids/JSON")
    if "exact_mass" in params:
        search_urls.append(f"{BASE_URL_PUBCHEM}/compound/molecular_weight/equals/{params['exact_mass']}/cids/JSON")

    if not search_urls:
        return {"error": "No se proporcionaron parámetros de búsqueda", "execution_time": 0, "compuestos": []}

    # Realizar las búsquedas en paralelo
    search_results = await asyncio.gather(*(fetch_data_pubchem(url) for url in search_urls))

    # Extraer listas de CIDs de cada búsqueda
    cid_sets = [set(result.get("IdentifierList", {}).get("CID", [])) for result in search_results if "IdentifierList" in result]

    if not cid_sets:
        return {"error": "No se encontraron compuestos", "execution_time": 0, "compuestos": []}

    # Intersección de los CIDs encontrados en todas las búsquedas
    common_cids = set.intersection(*cid_sets) if len(cid_sets) > 1 else cid_sets[0]

    if not common_cids:
        return {"error": "No hay coincidencias entre los parámetros de búsqueda", "execution_time": 0, "compuestos": []}

    # Obtener detalles de los CIDs en paralelo
    tasks = [fetch_pubchem_details(str(cid)) for cid in common_cids]
    compound_details = await asyncio.gather(*tasks)

    execution_time = time.perf_counter() - start_time
    return {"execution_time": execution_time, "compuestos": [c for c in compound_details if c]}
