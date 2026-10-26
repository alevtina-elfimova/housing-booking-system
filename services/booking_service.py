from models.booking import Booking
from services.availability_service import AvailabilityService


class BookingService:
    """Класс бизнес-логики бронирования"""

    def __init__(self, booking_system):
        self.booking_system = booking_system
        self.availability_service = AvailabilityService()

    def _generate_booking_id(self):
        """Возвращает следующий свободный номер бронирования"""
        bookings = self.booking_system.get_all_bookings()

        existing_ids = {
            booking.booking_id for booking in bookings
        }

        booking_id = 1
        while booking_id in existing_ids:
            booking_id += 1

        return booking_id

    def create_booking(
        self, customer, accommodation, check_in, check_out
    ):
        """Создаёт бронирование, если жильё доступно"""

        bookings = self.booking_system.get_all_bookings()

        if not self.availability_service.is_available(
            accommodation,
            bookings,
            check_in,
            check_out
        ):
            raise ValueError(
                "Это жильё уже забронировано на выбранные даты."
            )

        booking_id = self._generate_booking_id()

        booking = Booking(
            booking_id,
            customer,
            accommodation,
            check_in,
            check_out
        )

        self.booking_system.add_booking(booking)
        return booking

    def cancel_booking(self, booking_id):
        """Отменяет бронирование"""
        booking = self.booking_system.find_booking(booking_id)
        booking.cancel()
        return booking