import { useEffect, useState, useCallback } from "react";
import { Button, Container, ListGroup, Spinner, Alert, Dropdown, Form } from "react-bootstrap";
import LobbyHooks from "../components/hooks/LobbyHooks";
import { Lobby } from "../models/Lobby";
import { useUser } from "../components/hooks/UserHooks";

export default function LobbyPage() {
    const [lobbies, setLobbies] = useState<Lobby[]>([]);
    const { listLobbies, createLobby, joinLobby, leaveLobby, setPlayerColor, setPlayerStatus, startGame } = LobbyHooks(setLobbies, () => {});
    const { user } = useUser();
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const [creating, setCreating] = useState(false);

    const fetchLobbies = useCallback(async () => {
        setLoading(true);
        setError(null);
    
        try {
            const data = await listLobbies();    
            setLobbies(data.map(lobby => ({ ...lobby })));  
    
        } catch {
            setError("Fehler beim Laden der Lobbys.");
        } finally {
            setLoading(false);
        }
    }, [listLobbies]);
    
    useEffect(() => {
    }, [lobbies]);
      
    const handleCreateLobby = async () => {
        if (!user?.user_id || !user?.username) {
            setError("Fehler: Benutzer nicht gefunden.");
            return;
        }

        setCreating(true);
        setError(null);
        try {
            await createLobby(user.user_id, user.username);
            await fetchLobbies();
        } catch {
            setError("Fehler beim Erstellen der Lobby.");
        } finally {
            setCreating(false);
        }
    };

    const handleJoinLeaveLobby = async (gameId: string, isInLobby: boolean) => {
        if (!user?.user_id) return;

        try {
            if (isInLobby) {
                await leaveLobby(gameId, user.user_id);
            } else {
                await joinLobby(gameId, user.user_id, user.username);
            }
            await fetchLobbies();
        } catch {
            setError(isInLobby ? "Fehler beim Verlassen der Lobby." : "Fehler beim Beitreten zur Lobby.");
        }
    };

    const handleSetColor = async (gameId: string, color: "white" | "black") => {
        if (!user?.user_id) return;
        try {
            await setPlayerColor(gameId, user.user_id, color);
            await fetchLobbies();
        } catch {
            setError("Fehler beim Setzen der Spielfarbe.");
        }
    };

    const handleSetStatus = async (gameId: string, status: "ready" | "not_ready") => {
        if (!user?.user_id) return;
        try {
            await setPlayerStatus(gameId, user.user_id, status);
            await fetchLobbies();
        } catch {
            setError("Fehler beim Setzen des Status.");
        }
    };

    const handleStartGame = async (gameId: string) => {
        if (!user?.user_id) return;
        try {
            await startGame(gameId, user.user_id);
        } catch {
            setError("Fehler beim Starten des Spiels.");
        }
    };
    
    const isLobbyReady = (lobby: Lobby) => {
        if (lobby.players.length !== 2) return false;
        return lobby.players.every(p => p.color && p.status === "ready");
    };

    return (
        <Container className="mt-4">
            <h2 className="mb-3">Lobby Übersicht</h2>

            {error && <Alert variant="danger">{error}</Alert>}
            {lobbies.length === 0 && !error && (
                <Alert variant="info">Keine offenen Lobbys gefunden.</Alert>
            )}

            <div className="mb-3 d-flex gap-2">
                <Button onClick={fetchLobbies} disabled={loading} variant="secondary">
                    {loading ? <Spinner animation="border" size="sm" /> : "Aktualisieren"}
                </Button>
                <Button onClick={handleCreateLobby} disabled={creating} variant="primary">
                    {creating ? <Spinner animation="border" size="sm" /> : "Lobby erstellen"}
                </Button>
            </div>

            {loading && <Spinner animation="border" className="d-block mx-auto" />}

            {lobbies.length > 0 && (
                <ListGroup>
                    {lobbies.map((lobby) => {
                        const isInLobby = lobby.players.some(player => player.user_id === user?.user_id);

                        return (
                            <ListGroup.Item
                                key={lobby.game_id}
                                className="d-flex flex-column p-3 shadow-sm rounded"
                                style={{ background: "#f8f9fa", borderLeft: "5px solid #007bff" }}
                            >
                                <div className="d-flex justify-content-between align-items-center">
                                    <div>
                                        <h5 className="mb-0">{lobby.players[0]?.username}'s Lobby</h5>
                                        <small>{lobby.players.length} Spieler in der Lobby</small>
                                    </div>
                                    <Button
                                        variant={isInLobby ? "danger" : "success"}
                                        onClick={() => handleJoinLeaveLobby(lobby.game_id, isInLobby)}
                                    >
                                        {isInLobby ? "Verlassen" : "Beitreten"}
                                    </Button>
                                </div>

                                <ListGroup className="mt-3">
                                    {lobby.players.map((player) => (
                                        <ListGroup.Item key={player.user_id} className="d-flex justify-content-between align-items-center">
                                            <div>
                                                <strong>{player.username}</strong>
                                                <div className="small">
                                                    Farbe: {player.color ? player.color.toUpperCase() : "Noch nicht gewählt"}  
                                                    <br />
                                                    Status: {player.status === "ready" ? "Bereit" : "Nicht bereit"}
                                                </div>
                                            </div>
                                        </ListGroup.Item>
                                    ))}
                                </ListGroup>

                                {isInLobby && (
                                    <Dropdown className="mt-2">
                                        <Dropdown.Toggle variant="light">Farbe wählen</Dropdown.Toggle>
                                        <Dropdown.Menu>
                                            <Dropdown.Item onClick={() => handleSetColor(lobby.game_id, "white")}>Weiß</Dropdown.Item>
                                            <Dropdown.Item onClick={() => handleSetColor(lobby.game_id, "black")}>Schwarz</Dropdown.Item>
                                        </Dropdown.Menu>
                                    </Dropdown>
                                )}

                                {isInLobby && (
                                    <Form.Check
                                        className="mt-2"
                                        type="switch"
                                        label="Bereit"
                                        checked={user?.status === "ready"}
                                        onChange={(e) => handleSetStatus(lobby.game_id, e.target.checked ? "ready" : "not_ready")}
                                    />
                                )}

                                {isLobbyReady(lobby) && isInLobby && (
                                    <Button variant="success" className="mt-2" onClick={() => handleStartGame(lobby.game_id)}>
                                        Spiel starten...
                                    </Button>
                                )}

                            </ListGroup.Item>
                        );
                    })}
                </ListGroup>
            )}
        </Container>
    );
}
