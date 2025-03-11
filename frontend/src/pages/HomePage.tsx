import { useState } from "react";
import { Link } from "react-router-dom";
import { Button, Container, Col, Form, Alert, Spinner, Modal } from "react-bootstrap";
import UserHooks from "../components/hooks/UserHooks";

export default function HomePage() {
  const { login, register, user, logout } = UserHooks();
  const initialFormState = { username: "", password: "", confirmPassword: "" };
  const [isLogin, setIsLogin] = useState(true);
  const [formData, setFormData] = useState(initialFormState);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [showErrorModal, setShowErrorModal] = useState(false);

  const handleSubmit = async () => {
    setLoading(true);
    setError(null);

    if (!isLogin) {
      if (formData.password.length < 6) {
        setError("Das Passwort muss mindestens 6 Zeichen lang sein.");
        setShowErrorModal(true);
        setLoading(false);
        return;
      }
      if (formData.password !== formData.confirmPassword) {
        setError("Die Passwörter stimmen nicht überein.");
        setShowErrorModal(true);
        setLoading(false);
        return;
      }
    }

    try {
      if (isLogin) {
        await login(formData.username, formData.password);
      } else {
        await register(formData.username, formData.password);
      }
      setFormData(initialFormState); // Felder nach erfolgreichem Login/Register leeren
    } catch (err) {
      if (err instanceof Error) {
        setError(err.message);
      } else {
        setError("Ein unbekannter Fehler ist aufgetreten.");
      }
      setShowErrorModal(true);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container fluid className="vh-100 d-flex">
      {/* Linke Sidebar mit Login / Register */}
      <Col md={3} className="bg-light p-4 border-end">
        {user ? (
          <div className="text-center">
            <h5>Willkommen, {user}!</h5>
            <Button variant="danger" onClick={logout} className="mt-3 w-100">
              Logout
            </Button>
          </div>
        ) : (
          <>
            <h4 className="text-center">{isLogin ? "Login" : "Registrieren"}</h4>
            <Form key={isLogin ? "login" : "register"} autoComplete="off">
              <Form.Group className="mb-3">
                <Form.Label>Benutzername</Form.Label>
                <Form.Control
                  type="text"
                  placeholder="Gib deinen Namen ein"
                  value={formData.username}
                  onChange={(e) => setFormData({ ...formData, username: e.target.value })}
                  autoComplete="off"
                />
              </Form.Group>
              <Form.Group className="mb-3">
                <Form.Label>Passwort</Form.Label>
                <Form.Control
                  type="password"
                  placeholder="Gib dein Passwort ein"
                  value={formData.password}
                  onChange={(e) => setFormData({ ...formData, password: e.target.value })}
                  autoComplete="new-password"
                />
              </Form.Group>
              {!isLogin && (
                <Form.Group className="mb-3">
                  <Form.Label>Passwort bestätigen</Form.Label>
                  <Form.Control
                    type="password"
                    placeholder="Gib dein Passwort erneut ein"
                    value={formData.confirmPassword}
                    onChange={(e) => setFormData({ ...formData, confirmPassword: e.target.value })}
                    autoComplete="new-password"
                  />
                </Form.Group>
              )}
              <Button variant="primary" className="w-100" onClick={handleSubmit} disabled={loading}>
                {loading ? <Spinner animation="border" size="sm" /> : isLogin ? "Login" : "Registrieren"}
              </Button>
            </Form>
            <Button
              variant="link"
              className="w-100 mt-2"
              onClick={() => {
                setIsLogin(!isLogin);
                setFormData(initialFormState);
              }}
            >
              {isLogin ? "Noch kein Konto? Hier registrieren" : "Schon ein Konto? Hier einloggen"}
            </Button>
          </>
        )}
      </Col>

      {/* Hauptinhalt */}
      <Col md={9} className="p-5 text-center">
        <h1>Willkommen auf der Startseite!</h1>
        <nav>
          <Link to="/game" className="btn btn-primary">Zum Schachbrett</Link>
        </nav>
      </Col>

      {/* Fehler-Modal */}
      <Modal show={showErrorModal} onHide={() => setShowErrorModal(false)} centered>
        <Modal.Header closeButton>
          <Modal.Title>Fehler</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <Alert variant="danger">{error}</Alert>
        </Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={() => setShowErrorModal(false)}>
            Schließen
          </Button>
        </Modal.Footer>
      </Modal>
    </Container>
  );
}
