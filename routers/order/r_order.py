from fastapi import APIRouter, HTTPException
from schemas.order import Order
from middleware.components import ComponentMiddleware

router = APIRouter(tags = ["orders"])

@router.post("/")
async def index(order : Order):
    """Receives **list of component codes** and returns **total and parts related to those codes.**
    - Args : List[str] ex : ["I","A","D","F","K"]
    - Returns : Dict<order_id : str, total : float, parts : List[str]> 
    """
    code_middlerware = ComponentMiddleware()
    
    code_middlerware.set_details(order.components)
    
    if code_middlerware.failure:
        raise HTTPException(400, detail = code_middlerware.failure)
    else:
        return code_middlerware.component_details
