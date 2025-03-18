from fastapi import APIRouter, WebSocket

ws_router = APIRouter()

@ws_router.websocket("/test-ws")
async def websocket_test(websocket: WebSocket):
    print("WebSocket-Verbindung wird versucht...")
    await websocket.accept()
    print("WebSocket erfolgreich verbunden!")
    await websocket.send_text("WebSocket funktioniert!")
    await websocket.close()
