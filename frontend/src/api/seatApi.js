import axiosInstance from './axiosInstance';

export const getSeats = async (eventId) => {
    const response = await axiosInstance.get(`/seats/${eventId}`);
    return response.data;
};

export const lockSeats = async (eventId, seatNumbers) => {
    const response = await axiosInstance.post('/seats/lock', {
        event_id: eventId,
        seat_numbers: seatNumbers
    });
    return response.data;
};