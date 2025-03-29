from pydantic import BaseModel

class ModelRequest(BaseModel):
    action: str
    data: list

import akira.controllers.admin
import akira.controllers.judge