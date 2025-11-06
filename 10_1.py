from collections import UserDict
from datetime import datetime, timedelta


# Батьківський клас
class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    pass


class Phone(Field):
    def __init__(self, value):
        if not value.isdigit() or len(value) != 10:
            raise ValueError("Phone must contain exactly 10 digits")
        super().__init__(value)


class Birthday(Field):
    def __init__(self, value):
        try:
            self.date = datetime.strptime(value, "%d.%m.%Y")
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")
        super().__init__(value)


# Клас запису та його функції 
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

    def remove_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                self.phones.remove(p)
                return
        print("Phone not found")

    def edit_phone(self, old, new):
        for p in self.phones:
            if p.value == old:
                try:
                    p.value = Phone(new).value
                except ValueError as e:
                    print(e)
                return
        print("Phone not found")

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    def add_birthday(self, date):
        try:
            self.birthday = Birthday(date)
        except ValueError as e:
            print(e)

    def __str__(self):
        phones = "; ".join(p.value for p in self.phones)
        b = self.birthday.value if self.birthday else "—"
        return f"Contact name: {self.name.value}, phones: {phones}, birthday: {b}"


# Адресна книга та її функції 
class AddressBook(UserDict):

    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]

    def get_upcoming_birthdays(self):
        today = datetime.today()
        next_week = today + timedelta(days=7)

        result = []

        for rec in self.data.values():
            if rec.birthday is None:
                continue

            bday = rec.birthday.date.replace(year=today.year)

            if today <= bday <= next_week:
                result.append({"name": rec.name.value, "birthday": bday.strftime("%d.%m.%Y")})

        return result



book = AddressBook()


def main():
    print("Simple bot start. Type help")

    while True:
        cmd = input(">>> ").strip().lower()

        if cmd in ("exit", "close"):
            print("Bye!")
            break

        parts = cmd.split()

        if not parts:
            continue


        # add name phone
        if parts[0] == "add":
            if len(parts) < 3:
                print("Usage: add <name> <phone>")
                continue
            name = parts[1]
            phone = parts[2]

            rec = book.find(name)
            if rec:
                rec.add_phone(phone)
            else:
                rec = Record(name)
                rec.add_phone(phone)
                book.add_record(rec)
            print("ok")

        # show name
        elif parts[0] == "show":
            if len(parts) < 2:
                print("Usage: show <name>")
                continue
            rec = book.find(parts[1])
            if rec:
                print(rec)
            else:
                print("not found")

        # add-birthday name date
        elif parts[0] == "add-birthday":
            if len(parts) < 3:
                print("Usage: add-birthday <name> <DD.MM.YYYY>")
                continue

            name = parts[1]
            date = parts[2]

            rec = book.find(name)
            if not rec:
                print("Contact not found")
            else:
                rec.add_birthday(date)
                print("birthday added")

        # show-birthday name
        elif parts[0] == "show-birthday":
            if len(parts) < 2:
                print("Usage: show-birthday <name>")
                continue
            rec = book.find(parts[1])
            if rec and rec.birthday:
                print(rec.birthday)
            else:
                print("birthday not set")

        # birthdays
        elif parts[0] == "birthdays":
            res = book.get_upcoming_birthdays()
            for item in res:
                print(f"{item['name']} – {item['birthday']}")
            if not res:
                print("No upcoming birthdays")

        else:
            print("Unknown command")


if __name__ == "__main__":
    main()
