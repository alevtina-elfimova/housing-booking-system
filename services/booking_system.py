class BookingSystem:
    """Класс управления системой бронирования"""
    def __init__(self):
        self.bookings = []

    def add_booking(self, booking):
        """Добавляет бронирование"""
        self.bookings.append(booking)

    def get_all_bookings(self):
        """Возвращает список всех бронирований"""
        return self.bookings

    def find_booking(self, booking_id):
        """Находит бронирование по номеру"""
        for booking in self.bookings:
            if booking.booking_id == booking_id:
                return booking

        return None

    def update_booking_status(self, booking_id, new_status):
        """Изменяет статус бронирования"""
        booking = self.find_booking(booking_id)

        if booking is None:
            return False

        booking.status = new_status
        return True

    def delete_booking(self, booking_id):
        """Удаляет бронирование"""
        booking = self.find_booking(booking_id)

        if booking is None:
            return False

        self.bookings.remove(booking)
        return True
