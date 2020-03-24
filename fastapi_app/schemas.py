from typing import List

from pydantic import BaseModel

class LocCreate(BaseModel):
    key :str
    place_name : str
    admin_name1	: str
    latitude : float	
    longitude :float	
    accuracy :float


