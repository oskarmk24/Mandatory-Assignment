from collections import deque

class Book:
    def __init__(self, title, author, isbn):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.is_available = True

class User:
    def __init__(self, user_id, name, user_type):
        self.user_id = user_id
        self.name = name
        self.user_type = user_type

class LibrarySystem:
    def __init__(self):
        # Data Structure 1: List (For O(n) operations like searching by title)
        self.catalog_list = [] 
        
        # Data Structure 2: Dictionary / Hash Table (For O(1) direct lookups by ISBN)
        self.catalog_isbn = {} 
        
        # Data Structure 3: Queue via deque (For O(1) waitlist operations)
        self.waitlists = {}    

    def add_new_book(self, book):
        """Helper function to populate the library."""
        self.catalog_list.append(book)
        self.catalog_isbn[book.isbn] = book
        self.waitlists[book.isbn] = deque() 

    def search_by_title(self, title):
        """Lineært søk gjennom bøker ved søk på tittel."""
        # Time Complexity: O(n) because it must scan all books
        results = []
        for book in self.catalog_list:
            if title.lower() in book.title.lower():
                results.append(book)
        return results

    def find_book_by_isbn(self, isbn):
        """Oppslag i dictionary for å finne bok med ISBN."""
        # Time Complexity: O(1) for direct lookup
        return self.catalog_isbn.get(isbn, None)

    def borrow_book(self, isbn, user):
        """Checks availability and processes a loan."""
        book = self.find_book_by_isbn(isbn)
        if not book:
            return "Book not found."
        
        if book.is_available:
            book.is_available = False
            return f"{user.name} successfully borrowed '{book.title}'."
        else:
            return f"'{book.title}' is currently borrowed. Please join the waitlist."

    def add_to_waitlist(self, isbn, user):
        """Adds a user to the queue for a specific book."""
        # Time Complexity: O(1) using deque append operation
        if isbn in self.waitlists:
            self.waitlists[isbn].append(user)
            return f"{user.name} added to the waitlist for '{self.find_book_by_isbn(isbn).title}'."
        return "Book not found."

    def assign_next_user(self, isbn):
        """Automatic assignment to next user when the book is returned."""
        # Time Complexity: O(1) using deque popleft operation
        book = self.find_book_by_isbn(isbn)
        if book:
            if self.waitlists[isbn]:
                next_user = self.waitlists[isbn].popleft()
                return f"'{book.title}' returned and automatically assigned to {next_user.name} from the waitlist."
            else:
                book.is_available = True
                return f"'{book.title}' returned and is now available for anyone."
        return "Book not found."

# Demo with hardcoded values
if __name__ == "__main__":
    library = LibrarySystem()

    # Add some books
    library.add_new_book(Book("Python Crash Course", "Eric Matthes", "978-1593279288"))
    library.add_new_book(Book("Clean Code", "Robert C. Martin", "978-0132350884"))

    # Create a user
    user1 = User("U001", "Oskar", "student")

    # Search by title
    results = library.search_by_title("Python")
    for book in results:
        print(f"Found: {book.title} by {book.author}")

    # Borrow a book
    print(library.borrow_book("978-1593279288", user1))

    # Try borrowing it again
    user2 = User("U002", "Anna", "student")
    print(library.borrow_book("978-1593279288", user2))

    # Add to waitlist and return
    print(library.add_to_waitlist("978-1593279288", user2))
    print(library.assign_next_user("978-1593279288"))
