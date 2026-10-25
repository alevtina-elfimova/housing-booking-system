import json

class DataManager:
    """Класс чтения и сохранения данных"""
    def save_json(self, filename, data):
        """Сохраняет данные в JSON-файл"""
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

    def load_json(self, filename):
        """Загружает данные из JSON-файла"""
        with open(filename, "r", encoding="utf-8") as file:
            return json.load(file)

    def save_xml(self, filename, data):
        """Сохраняет данные в XML-файл"""
        import xml.etree.ElementTree as ET

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
        import xml.etree.ElementTree as ET

        tree = ET.parse(filename)
        root = tree.getroot()

        data = []

        for element in root:
            item = {}

            for field in element:
                item[field.tag] = field.text

            data.append(item)

        return data
