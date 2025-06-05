from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from app.db import DB
from app.routes import users, ai
from jose import JWTError, jwt
import os


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
    allow_origins=["*"],  # or specific domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def jwt_verification_middleware(request: Request, call_next):
    # Skip JWT check for excluded paths
    print("HERE")
    if request.url.path in {"/users/login", "/users/register"}:
        return await call_next(request)
    
    token = request.cookies.get("token")
    SECRET_KEY = os.getenv("JWT_TOKEN")

    if SECRET_KEY is None:
        raise KeyError("JWT key not found")
    
    if not token:
        return JSONResponse(
            content={"detail": "No JWT found"},
            status_code=401
        )
    
    if token:
        try:
            # Decode and validate token
            payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            request.state.user = payload.get("sub")
        except JWTError:
            # Token invalid – remove cookie and return 401
            print("NO TOKEN FOUND")
            response = JSONResponse(
                content={"detail": "Invalid or expired token"},
                status_code=401
            )
            response.delete_cookie("access_token")
            return response

    # If no token or token is valid, proceed normally
    response = await call_next(request)
    return response

app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(ai.router, prefix="/ai", tags=["ai"])

@app.get("/")
def read_root():
    return "Aplicación de Iker, Luis, Carlos, Ferza"





