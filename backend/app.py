import sys
import os
import logging

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from controllers.user_controller import user_router
from controllers.auth_controller import auth_router
from controllers.chess_lobby_controller import lobby_router
from controllers.chess_game_controller import game_router
from websocket_router import ws_router
from chess_exception import ChessException

# 🌟 FastAPI App initialisieren
app = FastAPI()

# 🌟 Logging aktivieren
logging.basicConfig(level=logging.DEBUG)

# 🌟 CORS aktivieren
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Alternativ: ["http://localhost:5173"] falls nur eine erlaubte Quelle
    allow_credentials=True,
    allow_methods=["*"],  # Erlaubt GET, POST, PUT, DELETE, etc.
    allow_headers=["*"],  # Erlaubt alle Header
)

# 🌟 Fehler-Logging Middleware für interne Serverfehler (500)
@app.middleware("http")
async def catch_exceptions_middleware(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception as e:
        logging.error(f"🔥 Ungefangener Fehler: {str(e)}", exc_info=True)
        return JSONResponse(
            status_code=500,
            content={"detail": f"Interner Serverfehler: {str(e)}"},
        )

# 🌟 Routen registrieren
app.include_router(user_router, prefix="/users", tags=["Users"])
app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(lobby_router, prefix="/lobby", tags=["Lobby"])
app.include_router(game_router, prefix="/game", tags=["Game"])

# 🌟 Fehlerbehandlung für benutzerdefinierte `ChessException`
@app.exception_handler(ChessException)
async def chess_exception_handler(request: Request, exc: ChessException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message},
    )

# 🌟 Startseite (Test-Route)
@app.get("/")
def home():
    return {"message": "Welcome to the Fullstack Chess API!"}

# 🌟 Server-Start
if __name__ == "__main__":
    import uvicorn
    logging.info("🚀 FastAPI Server startet auf http://localhost:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
