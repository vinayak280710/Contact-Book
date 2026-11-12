"""
Project 6: Contact Book
Group 6 - Rohit Pandey, Vinayak Madabhavi, Priya Davare, Aman Babu

A command-line program that stores phone contacts and lets the user
search and maintain them.

Key topics used
---------------
* Dictionaries : main data store  {name: (phone, email)}
* Tuples       : details of each contact are held as (phone, email)
* Sets         : a set of phone numbers prevents duplicates
* Recursion    : recursive binary search on the sorted list of names
* Nested loops : contacts printed as a table grouped by first letter
* File handling, exception handling, doctests, functions, strings, lists

Run the program :  python contact_book.py
Run the doctests:  python -m doctest contact_book.py -v
"""

import json

DATA_FILE = "contacts.json"

# Main data: {name: (phone, email)}
contacts = {}
# Every phone number in use, to stop two contacts sharing a number
phone_numbers = set()


# ----------------------------------------------------------------------
# Validation
# ----------------------------------------------------------------------
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
    username, server = email.split("@")
    if len(username)==0:
        return False
    if "." not in server:
        return False
    if server.startswith(".") or server.endswith("."):
        return False
    return True


# ----------------------------------------------------------------------
# Helpers
# ----------------------------------------------------------------------
def clean_name(name):
    """Tidy a name: trim spaces and capitalise each word.

    >>> clean_name("  rohit   pandey ")
    'Rohit Pandey'
    """
    return " ".join(name.split()).title()


def sorted_names():
    """Return all contact names in alphabetical (case-insensitive) order.

    >>> contacts.clear(); contacts.update({"Bob": ("1111111111", "b@x.com"),
    ...                                    "Alice": ("2222222222", "a@x.com")})
    >>> sorted_names()
    ['Alice', 'Bob']
    >>> contacts.clear()
    """
    return sorted(contacts, key=str.lower)


# ----------------------------------------------------------------------
# Recursion: binary search on the sorted list of names
# ----------------------------------------------------------------------
def binary_search(names, target, low, high):
    """Recursively search a sorted list of names for target (full name).

    Returns the index of target, or -1 if it is not present.
    The comparison ignores upper/lower case.

    >>> names = ["Aman", "Priya", "Rohit", "Vinayak"]
    >>> binary_search(names, "rohit", 0, len(names) - 1)
    2
    >>> binary_search(names, "Aman", 0, len(names) - 1)
    0
    >>> binary_search(names, "Zed", 0, len(names) - 1)
    -1
    >>> binary_search([], "Aman", 0, -1)
    -1
    """
    if low > high:                      # base case: not found
        return -1
    mid = (low + high) // 2
    middle = names[mid].lower()
    target = target.lower()
    if middle == target:                # base case: found
        return mid
    if target < middle:                 # recursive case: left half
        return binary_search(names, target, low, mid - 1)
    return binary_search(names, target, mid + 1, high)   # right half


def first_prefix_index(names, prefix, low, high):
    """Recursively find the first index whose name starts with prefix
    (or the position where such a name would be). Used for prefix search.

    >>> names = ["Aman", "Amit", "Priya", "Rohit"]
    >>> first_prefix_index(names, "am", 0, len(names))
    0
    >>> first_prefix_index(names, "p", 0, len(names))
    2
    """
    if low >= high:
        return low
    mid = (low + high) // 2
    if names[mid].lower() < prefix.lower():
        return first_prefix_index(names, prefix, mid + 1, high)
    return first_prefix_index(names, prefix, low, mid)


def search_by_prefix(prefix):
    """Return every name starting with prefix (case-insensitive).

    >>> contacts.clear(); contacts.update({
    ...     "Aman Babu": ("1111111111", "a@x.com"),
    ...     "Amit Shah": ("2222222222", "b@x.com"),
    ...     "Priya Davare": ("3333333333", "c@x.com")})
    >>> search_by_prefix("am")
    ['Aman Babu', 'Amit Shah']
    >>> search_by_prefix("z")
    []
    >>> contacts.clear()
    """
    names = sorted_names()
    start = first_prefix_index(names, prefix, 0, len(names))
    found = []
    while start < len(names) and names[start].lower().startswith(prefix.lower()):
        found.append(names[start])
        start += 1
    return found


# ----------------------------------------------------------------------
# Core operations
# ----------------------------------------------------------------------
def add_contact(name, phone, email):
    """Add a contact. Returns (True, message) or (False, reason).

    >>> contacts.clear(); phone_numbers.clear()
    >>> add_contact("rohit pandey", "9876543210", "rohit@example.com")
    (True, 'Contact Rohit Pandey added.')
    >>> add_contact("Rohit Pandey", "9123456780", "r@example.com")[0]
    False
    >>> add_contact("Aman Babu", "9876543210", "aman@example.com")[0]
    False
    >>> add_contact("Aman Babu", "12345", "aman@example.com")[0]
    False
    >>> add_contact("Aman Babu", "9123456780", "aman-example.com")[0]
    False
    >>> contacts.clear(); phone_numbers.clear()
    """
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
    contacts[name] = (phone, email)      # tuple of details
    phone_numbers.add(phone)             # set prevents duplicates
    return True, f"Contact {name} added."


def update_contact(name, new_phone=None, new_email=None):
    """Update phone and/or email of an existing contact.

    >>> contacts.clear(); phone_numbers.clear()
    >>> _ = add_contact("Priya Davare", "9000000001", "p@x.com")
    >>> update_contact("priya davare", new_phone="9000000002")
    (True, 'Contact Priya Davare updated.')
    >>> contacts["Priya Davare"]
    ('9000000002', 'p@x.com')
    >>> "9000000001" in phone_numbers
    False
    >>> update_contact("Nobody", new_phone="9000000003")[0]
    False
    >>> contacts.clear(); phone_numbers.clear()
    """
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
    """Delete a contact and free its phone number.

    >>> contacts.clear(); phone_numbers.clear()
    >>> _ = add_contact("Aman Babu", "9000000009", "a@x.com")
    >>> delete_contact("aman babu")
    (True, 'Contact Aman Babu deleted.')
    >>> phone_numbers
    set()
    >>> delete_contact("Aman Babu")[0]
    False
    """
    name = clean_name(name)
    if name not in contacts:
        return False, f"{name} not found."
    phone, _email = contacts.pop(name)
    phone_numbers.discard(phone)
    return True, f"Contact {name} deleted."


def search_by_name(name):
    """Full-name search using the recursive binary search.

    Returns (name, phone, email) or None.

    >>> contacts.clear(); phone_numbers.clear()
    >>> _ = add_contact("Rohit Pandey", "9000000001", "r@x.com")
    >>> _ = add_contact("Aman Babu", "9000000002", "a@x.com")
    >>> search_by_name("rohit pandey")
    ('Rohit Pandey', '9000000001', 'r@x.com')
    >>> search_by_name("Nobody") is None
    True
    >>> contacts.clear(); phone_numbers.clear()
    """
    names = sorted_names()
    index = binary_search(names, name.strip(), 0, len(names) - 1)
    if index == -1:
        return None
    found = names[index]
    phone, email = contacts[found]
    return found, phone, email


# ----------------------------------------------------------------------
# Display: nested loops, grouped by first letter
# ----------------------------------------------------------------------
def print_table():
    """Print all contacts as a table grouped by the first letter."""
    if not contacts:
        print("No contacts to show.")
        return
    names = sorted_names()
    letters = sorted({n[0].upper() for n in names})       # set of first letters
    line = "-" * 70
    print(line)
    print(f"{'Name':<24}{'Phone':<14}{'Email'}")
    print(line)
    for letter in letters:                                # outer loop
        print(f"[ {letter} ]")
        for name in names:                                # inner loop
            if name[0].upper() == letter:
                phone, email = contacts[name]
                print(f"  {name:<22}{phone:<14}{email}")
    print(line)
    print(f"Total contacts: {len(contacts)}")


# ----------------------------------------------------------------------
# File handling
# ----------------------------------------------------------------------
def save_contacts(filename=DATA_FILE):
    """Write all contacts to a JSON file."""
    data = {name: list(details) for name, details in contacts.items()}
    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        return True, f"Saved {len(contacts)} contact(s) to {filename}."
    except OSError as err:
        return False, f"Could not save file: {err}"


def load_contacts(filename=DATA_FILE):
    """Load contacts from a JSON file (called when the program starts)."""
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
        try:
            phone, email = details
        except (TypeError, ValueError):
            skipped += 1
            continue
        if validate_phone(phone) and validate_email(email) \
                and phone not in phone_numbers:
            contacts[name] = (phone, email)
            phone_numbers.add(phone)
        else:
            skipped += 1
    msg = f"Loaded {len(contacts)} contact(s)."
    if skipped:
        msg += f" Skipped {skipped} invalid record(s)."
    return True, msg


# ----------------------------------------------------------------------
# Menu
# ----------------------------------------------------------------------
def ask(prompt):
    """input() that survives Ctrl+D / Ctrl+C without a crash."""
    try:
        return input(prompt).strip()
    except (EOFError, KeyboardInterrupt):
        return ""


def menu():
    print("\n=========== CONTACT BOOK ===========")
    print("1. Add contact")
    print("2. Search by full name")
    print("3. Search by starting letters")
    print("4. Update contact")
    print("5. Delete contact")
    print("6. List all contacts (A-Z)")
    print("7. Save contacts")
    print("8. Exit")


def main():
    print(load_contacts()[1])
    while True:
        menu()
        choice = ask("Choose an option (1-8): ")

        if choice == "1":
            name = ask("Name  : ")
            phone = ask("Phone (10 digits): ")
            email = ask("Email : ")
            print(add_contact(name, phone, email)[1])

        elif choice == "2":
            result = search_by_name(ask("Full name: "))
            if result:
                print(f"Found -> {result[0]} | {result[1]} | {result[2]}")
            else:
                print("No contact with that name.")

        elif choice == "3":
            prefix = ask("Starting letters: ")
            matches = search_by_prefix(prefix) if prefix else []
            if matches:
                for n in matches:
                    print(f"  {n} | {contacts[n][0]} | {contacts[n][1]}")
            else:
                print("No matching contacts.")

        elif choice == "4":
            name = ask("Name of contact to update: ")
            print("(press Enter to keep the current value)")
            phone = ask("New phone: ")
            email = ask("New email: ")
            print(update_contact(name, phone or None, email or None)[1])

        elif choice == "5":
            print(delete_contact(ask("Name of contact to delete: "))[1])

        elif choice == "6":
            print_table()

        elif choice == "7":
            print(save_contacts()[1])

        elif choice == "8":
            print(save_contacts()[1])
            print("Goodbye!")
            break

        else:
            print("Invalid option. Please enter a number from 1 to 8.")


if __name__ == "__main__":
    main()
