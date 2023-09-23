from collections import UserDict
from datetime import timedelta, datetime


class Field:
    def __init__(self, value=None):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    pass


class Birthday(Field):
    def __init__(self, value=None):
        super().__init__(value)
        self.validate_birthday()

    def validate_birthday(self):
        if self.value:
            try:
                datetime.strptime(self.value, "%Y-%m-%d")
            except ValueError:
                raise ValueError("Incorrect birthday format. Select the 'YYYY-MM-DD' format")

    def get_value(self):
        return self.value

    def set_value(self, new_value):
        self.validate_birthday()
        self.value = new_value

    value = property(get_value, set_value)


class Phone(Field):
    def __init__(self, value=None):
        super().__init__(value)
        self.validate_phone()

    def validate_phone(self):
        if self.value and (not self.value.isdigit() or len(self.value) != 10):
            raise ValueError("Phone number should consist of 10 digits.")

    def get_value(self):
        return self.value

    def set_value(self, new_value):
        self.validate_phone()
        self.value = new_value

    value = property(get_value, set_value)


class Record:
    def __init__(self, name, birthday=None):
        self.name = Name(name)
        self.birthday = Birthday(birthday)
        self.phones = []

    def add_phone(self, phone):
        phone_obj = Phone(phone)
        self.phones.append(phone_obj)

    def remove_phone(self, phone):
        for phone_obj in self.phones[:]:
            if phone_obj.value == phone:
                self.phones.remove(phone_obj)

    def edit_phone(self, old_phone, new_phone):
        validation = Phone(new_phone)
        for phone_obj in self.phones:
            if phone_obj.value == old_phone:
                phone_obj.value = new_phone
                return
        raise ValueError

    def find_phone(self, phone):
        phone_obj = Phone(phone)
        for p in self.phones:
            if p.value == phone_obj.value:
                return p
        return None

    def days_to_birthday(self):
        if self.birthday.value:
            today = datetime.today()
            next_birthday = datetime(today.year, self.birthday.value.month, self.birthday.value.day)
            if today > next_birthday:
                next_birthday = datetime(today.year + 1, self.birthday.value.month, self.birthday.value.day)
            delta = next_birthday - today
            return delta.days
        return None

    def __str__(self):
        phone_str = "; ".join(map(str, self.phones))
        return f"Name: {self.name}, Phones: {phone_str}"


class AddressBook(UserDict):
    def __init__(self):
        super().__init__()
        self.data = {}

    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]

    def iterator(self, page_size=10):
        records = list(self.data.values())
        current_page = 0
        while current_page < len(records):
            yield records[current_page:current_page + page_size]
            current_page += page_size


if __name__ == "__main__":
    address_book = AddressBook()

    while True:
        command = input("Enter a command: ").strip().lower()

        if command == "add":
            name = input("Enter name: ")
            record = Record(name)
            while True:
                phone = input("Enter phone (or leave empty to finish): ").strip()
                if not phone:
                    break
                try:
                    record.add_phone(phone)
                except ValueError as e:
                    print(e)
            address_book.add_record(record)
        elif command == "find":
            name = input("Enter name to find: ")
            record = address_book.find(name)
            if record:
                print(record)
            else:
                print("Contact not found.")
        elif command == "delete":
            name = input("Enter name to delete: ")
            address_book.delete(name)
        elif command == "exit":
            break
        else:
            print("Invalid command. Try again.")
