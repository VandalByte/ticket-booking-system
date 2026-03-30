import { Navbar, Container, Nav, Button } from 'react-bootstrap';
import { Link, useNavigate } from 'react-router-dom';
import { useContext } from 'react';
import { AuthContext } from '../context/AuthContext';

const AppNavbar = () => {
    const { user, logout } = useContext(AuthContext);
    const navigate = useNavigate();

    return (
        <Navbar bg="dark" variant="dark" expand="lg" className="sticky-top shadow">
            <Container>
                <Navbar.Brand as={Link} to="/events" className="fw-bold">
                    🎟️ TicketMaster
                </Navbar.Brand>
                <Navbar.Toggle aria-controls="basic-navbar-nav" />
                <Navbar.Collapse id="basic-navbar-nav">
                    <Nav className="me-auto">
                        <Nav.Link as={Link} to="/events">Events</Nav.Link>
                        {user && <Nav.Link as={Link} to="/my-bookings">My Bookings</Nav.Link>}
                    </Nav>
                    <Nav>
                        {user ? (
                            <Button variant="outline-light" onClick={logout} size="sm">
                                Logout
                            </Button>
                        ) : (
                            <Button variant="primary" onClick={() => navigate('/login')} size="sm">
                                Login
                            </Button>
                        )}
                    </Nav>
                </Navbar.Collapse>
            </Container>
        </Navbar>
    );
};

export default AppNavbar;