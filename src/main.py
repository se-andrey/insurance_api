from fastapi import FastAPI
from .database import init_db, close_db
from .api.routes import router as api_router
from .calculation_tariff.routes import router as calc_router


app = FastAPI()

app.include_router(api_router, prefix="/api")
app.include_router(calc_router, prefix="/calculate")

app.add_event_handler("startup", init_db)
app.add_event_handler("shutdown", close_db)
