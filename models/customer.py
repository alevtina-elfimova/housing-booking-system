class Customer:
    """Класс клиента"""
    def __init__(self, customer_id, name, email):
        self.customer_id = customer_id
        self.name = name
        self.email = email

    def get_info(self):
        """Возвращает информацию о клиенте."""
        return (
            f"ID клиента: {self.customer_id}, "
            f"Имя: {self.name}, "
            f"Email: {self.email}"
        )

