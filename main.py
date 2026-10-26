from datetime import date

from models.accommodation import Apartment, House
from models.customer import Customer
from models.booking import Booking
from services.booking_system import BookingSystem
from services.data_manager import DataManager
from exceptions import BookingNotFoundError
from services.booking_service import BookingService
from services.accommodation_search_service import AccommodationSearchService

def create_test_data():
    """Создаёт начальные данные для демонстрации"""
    apartment = Apartment(
        1,
        "Уютная квартира",
        "Центральная улица, 10",
        2500,
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

    system = BookingSystem()
    system.add_booking(booking)

    customers = [customer]
    accommodations = [apartment]

    return system, customers, accommodations

def show_menu():
    """Показывает главное меню"""
    print("\nСистема бронирования жилья")
    print("1. Показать бронирования")
    print("2. Найти бронирование")
    print("3. Создать бронирование")
    print("4. Изменить статус бронирования")
    print("5. Удалить бронирование")
    print("6. Добавить клиента")
    print("7. Добавить жильё")
    print("8. Показать клиентов и жильё")
    print("9. Сохранить данные в JSON")
    print("10. Загрузить данные из JSON")
    print("11. Сохранить данные в XML")
    print("12. Загрузить данные из XML")
    print("13. Поиск свободного жилья")
    print("14. Выход")

def main():
    system, customers, accommodations = create_test_data()
    data_manager = DataManager()
    booking_service = BookingService(system)
    search_service = AccommodationSearchService()

    while True:
        show_menu()
        choice = input("Выберите действие: ")

        if choice == "1":
            bookings = system.get_all_bookings()

            if not bookings:
                print("Бронирований пока нет.")
            else:
                for booking in bookings:
                    print(booking.get_info())

        elif choice == "2":
            try:
                booking_id = int(input("Введите номер бронирования: "))
                booking = system.find_booking(booking_id)
                print(booking.get_info())
            except ValueError:
                print("Ошибка: нужно ввести целое число.")
            except BookingNotFoundError as error:
                print("Ошибка:", error)

        elif choice == "3":
            try:
                if not customers:
                    print("Сначала добавьте клиента.")
                    continue

                if not accommodations:
                    print("Сначала добавьте жильё.")
                    continue

                print("\nКлиенты")
                for customer in customers:
                    print(customer.get_info())

                customer_id = int(input("Введите ID клиента: "))
                customer = next(
                    (c for c in customers if c.customer_id == customer_id),
                    None
                )

                if customer is None:
                    print("Ошибка: клиент не найден.")
                    continue

                print("\nВсё жильё")
                for accommodation in accommodations:
                    print(accommodation.get_info())

                accommodation_id = int(
                    input("Введите ID жилья для бронирования: ")
                )

                accommodation = next(
                    (
                        a for a in accommodations
                        if a.accommodation_id == accommodation_id
                    ),
                    None
                )

                if accommodation is None:
                    print("Ошибка: жильё не найдено.")
                    continue



                check_in = date.fromisoformat(
                    input("Дата заезда (ГГГГ-ММ-ДД): ")
                )
                check_out = date.fromisoformat(
                    input("Дата выезда (ГГГГ-ММ-ДД): ")
                )

                # Проверяем доступность именно выбранного жилья
                if not search_service.availability_service.is_available(
                        accommodation,
                        system.get_all_bookings(),
                        check_in,
                        check_out
                ):
                    print(
                        "Отказ: выбранное жильё занято "
                        "на указанные даты. Бронирование не создано."
                    )
                    continue

                # Создаём бронирование только после проверки
                booking = booking_service.create_booking(
                    customer,
                    accommodation,
                    check_in,
                    check_out
                )

                print("\nБронирование успешно создано!")
                print("Номер бронирования:", booking.booking_id)
                print(booking.get_info())
                print(
                    "Стоимость проживания:",
                    booking.calculate_total()
                )

            except ValueError as error:
                print("Ошибка ввода или даты:", error)

        elif choice == "4":
            try:
                booking_id = int(input("Введите номер бронирования: "))
                new_status = input(
                    "Введите новый статус (подтверждено/отменено): "
                ).strip().lower()

                if new_status not in ("подтверждено", "отменено"):
                    print("Ошибка: допустимые статусы — подтверждено или отменено.")
                    continue

                system.update_booking_status(booking_id, new_status)
                print("Статус бронирования успешно изменён.")

            except ValueError:
                print("Ошибка: номер бронирования должен быть целым числом.")
            except BookingNotFoundError as error:
                print("Ошибка:", error)

        elif choice == "5":
            try:
                booking_id = int(input("Введите номер бронирования для удаления: "))
                system.delete_booking(booking_id)
                print("Бронирование успешно удалено.")

            except ValueError:
                print("Ошибка: номер бронирования должен быть целым числом.")
            except BookingNotFoundError as error:
                print("Ошибка:", error)

        elif choice == "6":
            try:
                customer_id = int(input("Введите ID клиента: "))

                if any(c.customer_id == customer_id for c in customers):
                    print("Ошибка: клиент с таким ID уже существует.")
                    continue

                name = input("Введите имя и фамилию клиента: ").strip()
                email = input("Введите email клиента: ").strip()

                if not name or not email or "@" not in email:
                    print("Ошибка: введите имя и корректный email.")
                    continue

                customer = Customer(customer_id, name, email)
                customers.append(customer)
                print("Клиент успешно добавлен.")

            except ValueError:
                print("Ошибка: ID должен быть целым числом.")

        elif choice == "7":
            try:
                accommodation_id = int(input("Введите ID жилья: "))

                if any(a.accommodation_id == accommodation_id
                       for a in accommodations):
                    print("Ошибка: жильё с таким ID уже существует.")
                    continue

                title = input("Введите название жилья: ").strip()
                address = input("Введите адрес жилья: ").strip()
                price = float(input("Введите цену за ночь: "))

                if not title or not address or price <= 0:
                    print("Ошибка: укажите название, адрес и положительную цену.")
                    continue

                print("1. Квартира")
                print("2. Дом")
                accommodation_type = input("Выберите тип жилья: ")

                if accommodation_type == "1":
                    floor = int(input("Введите этаж: "))
                    accommodation = Apartment(
                        accommodation_id, title, address, price, floor
                    )
                elif accommodation_type == "2":
                    garden_text = input("Есть сад? (да/нет): ").strip().lower()

                    if garden_text not in ("да", "нет"):
                        print("Ошибка: введите «да» или «нет».")
                        continue

                    has_garden = garden_text == "да"
                    accommodation = House(
                        accommodation_id, title, address, price, has_garden
                    )
                else:
                    print("Ошибка: выберите 1 или 2.")
                    continue

                accommodations.append(accommodation)
                print("Жильё успешно добавлено.")

            except ValueError:
                print("Ошибка: проверьте числовые данные.")

        elif choice == "8":
            print("\nКлиенты")
            for customer in customers:
                print(customer.get_info())

            print("\nЖильё")
            for accommodation in accommodations:
                print(accommodation.get_info())

        elif choice == "9":
            records = data_manager.prepare_data(customers, accommodations, system)

            try:
                data_manager.save_json("data/bookings.json", records)
                print("Данные успешно сохранены в data/bookings.json.")
            except (OSError, TypeError, ValueError) as error:
                print("Не удалось сохранить JSON:", error)

        elif choice == "10":
            records = data_manager.load_json("data/bookings.json")

            if records is not None:
                try:
                    customers, accommodations = data_manager.restore_data(records, system)
                    print("Данные успешно загружены из JSON.")
                except (ValueError, TypeError, KeyError) as error:
                    print("Не удалось восстановить данные из JSON:", error)

        elif choice == "11":
            records = data_manager.prepare_data(customers, accommodations, system)

            try:
                data_manager.save_xml("data/bookings.xml", records)
                print("Данные успешно сохранены в data/bookings.xml.")
            except (OSError, TypeError, ValueError) as error:
                print("Не удалось сохранить XML:", error)

        elif choice == "12":
            records = data_manager.load_xml("data/bookings.xml")

            if records is not None:
                try:
                    customers, accommodations = data_manager.restore_data(records, system)
                    print("Данные успешно загружены из XML.")
                except (ValueError, TypeError, KeyError) as error:
                    print("Не удалось восстановить данные из XML:", error)

        elif choice == "13":
            try:
                check_in = date.fromisoformat(
                    input("Дата заезда (ГГГГ-ММ-ДД): ")
                )
                check_out = date.fromisoformat(
                    input("Дата выезда (ГГГГ-ММ-ДД): ")
                )

                if check_out <= check_in:
                    print("Ошибка: дата выезда должна быть позже даты заезда.")
                    continue

                available = search_service.search_available(
                    accommodations,
                    system.get_all_bookings(),
                    check_in,
                    check_out
                )

                if not available:
                    print(
                        "На выбранные даты нет свободного жилья. "
                        "Попробуйте другие даты."
                    )
                    continue

                print("\nСвободное жильё")
                for accommodation in available:
                    print(accommodation.get_info())

                max_price = input(
                    "\nМаксимальная цена за ночь "
                    "(Enter — без ограничения): "
                ).strip()

                if max_price:
                    price_limit = float(max_price)

                    if price_limit <= 0:
                        print("Цена должна быть положительной.")
                        continue

                    available = search_service.search_by_price(
                        available,
                        price_limit
                    )

                if available:
                    print("\nПодходящее жильё")
                    for accommodation in available:
                        print(accommodation.get_info())
                else:
                    print(
                        "Свободное жильё найдено, "
                        "но вариантов в заданном бюджете нет."
                    )

            except ValueError as error:
                print("Ошибка ввода или даты:", error)

        elif choice == "14":
            print("Программа завершена.")
            break

        else:
            print("Ошибка: выберите пункт от 1 до 13.")


if __name__ == "__main__":
    main()
