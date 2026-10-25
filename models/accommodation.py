class Accommodation:
    """Базовый класс жилья"""
    def __init__(self, accommodation_id, title, address, price_per_night):
        self.accommodation_id = accommodation_id
        self.title = title
        self.address = address
        self.price_per_night = price_per_night
        self.is_available = True

    def get_info(self):
        """Возвращает информацию о жилье"""
        return (
            f"ID: {self.accommodation_id}, "
            f"Название: {self.title}, "
            f"Адрес: {self.address}, "
            f"Цена за ночь: {self.price_per_night}, "
            f"Доступно: {self.is_available}"
        )

class Apartment(Accommodation):
    """Класс квартиры"""

    def __init__(
            self, accommodation_id, title, address, price_per_night, floor
    ):
        super().__init__(
            accommodation_id, title, address, price_per_night
        )
        self.floor = floor

    def get_info(self):
        return f"{super().get_info()}, Этаж: {self.floor}"


class House(Accommodation):
    """Класс частного дома"""

    def __init__(
            self, accommodation_id, title, address, price_per_night, has_garden
    ):
        super().__init__(
            accommodation_id, title, address, price_per_night
        )
        self.has_garden = has_garden

    def get_info(self):
        garden = "да" if self.has_garden else "нет"
        return f"{super().get_info()}, Сад: {garden}"

