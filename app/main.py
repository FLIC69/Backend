from fastapi import FastAPI

from app.routes import users, ai

app = FastAPI()

app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(ai.router, prefix="/ai", tags=["ai"])

@app.get("/")
def read_root():
    return "Aplicación de Iker, Luis, Carlos, Ferza"



