import os, subprocess, sys
from colorama import Fore, Style
from datetime import datetime, timedelta
from prettytable import PrettyTable
from config_addressbook import Address, AddressBook, Birthday, Email, Name, Phone, Record
from config_notes import NoteManager
import main_cleaner as folder_cleaner
import main_minicalc

def clear_screen():
    if os.name == 'posix':
        os.system('clear')
    elif os.name == 'nt':
        os.system('cls')


# SECTION BASE MENU
def main_menu():
    while True:
        clear_screen()
        menu = PrettyTable()
        menu.field_names = [Fore.RED + "Option", Fore.RED + "Description"]

        
        menu.add_row(["1", "Contacts"])
        menu.add_row(["2", "Notes"])
        menu.add_row(["3", "Sorting files"])
        menu.add_row(["4", "Mini Calculator"])
        menu.add_row(["5", "Game BanderoGoose"])
        menu.add_row(["6", "Quit"])
        
        
        print(Fore.RED + "Welcome to your Personal Assistant!")
        print(menu)
        print(Style.RESET_ALL)

        choice = input(Fore.YELLOW +"Select an option [1 / 2 / 3 / 4 / 5 / 6]: " + Style.RESET_ALL)

        if choice == "1":
            contacts_menu()
        elif choice == "2":
            notes_menu()
        elif choice == "3":
            files_menu()
        elif choice == "4":
            clear_screen()
            main_minicalc.main()
            input("Press Enter to continue.")
        elif choice == "5":
            try:
                dir_goose = os.path.dirname(os.path.abspath(__file__))
                goose = os.path.join(dir_goose, "main_banderogoose.py")
                subprocess.run(["python", goose], check = True)
            except subprocess.CalledProcessError:
                input(f"An error occurred while executing the script {goose}.")                
        elif choice == "6":
            sys.exit()
        else:
            input("Incorrect choice. Press Enter to continue.")


# SECTION OF CONTACTS
def contacts_menu():
    book = AddressBook()

    while True:
        clear_screen()
        menu = PrettyTable()
        menu.field_names = [Fore.BLUE + "Option", Fore.BLUE + "Description"]

        menu.add_row(["1", "Add a Contact"])
        menu.add_row(["2", "Edit a Contact"])
        menu.add_row(["3", "Delete a Contact"])
        menu.add_row(["4", "List All Contacts"])
        menu.add_row(["5", "Save Address Book"])
        menu.add_row(["6", "Load Address Book"])
        menu.add_row(["7", "Search Contacts"])
        menu.add_row(["8", "View Upcoming Birthdays"])
        menu.add_row(["9", "Exit"])

        print(Fore.BLUE + "Address Book Menu:")
        print(menu)

        choice = input(Fore.YELLOW + "Enter your choice (1/2/3/4/5/6/7/8/9): " + Style.RESET_ALL)

        if choice == "1":
            clear_screen()
            while True:
                print("Enter contact details (or enter '0' to exit):")
                name = input("Enter the contact's name: ")
                if name == '0':
                    break

                address = input("Enter the contact's address: ")
                if address == '0':
                    break

                phone = input("Enter the contact's phone number: ")
                if phone == '0':
                    break

                email = input("Enter the contact's email address: ")
                if email == '0':
                    break

                birthday = input("Enter the contact's birthday (YYYY-MM-DD): ")
                if birthday == '0':
                    break

                if name and address and phone and email and birthday:
                    try:
                        name_field = Name(name)
                        address_field = Address(address)
                        phone_field = Phone(phone)
                        email_field = Email(email)
                        birthday_field = Birthday(datetime.strptime(birthday, "%Y-%m-%d"))
                        record = Record(name_field, address_field, [phone_field], [email_field], birthday_field)
                        book.add_record(record)
                        # print(f"Contact {name} added successfully!")
                        input(f"Contact {name} added successfully!\nPress [Enter] to continue.")
                        break
                    except ValueError as e:
                        print(f"Error: {e}")
                        # print("Please enter valid data.")
                        input("Please enter valid data.\nPress [Enter] to continue.")
                else:
                    # print("All fields are required. Please try again or enter '0' to cancel.\nPress [Enter] to continue.")
                    input("All fields are required. Please try again or enter '0' to cancel.\nPress [Enter] to continue.")

        elif choice == "2":
            clear_screen()
            name = input("Enter the contact's name to edit: ")
            if name in book.data:
                record = book.data[name]
                print(f"Editing Contact: {record.name}")
                print("1. Edit Name")
                print("2. Edit Address")
                print("3. Edit Phone")
                print("4. Edit Email")
                print("5. Edit Birthday")
                edit_choice = input("Enter your choice (1/2/3/4/5): ")

                if edit_choice == "1":
                    while True:
                        new_name = input("Enter the new name: ")
                        try:
                            record.name = new_name
                            # print(f"Contact {name} name updated to {new_name}")
                            input(f"Contact {name} name updated to {new_name}.\nPress [Enter] to continue.")
                            break
                        except ValueError as e:
                            print(f"Error: {e}")
                            # print("Please enter a valid name.")
                            input("Please enter a valid name.\nPress [Enter] to continue.")

                elif edit_choice == "2":
                    while True:
                        new_address = input("Enter the new address: ")
                        try:
                            record.address = new_address
                            # print(f"Address updated for {record.name}.")
                            input(f"Address updated for {record.name}.\nPress [Enter] to continue.")
                            break
                        except ValueError as e:
                            print(f"Error: {e}")
                            # print("Please enter a valid address.")
                            input("Please enter a valid address.\nPress [Enter] to continue.")

                # elif edit_choice == "3":
                #     old_phone = input("Enter the old phone number: ")
                #     while True:
                #         new_phone = input("Enter the new phone number: ")
                #         try:
                #             record.edit_phone(old_phone, new_phone)
                #             # print(f"Phone number updated for {record.name}")
                #             input(f"Phone number updated for {record.name}.\nPress [Enter] to continue.")
                #             break
                #         except ValueError as e:
                #             print(f"Error: {e}")
                #             # print("Please enter a valid phone number.")
                #             input("Please enter a valid phone number.\nPress [Enter] to continue.")

                elif edit_choice == "3":
                    action = input("Enter [1] to edit an existing phone number or [2] to add a new one: ")
                    if action == "1":
                        old_phone = input("Enter the old phone number: ")
                        new_phone = input("Enter the new phone number: ")
                        try:
                            record.edit_phone(old_phone, new_phone)
                            input(f"Phone number updated for {record.name}.\nPress [Enter] to continue.")
                        except ValueError as e:
                            print(f"Error: {e}")
                            input("Please enter a valid phone number.\nPress [Enter] to continue.")
                    elif action == "2":
                        new_phone = input("Enter the new phone number: ")
                        record.add_phone(new_phone)
                        input(f"Phone number added for {record.name}.\nPress [Enter] to continue.")

                elif edit_choice == "4":
                    while True:
                        new_email = input("Enter the new email address: ")
                        try:
                            record.emails[0] = new_email
                            # print(f"Email address updated for {record.name}")
                            input(f"Email address updated for {record.name}.\nPress [Enter] to continue.")
                            break
                        except ValueError as e:
                            print(f"Error: {e}")
                            # print("Please enter a valid email address.")
                            input("Please enter a valid email address.\nPress [Enter] to continue.")

                elif edit_choice == "5":
                    while True:
                        new_birthday = input("Enter the new birthday (YYYY-MM-DD): ")
                        try:
                            record.birthday = Birthday(datetime.strptime(new_birthday, "%Y-%m-%d"))
                            # print(f"Birthday updated for {record.name}")
                            input(f"Birthday updated for {record.name}.\nPress [Enter] to continue.")
                            break
                        except ValueError as e:
                            print(f"Error: {e}")
                            # print("Please enter a valid birthday (YYYY-MM-DD).")
                            input("Please enter a valid birthday (YYYY-MM-DD).\nPress [Enter] to continue.")

        elif choice == "3":
            clear_screen()
            name = input("Enter the contact's name to delete: ")
            if name in book.data:
                del book.data[name]
                # print(f"Contact {name} deleted successfully!")
                input(f"Contact {name} deleted successfully!\nPress [Enter] to continue.")

        elif choice == "4":
            clear_screen()
            print("List of All Contacts:")
            if book.data:
                for record in book.data.values():
                    print(record)
                    print("-" * 30)
            input("Press [Enter] to continue.")

        elif choice == "5":
            clear_screen()
            filename = input("Enter the filename to save the address book (addressbook.json): ")
            book.save_to_file(filename)
            # print(f"Address book saved to {filename} successfully!")
            input(f"Address book saved to {filename} successfully!")

        elif choice == "6":
            clear_screen()
            filename = input("Enter the filename to load the address book from (addressbook.json): ")
            book = AddressBook.load_from_file(filename)
            # print(f"Address book loaded from {filename} successfully!\nPress [Enter] to continue.")
            input(f"Address book loaded from {filename} successfully!\nPress [Enter] to continue.")

        elif choice == "7":
            clear_screen()
            query = input("Enter a search query: ")
            found_records = book.search_records(query)
            if found_records:
                print("Search Results:")
                for record in found_records:
                    print(record)
                    print("-" * 30)
                input("Press [Enter] to continue.")
            else:
                # print("No matching records found.")
                input("No matching records found.\nPress [Enter] to continue.")

        elif choice == "8":
            clear_screen()
            days = int(input("Enter the number of days for upcoming birthdays: "))
            upcoming_birthday_contacts = book.get_upcoming_birthday_contacts(days)
            if upcoming_birthday_contacts:
                print(f"Upcoming Birthdays in {days} days:")
                for record in upcoming_birthday_contacts:
                    print(record)
                    print("-" * 30)
                input("Press [Enter] to continue.")
            else:
                # print("No upcoming birthdays found.")
                input("No upcoming birthdays found.\nPress [Enter] to continue.")

        elif choice == "9":
            print("Exiting the Address Book program. Goodbye!")
            break

        else:
            # print("Invalid choice. Please enter a valid choice (1/2/3/4/5/6/7/8/9).")
            input("Invalid choice. Please enter a valid choice (1/2/3/4/5/6/7/8/9).")


# SECTION OF NOTES
def notes_menu():
    note_manager = NoteManager("notes.json")

    while True:
        clear_screen()
        menu = PrettyTable()
        menu.field_names = [Fore.GREEN + "Option", Fore.GREEN + "Description"]

        menu.add_row(["1", "Add a note"])
        menu.add_row(["2", "Edit note"])
        menu.add_row(["3", "Delete note"])
        menu.add_row(["4", "Search notes"])
        menu.add_row(["5", "Sort notes by tags"])
        menu.add_row(["6", "Show all notes"])
        menu.add_row(["7", "Delete all notes"])
        menu.add_row(["8", "Exit"])

        print(Fore.GREEN + "Notes Menu:")
        print(menu)

        choice = input(Fore.YELLOW + "Enter your choice (1/2/3/4/5/6/7/8): " + Style.RESET_ALL)

        # choice = input("Оберіть опцію (1/2/3/4/5/6/7/8): ")

        if choice == "1":
            add_note(note_manager)
        elif choice == "2":
            edit_note(note_manager)
        elif choice == "3":
            delete_note(note_manager)
        elif choice == "4":
            search_notes(note_manager)
        elif choice == "5":
            clear_screen()
            tags_input = input("Enter tags (separated by commas) to sort by: ")
            tags = [tag.strip() for tag in tags_input.split(',')]
            sort_notes_by_tags(note_manager, tags)
        elif choice == "6":
            show_all_notes(note_manager)
        elif choice == "7":
            clear_all_notes(note_manager)
        elif choice == "8":
            return
        else:
            input("Incorrect choice.\nPress [Enter] to continue.")

def add_note(note_manager):
    clear_screen()
    print("Try to Add a note.")
    title = input("Title: ")
    body = input("Body of note: ")
    if not body:
        input("The field [Body of note] cannot be empty.\nPress [Enter] to continue.")
        return
    tags = input("Tags (separated comma): ").strip().split(',')

    note_manager.add_note(title, body, tags)
    input("Note successfully added.\nPress [Enter] to continue.")

def edit_note(note_manager):
    clear_screen()
    print("Try to Edit a note.")
    title = input("Enter the title of the note to edit: ")

    if not title:
        input("You have not entered anything, please try again.\nPress [Enter] to continue.")
        return
    
    note = note_manager.search_notes(title)

    if note:
        note = note[0]

        print("Current data:")
        print(f"Title: {note['title']}")
        print(f"Body of note: {note['body']}")
        print(f"Tags: {', '.join(note['tags'])}")

        new_title = input("New Title (or Enter to save the current one): ")
        new_body = input("New Body of note (or Enter to save the current one): ")
        new_tags = input("New Tags (separated comma) (or Enter to save current): ").strip().split(',')

        note_manager.edit_note(title, new_title, new_body, new_tags)
        input("Note edited successfully.\nPress [Enter] to continue.")
    else:
        input("Note with this [Title] was not found.\nPress [Enter] to continue.")

def delete_note(note_manager):
    clear_screen()
    print("Try to Delete a note.")
    title = input("Enter the [Title] of the note to delete: ")
    if not title:
        input("The field [Title] cannot be empty.\nPress [Enter] to continue.")
        return
    notes = note_manager.search_notes(title)

    if notes:
        note = notes[0]
        print("Current data:")
        print(f"Title: {note['title']}")
        print(f"Body of note: {note['body']}")
        print(f"Tags: {', '.join(note['tags'])}")

        confirmation = input(f"Are you sure you want to delete the note \"{note['title']}\"? (Y/N): ")
        if confirmation.lower() == "y":
            note_manager.delete_note(note['title'])
            input("Note deleted successfully.\nPress [Enter] to continue.")
        elif confirmation.lower() == "n":
            input("Note deletion cancelled.\nPress [Enter] to continue.")
    else:
        input("Note with this [Title] was not found.\nPress [Enter] to continue.")

def search_notes(note_manager):
    clear_screen()
    print("Try to Search notes.")
    query = input("Enter a search query [Title] or [Tags]: ")

    if not query:
        input("You have not entered anything, please try again.\nPress [Enter] to continue.")
        return
    
    results = note_manager.search_notes(query)

    if results:
        print("Search Results:")
        for i, note in enumerate(results, start=1):
            print(f"{i}.\tTitle: {note['title']}")
            print(f"\tBody of note: {note['body']}")
            print(f"\tTags: {', '.join(note['tags'])}")

        input("Press [Enter] to continue.")
    else:
        input("No notes found by Your request.\nPress [Enter] to continue.")

def sort_notes_by_tags(note_manager, tags):
    # clear_screen()
    print("Try to Sort notes by tags.")

    if not tags:
        input("You have not entered any [Tags].\nPress [Enter] to continue.")
        return
    
    sorted_notes = []
    exact_match_notes = []

    for tag in tags:
        notes = note_manager.search_notes(tag)
        if notes:
            exact_match_notes.extend(notes)

    all_notes = note_manager.show_all_notes()
    for note in all_notes:
        if note not in exact_match_notes:
            sorted_notes.append(note)

    if exact_match_notes:
        print(f"Notes with the best match of tag #{', '.join(tags)}:")
        for i, note in enumerate(exact_match_notes, start=1):
            print(f"{i}.\tTitle: {note['title']}")
            print(f"\tBody of note:: {note['body']}")
            print(f"\tTags: {', '.join(note['tags'])}")

    sorted_notes.sort(key=lambda x: ', '.join(x['tags']))
    if sorted_notes:
        print("Other notes are sorted alphabetically by [Tags]:")
        for i, note in enumerate(sorted_notes, start=1):
            print(f"{i}.\t{note['title']} - {note['body']} - #{', '.join(sorted(note['tags']))}")

    input("Press [Enter] to continue.")

def show_all_notes(note_manager):
    clear_screen()
    print("All notes:")
    all_notes = note_manager.show_all_notes()

    if all_notes:
        for i, note in enumerate(all_notes, start=1):
            print(f"{i}.\tTitle: {note['title']}")
            print(f"\tBody of note: {note['body']}")
            print(f"\tTags: {', '.join(note['tags'])}")
    else:
        print("The notes list is empty.")

    input("Press [Enter] to continue.")

def clear_all_notes(note_manager):
    clear_screen()
    print("Try to Delete all notes.")
    confirmation = input("Are You sure want to delete all notes? (Y/N):")

    if confirmation.lower() == "y":
        note_manager.clear_all_notes()
        input("All notes have been deleted.\nPress [Enter] to continue.")
    elif confirmation.lower() == "n":
        input("Canceled delete all notes.\nPress [Enter] to continue.")
    else:
        input("Incorrect input, action cancelled.\nPress [Enter] to continue.")


# SECTION OF CLEAN FOLDER
def files_menu():

    while True:
        clear_screen()
        menu = PrettyTable()
        print(Fore.YELLOW +"The script will help to sort the files in the specified folder by their extension by categories." + Style.RESET_ALL)
        menu.field_names = [Fore.BLUE + "Option", Fore.BLUE + "Description"]

        menu.add_row(["1", "Sort files by category"])
        menu.add_row(["2", "Quit"])
        
        print(Fore.BLUE + "Clean Folder Menu:")
        print(menu)

        choice = input(Fore.YELLOW + "Select an option [1 / 2]: " + Style.RESET_ALL)

        # print("The script will help to sort the files in the specified folder by their extension by categories.")
        # print("1. Sort files by category")
        # print("2. Quit")

        # choice = input("Select an option [1 / 2]: ")

        if choice == "1":
            folder_path = input("Enter the folder to sort (preferably in the working folder): ")
            if folder_path == "":
                continue
            else:
                folder_cleaner.main(folder_path)
                input("Files have been successfully sorted by category. Press Enter to continue.")
        elif choice == "2":
            return
        else:
            input("Incorrect choice. Press Enter to continue.")



if __name__ == "__main__":
    main_menu()
