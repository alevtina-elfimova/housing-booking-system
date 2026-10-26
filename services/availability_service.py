class AvailabilityService:
    """Класс для проверки доступности жилья"""

    def is_available(
        self, accommodation, bookings, check_in, check_out
    ):
        """Проверяет, свободно ли жильё на выбранные даты."""

        if check_out <= check_in:
            raise ValueError(
                "Дата выезда должна быть позже даты заезда."
            )

        for booking in bookings:
            if booking.accommodation.accommodation_id != accommodation.accommodation_id:
                continue

            if str(booking.status).strip().casefold() == "отменено":
                continue

            if check_in < booking.check_out and check_out > booking.check_in:
                return False

        return True

    def get_available_accommodations(
        self, accommodations, bookings, check_in, check_out
    ):
        """Возвращает список жилья, свободного на выбранные даты"""

        available = []

        for accommodation in accommodations:
            if self.is_available(
                accommodation, bookings, check_in, check_out
            ):
                available.append(accommodation)

        return available
