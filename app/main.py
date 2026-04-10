from fastapi import FastAPI
from app.api.routes import auth
from app.api.routes import registros
from app.api.routes import pagos
from app.api.routes import analytics
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.include_router(analytics.router, prefix="/analytics", tags=["Analytics"])
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(registros.router, prefix="/registros", tags=["Registros"])
app.include_router(pagos.router, prefix="/pagos", tags=["Pagos"])

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "LactaSys API 🚀"}




