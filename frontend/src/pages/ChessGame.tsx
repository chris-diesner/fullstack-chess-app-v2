import { useEffect, useState } from "react";
import { DndProvider } from "react-dnd";
import { HTML5Backend } from "react-dnd-html5-backend";
import ChessBoard from "../components/ChessBoard";
import "../styles/chessboard.css";

type Figure = {
    type: string;
    color: string;
};

const ChessGame = () => {
    const [gameId, setGameId] = useState<string | null>(null);
    const [isBoardSet, setIsBoardSet] = useState<boolean>(false);
    const [boardState, setBoardState] = useState<(Figure | null)[][]>(Array(8).fill(Array(8).fill(null)));
    const [moveHistory, setMoveHistory] = useState<{white_moves: {figure: string, start: string, end: string}[], black_moves: {figure: string, start: string, end: string}[]}>({white_moves: [], black_moves: []});

    const parseMoveNotation = (move: string) => {
        const cleanedMove = move.replace(/\s*\(.*?\)/g, "").trim();
        const parts = cleanedMove.split(" ");
    
        if (parts.length < 5) {
            console.error("⚠️ Unerwartetes Move-Format:", move);
            return move;
        }
    
        const figure = parts[0];
    
        if (move.includes("en passant")) {
            const start = parts[parts.length - 3];
            const end = parts[parts.length - 1];
            const capturePosition = parts[parts.length - 7];
            return `en passant: ${figure} von ${start} auf ${end} schlägt pawn auf ${capturePosition}`;
        } else if (parts.includes("schlägt")) {
            const capturedFigure = parts[2];
            const start = parts[parts.length - 3];
            const end = parts[parts.length - 1];
            return `${figure} von ${start} schlägt ${capturedFigure} auf ${end}`;
        } else {
            const start = parts[parts.length - 3];
            const end = parts[parts.length - 1];
            return `${figure} von ${start} auf ${end}`;
        }
    };
    
    const startNewGame = () => {
        console.log(isBoardSet)
        fetch("http://localhost:8000/game/new", { method: "POST" })
            .then((res) => res.json())
            .then((data) => {
                setGameId(data.game_id);
                setIsBoardSet(true);
                setMoveHistory({white_moves: [], black_moves: []});
            })
            .catch((err) => console.error("Fehler beim Starten eines neuen Spiels:", err));
    };

    useEffect(() => {
        if (!gameId || !boardState) return;

        const fetchMoveHistory = () => {
                fetch(`http://localhost:8000/game/${gameId}/history`)
                    .then((res) => res.json())
                    .then((data) => {
                        console.log("📥 Move-Historie erhalten:", data);
                        setMoveHistory({
                            white_moves: data.white_moves.map(parseMoveNotation),
                            black_moves: data.black_moves.map(parseMoveNotation),
                        });
                    })
                    .catch((err) => console.error("Fehler beim Abrufen der Move-Historie:", err));
            };

        fetchMoveHistory();
    }, [gameId, boardState]);

    return (
        <div className="game-container">
            <div className="sidebar">
                <button onClick={startNewGame}>Neues Spiel starten</button>
                {gameId && <p>Spiel-ID: {gameId}</p>}
            </div>
            <h3>Zug-Historie</h3>
            <div className="move-list">
                <strong>Weiß:</strong>
                <ul>
                        {moveHistory.white_moves.map((move, index) => (
    <li key={`w${index}`}>{JSON.stringify(move)}</li>
))
}
                </ul>

                <strong>Schwarz:</strong>
                <ul>
                        {moveHistory.black_moves.map((move, index) => (
    <li key={`w${index}`}>{JSON.stringify(move)}</li>
))
}
                </ul>
                </div>

            <DndProvider backend={HTML5Backend}>
                <ChessBoard gameId={gameId} onBoardChange={setBoardState} />
            </DndProvider>
        </div>
    );
};

export default ChessGame;
