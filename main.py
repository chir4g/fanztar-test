from fastapi import FastAPI
from routers.order import r_order

app = FastAPI()
app.include_router(router = r_order.router, prefix = "/orders")

@app.get("/")
async def root():
    return {"message": "Hello World"}


