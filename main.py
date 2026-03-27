from collections import deque


class Book:
    def __init__(self, title, author, isbn):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.is_available = True
        self.borrowed_by = None


class User:
    def __init__(self, user_id, name, user_type):
        self.user_id = user_id
        self.name = name
        self.user_type = user_type


class LibrarySystem:
    def __init__(self):
        # Data Structure 1: List (for O(n) operations like searching by title)
        self.catalog_list = []

        # Data Structure 2: Dictionary / Hash Table (for O(1) direct lookups by ISBN)
        self.catalog_isbn = {}

        # Data Structure 3: Queue via deque (for O(1) waitlist operations)
        self.waitlists = {}

    def add_new_book(self, book):
        """Helper function to populate the library."""
        self.catalog_list.append(book)
        self.catalog_isbn[book.isbn] = book
        self.waitlists[book.isbn] = deque()

    def search_by_title(self, title):
        """Linear search through books by title."""
        results = []
        title = title.lower().strip()

        for book in self.catalog_list:
            if title in book.title.lower():
                results.append(book)

        return results

    def find_books_by_title(self, title):
        """Find all books that match all or part of the title."""
        title = title.lower().strip()
        matches = []

        for book in self.catalog_list:
            if title in book.title.lower():
                matches.append(book)

        return matches

    def find_book_by_title(self, title):
        """Find the first matching book by title."""
        matches = self.find_books_by_title(title)
        if matches:
            return matches[0]
        return None

    def find_book_by_isbn(self, isbn):
        """Lookup in dictionary to find a book by ISBN."""
        return self.catalog_isbn.get(isbn, None)

    def borrow_book_by_title(self, title, user):
        """Borrow the first matching book by title."""
        book = self.find_book_by_title(title)
        return self.borrow_book(book, user)

    def add_to_waitlist_by_title(self, title, user):
        """Add user to waitlist for the first matching book by title."""
        book = self.find_book_by_title(title)
        return self.add_to_waitlist(book, user)

    def return_book_by_title(self, title):
        """Return the first matching book by title."""
        book = self.find_book_by_title(title)
        return self.return_book(book)

    def borrow_book(self, book, user):
        """Borrow a selected book object."""
        if not book:
            return "Book not found."

        if book.is_available:
            book.is_available = False
            book.borrowed_by = user
            return f"{user.name} borrowed '{book.title}'."
        else:
            return f"'{book.title}' is currently borrowed. Please join the waitlist."

    def add_to_waitlist(self, book, user):
        """Add a user to the selected book's waitlist, avoiding duplicates."""
        if not book:
            return "Book not found."

        if book.is_available:
            return f"'{book.title}' is available. You can borrow it instead of joining the waitlist."

        for waiting_user in self.waitlists[book.isbn]:
            if waiting_user.user_id == user.user_id:
                return f"{user.name} is already in the waitlist for '{book.title}'."

        self.waitlists[book.isbn].append(user)
        return f"{user.name} added to waitlist for '{book.title}'."

    def return_book(self, book):
        """Return a selected book object."""
        if not book:
            return "Book not found."

        if self.waitlists[book.isbn]:
            next_user = self.waitlists[book.isbn].popleft()
            book.borrowed_by = next_user
            book.is_available = False
            return f"'{book.title}' returned and assigned to next user: {next_user.name}"
        else:
            book.is_available = True
            book.borrowed_by = None
            return f"'{book.title}' is now available."

    def add_to_waitlist_by_isbn(self, isbn, user):
        """Adds a user to the queue for a specific book by ISBN."""
        book = self.find_book_by_isbn(isbn)

        if not book:
            return "Book not found."

        return self.add_to_waitlist(book, user)

    def assign_next_user(self, isbn):
        """Automatic assignment to next user when the book is returned."""
        book = self.find_book_by_isbn(isbn)

        if not book:
            return "Book not found."

        if self.waitlists[isbn]:
            next_user = self.waitlists[isbn].popleft()
            book.borrowed_by = next_user
            book.is_available = False
            return f"'{book.title}' returned and automatically assigned to {next_user.name} from the waitlist."
        else:
            book.is_available = True
            book.borrowed_by = None
            return f"'{book.title}' returned and is now available for anyone."

    def show_waitlists(self):
        """Shows all books that currently have users in the waitlist."""
        books_with_waitlists = []

        for isbn, queue in self.waitlists.items():
            if queue:
                book = self.find_book_by_isbn(isbn)
                waiting_users = [
                    f"{i + 1}. {user.name} ({user.user_type})"
                    for i, user in enumerate(queue)
                ]
                books_with_waitlists.append((book, waiting_users))

        return books_with_waitlists


def select_book_from_matches(matches):
    """Let the user choose one book from a list of matches."""
    if not matches:
        return None

    if len(matches) == 1:
        return matches[0]

    print("\nMultiple books found:")
    for i, book in enumerate(matches, start=1):
        status = "Available" if book.is_available else f"Borrowed by {book.borrowed_by.name}"
        print(f"{i}. {book.title} by {book.author} | ISBN: {book.isbn} | {status}")

    choice = input("Choose book number: ").strip()

    if not choice.isdigit():
        print("Invalid choice.")
        return None

    choice_num = int(choice)

    if 1 <= choice_num <= len(matches):
        return matches[choice_num - 1]

    print("Invalid choice.")
    return None


def setup_demo_state(library, users):
    """Create a more realistic starting state for the prototype."""

    # Borrowed books
    book1 = library.find_book_by_title("Python Crash Course")
    book2 = library.find_book_by_title("Clean Code")
    book3 = library.find_book_by_title("Introduction to Algorithms")

    if book1:
        book1.is_available = False
        book1.borrowed_by = users["1"]  # Oskar

    if book2:
        book2.is_available = False
        book2.borrowed_by = users["3"]  # Karoline

    if book3:
        book3.is_available = False
        book3.borrowed_by = users["5"]  # Helle

    # Waitlists
    if book1:
        library.waitlists[book1.isbn].append(users["2"])  # Anna
        library.waitlists[book1.isbn].append(users["4"])  # Milana

    if book2:
        library.waitlists[book2.isbn].append(users["1"])  # Oskar

    if book3:
        library.waitlists[book3.isbn].append(users["2"])  # Anna
        library.waitlists[book3.isbn].append(users["3"])  # Karoline


def run_prototype():
    """Prototype with hardcoded values for demonstration."""
    library = LibrarySystem()

    # Hardcoded demo data
    library.add_new_book(Book("Python Crash Course", "Eric Matthes", "9781593279288"))
    library.add_new_book(Book("Clean Code", "Robert C. Martin", "9780132350884"))
    library.add_new_book(Book("The Pragmatic Programmer", "Andrew Hunt", "9780201616224"))
    library.add_new_book(Book("Introduction to Algorithms", "Thomas H. Cormen", "9780262033848"))
    library.add_new_book(Book("Design Patterns", "Erich Gamma", "9780201633610"))
    library.add_new_book(Book("Artificial Intelligence: A Modern Approach", "Stuart Russell", "9780136042594"))
    library.add_new_book(Book("Fluent Python", "Luciano Ramalho", "9781492056355"))
    library.add_new_book(Book("Automate the Boring Stuff with Python", "Al Sweigart", "9781593275990"))
    library.add_new_book(Book("Deep Learning", "Ian Goodfellow", "9780262035613"))
    library.add_new_book(Book("Refactoring", "Martin Fowler", "9780134757599"))

    users = {
        "1": User("U1", "Oskar", "student"),
        "2": User("U2", "Anna", "student"),
        "3": User("U3", "Karoline", "student"),
        "4": User("U4", "Milana", "researcher"),
        "5": User("U5", "Helle", "library staff"),
    }

    setup_demo_state(library, users)

    while True:
        print("\n--- SMART LIBRARY SYSTEM ---")
        print("1 Search book")
        print("2 Borrow book")
        print("3 Join waitlist")
        print("4 Return book")
        print("5 Show catalog")
        print("6 Show waitlists")
        print("0 Exit")

        choice = input("Choice: ").strip()

        if choice == "1":
            query = input("Enter title keyword or ISBN: ").strip()
            book_by_isbn = library.find_book_by_isbn(query)
            
            if book_by_isbn:
                results = [book_by_isbn]
            else:
                results = library.search_by_title(query)

            if results:
                for b in results:
                    status = "Available" if b.is_available else f"Borrowed by {b.borrowed_by.name}"
                    print(f"{b.title} | ISBN: {b.isbn} | {status}")
            else:
                print("No books found.")

        elif choice == "2":
            query = input("Enter title or ISBN: ").strip()
            user_choice = input("User (1, 2, 3, 4 or 5): ").strip()

            if user_choice in users:
                book_by_isbn = library.find_book_by_isbn(query)
                matches = [book_by_isbn] if book_by_isbn else library.find_books_by_title(query)
                selected_book = select_book_from_matches(matches)

                if selected_book:
                    print(library.borrow_book(selected_book, users[user_choice]))
                else:
                    print("No valid book selected.")
            else:
                print("Invalid user.")

        elif choice == "3":
            query = input("Enter title or ISBN: ").strip()
            user_choice = input("User (1, 2, 3, 4 or 5): ").strip()

            if user_choice in users:
                book_by_isbn = library.find_book_by_isbn(query)
                matches = [book_by_isbn] if book_by_isbn else library.find_books_by_title(query)
                selected_book = select_book_from_matches(matches)

                if selected_book:
                    print(library.add_to_waitlist(selected_book, users[user_choice]))
                else:
                    print("No valid book selected.")
            else:
                print("Invalid user.")

        elif choice == "4":
            query = input("Enter title or ISBN: ").strip()
            book_by_isbn = library.find_book_by_isbn(query)
            matches = [book_by_isbn] if book_by_isbn else library.find_books_by_title(query)
            selected_book = select_book_from_matches(matches)

            if selected_book:
                print(library.return_book(selected_book))
            else:
                print("No valid book selected.")

        elif choice == "5":
            print("\n--- CATALOG ---")
            for b in library.catalog_list:
                if b.is_available:
                    status = "Available"
                else:
                    status = f"Borrowed by {b.borrowed_by.name}"

                waitlist_count = len(library.waitlists[b.isbn])
                print(f"{b.title} | {b.author} | ISBN: {b.isbn} | {status} | Waitlist: {waitlist_count}")

        elif choice == "6":
            waitlists = library.show_waitlists()

            if waitlists:
                print("\n--- CURRENT WAITLISTS ---")
                for book, users_waiting in waitlists:
                    print(f"{book.title}")
                    for user_info in users_waiting:
                        print(f"   {user_info}")
            else:
                print("Currently no waitlists.")

        elif choice == "0":
            print("Exiting system.")
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    run_prototype()