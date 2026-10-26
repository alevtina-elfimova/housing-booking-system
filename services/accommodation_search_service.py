from services.availability_service import AvailabilityService


class AccommodationSearchService:
    """Класс поиска подходящего жилья"""

    def __init__(self):
        self.availability_service = AvailabilityService()

    def search_available(
        self, accommodations, bookings, check_in, check_out
    ):
        """Находит свободное жильё на выбранные даты"""

        return self.availability_service.get_available_accommodations(
            accommodations, bookings, check_in, check_out
        )

    def search_by_price(self, accommodations, max_price):
        """Находит жильё с ценой не выше заданной"""

        return [
            accommodation
            for accommodation in accommodations
            if accommodation.price_per_night <= max_price
        ]
    