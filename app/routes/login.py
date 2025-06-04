from fastapi import APIRouter, HTTPException, status, Depends, Request
from app.models.user import UserLogin
from app.utils.auth import verify_password, create_access_token, get_user_by_username
from app.utils.getDb import get_db
from datetime import timedelta


router = APIRouter()

@router.post("/login")
def login(data: UserLogin, request: Request, db = Depends(get_db)):
    user = get_user_by_username(data.username, db)
    if not user:
        guardar_log(data.username, "FALLIDO - usuario no encontrado")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciales inválidas")
    
    if not verify_password(data.password, user["password"]):
        guardar_log(data.username, "FALLIDO - contraseña incorrecta")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciales inválidas")
    
    access_token = create_access_token(
        data={"sub": user["username"]},
        expires_delta=timedelta(minutes=30)
    )
    guardar_log(data.username, "ÉXITO")
    return {"access_token": access_token, "token_type": "bearer"}

# Guardado de logs en archivo
def guardar_log(usuario: str, evento: str):
    with open("logs.txt", "a") as f:
        f.write(f"{usuario} - {evento}\n")
    print(f"Log guardado: {usuario} - {evento}")