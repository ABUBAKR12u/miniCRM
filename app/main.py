from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from app.routers.createlogin import router as create_login_router
from app.routers.Login import router as login_router
from app.routers.Lead import router as lead_router
from app.routers.Dashboard import router as dashboard_router
from app.database.Base import Base
from app.database.connection import engine

Base.metadata.create_all(bind=engine)

app = FastAPI(docs_url="/docs")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(create_login_router)
app.include_router(login_router)
app.include_router(lead_router)
app.include_router(dashboard_router)


@app.get("/")
def serve_frontend():
    return FileResponse("static/index.html")
