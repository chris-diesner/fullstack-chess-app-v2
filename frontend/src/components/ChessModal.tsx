import { Modal, Button } from "react-bootstrap";

interface ChessModalProps {
  show: boolean;
  handleClose: () => void;
  message: string;
}

const ChessModal: React.FC<ChessModalProps> = ({ show, handleClose, message }) => {
  return (
    <Modal show={show} onHide={handleClose} centered>
      <Modal.Header closeButton>
        <Modal.Title>Hinweis</Modal.Title>
      </Modal.Header>
      <Modal.Body>
        <p>{message}</p>
      </Modal.Body>
      <Modal.Footer>
        <Button variant="primary" onClick={handleClose}>
          Verstanden
        </Button>
      </Modal.Footer>
    </Modal>
  );
};

export default ChessModal;