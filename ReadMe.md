# IS-211 Mandatory group assignment
Group 5: 
- Oskar Kirkbride
- Helle Aanonsen 
- Milana Dubkova
- Karoline Aas-Mehren



# Smart Library Search and Reservation Prototype

A command-line based smart library management prototype written in Python. The system demonstrates how different data structures can be used efficiently in a realistic application scenario involving book search, borrowing, and reservation queues.

## Classes 
### Book 
 Represents a book with: 
 - title 
 - author
 - **ISBN** 
 - availability status 
 - the current user who has borrowed the book
 ### User 
 Represents a library patron with: 
 - user ID 
 - name 
 - user type (e.g. student, researcher, library staff) 
 ### LibrarySystem 
 The main system that manages all books, loans, and waitlists. 
 
 ## Data Structures Used

The system demonstrates choosing appropriate data structures based on task requirements.

### List (catalog_list)

Stores all books in the catalog. Used for flexible title searching.

- Operation: sequential scan 
- Time Complexity: O(n) 

### Dictionary / Hash Table (catalog_isbn)

Maps **ISBN** → Book object.

- Operation: direct lookup 
- Time Complexity: O(1) 

### Dictionary of Queues (waitlists)

Each book’s **ISBN** maps to a deque queue that stores users waiting for the book.

- Add user to queue: O(1)
- Remove next user: O(1)
- Ensures **FIFO** fairness (first-come-first-served)


## Features

| Method                   | Description                                                                                           |
|--------------------------|-------------------------------------------------------------------------------------------------------|
| add_new_book             | Adds a book to the catalog list, ISBN dictionary, and creates an empty waitlist queue.               |
| search_by_title          | Performs flexible case-insensitive search through all books.                                         |
| find_book_by_title       | Finds the first matching book using partial title matching.                                          |
| borrow_book_by_title     | Allows a user to borrow a book if available.                                                         |
| add_to_waitlist_by_title | Adds a user to the reservation queue if the book is already borrowed.                                |
| return_book_by_title     | Returns a book and automatically assigns it to the next user in queue.                               |
| assign_next_user           | When a book is returned, it automatically gives it to the next person in the waitlist. If no one is waiting, it marks the book as available again.                       |
| show_waitlists           | Displays all books that currently have active waitlists and the users waiting.                       |


### Interactive Prototype

The system runs as an interactive command-line application.

### Menu Options

1. Search book 
2. Borrow book 
3. Join waitlist 
4. Return book 
5. Show catalog 
6. Show waitlists 
0. Exit

Users can search by full or partial title, making the prototype more realistic.

### Demo Dataset

The prototype includes a preloaded dataset of real programming and computer science books, such as:

- Python Crash Course
- Clean Code 
- Introduction to Algorithms 
- Fluent Python
- Deep Learning 
- Design Patterns

Multiple demo users are also created.

### Preconfigured Demo State

When the system starts:

- Some books are already borrowed 
- Some books already have multiple users in the waitlist 
- Different user types are represented

This allows the prototype to immediately demonstrate:

- queue ordering 
- automatic reassignment on return 
- catalog status updates 
- waitlist visualization 


### How to Run

Run the prototype from the terminal:

python main.py


### Example Demo Flow

A typical demonstration sequence:

- Show catalog 
- Show waitlists 
- Return a borrowed book 
- Observe automatic assignment to next user 
- Show updated waitlist and catalog 

### Key Takeaway

This prototype demonstrates how selecting the correct data structure improves both performance and system design:

- Lists enable flexible search 
- Hash tables provide instant lookup 
- Queues ensure fair reservation handling

Together, they create a scalable and realistic foundation for a smart library system.