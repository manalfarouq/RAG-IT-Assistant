from fastapi import FastAPI

from routes import getAllUsers_router, login_router, register_router, query_router, cluster_router
from db.database import Base, engine

# Créer l'application
app = FastAPI()

# Créer les tables si elles n'existent pas
Base.metadata.create_all(bind=engine)

# Inclure les routers
app.include_router(register_router.router)
app.include_router(login_router.router)
app.include_router(getAllUsers_router.router)
app.include_router(query_router.router)
app.include_router(cluster_router.router)
