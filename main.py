# main.py
from fastapi import FastAPI
from routers import masbank, pubchem
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="API de Búsqueda en MassBank")

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir todos los orígenes (cualquier frontend)
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos los métodos (GET, POST, PUT, DELETE)
    allow_headers=["*"],  # Permitir todos los encabezados
)

app.include_router(masbank.router, prefix="/massbank", tags=["MassBank"])
app.include_router(pubchem.router, prefix="/pubchem", tags=["PubChem"])

@app.get("/")
async def root():
    return {"message": "Bienvenido a la API de Búsqueda en MassBank"}
