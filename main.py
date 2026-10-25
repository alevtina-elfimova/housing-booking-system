from datetime import date

from models.accommodation import Apartment
from models.customer import Customer
from models.booking import Booking
from models.payment import Payment
from models.review import Review
from services.booking_system import BookingSystem

from services.data_manager import DataManager
from pathlib import Path


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

print("\nПроверка сохранения данных")

data_manager = DataManager()

test_data = [
    {
        "booking_id": 1,
        "customer": "Анна Иванова",
        "accommodation": "Уютная квартира",
        "status": "Подтверждено"
    }
]

data_folder = Path("data")
data_folder.mkdir(exist_ok=True)

json_file = data_folder / "test_data.json"
xml_file = data_folder / "test_data.xml"

data_manager.save_json(json_file, test_data)
loaded_json = data_manager.load_json(json_file)
print("Данные JSON:", loaded_json)

data_manager.save_xml(xml_file, test_data)
loaded_xml = data_manager.load_xml(xml_file)
print("Данные XML:", loaded_xml)