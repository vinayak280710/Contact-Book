Contact Book 📖

Description

Contact Book is a robust, command-line Python application designed to help users store, search, and manage their phone contacts efficiently. Built with data integrity in mind, the program ensures that no duplicate names or phone numbers are saved and automatically validates phone numbers and email addresses. Contacts are saved persistently to a local JSON file, ensuring your data is ready for you every time you launch the program.

Features

Add, Update, and Delete: Easily maintain your contacts with input validation (requires 10-digit phone numbers and standard email formatting).

Smart Search:

Full Name Search: Uses a highly efficient recursive binary search to find contacts instantly.

Prefix Search: Can't remember the full name? Search by the first few letters to get a list of matches.

Organized Display: View all contacts neatly formatted in an alphabetical table, grouped by their starting letter.

Data Persistence: Automatically saves and loads your contact list using a lightweight contacts.json file.

Duplicate Prevention: Uses Python sets and dictionaries to strictly prevent duplicate entries or shared phone numbers between contacts.

Technical Concepts Demonstrated

This project serves as a showcase for several core Python programming concepts:

Dictionaries & Tuples: Used as the primary data store for mapping Name -> (Phone, Email).

Sets: Utilized to maintain a unique registry of phone numbers.

Recursion: Implemented via a custom Recursive Binary Search for fast name lookups.

File Handling: Read/Write operations using the json library.

Exception Handling: Graceful error catching for file loading, saving, and user interrupts (Ctrl+C/Ctrl+D).

Automated Testing: Built-in doctest strings for robust function validation.

Prerequisites

Python 3.x installed on your machine.

No external dependencies or libraries required (uses only built-in Python modules).

How to Run

Clone the repository or download the project files.

Open your terminal or command prompt.

Navigate to the directory containing the project.

Run the application using:

python contact_book.py


Running Tests

The code includes embedded doctest modules to verify that functions work as expected. To run the tests, use the following command:

python -m doctest contact_book.py -v


Team / Credits

Group 6

Rohit Pandey

Vinayak Madabhavi

Priya Davare

Aman Babu
