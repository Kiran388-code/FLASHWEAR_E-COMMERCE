from typing import Optional, List
from pydantic import BaseModel

class PickItem(BaseModel):
    item_id: int
    title: str
    size: str
    location_code: str # e.g. A12-03-02
    barcode: str
    picked: bool = False

class PickListResponse(BaseModel):
    id: int
    order_id: int
    order_number: str
    status: str
    scanned_barcodes: int
    total_items: int
    items: List[PickItem]

class BarcodeScanRequest(BaseModel):
    order_id: int
    barcode: str
