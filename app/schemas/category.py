from typing import Optional
from pydantic import BaseModel

class CategoryBase(BaseModel):
    name: str
    slug: str
    description: Optional[str] = None
    image_url: Optional[str] = None
    is_active: bool = True

class CategoryCreate(CategoryBase):
    pass

class CategoryResponse(CategoryBase):
    id: int
    model_config = {"from_attributes": True}

class BrandBase(BaseModel):
    name: str
    slug: str
    logo_url: Optional[str] = None
    description: Optional[str] = None
    is_active: bool = True

class BrandCreate(BrandBase):
    pass

class BrandResponse(BrandBase):
    id: int
    model_config = {"from_attributes": True}
