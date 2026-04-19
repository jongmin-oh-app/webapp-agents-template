from fastapi import FastAPI
from mangum import Mangum

from app.routers import health

app = FastAPI(title="Webapp API")
app.include_router(health.router)

lambda_handler = Mangum(app)
