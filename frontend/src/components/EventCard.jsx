import { Card, Button, Badge } from 'react-bootstrap';
import { useNavigate } from 'react-router-dom';

const EventCard = ({ event }) => {
    const navigate = useNavigate();

    // Formatting date for better readability
    const eventDate = new Date(event.date).toLocaleDateString('en-US', {
        weekday: 'long',
        year: 'numeric',
        month: 'long',
        day: 'numeric',
    });

    return (
        <Card className="h-100 shadow-sm border-0">
            <Card.Body className="d-flex flex-column">
                <div className="d-flex justify-content-between align-items-start mb-2">
                    <Card.Title className="fw-bold">{event.title}</Card.Title>
                    <Badge bg="success">₹{event.price_per_seat}</Badge>
                </div>
                
                <Card.Subtitle className="mb-3 text-muted">
                    <i className="bi bi-geo-alt-fill me-1"></i> {event.venue}
                </Card.Subtitle>
                
                <Card.Text className="small text-secondary flex-grow-1">
                    {eventDate}
                </Card.Text>

                <div className="mt-3">
                    <Button 
                        variant="outline-primary" 
                        className="w-100 fw-bold"
                        onClick={() => navigate(`/events/${event.id || event._id}`)}
                    >
                        View Seats
                    </Button>
                </div>
            </Card.Body>
        </Card>
    );
};

export default EventCard;