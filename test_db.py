import os
from sqlalchemy import create_engine, text

DATABASE_URL = "postgresql://luis:flic123@172.28.69.243:5432/mydatabase"

engine = create_engine(DATABASE_URL)

try:
    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1"))
        print("¡Conexión exitosa! 🎉", result.fetchone())
except Exception as e:
    print("Error al conectar con la base de datos:", e)
