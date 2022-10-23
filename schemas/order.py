from pydantic import BaseModel
from typing import List

class Order(BaseModel):
    components : List[str]
