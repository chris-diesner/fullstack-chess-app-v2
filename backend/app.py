from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from router import game_api
from chess_exception import ChessException
from fastapi.responses import JSONResponse

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(game_api.game_router, prefix="/game", tags=["Game"])

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
