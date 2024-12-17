from collections import UserDict
from datetime import datetime, timedelta
import calendar

class Field:
    """Базовий клас для полів запису."""
    pass

class Name(Field):
    """Клас для зберігання імені контакту."""
    def __init__(self, name):
        if not name:
            raise ValueError("Ім'я не може бути порожнім")
        self.value = name

    def __str__(self):
        return self.value

class Phone(Field):
    """Клас для зберігання номера телефону з валідацією."""
    def __init__(self, phone):
        if not phone.isdigit() or len(phone) != 10:
            raise ValueError("Номер телефону має містити 10 цифр.")
        self.value = phone

    def __str__(self):
        return self.value

class Birthday(Field):
    """Клас для зберігання дня народження з валідацією."""
    def __init__(self, value):
        try:
            self.value = datetime.strptime(value, "%d.%m.%Y").date()
        except ValueError:
            raise ValueError("Невірний формат дати. Використовуйте DD.MM.YYYY")

    def __str__(self):
        return self.value.strftime("%d.%m.%Y")

    def get_congrats_date(self, current_year):
        """Обчислює дату привітання з днем народження, враховуючи вихідні."""
        birthday_this_year = self.value.replace(year=current_year)
        # Якщо день народження вже пройшов у цьому році, беремо наступний рік
        if birthday_this_year < datetime.now().date():
            birthday_this_year = birthday_this_year.replace(year=current_year + 1)
        
        # Перевірка, чи це вихідний
        if birthday_this_year.weekday() >= 5:  # Субота або неділя
            # Переносимо на понеділок
            birthday_this_year += timedelta(days=(7 - birthday_this_year.weekday()))
        return birthday_this_year

class Record:
    """Клас для зберігання інформації про контакт."""
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_birthday(self, date):
        self.birthday = Birthday(date)
    
    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                self.phones.remove(p)
                return
        raise ValueError("Телефон не знайдено.")

    def edit_phone(self, old_phone, new_phone):
        for p in self.phones:
            if p.value == old_phone:
                p.value = Phone(new_phone).value
                return
        raise ValueError("Старий номер телефону не знайдено.")

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    def __str__(self):
        phones = ", ".join(str(phone) for phone in self.phones)
        birthday = f", День народження: {self.birthday}" if self.birthday else ""
        return f"{self.name}: {phones}{birthday}"

class AddressBook(UserDict):
    """Клас для зберігання та управління записами."""
    def add_record(self, record):
        if record.name.value in self.data:
            raise ValueError("Контакт з таким іменем вже існує.")
        self.data[record.name.value] = record

    def delete_record(self, name):
        if name not in self.data:
            raise ValueError("Контакт не знайдено.")
        del self.data[name]

    def search_record(self, name):
        return self.data.get(name, None)

    def get_upcoming_birthdays(self):
        """Повертає список контактів із днями народження, що наближаються протягом 7 днів."""
        today = datetime.now().date()
        upcoming_birthdays = []

        for record in self.data.values():
            if record.birthday:
                congrats_date = record.birthday.get_congrats_date(today.year)
                delta_days = (congrats_date - today).days

                if 0 <= delta_days <= 7:  # День народження протягом 7 днів включно
                    upcoming_birthdays.append({
                        "name": record.name.value,
                        "birthday": congrats_date.strftime("%d.%m.%Y")
                    })
        return upcoming_birthdays

    def __str__(self):
        return "\n".join(str(record) for record in self.data.values())

def main():
    book = AddressBook()

    while True:
        command = input("\nВведіть команду (add, show_all, edit_phone, remove_phone, birthday, delete, upcoming_birthdays, exit): ").strip().lower()

        if command == "add":
            name = input("Введіть ім'я: ").strip()
            phone = input("Введіть номер телефону (10 цифр, або залиште порожнім): ").strip()
            try:
                record = Record(name)
                if phone:
                    record.add_phone(phone)
                book.add_record(record)
                print(f"Контакт {name} додано.")
            except ValueError as e:
                print(f"Помилка: {e}")

        elif command == "birthday":
            name = input("Введіть ім'я: ").strip()
            date = input("Введіть день народження (DD.MM.YYYY): ").strip()
            record = book.search_record(name)
            if record:
                try:
                    record.add_birthday(date)
                    print(f"День народження {date} додано до контакту {name}.")
                except ValueError as e:
                    print(f"Помилка: {e}")
            else:
                print("Контакт не знайдено.")

        elif command == "show_all":
            print("Адресна книга:")
            print(book)

        elif command == "upcoming_birthdays":
            print("Наближаються дні народження:")
            birthdays = book.get_upcoming_birthdays()
            if birthdays:
                for b in birthdays:
                    print(f"{b['name']}: {b['birthday']}")
            else:
                print("Немає днів народження у найближчі 7 днів.")

        elif command == "exit":
            print("До побачення!")
            break

if __name__ == "__main__":
    main()
