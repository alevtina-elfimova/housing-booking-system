from datetime import date

class Booking:
    """Класс бронирования"""

    def __init__(self, booking_id, customer, accommodation,
                 check_in, check_out):
        self.booking_id = booking_id
        self.customer = customer
        self.accommodation = accommodation
        self.check_in = check_in
        self.check_out = check_out
        self.status = "Создано"

    def calculate_total(self):
        """Рассчитывает общую стоимость проживания"""
        nights = (self.check_out - self.check_in).days
        return nights * self.accommodation.price_per_night

    def cancel(self):
        """Отменяет бронирование"""
        self.status = "Отменено"

    def get_info(self):
        """Возвращает информацию о бронировании"""
        return (
            f"Бронирование №{self.booking_id}, "
            f"клиент: {self.customer.name}, "
            f"жильё: {self.accommodation.title}, "
            f"заезд: {self.check_in}, "
            f"выезд: {self.check_out}, "
            f"статус: {self.status}"
        )
