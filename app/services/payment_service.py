from fastapi import HTTPException, status


class PaymentService:
    def __init__(self, payment_repo, booking_repo, seat_repo, redis_client):
        self.payment_repo = payment_repo
        self.booking_repo = booking_repo
        self.seat_repo = seat_repo
        self.redis = redis_client

    async def confirm_and_process(self, booking_id: str, user_id: str, method: str):
        # Verify Booking exists and belongs to the user
        booking = await self.booking_repo.get_booking_by_id(booking_id)
        if not booking:
            raise HTTPException(status_code=404, detail="Booking not found")
        if booking["user_id"] != user_id:
            raise HTTPException(
                status_code=403, detail="Not authorized to pay for this booking"
            )
        if booking["status"] == "confirmed":
            raise HTTPException(status_code=400, detail="Booking already paid")

        # Record the payment as 'success' (SIMULATED)
        payment = await self.payment_repo.create_payment_record(
            booking_id=booking_id,
            amount=booking["total_price"],
            method=method,
            status="success",
        )

        # Update booking to 'confirmed'
        await self.booking_repo.update_status(booking_id, "confirmed")

        # Permanently mark seats as 'booked' in MongoDB
        await self.seat_repo.mark_seats_booked(
            booking["event_id"], booking["seat_numbers"]
        )

        # REMOVE the locks from Redis so seats aren't "held" anymore
        for seat in booking["seat_numbers"]:
            self.redis.delete(f"lock:{booking['event_id']}:{seat}")

        return payment
