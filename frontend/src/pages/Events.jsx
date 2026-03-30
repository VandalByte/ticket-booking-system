import { useState, useEffect } from 'react';
import { Container, Row, Col, Spinner, Alert } from 'react-bootstrap';
import { getEvents } from '../api/eventApi';
import EventCard from '../components/EventCard';

const Events = () => {
    const [events, setEvents] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchEvents = async () => {
            try {
                const data = await getEvents();
                setEvents(data);
            } catch (err) {
                setError('Failed to load events. Please try again later.');
                console.error(err);
            } finally {
                setLoading(false);
            }
        };

        fetchEvents();
    }, []);

    if (loading) {
        return (
            <Container className="text-center mt-5">
                <Spinner animation="border" variant="primary" />
                <p className="mt-3">Loading exciting events...</p>
            </Container>
        );
    }

    return (
        <Container className="py-5">
            <h2 className="mb-4 fw-bold">Upcoming Events</h2>

            {error && <Alert variant="danger">{error}</Alert>}

            {!error && events.length === 0 && (
                <Alert variant="info">No events found. Check back later!</Alert>
            )}

            <Row xs={1} md={2} lg={3} className="g-4">
                {events.map((event) => (
                    <Col key={event.id || event._id}>
                        <EventCard event={event} />
                    </Col>
                ))}
            </Row>
        </Container>
    );
};

export default Events;