# init_from_xml.py
import xml.etree.ElementTree as ET
import json
import os
import sys

def parse_bool(text: str) -> bool:
    return text.strip().lower() in ("true", "1", "yes")

def init_data_from_xml(xml_path: str, output_dir: str = "data"):

    if not os.path.exists(xml_path):
        raise FileNotFoundError(f"XML-файл не найден: {xml_path}")

    os.makedirs(output_dir, exist_ok=True)
    tree = ET.parse(xml_path)
    root = tree.getroot()


    members = []
    for el in root.findall(".//member"):

        members.append({
            "id": int(el.find("id").text),
            "first_name": el.find("first_name").text,
            "last_name": el.find("last_name").text,
            "email": el.find("email").text,
            "phone": el.find("phone").text,
            "membership_start": el.find("membership_start").text,  # ← без _date
            "membership_end": el.find("membership_end").text,  # ← без _date
            "is_active": parse_bool(el.find("is_active").text)
        })
    with open(os.path.join(output_dir, "members.json"), "w", encoding="utf-8") as f:
        json.dump(members, f, ensure_ascii=False, indent=2)


    coaches = []
    for el in root.findall(".//coach"):
        coaches.append({
            "id": int(el.find("id").text),
            "first_name": el.find("first_name").text,
            "last_name": el.find("last_name").text,
            "email": el.find("email").text,
            "phone": el.find("phone").text,
            "specialization": el.find("specialization").text,
            "hourly_rate": int(el.find("hourly_rate").text),
            "is_active": parse_bool(el.find("is_active").text)
        })
    with open(os.path.join(output_dir, "coaches.json"), "w", encoding="utf-8") as f:
        json.dump(coaches, f, ensure_ascii=False, indent=2)

    rooms = []
    for el in root.findall(".//gym_room"):
        rooms.append({
            "room_id": int(el.find("room_id").text),
            "room_name": el.find("room_name").text,
            "room_type": el.find("room_type").text,
            "capacity": int(el.find("capacity").text)
        })
    with open(os.path.join(output_dir, "gym_rooms.json"), "w", encoding="utf-8") as f:
        json.dump(rooms, f, ensure_ascii=False, indent=2)


    classes = []
    for el in root.findall(".//group_class"):
        attendees_text = el.find("attendees").text or ""
        attendees = [int(x.strip()) for x in attendees_text.split(",")] if attendees_text else []

        classes.append({
            "class_id": int(el.find("class_id").text),
            "class_name": el.find("class_name").text,
            "coach_id": int(el.find("coach_id").text),
            "room_id": int(el.find("room_id").text),
            "schedule": el.find("schedule").text,
            "max_capacity": int(el.find("max_capacity").text),
            "current_attendees": int(el.find("current_attendees").text),
            "attendees": attendees
        })
    with open(os.path.join(output_dir, "group_classes.json"), "w", encoding="utf-8") as f:
        json.dump(classes, f, ensure_ascii=False, indent=2)


    plans = []
    for el in root.findall(".//membership_plan"):
        plans.append({
            "plan_id": int(el.find("plan_id").text),
            "name": el.find("name").text,
            "duration_days": int(el.find("duration_days").text),
            "price": int(el.find("price").text)
        })
    with open(os.path.join(output_dir, "membership_plans.json"), "w", encoding="utf-8") as f:
        json.dump(plans, f, ensure_ascii=False, indent=2)

    payments = []
    for el in root.findall(".//payment"):
        payments.append({
            "payment_id": int(el.find("payment_id").text),
            "member_id": int(el.find("member_id").text),
            "plan_id": int(el.find("plan_id").text),
            "amount": int(el.find("amount").text),
            "payment_date": el.find("payment_date").text,
            "payment_method": el.find("payment_method").text
        })
    with open(os.path.join(output_dir, "payments.json"), "w", encoding="utf-8") as f:
        json.dump(payments, f, ensure_ascii=False, indent=2)

    print(f"✅ Все JSON-файлы созданы в папке: {output_dir}")

def test_import():
    print("Проверка импорта данных из XML...")

    xml_file = "test_data.xml"
    if not os.path.exists(xml_file):
        print(f"Ошибка: Файл {xml_file} не найден")
        return False

    try:
        init_data_from_xml(xml_file)
        print("Импорт успешно выполнен")
    except Exception as e:
        print(f"Ошибка при импорте: {e}")
        return False
    
    # Проверяем созданные JSON-файлы
    data_dir = "data"
    expected_files = [
        "members.json",
        "coaches.json", 
        "gym_rooms.json",
        "group_classes.json",
        "membership_plans.json",
        "payments.json"
    ]
    
    for file_name in expected_files:
        file_path = os.path.join(data_dir, file_name)
        if not os.path.exists(file_path):
            print(f"Ошибка: Файл {file_name} не был создан")
            return False
            
        # Проверяем, что файл содержит корректный JSON
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            print(f"✓ {file_name}: OK ({len(data)} записей)")
        except Exception as e:
            print(f"Ошибка в файле {file_name}: {e}")
            return False
    
    print("\nВсе тесты пройдены успешно!")
    return True

if __name__ == "__main__":
    XML_FILE = "test_data.xml"
    init_data_from_xml(XML_FILE)