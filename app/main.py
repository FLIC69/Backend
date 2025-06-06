from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.db import DB
from app.routes import users, ai, log


from dotenv import load_dotenv
load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.db = DB()
    yield
    app.state.db.close_all()

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
        allow_origins=[
        "http://localhost:5173",
        "https://172.28.69.248",
        "https://172.28.69.210"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(ai.router, prefix="/ai", tags=["ai"])
app.include_router(log.router, prefix="/log", tags=["logs"])


@app.get("/")
def read_root():
    return "Aplicación de Iker, Luis, Carlos, Ferza"





