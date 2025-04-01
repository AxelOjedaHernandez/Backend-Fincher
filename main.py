# main.py
from fastapi import FastAPI
from routers import masbank, pubchem

app = FastAPI(title="API de Búsqueda en MassBank")

app.include_router(masbank.router, prefix="/massbank", tags=["MassBank"])
app.include_router(pubchem.router, prefix="/pubchem", tags=["PubChem"])

@app.get("/")
async def root():
    return {"message": "Bienvenido a la API de Búsqueda en MassBank"}
