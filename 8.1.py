import pickle

def save_data(book, filename="addressbook.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(book, f)

def load_data(filename="addressbook.pkl"):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook() 

def main():
    book = load_data()

from collections import UserDict
from datetime import datetime, timedelta

class Field:
    def __init__(self, value):
        self.value = value
    
    def __str__(self):
        return str(self.value)

class Name (Field):
    pass

class Phone(Field):
    def __init__(self,value):
        if not value.isdigit() or len(value) != 10:
            raise ValueError
        super().__init__(value)

class Birthday(Field):
    def __init__(self,value):
        try:
            datetime.strptime(value, "%d.%m.%Y")
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")
        super().__init__(value)

class Record:
    def __init__(self,name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def show_all(contacts):
        return contacts

    def add_phone(self, phone_number):
        phone = Phone(phone_number)
        self.phones.append(phone)
    
    def remove_phone(self,phone_number):
        self.phones = [p for p in self.phones if str(p) != phone_number]

    def edit_phone(self, old_phone_number, new_phone_number):
        self.remove_phone(old_phone_number)
        self.add_phone(new_phone_number)

    def find_phone(self,phone_number):
        return phone_number if phone_number in [str(p) for p in self.phones] else None

    def add_birthday(self, value):
        self.birthday = Birthday(value)
  
    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(str(p) for p in self.phones)}"

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record
    
    def find(self, name):
        return self.data.get(name, None)
    
    def delete(self,name):
        del self.data[name]

def add_birthday(args, book):
    name, birthday = args
    record = book.find(name)
    if record:
        record.add_birthday(birthday)
        return "Birthday added/updated."
    else:
        return "Contact not found."

def show_birthday(args, book):
    name = args[0]
    record = book.find(name)
    if record and record.birthday:
        return f"{name}'s birthday: {record.birthday}"
    else:
        return "Birthday not found."

def birthdays(args, book):
    today = datetime.today()
    next_week = today + datetime.timedelta(days=7)
    upcoming_birthdays = []
    for record in book.values():
        if record.birthday:
            birthday_date = datetime.datetime.strptime(record.birthday.value, "%d.%m.%Y").date()
            if today <= birthday_date < next_week:
                upcoming_birthdays.append((record.name.value, record.birthday.value))
    if not upcoming_birthdays:
        return "No upcoming birthdays."
    else:
        return "\n".join(f"{name}: {birthday}" for name, birthday in upcoming_birthdays)

def add_contact(args, book):
    try:
        name, phone = args
        book[name] = phone
        return "Contact added."
    except:
        return "Not all details"

def change_contact(args, book):
    try:
        name, phone = args
        
        if name in book:
            book[name] = phone
            return "Contact updated."
        else:
            return "Contact not founded"
    except:
        return "Not all details"
    
def show_phone(args, book):
    try:
        name = args[0]

        if name in book:
            return book[name]
        else: 
           return "Contact not founded" 
    except:
        return "Not all details"

def show_all(book):
    return book

def main():
    book = AddressBook()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = user_input.split()

        if command in ["close", "exit"]:
            print("Good bye!")
            save_data(book)
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

