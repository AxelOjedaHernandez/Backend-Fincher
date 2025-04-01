from pydantic import BaseModel
from typing import List, Optional

class CompoundDetail(BaseModel):
    nombre: Optional[str]
    formula: Optional[str]
    masa_exacta: Optional[str]
    imagen: Optional[str]
    url: Optional[str]

class SearchResponse(BaseModel):
    execution_time: float
    compuestos: List[CompoundDetail]
