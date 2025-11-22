from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware

from web.routes import dashboard, users, payments, promotions
from web.auth import auth_router

def create_app(bot=None) -> FastAPI:
    """Создание FastAPI приложения"""
    app = FastAPI(title="Alina Bot Admin", debug=False)
    
    # Middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Mount static files
    app.mount("/static", StaticFiles(directory="src/web/static"), name="static")
    
    # Templates
    templates = Jinja2Templates(directory="src/web/templates")
    
    # Include routers
    app.include_router(auth_router, prefix="/auth", tags=["auth"])
    app.include_router(dashboard.router, prefix="/admin", tags=["admin"])
    app.include_router(users.router, prefix="/admin", tags=["users"])
    app.include_router(payments.router, prefix="/admin", tags=["payments"])
    app.include_router(promotions.router, prefix="/admin", tags=["promotions"])
    
    # Store bot instance in app state
    if bot:
        app.state.bot = bot
    
    return app