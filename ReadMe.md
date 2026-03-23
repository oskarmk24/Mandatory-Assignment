# Library Management System

A simple library management system written in Python that demonstrates the use of different data structures for different tasks.

## Classes

- **`Book`** — Represents a book with a title, author, ISBN, and an availability flag.
- **`User`** — Represents a library user with an ID, name, and type (e.g. student).
- **`LibrarySystem`** — The main system that manages the library. It uses three data structures:
  - A **list** (`catalog_list`) — stores all books, used when searching by title (has to scan every book, so it's O(n)).
  - A **dictionary** (`catalog_isbn`) — maps ISBN → Book for instant O(1) lookups.
  - A **dictionary of queues** (`waitlists`) — each book's ISBN maps to a `deque` (double-ended queue) that holds users waiting for that book, with O(1) add/remove.

## Features

| Method | Description |
|---|---|
| `add_new_book` | Adds a book to both the list and the dictionary, and creates an empty waitlist for it. |
| `search_by_title` | Loops through all books and returns any whose title contains the search text (case-insensitive). |
| `find_book_by_isbn` | Looks up a book instantly by its ISBN using the dictionary. |
| `borrow_book` | Checks if a book is available — if yes, marks it as borrowed; if not, tells the user to join the waitlist. |
| `add_to_waitlist` | Adds a user to the end of the queue for a specific book. |
| `assign_next_user` | When a book is returned, it automatically gives it to the next person in the waitlist. If no one is waiting, it marks the book as available again. |

## Demo

The `if __name__ == "__main__"` block at the bottom of `main.py` runs a demonstration that:

1. Adds two books to the library.
2. Searches for a book by title.
3. Has a user (Oskar) borrow a book.
4. Shows another user (Anna) being denied because the book is already borrowed.
5. Puts Anna on the waitlist.
6. Simulates the book being returned, which automatically assigns it to Anna.

## Key Takeaway

The code demonstrates choosing the right data structure for the job: a **list** for sequential search, a **hash map** for direct lookup, and a **queue** for fair first-come-first-served ordering.
