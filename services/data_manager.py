import json
import xml.etree.ElementTree as ET
from datetime import date

from models.accommodation import Apartment, House
from models.customer import Customer
from models.booking import Booking

class DataManager:
    """Класс чтения и сохранения данных"""

    def prepare_data(self, customers, accommodations, system):
        """Преобразует объекты системы в список словарей для сохранения."""
        records = []

        for customer in customers:
            records.append({
                "type": "customer",
                "customer_id": customer.customer_id,
                "name": customer.name,
                "email": customer.email
            })

        for accommodation in accommodations:
            record = {
                "type": "accommodation",
                "accommodation_id": accommodation.accommodation_id,
                "title": accommodation.title,
                "address": accommodation.address,
                "price_per_night": accommodation.price_per_night
            }

            if isinstance(accommodation, Apartment):
                record["kind"] = "apartment"
                record["floor"] = accommodation.floor
            elif isinstance(accommodation, House):
                record["kind"] = "house"
                record["has_garden"] = accommodation.has_garden

            records.append(record)

        for booking in system.get_all_bookings():
            records.append({
                "type": "booking",
                "booking_id": booking.booking_id,
                "customer_id": booking.customer.customer_id,
                "accommodation_id": booking.accommodation.accommodation_id,
                "check_in": booking.check_in.isoformat(),
                "check_out": booking.check_out.isoformat(),
                "status": booking.status
            })

        return records

    def restore_data(self, records, system):
        """Восстанавливает объекты системы из списка словарей."""
        if not isinstance(records, list):
            raise ValueError("Данные должны быть представлены списком.")

        customers = []
        accommodations = []
        bookings = []

        for record in records:
            if record["type"] == "customer":
                customers.append(Customer(
                    record["customer_id"],
                    record["name"],
                    record["email"]
                ))

        for record in records:
            if record["type"] == "accommodation":
                if record["kind"] == "apartment":
                    accommodation = Apartment(
                        record["accommodation_id"],
                        record["title"],
                        record["address"],
                        record["price_per_night"],
                        record["floor"]
                    )
                elif record["kind"] == "house":
                    accommodation = House(
                        record["accommodation_id"],
                        record["title"],
                        record["address"],
                        record["price_per_night"],
                        record["has_garden"]
                    )
                else:
                    raise ValueError("Неизвестный тип жилья.")

                accommodations.append(accommodation)

        customers_by_id = {
            customer.customer_id: customer for customer in customers
        }
        accommodations_by_id = {
            accommodation.accommodation_id: accommodation
            for accommodation in accommodations
        }

        for record in records:
            if record["type"] == "booking":
                customer = customers_by_id[record["customer_id"]]
                accommodation = accommodations_by_id[
                    record["accommodation_id"]
                ]

                booking = Booking(
                    record["booking_id"],
                    customer,
                    accommodation,
                    date.fromisoformat(record["check_in"]),
                    date.fromisoformat(record["check_out"])
                )
                booking.status = record["status"]
                bookings.append(booking)

        system.bookings = bookings
        return customers, accommodations
    def save_json(self, filename, data):
        """Сохраняет данные в JSON-файл"""
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

    def load_json(self, filename):
        """Загружает данные из JSON-файла"""
        try:
            with open(filename, "r", encoding="utf-8") as file:
                return json.load(file)

        except FileNotFoundError:
            print("Ошибка: файл JSON не найден.")
            return None

        except json.JSONDecodeError:
            print("Ошибка: файл JSON содержит неправильные данные.")
            return None

        except PermissionError:
            print("Ошибка: нет разрешения на чтение файла.")
            return None

    def save_xml(self, filename, data):
        """Сохраняет данные в XML-файл"""
        root = ET.Element("data")

        for item in data:
            element = ET.SubElement(root, "item")

            for key, value in item.items():
                field = ET.SubElement(element, key)
                field.text = str(value)

        tree = ET.ElementTree(root)
        tree.write(filename, encoding="utf-8", xml_declaration=True)

    def load_xml(self, filename):
        """Загружает данные из XML-файла"""
        try:
            tree = ET.parse(filename)
            root = tree.getroot()

            data = []

            for element in root:
                item = {}

                for field in element:
                    item[field.tag] = field.text

                data.append(item)

            return data

        except FileNotFoundError:
            print("Ошибка: файл XML не найден.")
            return None

        except ET.ParseError:
            print("Ошибка: файл XML содержит неправильные данные.")
            return None

        except PermissionError:
            print("Ошибка: нет разрешения на чтение файла.")
            return None
