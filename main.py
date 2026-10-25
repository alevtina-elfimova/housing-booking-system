from datetime import date

from models.accommodation import Apartment
from models.customer import Customer
from models.booking import Booking
from models.payment import Payment
from models.review import Review
from services.booking_system import BookingSystem


apartment = Apartment(
    1,
    "Уютная квартира",
    "Центральная улица, 10",
    50,
    3
)

customer = Customer(
    1,
    "Анна Иванова",
    "anna@example.com"
)

booking = Booking(
    1,
    customer,
    apartment,
    date(2026, 11, 10),
    date(2026, 11, 14)
)

payment = Payment(1, booking, 200, "Банковская карта")

review = Review(
    1,
    customer,
    apartment,
    5,
    "Все понравилось"
)

system = BookingSystem()
system.add_booking(booking)

print(apartment.get_info())
print(customer.get_info())
print(booking.get_info())
print(payment.get_info())
print(review.get_info())

print("Всего бронирований:", len(system.get_all_bookings()))

print("\nПроверка управления бронированиями")

found_booking = system.find_booking(1)
print("Найдено бронирование:", found_booking is not None)

updated = system.update_booking_status(1, "Подтверждено")
print("Статус изменён:", updated)
print("Новый статус:", booking.status)

deleted = system.delete_booking(1)
print("Бронирование удалено:", deleted)
print("Осталось бронирований:", len(system.get_all_bookings()))