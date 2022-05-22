from pydantic import BaseModel
from typing import Optional
import datetime

class face_data(BaseModel):
    is_face : bool
    time_stick: str