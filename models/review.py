class Review:
    """Класс отзыва о жилье"""
    def __init__(self, review_id, customer, accommodation, rating, comment):
        self.review_id = review_id
        self.customer = customer
        self.accommodation = accommodation
        self.rating = rating
        self.comment = comment

    def get_info(self):
        """Возвращает информацию об отзыве"""
        return (
            f"Отзыв №{self.review_id}, "
            f"клиент: {self.customer.name}, "
            f"жильё: {self.accommodation.title}, "
            f"оценка: {self.rating}, "
            f"комментарий: {self.comment}"
        )
