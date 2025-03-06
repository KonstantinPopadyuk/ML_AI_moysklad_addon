from pydantic import BaseModel
from datetime import datetime


# Pydantic модель данных
class AssortmentData(BaseModel):
    id: str
    updated: str
    name: str
    description: str
    code: str
    archived: bool
    pathname: str
    paymentitemtype: str
    volume: float
    variantscount: float
    stock: float
    reserve: float
    intransit: float
    quantity: float
    price_usd: float
    price_distr: float
    price_opt: float
    price_proiz: float
    price_rrz: float
    price_site: float
    price_tech: float
