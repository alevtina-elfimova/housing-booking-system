class Payment:
    """Класс оплаты"""
    def __init__(self, payment_id, booking, amount, method):
        self.payment_id = payment_id
        self.booking = booking
        self.amount = amount
        self.method = method
        self.status = "Ожидает оплаты"

    def make_payment(self):
        """Изменяет статус оплаты."""
        self.status = "Оплачено"

    def get_info(self):
        """Возвращает информацию об оплате."""
        return (
            f"Оплата №{self.payment_id}, "
            f"сумма: {self.amount}, "
            f"способ: {self.method}, "
            f"статус: {self.status}"
        )
