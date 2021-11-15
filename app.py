from models import (Base, session, Book, engine)
import datetime
import csv


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
    month = int(months.index(split_date[0])) + 1 #takes the index 0 of date list (month in this case) and finds index of equivilent month in months list and returns its index + 1 as that is equal to the month number. ie Jan is index 0 so +1 =1st month
    day = int(split_date[1].split(',')[0]) #removes comma from the day element of list left from initial string split
    year = int(split_date[2])
    return datetime.date(year, month, day)


def clean_price(price_str):
    price_float = float(price_str)
    return int(price_float*100)


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
            #add book
            pass
        elif choice == '2':
            #view books
            pass
        elif choice == '3':
            #search for a book
            pass
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
    #app()
    add_csv()

    for book in session.query(Book):
        print(book)