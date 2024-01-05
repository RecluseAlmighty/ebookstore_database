import sqlite3

db = sqlite3.connect('ebookstore') # Connecting to the database 'ebookstore'

cursor = db.cursor()

cursor.execute(''' 
    CREATE TABLE IF NOT EXISTS book (id INTEGER PRIMARY KEY, 
               title TEXT, author TEXT, qty INTEGER, UNIQUE(id, title, author, qty))
''') # Creating the table for the books..
db.commit()

cursor = db.cursor()

id1 = 3001
title1 = "A Tale of Two Cities"
author1 = "Charles Dickens"
qty1 = 30

id2 = 3002
title2 = "Harry Potter and the Philosopher's Stone"
author2 = "J.K. Rowling"
qty2 = 40

id3 = 3003
title3 = "The Lion, the Witch and the Wardrobe"
author3 = "C.S Lewis"
qty3 = 25

id4 = 3004
title4 = "The Lord of the Rings"
author4 = "J.R.R Tolkien"
qty4 = 37

id5 = 3005
title5 = "Alice in Wonderland"
author5 = "Lewis Carroll"
qty5 = 12

cursor.execute('''INSERT OR REPLACE INTO book (id, title, author, qty)
               VALUES (?, ?, ?, ?)''', (id1, title1, author1, qty1))

cursor.execute('''INSERT OR REPLACE INTO book (id, title, author, qty)
               VALUES (?, ?, ?, ?)''', (id2, title2, author2, qty2))

cursor.execute('''INSERT OR REPLACE INTO book (id, title, author, qty)
               VALUES (?, ?, ?, ?)''', (id3, title3, author3, qty3))

cursor.execute('''INSERT OR REPLACE INTO book (id, title, author, qty)
               VALUES (?, ?, ?, ?)''', (id4, title4, author4, qty4))

cursor.execute('''INSERT OR REPLACE INTO book (id, title, author, qty)
               VALUES (?, ?, ?, ?)''', (id5, title5, author5, qty5))

db.commit()

db.close()

def add_book(): # Add book function..
    
    print("\nWhat book would you like to add to the ebookstore database")
    
    try:
        
        db = sqlite3.connect('ebookstore')
    
        cursor = db.cursor()

        # User enters the details for the book being added to the database..
        book_title = input("\nPlease enter the title of the book you would like to enter in to the database: ")
        book_author = input("\nPlease enter the author of the book you are entering in to the database: ")
        book_qty = input("\nPlease enter the quantity of the book being entered into the database: ")
        
        cursor.execute('''INSERT OR REPLACE INTO book (title, author, qty)
                VALUES (?, ?, ?)''', (book_title, book_author, book_qty))
        
        db.commit()
        
        print(f"\nThe book {book_title} by {book_author} has now been added to the database!")
    
    except Exception as DatabaseError: # Exception if book aready exists 
        db.rollback()
        print("\nOops. That book title already exists in the database .")
        raise DatabaseError
    finally:
        db.close()
    
def update_book(): # Update book function..
    
    # Allows user to input id of book directly to retrieve it from the database..
    id_query = input("\nDo you know the id of the book you would like to update? (y/n): ").lower()
    
    if id_query == "y":
        id_known = input("\nPlease enter the id of the book you would like to update: ")
            
    try:
            
        db = sqlite3.connect('ebookstore')
        
        cursor = db.cursor()
            
        cursor.execute('''SELECT* FROM book WHERE id=?''', (id_known,))
        chosen_book = cursor.fetchall()
        print(f"{chosen_book}")
            
        # Update the chosen book's quantity..
        quantity_update = input("\nWhat is the new quantity: ")
        cursor.execute('''INSERT OR REPLACE INTO book (qty) VALUES (?)''', (quantity_update, ))
        db.commit()
        print(f"You have successfully updated the quantities for {id_known}")
            
    except Exception as DatabaseError:
        db.rollback()
        print("\nOops. Looks like that book id does not exist in the current database.")
        raise DatabaseError
    finally:
        db.close()
        # If book already exists then allows user to access add book function
        opt_add_book = input("Would you like to add the book? (y/n): ")
        while opt_add_book == "y":
            add_book()
            if opt_add_book == "n":
                break
        else:
            print("\nYou have made entered an invalid input. Please try again")
                  
              
    if id_query == "n": # if id is not known then user can use the title to access the book they would like to update
        book_title_known = print(input("\nWhich book would you like to update: "))
        
    try:
            
        db = sqlite3.connect('ebookstore')
    
        cursor = db.cursor()
        
        cursor.execute('''SELECT* FROM book WHERE title=?''', (book_title_known))
        chosen_book = cursor.fetchall()
        print(f"{chosen_book}")
            
        quantity_update = input("\nWhat is the new quantity: ")
        cursor.execute('''INSERT OR REPLACE INTO book (qty) VALUES (?)''', (quantity_update, ))
        db.commit()
        print(f"You have successfully updated the quantities for {id_known}")
            
    except Exception as DatabaseError:
        db.rollback()
        print("\nOops. Looks like that book does not exist in the current database.")
        raise DatabaseError
    finally:
        db.close()
        opt_add_book = input("Would you like to add the book? (y/n): ")
        while opt_add_book == "y":
            add_book()
            if opt_add_book == "n":
                break
        else:
            print("\nYou have made entered an invalid input. Please try again")
            
    '''else:
        print("\nYou have made entered an invalid input. Please try again")
        return update_book()'''
            
def delete_book(): # Delete book function..
    
    id_query = input("\nDo you know the id of the book you would like to delete? (y/n): ").lower()
    
    if id_query == "y":
        id_known = input("\nPlease enter the id of the book you would like to delete: ")
            
        try:
            
            db = sqlite3.connect('ebookstore')
        
            cursor = db.cursor()
            
            cursor.execute('''SELECT* FROM book WHERE id=?''', (id_known,))
            chosen_book = cursor.fetchall()
            print(f"{chosen_book}")
            
            delete_confirm = input(f"\nAre you sure you want to delete the record for {id_known}? (y/n): ")
            
            while delete_confirm == "y":
            
                cursor.execute('''DELETE* FROM book WHERE id = ? ''', (id_known,))
                db.commit()
                print(f"\nThe record for {id_known} has been successfully deleted.")
                
                if delete_confirm == "n":
                    break
                
            else:
                print("\nYou have made entered an invalid input. Please try again")
                return delete_book()
            
        except Exception as DatabaseError:
            db.rollback()
            print("\nOops. Looks like that book id does not exist in the current database.")
            raise DatabaseError
        finally:
            db.close()
            
                
    if id_query == "n":
        book_title_known = input("\nWhich book would you like to delete: ")
        
        try:
            
            db = sqlite3.connect('ebookstore')
        
            cursor = db.cursor()
            
            cursor.execute('''SELECT* FROM book WHERE title =?''', (book_title_known,))
            chosen_book = cursor.fetchall()
            print(f"{chosen_book}")
            
            delete_confirm = input(f"\nAre you sure you want to delete the record for {book_title_known}? (y/n): ")
            
            while delete_confirm == "y":
            
                cursor.execute('''DELETE* FROM book WHERE id = ? ''', (book_title_known,))
                db.commit()
                print(f"\nThe record for {book_title_known} has been successfully deleted.")
                
                if delete_confirm == "n":
                    break
                
            else:
                print("\nYou have made entered an invalid input. Please try again")
                return delete_book()
            
        except Exception as DatabaseError:
            db.rollback()
            print("\nOops. Looks like that book title does not exist in the current database.")
            raise DatabaseError
        finally:
            db.close()
            
            
def search_book(): # Search book function..
    
    # Search book database using any of the variables attached to books in database
    search_query = input("Please enter a book id, title or author to search: ")
    
    try:
        
        db = sqlite3.connect('ebookstore')
        
        cursor = db.cursor()
        
        cursor.execute('''SELECT* FROM book WHERE id =? OR title =? OR author =?''', (search_query, search_query, search_query, ))
        chosen_books = cursor.fetchall()
        print(f"{chosen_books}")
        
    except Exception as DatabaseError:
            db.rollback()
            print("\nOops. Looks like no books with that id, title or author in the current database.")
            raise DatabaseError
    finally:
        db.close()
        
def display_database(): # Displays entire database...
        
        db = sqlite3.connect('ebookstore')
        
        cursor = db.cursor()
        
        cursor.execute('''SELECT* FROM book''')
        entire_database = cursor.fetchall()
        print(f"\n{entire_database}")
        db.close()
        
while True:
    # Present the menu to the user
    menu = input('''\nSelect one of the following options:
    1. Enter book
    2. Update book
    3. Delete book
    4. Search book
    5. Display entire database
    0. Exit
    : ''')

    if menu == '1':
        add_book()

    elif menu == '2':
        update_book()

    elif menu == '3':
        delete_book()

    elif menu == '4':
        search_book()

    elif menu == '5':
        display_database()

    elif menu == '0':
        print('Goodbye!!!')
        exit()

    else:
        print("You have made entered an invalid input. Please try again")