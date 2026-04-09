from fastapi import FastAPI
from app.api.routes import auth
from app.api.routes import registros

app = FastAPI()

app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(registros.router, prefix="/registros", tags=["Registros"])

@app.get("/")
def root():
    return {"message": "LactaSys API 🚀"}




