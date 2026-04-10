from fastapi import FastAPI
from app.api.routes import auth
from app.api.routes import registros
from app.api.routes import pagos
from app.api.routes import analytics

app = FastAPI()

app.include_router(analytics.router, prefix="/analytics", tags=["Analytics"])
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(registros.router, prefix="/registros", tags=["Registros"])
app.include_router(pagos.router, prefix="/pagos", tags=["Pagos"])

@app.get("/")
def root():
    return {"message": "LactaSys API 🚀"}




