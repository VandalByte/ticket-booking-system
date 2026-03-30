import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Container, Row, Col, Button, Badge, Spinner } from 'react-bootstrap';
import { getSeats, lockSeats } from '../api/seatApi';

const SeatSelection = () => {
    const { eventId } = useParams();
    const navigate = useNavigate();
    const [seats, setSeats] = useState([]);
    const [selectedSeats, setSelectedSeats] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        fetchSeats();
    }, [eventId]);

    const fetchSeats = async () => {
        try {
            const data = await getSeats(eventId);
            setSeats(data);
        } catch (err) {
            console.error("Error fetching seats", err);
        } finally {
            setLoading(false);
        }
    };

    const toggleSeat = (seatNumber, status) => {
        if (status !== 'available') return; // Can't click booked seats
        
        if (selectedSeats.includes(seatNumber)) {
            setSelectedSeats(selectedSeats.filter(s => s !== seatNumber));
        } else {
            setSelectedSeats([...selectedSeats, seatNumber]);
        }
    };

    const handleProceed = async () => {
        try {
            await lockSeats(eventId, selectedSeats);
            // If lock is successful, move to payment
            navigate('/payment', { state: { eventId, selectedSeats } });
        } catch (err) {
            alert(err.response?.data?.detail || "Could not lock seats");
        }
    };

    if (loading) return <Spinner animation="border" className="d-block mx-auto mt-5" />;

    return (
        <Container className="py-5">
            <h2 className="text-center mb-4">Select Your Seats</h2>
            
            {/* The Stage / Screen */}
            <div className="bg-dark text-white text-center py-2 mb-5 rounded-pill shadow-sm">
                STAGE THIS WAY
            </div>

            <Row className="justify-content-center">
                <Col md={8} className="d-flex flex-wrap justify-content-center gap-2">
                    {seats.map((seat) => (
                        <Button
                            key={seat.id}
                            variant={
                                seat.status === 'booked' ? 'danger' :
                                selectedSeats.includes(seat.seat_number) ? 'warning' : 'outline-success'
                            }
                            disabled={seat.status === 'booked'}
                            style={{ width: '50px', height: '50px' }}
                            onClick={() => toggleSeat(seat.seat_number, seat.status)}
                        >
                            {seat.seat_number}
                        </Button>
                    ))}
                </Col>
            </Row>

            <div className="text-center mt-5">
                <p>Selected: <strong>{selectedSeats.join(', ') || 'None'}</strong></p>
                <Button 
                    variant="primary" 
                    size="lg" 
                    disabled={selectedSeats.length === 0}
                    onClick={handleProceed}
                >
                    Confirm & Pay
                </Button>
            </div>
        </Container>
    );
};

export default SeatSelection;