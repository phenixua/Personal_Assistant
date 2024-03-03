import json, os, re
from datetime import datetime
from collections import UserDict


class Field:
    def __init__(self, value):
        self.value = value

class Phone(Field):
    def __init__(self, value):
        if not self.validate_phone(value):
            raise ValueError("Invalid phone number")
        super().__init__(value)

    @staticmethod
    def validate_phone(value):
        # Check the format +38-000-0000000 or +380000000000
        if re.match(r'^\+\d{2}-\d{3}-\d{7}$', value) or re.match(r'^\+\d{12}$', value):
            return True
        # Check the format 000-0000000 or 0000000000
        if re.match(r'^\d{3}-\d{7}$', value) or re.match(r'^\d{10}$', value):
            return True
        return False

    def __str__(self):
        return self.value

class Email(Field):
    def __init__(self, value):
        if not self.validate_email(value):
            raise ValueError("Invalid email")
        super().__init__(value)

    @staticmethod
    def validate_email(value):
        email_pattern = re.compile(r'^[\w\.-]+@[\w\.-]+(\.\w+)+$')
        return bool(email_pattern.match(value))

    def __str__(self):
        return self.value

class Name(Field):
    def __str__(self):
        return self.value

class Address(Field):
    def __str__(self):
        return self.value

class Birthday(Field):
    def __init__(self, value):
        if not self.validate_birthday(value):
            raise ValueError("Invalid birthday")
        super().__init__(value)

    @staticmethod
    def validate_birthday(value):
        return isinstance(value, datetime) and value <= datetime.now()

    def __str__(self):
        return self.value.strftime('%Y-%m-%d')

class Record:
    def __init__(self, name: Name, address: Address, phones: list, emails: list=None, birthday: Birthday=None):
        self.name = str(name)
        self.address = str(address)
        self.phones = self.process_phones(phones)
        self.emails = [str(email) for email in emails] if emails else []
        self.birthday = birthday

    def process_phones(self, phones):
        processed_phones = []
        for phone_field in phones:
            phone = str(phone_field)
            phone_numbers = re.split(r'[,\s]+', phone)
            for phone_number in phone_numbers:
                if Phone.validate_phone(phone_number):
                    processed_phones.append(str(Phone(phone_number)))
                else:
                    raise ValueError(f"Error: Invalid phone number: {phone_number}")
        return processed_phones

    def add_phone(self, phone):
        try:
            phone_number = Phone(phone)
            self.phones.append(phone_number)
            print(f"Phone number {phone} added for {self.name}")
            self.update_record_phones()
        except ValueError as e:
            print(f"Error: {e}")

    def delete_phone(self, phone):
        new_phones = [p for p in self.phones if p.value != phone]
        self.phones = new_phones

    def edit_phone(self, old_phone, new_phone):
        old_phone_found = False
        for i, phone in enumerate(self.phones):
            if phone == old_phone:
                old_phone_found = True
                try:
                    self.phones[i] = new_phone
                    print(f"Phone number updated for {self.name}")
                    print(f"Old phone number: {old_phone}")
                    print(f"New phone number: {new_phone}")
                except ValueError as e:
                    print(f"Error: {e}")
                    print("Please enter a valid phone number.")
                break

        if not old_phone_found:
            print(f"Error: Old phone number {old_phone} not found in {self.name}'s record.")

    def update_record_phones(self):
        self.phones = [str(phone) for phone in self.phones]

    def days_to_birthday(self):
        if not self.birthday:
            return None

        today = datetime.now().date()
        next_birthday = datetime(today.year, self.birthday.value.month, self.birthday.value.day).date()

        if today > next_birthday:
            next_birthday = datetime(today.year + 1, self.birthday.value.month, self.birthday.value.day).date()

        days_left = (next_birthday - today).days
        return days_left

    def __str__(self):
        result = f"Name: {self.name}\n"
        result += f"Address: {self.address}\n"
        result += f"Phones: {', '.join(self.phones)}\n"
        result += f"Emails: {', '.join(self.emails)}\n"
        if self.birthday:
            result += f"Birthday: {self.birthday}\n"
        result += "-" * 30
        return result

class AddressBook(UserDict):
    def add_record(self, record: Record):
        self.data[record.name] = record

    def iterator(self):
        return self.data.values()

    def save_to_file(self, filename):
        if filename == "":
            filename = "addressbook.json"
        with open(filename, "w", encoding = "UTF-8") as file:
            data = {
                "records": [record.__dict__ for record in self.values()]
            }
            # Serialize birthdays to strings
            for record_data in data["records"]:
                if record_data["birthday"]:
                    record_data["birthday"] = record_data["birthday"].value.strftime('%Y-%m-%d')
            json.dump(data, file, ensure_ascii = False, indent = 4)

    @classmethod
    def load_from_file(cls, filename):
        if filename == "":
            filename = "addressbook.json"
        if os.path.exists(filename):
            try:
                with open(filename, "r", encoding = "UTF-8") as file:
                    data = json.load(file)
                    book = cls()
                    for record_data in data["records"]:
                        name = Name(record_data["name"])
                        address = Address(record_data["address"])
                        phones = [Phone(phone) for phone in record_data["phones"]]
                        emails = [Email(email) for email in record_data["emails"]]
                        birthday = Birthday(datetime.strptime(record_data["birthday"], "%Y-%m-%d")) if record_data["birthday"] else None
                        record = Record(name, address, phones, emails, birthday)
                        book.add_record(record)
                    return book
            except FileNotFoundError:
                return cls()
        else:
            return cls()

    def search_records(self, query):
        query = query.lower()
        found_records = []
        found_record_names = set()

        for record in self.data.values():
            if query in record.name.lower() and record.name not in found_record_names:
                found_records.append(record)
                found_record_names.add(record.name)

            for phone in record.phones:
                if query in phone.lower() and record.name not in found_record_names:
                    found_records.append(record)
                    found_record_names.add(record.name)

            for email in record.emails:
                if query in email.lower():
                    found_records.append(record)
                    break
            found_records = list(set(found_records))

        return found_records

    def get_upcoming_birthday_contacts(self, days):
        today = datetime.now().date()
        upcoming_birthday_contacts = []

        for record in self.data.values():
            if record.birthday:
                if isinstance(record.birthday, str):
                    # If birthday is loaded as a string, parse it
                    record.birthday = Birthday(datetime.strptime(record.birthday, "%Y-%m-%d"))

                next_birthday = datetime(today.year, record.birthday.value.month, record.birthday.value.day).date()
                if today > next_birthday:
                    next_birthday = datetime(today.year + 1, record.birthday.value.month, record.birthday.value.day).date()
                days_left = (next_birthday - today).days

                if days_left <= days:
                    upcoming_birthday_contacts.append(record)

        return upcoming_birthday_contacts


if __name__ == "__main__":
    book = AddressBook()