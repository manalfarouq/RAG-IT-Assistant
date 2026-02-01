from fastapi import FastAPI
from app.routes import query_router
from routes import getAllUsers_router, login_router, register_router, query_router
from db.db_connection import Base, engine

# Créer l'application
app = FastAPI()

Base.metadata.create_all(bind=engine)

# Inclure les routers
app.include_router(register_router.router)
app.include_router(login_router.router)
app.include_router(getAllUsers_router.router)
app.include_router(query_router.router)

