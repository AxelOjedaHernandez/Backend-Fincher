import time
import logging
import requests
import concurrent.futures
import os
from config import BASE_URL_MASSBANK

def fetch_details(record_id: str):
    """Obtiene detalles de un compuesto dado su ID en MassBank."""
    detail_url = f"{BASE_URL_MASSBANK}/{record_id}"
    
    try:
        response = requests.get(detail_url, timeout=10)
        response.raise_for_status()
        detail_data = response.json()
    except Exception as e:
        logging.error(f"Error obteniendo detalles de {record_id}: {e}")
        return None

    return {
        "nombre": detail_data.get("compound", {}).get("names", ["No disponible"])[0],
        "formula": detail_data.get("compound", {}).get("formula", "No disponible"),
        "masa_exacta": str(detail_data.get("compound", {}).get("mass", "No disponible")),
        "imagen": detail_data.get("splash", "No disponible"),
        "url": f"https://massbank.eu/MassBank/RecordDisplay?id={record_id}"
    }

def fetch_data_massbank_sync(url: str, params: dict = None):
    """Función sincrónica para hacer solicitud HTTP a MassBank."""
    try:
        response = requests.get(url, params=params, timeout=15)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        logging.error(f"Error en fetch_data_massbank: {e}")
        return {"error": str(e)}

def search_compounds(params: dict):
    """Busca compuestos en MassBank y obtiene sus detalles usando múltiples hilos."""
    start_time = time.perf_counter()
    search_url = f"{BASE_URL_MASSBANK}/search"

    print(f"Realizando solicitud a: {search_url} con parámetros: {params}")
    
    search_results = fetch_data_massbank_sync(search_url, params)
    if "error" in search_results:
        return {"error": search_results["error"], "execution_time": 0, "compuestos": []}

    record_ids = [record.get("accession") for record in search_results.get("data", []) if record.get("accession")]

    max_workers = os.cpu_count() or 4  # fallback por si cpu_count() falla

    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        compound_details = list(executor.map(fetch_details, record_ids))

    compound_details = [c for c in compound_details if c]

    execution_time = time.perf_counter() - start_time
    return {"execution_time": execution_time, "compuestos": compound_details}

