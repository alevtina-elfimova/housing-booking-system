class BookingError(Exception):
    """Базовое исключение системы бронирования"""

class BookingNotFoundError(BookingError):
    """Исключение, если бронирование не найдено"""

class InvalidBookingError(BookingError):
    """Исключение, если данные бронирования неправильные"""
