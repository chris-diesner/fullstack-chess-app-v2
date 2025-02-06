from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from router import game_api

app = FastAPI()

# CORS-Unterstützung für das Frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Für die Entwicklung offen, später einschränken
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API-Router registrieren
app.include_router(game_api.game_router, prefix="/game", tags=["Game"])
# app.include_router(status.router, prefix="/status", tags=["Status"])

@app.get("/")
def home():
    return {"message": "Welcome to the Fullstack Chess API!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=10000)
