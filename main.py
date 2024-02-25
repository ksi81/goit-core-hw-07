import re
from datetime import datetime, timedelta
from collections import UserDict

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value) #  Повернення значення у вигляді рядка

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
            self.value = datetime.strptime(value, "%d.%m.%Y") # Перетворення рядка у формат datetime
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY") # Викидання винятку при невірному форматі дати

class Record:
    def __init__(self, name):
        self.name = Name(name) # Ім'я контакту
        self.phones = [] # Список телефонів
        self.birthday = None # День народження (за замовчуванням None)

    def add_phone(self, phone):
        try:
            self.phones.append(Phone(phone)) # Додавання телефону до списку
        except ValueError as e:
            print(e)

    def add_birthday(self, birthday):
        try:
            self.birthday = Birthday(birthday) # Додавання дня народження до контакту
        except ValueError as e:
            print(e)

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(str(p) for p in self.phones)}, birthday: {self.birthday.value if self.birthday else 'Not set'}"

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record # Додавання запису до адресної книги

    def find(self, name):
        return self.data.get(name) # Пошук запису за ім'ям
    
    def delete(self, name):
        if name in self.data:
            del self.data[name] # Видалення запису за ім'ям

    def get_upcoming_birthdays(self):
        today = datetime.now()
        next_week = today + timedelta(days=7)
        upcoming_birthdays = []
        for record in self.data.values():
            if record.birthday:
                birthday_this_year = record.birthday.value.replace(year=today.year)
                if birthday_this_year >= today and birthday_this_year < next_week:
                    upcoming_birthdays.append(record)
                elif birthday_this_year < today:  # якщо день народження вже пройшов у цьому році
                    next_birthday_this_year = record.birthday.value.replace(year=today.year + 1)
                    if next_birthday_this_year < next_week:
                        upcoming_birthdays.append(record)
        return upcoming_birthdays  #Повертає список контактів, яких потрібно привітати в найближчі дні народження


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
