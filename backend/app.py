from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from controllers.user_controller import user_router
from controllers.auth_controller import auth_router
from controllers.chess_lobby_controller import lobby_router
from chess_exception import ChessException
from fastapi.responses import JSONResponse

app = FastAPI()
app.include_router(user_router, prefix="/users", tags=["Users"])
# app.include_router(game_router, prefix="/games", tags=["Games"])
app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(lobby_router, prefix="/lobby", tags=["Lobby"])

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(ChessException)
async def chess_exception_handler(request, exc: ChessException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message},
    )

@app.get("/")
def home():
    return {"message": "Welcome to the Fullstack Chess API!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=10000)
