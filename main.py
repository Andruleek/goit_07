from collections import UserDict

class Field:
    def __init__(self, value):
        self.value = value

class Name(Field):
    def __init__(self, value):
        if not value:
            raise ValueError("Name cannot be empty.")
        super().__init__(value)

class Phone(Field):
    def __init__(self, value):
        if not value.isdigit() or len(value) != 10:
            raise ValueError("Phone number must be 10 digits.")
        super().__init__(value)

class Birthday(Field):
    def __init__(self, value):
        if not value:
            self.value = None
        else:
            try:
                year, month, day = map(int, value.split('-'))
                if not (1 <= month <= 12) or not (1 <= day <= 31):
                    raise ValueError("Invalid date format.")
                self.value = value
            except ValueError:
                raise ValueError("Invalid date format. Use 'YYYY-MM-DD'")

class Record:
    def __init__(self, name: Name, birthday: Birthday = None):
        self.name = name
        self.phones = []
        self.birthday = birthday

    def add_phone(self, phone: Phone):
        self.phones.append(phone)

    def remove_phone(self, phone_value: str):
        phone = self.find_phone(phone_value)
        if phone:
            self.phones.remove(phone)
        else:
            raise ValueError(f"Phone {phone_value} not found.")

    def edit_phone(self, old_value: str, new_value: str):
        old_phone = self.find_phone(old_value)
        if old_phone:
            self.phones.remove(old_phone)
            self.phones.append(Phone(new_value))
        else:
            raise ValueError(f"Phone {old_value} not found.")

    def find_phone(self, phone_value: str):
        for phone in self.phones:
            if phone.value == phone_value:
                return phone
        return None

    def __str__(self):
        phones = ", ".join(phone.value for phone in self.phones)
        birthday = f" Birthday: {self.birthday.value}" if self.birthday and self.birthday.value else ""
        return f"{self.name.value}: {phones}{birthday}"

class AddressBook(UserDict):
    def add_record(self, record: Record):
        self.data[record.name.value] = record

    def find(self, name: str):
        return self.data.get(name)

    def delete(self, name: str):
        if name in self.data:
            del self.data[name]
        else:
            raise KeyError(f"Contact {name} not found.")

    def __str__(self):
        return "\n".join(str(record) for record in self.data.values())

def add_contact(args, address_book):
    if len(args) < 2 or len(args) > 3:
        raise ValueError("Invalid input. Expected: add <name> <phone> [<birthday>]")

    name, phone = args[:2]
    birthday = args[2] if len(args) == 3 else None

    record = address_book.find(name)
    if record:
        record.add_phone(Phone(phone))
    else:
        record = Record(Name(name), Birthday(birthday) if birthday else None)
        record.add_phone(Phone(phone))
        address_book.add_record(record)

    return f"Contact {name} added/updated."

def change_contact(args, address_book):
    if len(args) != 3:
        raise ValueError("Invalid input. Expected: change <name> <old_phone> <new_phone>")
    name, old_phone, new_phone = args
    record = address_book.find(name)
    if not record:
        raise KeyError(f"Contact {name} not found.")
    record.edit_phone(old_phone, new_phone)
    return f"Contact {name} updated."

def show_phone(args, address_book):
    if len(args) != 1:
        raise ValueError("Invalid input. Expected: phone <name>")
    name = args[0]
    record = address_book.find(name)
    if not record:
        raise KeyError(f"Contact {name} not found.")
    return str(record)

def show_all(address_book):
    return str(address_book) if address_book.data else "No contacts found."

def add_birthday(args, address_book):
    if len(args) != 2:
        raise ValueError("Invalid input. Expected: add_birthday <name> <birthday>")
    name, birthday_str = args
    try:
        birthday = Birthday(birthday_str)
    except ValueError as e:
        raise ValueError(f"Invalid birthday format: {e}")

    record = address_book.find(name)
    if record:
        record.birthday = birthday
        return f"Birthday for {name} added/updated."
    else:
        return f"Contact {name} not found."

def parse_input(user_input):
    parts = user_input.split()
    cmd = parts[0].strip().lower()
    args = parts[1:]
    return cmd, args

def main():
    address_book = AddressBook()
    while True:
        user_input = input("\nEnter a command: ").strip()
        command, args = parse_input(user_input)

        try:
            if command in ["close", "exit"]:
                print("Good bye!")
                break
            elif command == "hello":
                print("How can I help you?")
            elif command == "add":
                print(add_contact(args, address_book))
            elif command == "change":
                print(change_contact(args, address_book))
            elif command == "phone":
                print(show_phone(args, address_book))
            elif command == "all":
                print(show_all(address_book))
            elif command == "remove_phone":
                if len(args) != 2:
                    raise ValueError("Invalid input. Expected: remove_phone <name> <phone>")
                contact_name, phone_number = args
                record = address_book.find(contact_name)
                if record:
                    record.remove_phone(phone_number)
                    print(f"Phone number {phone_number} removed from contact {contact_name}.")
                else:
                    print(f"Contact {contact_name} not found.")
            elif command == "find_phone":
                if len(args) != 1:
                    raise ValueError("Invalid input. Expected: find_phone <phone>")
                phone_number = args[0]
                found = False
                for contact_name, contact in address_book.items():
                    if contact.find_phone(phone_number):
                        print(f"Phone number {phone_number} belongs to contact {contact_name}.")
                        found = True
                        break
                if not found:
                    print(f"Phone number {phone_number} not found.")
            elif command == "add_birthday":
                print(add_birthday(args, address_book))
            else:
                print("Invalid command. Type 'hello' for assistance.")
        except ValueError as ve:
            print(f"ValueError: {ve}")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
    