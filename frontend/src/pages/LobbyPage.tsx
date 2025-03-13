import { useEffect, useState, useCallback } from "react";
import { Button, Container, ListGroup, Spinner, Alert } from "react-bootstrap";
import GameHooks from "../components/hooks/GameHooks";
import { Lobby } from "../models/lobby";
import { useUser } from "../components/hooks/UserHooks";

export default function LobbyPage() {
    const { listLobbies, createLobby } = GameHooks();
    const { user } = useUser();

    const [lobbies, setLobbies] = useState<Lobby[]>([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const [creating, setCreating] = useState(false);

    const fetchLobbies = useCallback(async () => {
        setLoading(true);
        setError(null);

        try {
            const data = await listLobbies();
            setLobbies(data);
        } catch {
            setError("Fehler beim Laden der Lobbys.");
        } finally {
            setLoading(false);
        }
    }, [listLobbies]);

    useEffect(() => {
        fetchLobbies();
    }, [fetchLobbies]);

    const handleCreateLobby = async () => {
        if (!user?.user_id || !user?.username) {
            setError("Fehler: Benutzer nicht gefunden.");
            return;
        }

        setCreating(true);
        setError(null);
        try {
            if (createLobby) {
                await createLobby(user.user_id, user.username);
            } else {
                setError("Fehler: Lobby-Erstellungsfunktion nicht verfügbar.");
            }
            await fetchLobbies();
        } catch {
            setError("Fehler beim Erstellen der Lobby.");
        } finally {
            setCreating(false);
        }
    };

    return (
        <Container className="mt-4">
            <h2 className="mb-3">🔹 Lobby Übersicht</h2>

            {error && <Alert variant="danger">{error}</Alert>}
            {lobbies.length === 0 && !error && (
                <Alert variant="info">🔍 Keine offenen Lobbys gefunden.</Alert>
            )}

            <div className="mb-3 d-flex gap-2">
                <Button onClick={fetchLobbies} disabled={loading} variant="secondary">
                    {loading ? <Spinner animation="border" size="sm" /> : "🔄 Aktualisieren"}
                </Button>
                <Button onClick={handleCreateLobby} disabled={creating} variant="primary">
                    {creating ? <Spinner animation="border" size="sm" /> : "➕ Lobby erstellen"}
                </Button>
            </div>

            {loading && <Spinner animation="border" className="d-block mx-auto" />}

            {lobbies.length > 0 && (
                <ListGroup>
                    {lobbies.map((lobby) => (
                        <ListGroup.Item
                            key={lobby.game_id}
                            className="d-flex justify-content-between align-items-center p-3 shadow-sm rounded"
                            style={{ background: "#f8f9fa", borderLeft: "5px solid #007bff" }}
                        >
                            <div>
                                <h5 className="mb-0">{lobby.players[0]?.username}'s Lobby</h5>
                                <small>{lobby.players.length} Spieler in der Lobby</small>
                            </div>
                        </ListGroup.Item>
                    ))}
                </ListGroup>
            )}
        </Container>
    );
}
