from models import (Base, session, Book, engine)
import datetime
import csv
import time


def menu():
    while True:
        print('''
            \nPROGRAMMING BOOKS
            \r1) Add book
            \r2) View all books
            \r3) Search for book
            \r4) Book analysis
            \r5) Exit
        ''')
        choice = input('What would you like to do?  ')
        if choice in ['1', '2', '3', '4', '5']:
            return choice
        else:
            input('''
            \rPlease choose one of the options above.
            \rA number from 1-5.
            \rPress enter to try again.''')


def clean_date(date_str):
    months = ['January', 'February', 'March', 'April', 'May', 
    'June', 'July', 'August', 'September', 'October', 'November', 'December']
    split_date = date_str.split(' ') #takes the string formatted dates and splits on the space and turns each information into list element
    try:
        month = int(months.index(split_date[0])) + 1 #takes the index 0 of date list (month in this case) and finds index of equivilent month in months list and returns its index + 1 as that is equal to the month number. ie Jan is index 0 so +1 =1st month
        day = int(split_date[1].split(',')[0]) #removes comma from the day element of list left from initial string split
        year = int(split_date[2])
        return_date = datetime.date(year, month, day)
    except ValueError:
        input('''
        \n***** DATE ERROR *****
        \rThe date format should include a valid Month Day, Year.
        \rEx: January 13, 2003
        \rpress enter to try again
        \r************************
        ''')
        return
    else:
        return return_date


def clean_price(price_str):
    try:
        price_float = float(price_str)
    except ValueError:
        input('''
        \n***** PRICE ERROR *****
        \rThe price should be a number without a currency symbol.
        \rEx: 9.99
        \rpress enter to try again
        \r************************
        ''')
        return
    else:
        return int(price_float*100)


def clean_id(id_str, options):
    try:
        book_id = int(id_str)
    except ValueError:
        input('''
        \n***** ID ERROR *****
        \rThe ID should be a number.
        \rpress enter to try again
        \r************************
        ''')
        return
    else:
        if book_id in options:
            return book_id
        else:
            input(f'''
        \n***** ID ERROR *****
        \rOptions: {options}.
        \rpress enter to try again
        \r************************
        ''')
            return


def add_csv():
    with open('suggested_books.csv') as csvfile:
        data = csv.reader(csvfile) #interpreting csvfile data as lists, good for any data that needs to be seen as a string but creates issues if data needs to be held in different format like int.
        for row in data:
            book_in_db = session.query(Book).filter(Book.title==row[0]).one_or_none()#prevents duplicate books from being added to db
            if book_in_db == None:
                title = row[0]
                author = row[1]
                date = clean_date(row[2])
                price = clean_price(row[3])
                new_book = Book(title=title, author=author, published_date=date, price=price)
                session.add(new_book)
        session.commit()


def app():
    app_running = True
    while app_running:
        choice = menu()
        if choice == '1':
            title = input('Title: ')
            author = input('Author: ')
            date_error = True
            while date_error: #handles errors in date formatting
                date = input('Published Date (Ex: October 25, 2017): ')
                date = clean_date(date)
                if type(date) == datetime.date: #conditional on variable data type
                    date_error = False
            price_error = True
            while price_error:
                price = input('Price (Ex: 35.96): ')
                price = clean_price(price)
                if type(price) == int:
                    price_error = False
            new_book = Book(title=title, author=author, published_date=date, price=price)
            session.add(new_book)
            session.commit()
            print('Book added')
            time.sleep(1.5)
        elif choice == '2':
            for book in session.query(Book):
                print(f'{book.id} | {book.title} | {book.author}')
            input('\nPress enter to return to the main menu.')
        elif choice == '3':
            id_options = []
            for book in session.query(Book):
                id_options.append(book.id)
            id_error = True
            while id_error:
                id_choice = input(f'''
                \nID Options: {id_options}
                \rBook ID:  ''')
                id_choice = clean_id(id_choice, id_options)
                if type(id_choice) == int:
                    id_error = False
            searched_book = session.query(Book).filter(Book.id==id_choice).first()
            print(f'''
            \n{searched_book.title} by {searched_book.author}
            \rPublished: {searched_book.published_date}
            \rPrice: £{searched_book.price / 100}
            ''')
            input('\nPress enter to return to main menu')
        elif choice == '4':
            #analysis
            pass
        else:
            print('Goodbye')
            app_running = False


# edit books
# delete books
# search books
# data cleaning
# loop runs program


if __name__ == '__main__':
    Base.metadata.create_all(engine)
    add_csv
    app()

    #for book in session.query(Book):
        #print(book)