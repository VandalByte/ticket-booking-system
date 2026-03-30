import { useLocation, useNavigate } from 'react-router-dom';
import { Container, Card, Button, ListGroup, Alert } from 'react-bootstrap';
import axiosInstance from '../api/axiosInstance';

const Payment = () => {
    const location = useLocation();
    const navigate = useNavigate();
    const { eventId, selectedSeats } = location.state || {};

    const handlePayment = async () => {
        try {
            // 1. Create the Pending Booking
            const bookingRes = await axiosInstance.post('/bookings/', {
                event_id: eventId,
                seat_numbers: selectedSeats
            });

            const bookingId = bookingRes.data.id;

            // 2. Confirm the Payment
            await axiosInstance.post('/payments/confirm', {
                booking_id: bookingId,
                amount: bookingRes.data.total_price,
                payment_method: "card"
            });

            alert("Tickets Booked Successfully!");
            navigate('/my-bookings');
        } catch (err) {
            alert(err.response?.data?.detail || "Payment failed");
        }
    };

    if (!eventId) return <Alert variant="danger">No booking data found.</Alert>;

    return (
        <Container className="mt-5">
            <Card className="mx-auto shadow" style={{ maxWidth: '500px' }}>
                <Card.Header className="bg-primary text-white">Payment Summary</Card.Header>
                <Card.Body>
                    <ListGroup variant="flush" className="mb-4">
                        <ListGroup.Item><strong>Seats:</strong> {selectedSeats.join(', ')}</ListGroup.Item>
                        <ListGroup.Item><strong>Total Seats:</strong> {selectedSeats.length}</ListGroup.Item>
                    </ListGroup>
                    <Button variant="success" className="w-100" onClick={handlePayment}>
                        Pay Now
                    </Button>
                </Card.Body>
            </Card>
        </Container>
    );
};

export default Payment;