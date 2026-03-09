from pydantic import BaseModel

class ItemBase(BaseModel):
    title: str
    description: str | None = None
    is_active: bool = True


class ItemCreate(ItemBase):
    pass


class ItemUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    is_active: bool | None = None


class Item(ItemBase):
    id: int

    class Config:
        from_attributes = True  # for Pydantic v2; use orm_mode=True for v1
