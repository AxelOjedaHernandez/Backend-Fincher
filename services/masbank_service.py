import asyncio
import time
import logging
from config import BASE_URL_MASSBANK
from utils.http_client import fetch_data_massbank

async def fetch_details(record_id: str):
    """Obtiene detalles de un compuesto dado su ID en MassBank."""
    detail_url = f"{BASE_URL_MASSBANK}/{record_id}"
    detail_data = await fetch_data_massbank(detail_url)

    if "error" in detail_data:
        logging.error(f"Error obteniendo detalles de {record_id}")
        return None

    return {
        "nombre": detail_data.get("compound", {}).get("names", ["No disponible"])[0],
        "formula": detail_data.get("compound", {}).get("formula", "No disponible"),
        "masa_exacta": detail_data.get("compound", {}).get("mass", "No disponible"),
        "imagen": detail_data.get("splash", "No disponible"),
        "url": f"https://massbank.eu/MassBank/RecordDisplay?id={record_id}"
    }

async def search_compounds(params: dict):
    """Busca compuestos en MassBank y obtiene sus detalles en paralelo."""
    start_time = time.perf_counter()
    search_url = f"{BASE_URL_MASSBANK}/search"
    
    search_results = await fetch_data_massbank(search_url, params)
    if "error" in search_results:
        return {"error": search_results["error"], "execution_time": 0, "compuestos": []}

    record_ids = [record.get("accession") for record in search_results.get("data", []) if record.get("accession")]
    
    tasks = [fetch_details(record_id) for record_id in record_ids]
    compound_details = await asyncio.gather(*tasks)

    # Convertir 'masa_exacta' a cadena
    for compound in compound_details:
        if compound and "masa_exacta" in compound:
            compound["masa_exacta"] = str(compound["masa_exacta"])

    execution_time = time.perf_counter() - start_time
    return {"execution_time": execution_time, "compuestos": [c for c in compound_details if c]}
