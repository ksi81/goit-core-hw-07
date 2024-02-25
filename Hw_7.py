def main():
    book = AddressBook()  # Створення нової адресної книги
    print("Ласкаво просимо до бота-асистента!")
    while True:
        user_input = input("Введіть команду: ")
        command, *args = parse_input(user_input)  # Розбиває введений рядок на команду та аргументи

        if command in ["close", "exit"]:  # Перевірка чи користувач ввів команду закриття
            print("До побачення!")
            break

        elif command == "hello":  # Вивід привітання користувачу
            print("Як я можу вам допомогти?")

        elif command == "add":
            # реалізація додавання нового контакту
            if len(args) != 2:
                print("Невірна команда. Використання: add [ім'я] [телефон]")
            else:
                name, phone = args
                try:
                    record = Record(name)
                    record.add_phone(phone)
                    book.add_record(record)
                    print("Контакт додано.")
                except ValueError as e:
                    print(str(e))

        elif command == "change":
            # реалізація зміни контакту
            if len(args) != 2:
                print("Невірна команда. Використання: change [ім'я] [новий_телефон]")
            else:
                name, new_phone = args
                try:
                    record = book.find(name)
                    if record:
                        record.edit_phone(record.phones[0].value, new_phone)
                        print("Контакт оновлено.")
                    else:
                        print("Контакт не знайдено.")
                except ValueError as e:
                    print(str(e))

        elif command == "phone":
            # реалізація відображення телефонного номеру для вказаного контакту
            if len(args) != 1:
                print("Невірна команда. Використання: phone [ім'я]")
            else:
                name = args[0]
                record = book.find(name)
                if record:
                    print(record.phones[0].value)
                else:
                    print("Контакт не знайдено.")

        elif command == "all":
            # реалізація відображення всіх контактів в адресній книзі
            if not book.data:
                print("Контакти не знайдено.")
            else:
                for record in book.data.values():
                    print(f"Ім'я контакту: {record.name.value}, телефон: {record.phones[0].value}")

        elif command == "add-birthday":
            # реалізація додавання дня народження для вказаного контакту
            if len(args) != 2:
                print("Невірна команда. Використання: add-birthday [ім'я] [DD.MM.YYYY]")
            else:
                name, birthday = args
                try:
                    record = book.find(name)
                    if record:
                        record.add_birthday(birthday)
                        print("День народження додано.")
                    else:
                        print("Контакт не знайдено.")
                except ValueError as e:
                    print(str(e))

        elif command == "show-birthday":
            # реалізація відображення дня народження для вказаного контакту
            if len(args) != 1:
                print("Невірна команда. Використання: show-birthday [ім'я]")
            else:
                name = args[0]
                record = book.find(name)
                if record and record.birthday:
                    print(f"День народження {name}: {record.birthday.value.strftime('%d.%m.%Y')}")
                else:
                    print("День народження не знайдено.")

        elif command == "birthdays":
            # реалізація відображення майбутніх днів народження
            upcoming_birthdays = book.get_upcoming_birthdays()
            if not upcoming_birthdays:
                print("Майбутні дні народження не знайдено.")
            else:
                print("Майбутні дні народження:")
                for record in upcoming_birthdays:
                    print(f"День народження {record.name.value}: {record.birthday.value.strftime('%d.%m.%Y')}")

        else:
            print("Невірна команда.")

if __name__ == "__main__":
    main()
