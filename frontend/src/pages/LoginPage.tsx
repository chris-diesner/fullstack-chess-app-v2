import {useState, FormEvent, ChangeEvent} from 'react';
import {useNavigate} from 'react-router-dom';
import {useDispatch} from 'react-redux';
import axios from 'axios';
import {User} from '../models/User';
import {setUserDetails} from '../actions/ChessAppActions';
import {motion} from 'framer-motion';
import {Button, Container, Form, Toast} from 'react-bootstrap';

type Props = {
    login: (username: string, password: string) => Promise<void>
}

function Login(props: Props) {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [showSuccessToast, setShowSuccessToast] = useState(false);
    const [showErrorToast, setShowErrorToast] = useState(false);
    const navigate = useNavigate();
    const dispatch = useDispatch();
    const BACKEND_URL = import.meta.env.VITE_BACKEND_URL;

    function loginOnSubmit(e: FormEvent<HTMLFormElement>) {
        e.preventDefault();
        props.login(username, password)
            .then (() => {
                setShowSuccessToast(true);
                setTimeout(() => {
                    navigate('/');
                }, 5000);
            })
            .then(() => axios
                .get(`${BACKEND_URL}/auth/user` + username)
                .then((response) => {
                    const user: User = {
                        id: response.data.id,
                        username: response.data.username,
                        capturedFigures: response.data.capturedFigures,
                        moveHistory: response.data.moveHistory
                    };
                    dispatch(setUserDetails(user));
                })
                .catch((error) => {
                    console.log(error);
                }
            )
        );
    }

    function onChangeHandlerUsername(e: ChangeEvent<HTMLInputElement>) {
        setUsername(e.target.value);
    }

    function onChangeHandlerPassword(e: ChangeEvent<HTMLInputElement>) {
        setPassword(e.target.value);
    }

    return (
        <Container className="d-flex justify-content-center align-items-center" style={{height: "100vh"}}>
            <motion.div initial={{opacity: 0}} animate={{opacity: 1}} exit={{opacity: 0}}>
                <Form onSubmit={loginOnSubmit}>
                    <Form.Group controlId="formBasicUsername">
                        <Form.Label>Username</Form.Label>
                        <Form.Control type="text" placeholder="Enter username" onChange={onChangeHandlerUsername} />
                    </Form.Group>
                    <Form.Group controlId="formBasicPassword">
                        <Form.Label>Password</Form.Label>
                        <Form.Control type="password" placeholder="Password" onChange={onChangeHandlerPassword} />
                    </Form.Group>
                    <Button variant="primary" type="submit">
                        Submit
                    </Button>
                </Form>
                <Toast show={showSuccessToast} onClose={() => setShowSuccessToast(false)}>
                    <Toast.Header>
                        <strong className="me-auto">Success</strong>
                    </Toast.Header>
                    <Toast.Body>Successfully logged in.</Toast.Body>
                </Toast>
                <Toast show={showErrorToast} onClose={() => setShowErrorToast(false)}>
                    <Toast.Header>
                        <strong className="me-auto">Error</strong>
                    </Toast.Header>
                    <Toast.Body>Failed to log in.</Toast.Body>
                </Toast>
            </motion.div>
        </Container>
    );    
}
export default Login;