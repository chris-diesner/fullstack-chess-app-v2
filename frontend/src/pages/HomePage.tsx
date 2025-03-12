import { Container, Col } from "react-bootstrap";

export default function HomePage() {

  return (
    <Container fluid className="vh-100 d-flex">
      <Col md={9} className="p-5 text-center">
        <h1>Willkommen auf der Startseite!</h1>
      </Col>
    </Container>
  );
}
