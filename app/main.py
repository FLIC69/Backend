from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.db import DB
from app.routes import users, ai, login

from dotenv import load_dotenv
load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.db = DB()
    yield
    app.state.db.close_all()

app = FastAPI(lifespan=lifespan)

app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(ai.router, prefix="/ai", tags=["ai"])
app.include_router(login.router, prefix="", tags=["login"])


@app.get("/")
def read_root():
    return "Aplicación de Iker, Luis, Carlos, Ferza"

@app.get("/health")
def health_check():
    return{"status": "healthy", "service": "FastAPI" }





