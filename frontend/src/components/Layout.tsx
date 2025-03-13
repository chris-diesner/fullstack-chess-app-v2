import { useState } from "react";
import { Outlet, Link } from "react-router-dom";
import { Button, Container, Col, Form, Alert, Spinner } from "react-bootstrap";
import { useUser } from "./hooks/UserHooks";

export default function Layout() {
  const { user, login, register, logout } = useUser();
  const [isLogin, setIsLogin] = useState(true);
  const initialFormState = { username: "", password: "", confirmPassword: "" };
  const [formData, setFormData] = useState(initialFormState);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async () => {
    setLoading(true);
    setError(null);

    if (!isLogin) {
      if (formData.password.length < 6) {
        setError("Das Passwort muss mindestens 6 Zeichen lang sein.");
        setLoading(false);
        return;
      }
      if (formData.password !== formData.confirmPassword) {
        setError("Die Passwörter stimmen nicht überein.");
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
      setFormData(initialFormState);
    } catch (err) {
      if (err instanceof Error) {
        setError(err.message);
      } else {
        setError("Ein unbekannter Fehler ist aufgetreten.");
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container fluid className="vh-100 d-flex">
      <Col md={3} className="bg-light p-4 border-end">
        {user ? (
          <div className="text-center">
            <h5>Willkommen, {user.username}!</h5>
            <nav className="d-flex flex-column">
              <Link to="/" className="btn btn-secondary mt-2">Startseite</Link>
              <Link to="/lobby" className="btn btn-secondary mt-2">Zum Spiel</Link>
              <Link to="/about" className="btn btn-secondary mt-2">Über uns</Link>
            </nav>
            <Button variant="danger" onClick={logout} className="mt-3 w-100">
              Logout
            </Button>
          </div>
        ) : (
          <>
            <h4 className="text-center">{isLogin ? "Login" : "Registrieren"}</h4>
            {error && <Alert variant="danger">{error}</Alert>}
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

      <Col md={9} className="p-5">
        <Outlet />
      </Col>
    </Container>
  );
}
