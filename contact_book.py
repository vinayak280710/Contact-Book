import json

DATA_FILE = "contacts.json"
contacts = {}
phone_numbers = set()


def validate_phone(phone):
    """Return True if phone is exactly ten characters, all digits.

    >>> validate_phone("9876543210")
    True
    >>> validate_phone("98765")
    False
    >>> validate_phone("98765abcde")
    False
    >>> validate_phone("")
    False
    """
    return len(phone) == 10 and phone.isdigit()


def validate_email(email):
    """Return True if email has an '@' and a dot after the '@'.

    >>> validate_email("rohit@example.com")
    True
    >>> validate_email("rohit.example.com")
    False
    >>> validate_email("rohit@examplecom")
    False
    >>> validate_email("a b@x.com")
    False
    """
    if " " in email or email.count("@") != 1:
        return False
    user, server = email.split("@")
    return len(user) > 0 and "." in server and not server.startswith(".") and not server.endswith(".")


def clean_name(name):
    """Tidy a name: trim spaces and capitalise each word.

    >>> clean_name("  rohit   pandey ")
    'Rohit Pandey'
    """
    return " ".join(name.split()).title()

def sorted_names():
    return sorted(contacts, key=str.lower)


def binary_search(names, target, low, high):
    if low > high:
        return -1
    mid = (low + high) // 2
    if names[mid].lower() == target.lower():
        return mid
    if target.lower() < names[mid].lower():
        return binary_search(names, target, low, mid - 1)
    return binary_search(names, target, mid + 1, high)


def first_prefix_index(names, prefix, low, high):
    if low >= high:
        return low
    mid = (low + high) // 2
    if names[mid].lower() < prefix.lower():
        return first_prefix_index(names, prefix, mid + 1, high)
    return first_prefix_index(names, prefix, low, mid)


def search_by_prefix(prefix):
    names = sorted_names()
    i = first_prefix_index(names, prefix, 0, len(names))
    found = []
    while i < len(names) and names[i].lower().startswith(prefix.lower()):
        found.append(names[i])
        i += 1
    return found


def search_by_name(name):
    names = sorted_names()
    idx = binary_search(names, name.strip(), 0, len(names) - 1)
    if idx == -1:
        return None
    found = names[idx]
    return found, contacts[found][0], contacts[found][1]


def add_contact(name, phone, email):
    name = clean_name(name)
    if not name:
        return False, "Name cannot be empty."
    if not validate_phone(phone):
        return False, "Phone must be exactly 10 digits (digits only)."
    if not validate_email(email):
        return False, "Email must contain '@' and a dot."
    if name in contacts:
        return False, f"{name} already exists. Use update instead."
    if phone in phone_numbers:
        return False, "That phone number already belongs to another contact."
    contacts[name] = (phone, email)
    phone_numbers.add(phone)
    return True, f"Contact {name} added."


def update_contact(name, new_phone=None, new_email=None):
    name = clean_name(name)
    if name not in contacts:
        return False, f"{name} not found."
    old_phone, old_email = contacts[name]
    phone = new_phone if new_phone else old_phone
    email = new_email if new_email else old_email
    if not validate_phone(phone):
        return False, "Phone must be exactly 10 digits (digits only)."
    if not validate_email(email):
        return False, "Email must contain '@' and a dot."
    if phone != old_phone and phone in phone_numbers:
        return False, "That phone number already belongs to another contact."
    phone_numbers.discard(old_phone)
    phone_numbers.add(phone)
    contacts[name] = (phone, email)
    return True, f"Contact {name} updated."


def delete_contact(name):
    name = clean_name(name)
    if name not in contacts:
        return False, f"{name} not found."
    phone, _ = contacts.pop(name)
    phone_numbers.discard(phone)
    return True, f"Contact {name} deleted."


def print_table():
    if not contacts:
        print("No contacts to show.")
        return
    names = sorted_names()
    letters = sorted({n[0].upper() for n in names})
    line = "-" * 70
    print(f"{line}\n{'Name':<24}{'Phone':<14}{'Email'}\n{line}")
    for letter in letters:
        print(f"[ {letter} ]")
        for name in names:
            if name[0].upper() == letter:
                print(f"  {name:<22}{contacts[name][0]:<14}{contacts[name][1]}")
    print(f"{line}\nTotal contacts: {len(contacts)}")


def save_contacts(filename=DATA_FILE):
    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump({k: list(v) for k, v in contacts.items()}, f, indent=2)
        return True, f"Saved {len(contacts)} contact(s) to {filename}."
    except OSError as err:
        return False, f"Could not save file: {err}"


def load_contacts(filename=DATA_FILE):
    try:
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        return False, "No saved file found. Starting with an empty contact book."
    except (json.JSONDecodeError, OSError):
        return False, "Saved file is unreadable. Starting with an empty contact book."

    contacts.clear()
    phone_numbers.clear()
    skipped = 0
    for name, details in data.items():
        if isinstance(details, list) and len(details) == 2 and validate_phone(details[0]) and validate_email(details[1]) and details[0] not in phone_numbers:
            contacts[name] = (details[0], details[1])
            phone_numbers.add(details[0])
        else:
            skipped += 1
    msg = f"Loaded {len(contacts)} contact(s)."
    return True, msg + (f" Skipped {skipped} invalid record(s)." if skipped else "")


def ask(prompt):
    try:
        return input(prompt).strip()
    except (EOFError, KeyboardInterrupt):
        return ""


def main():
    print(load_contacts()[1])
    while True:
        print("\n=========== CONTACT BOOK ===========\n1. Add contact\n2. Search by full name\n3. Search by starting letters\n4. Update contact\n5. Delete contact\n6. List all contacts (A-Z)\n7. Save contacts\n8. Exit")
        choice = ask("Choose an option (1-8): ")
        if choice == "1":
            print(add_contact(ask("Name  : "), ask("Phone (10 digits): "), ask("Email : "))[1])
        elif choice == "2":
            res = search_by_name(ask("Full name: "))
            print(f"Found -> {res[0]} | {res[1]} | {res[2]}" if res else "No contact with that name.")
        elif choice == "3":
            prefix = ask("Starting letters: ")
            matches = search_by_prefix(prefix) if prefix else []
            print("\n".join(f"  {n} | {contacts[n][0]} | {contacts[n][1]}" for n in matches) if matches else "No matching contacts.")
        elif choice == "4":
            name = ask("Name of contact to update: ")
            print("(press Enter to keep the current value)")
            print(update_contact(name, ask("New phone: ") or None, ask("New email: ") or None)[1])
        elif choice == "5":
            print(delete_contact(ask("Name of contact to delete: "))[1])
        elif choice == "6":
            print_table()
        elif choice == "7":
            print(save_contacts()[1])
        elif choice == "8":
            print(save_contacts()[1], "\nGoodbye !", sep="")
            break
        else:
            print("Invalid option. Please enter a number from 1 to 8 only.")


if __name__ == "__main__":
    main()
