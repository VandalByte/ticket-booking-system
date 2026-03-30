import axiosInstance from './axiosInstance';

export const getEvents = async () => {
    const response = await axiosInstance.get('/events/');
    return response.data;
};

export const getEventSeats = async (eventId) => {
    const response = await axiosInstance.get(`/events/${eventId}/seats`);
    return response.data;
};
