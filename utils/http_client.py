import httpx
import logging
import asyncio

async def fetch_data_massbank(url: str, params: dict = None):
    """Realiza una solicitud GET asíncrona y maneja errores."""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, params=params)
            response.raise_for_status()  # Lanza un error si el status_code no es 200
            return response.json()
        except httpx.HTTPStatusError as e:
            return {"error": f"Error HTTP {e.response.status_code}"}
        except Exception as e:
            return {"error": f"Error inesperado: {str(e)}"}
        



async def fetch_data_pubchem(url: str, max_retries: int = 5, delay: int = 2):
    """Realiza una solicitud GET a PubChem y maneja respuestas con ListKey si es necesario."""
    async with httpx.AsyncClient() as client:
        for _ in range(max_retries):
            try:
                response = await client.get(url, timeout=10)
                response.raise_for_status()
                data = response.json()

                # Manejo de ListKey si la búsqueda aún no ha terminado
                if "Waiting" in data and "ListKey" in data["Waiting"]:
                    list_key = data["Waiting"]["ListKey"]
                    logging.info(f"Esperando resultados en PubChem. ListKey: {list_key}")
                    await asyncio.sleep(delay)  # Espera antes de reintentar
                    url = f"{BASE_URL_PUBCHEM}/compound/listkey/{list_key}/cids/JSON"
                    continue  # Reintentar con la nueva URL

                return data  # Retornar los datos obtenidos

            except httpx.HTTPStatusError as e:
                logging.error(f"Error HTTP en PubChem: {e.response.status_code} - {url}")
            except httpx.RequestError as e:
                logging.error(f"Error de conexión con PubChem: {str(e)}")

        return {"error": "Tiempo de espera agotado para la consulta en PubChem"}