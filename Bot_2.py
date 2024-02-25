import re
from datetime import datetime, timedelta
from collections import UserDict

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    pass

class Phone(Field):
    def __init__(self, value):
        if not re.match(r'^\d{10}$', value):
            raise ValueError("Invalid phone number format. Phone number must contain 10 digits.")
        super().__init__(value)

class Birthday(Field):
    def __init__(self, value):
        try:
            self.value = datetime.strptime(value, "%d.%m.%Y")
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        try:
            self.phones.append(Phone(phone))
        except ValueError as e:
            print(e)

    def add_birthday(self, birthday):
        try:
            self.birthday = Birthday(birthday)
        except ValueError as e:
            print(e)

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(str(p) for p in self.phones)}, birthday: {self.birthday.value if self.birthday else 'Not set'}"

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)
    
    def delete(self, name):
        if name in self.data:
            del self.data[name]

    def get_upcoming_birthdays(self):
        today = datetime.now()
        next_week = today + timedelta(days=7)
        upcoming_birthdays = []
        for record in self.data.values():
            if record.birthday and today <= record.birthday.value < next_week:
                upcoming_birthdays.append(record)
        return upcoming_birthdays

# Функція parse_input розбиває введений рядок на слова, використовуючи пробіл як розділювач
def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, args

def add_contact(args, book):
    if len(args) != 2:
        return "Invalid command. Usage: add [name] [phone]"
    
    name, phone = args
    record = Record(name)
    record.add_phone(phone)
    book.add_record(record)
    return "Contact added."

def change_contact(args, book):
    if len(args) != 2:
        return "Invalid command. Usage: change [name] [new_phone]"
    
    name, new_phone = args
    record = book.find(name)
    if record:
        record.phones = []
        record.add_phone(new_phone)
        return "Contact updated."
    else:
        return "Contact not found."

def add_birthday(args, book):
    if len(args) != 2:
        return "Invalid command. Usage: add-birthday [name] [DD.MM.YYYY]"
    
    name, birthday = args
    record = book.find(name)
    if record:
        record.add_birthday(birthday)
        return "Birthday added."
    else:
        return "Contact not found."

def show_birthday(args, book):
    if len(args) != 1:
        return "Invalid command. Usage: show-birthday [name]"
    
    name = args[0]
    record = book.find(name)
    if record and record.birthday:
        return f"{name}'s birthday is on {record.birthday.value.strftime('%d.%m.%Y')}"
    else:
        return "Contact not found or birthday not set."

def birthdays(args, book):
    upcoming_birthdays = book.get_upcoming_birthdays()
    if not upcoming_birthdays:
        return "No upcoming birthdays."
    else:
        result = "Upcoming birthdays:\n"
        for record in upcoming_birthdays:
            result += f"{record.name.value}: {record.birthday.value.strftime('%d.%m.%Y')}\n"
        return result

def show_phone(args, book):
    if len(args) != 1:
        return "Invalid command. Usage: phone [name]"
    
    name = args[0]
    record = book.find(name)
    if record:
        return '; '.join(str(phone) for phone in record.phones)
    else:
        return "Contact not found."

def show_all(book):
    if not book.data:
        return "No contacts found."
    
    for name, record in book.data.items():
        print(f"{name}: {'; '.join(str(phone) for phone in record.phones)}")
    return ""

def main():
    book = AddressBook()  # створення об'єкту адресної книги
    print("Welcome to the assistant bot!")
    
    while True:
        user_input = input("Enter a command: ")
        command, args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, book))
        elif command == "change":
            print(change_contact(args, book))
        elif command == "phone":
            print(show_phone(args, book))
        elif command == "all":
            print(show_all(book))
        elif command == "add-birthday":
            print(add_birthday(args, book))
        elif command == "show-birthday":
            print(show_birthday(args, book))
        elif command == "birthdays":
            print(birthdays(args, book))
        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()
