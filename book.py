"""Skrypt opisujący klasę Book wraz możliwymimetodami do wykorzystania"""

#Bilioteki zewnętrzne
import datetime
import os
import time

import pyodbc

#Utworzenie klasy Book wraz z parametrami inicjalizującymi
class Book:
    def __init__(self, book_id=0, ISBN="", title="", pages="",
                 cover="", book_genre="", thumbnail="",
                 publisher="", published_year="", description="", state=1, author_id=("",)
                 ):
        self.book_id =book_id
        self.ISBN = ISBN
        self.title = title
        self.pages = pages
        self.cover = cover
        self.book_genre = book_genre
        self.thumbnail = thumbnail
        self.publisher = publisher
        self.published_year = published_year
        self.description = description
        self.state = state #domyślny status = 1,czyli książka dostępna
        self.author_id = author_id


    def book_add(self):
        # Wywołanie metody powoduje dodanie książki do tabeli tblBook.
        # Metoda powinna być tylko dostępna, gdy parametr librarian dla aktualnie pracującego użytkownika = 1
        # Atrybut state domyślnie przyjmuje wartość 1 - dostępna.

        # Wprowadzanie danych o książce
        self.ISBN = input("Wprowadź kod ISBN książki: ")
        self.title = input("Wprowadź tytuł książki: ")
        self.pages = int(input("Wprowadź liczbę stron książki: "))
        self.cover = input("Wprowadź rodzaj okładki twarda (h) czy miękka (s): ")
        self.book_genre = input("Wprowadź gatunek książki: ")
        self.thumbnail = input("Wprowadź adres do ikony książki: ")
        self.publisher = input("Wprowadź wydawcę książki: ")
        self.published_year = int(input("Wprowadź rok wydania książki: "))
        self.description = input("Wprowadź opis: ")
        #Zaczytanie lsty autorów:
        author_name = ()
        author_name_first = input("Wprowadż nazwę pierwszego autora: ")
        author_name = author_name + (author_name_first,)
        author_name_next = input("Wprowadż nazwę kolejnego autora lub 0: ")
        while author_name_next != '0':
            author_name = author_name + (author_name_next,)
            author_name_next = input("Wprowadż nazwę kolejnego autora lub 0: ")

        print(author_name)

        # Sprawdzanie czy autorzy istnieją w bazie
        self.author_id = self.author_id_search(author_name)
        print( {self.author_id} )


        # Połączenie do SQL
        db_msql = pyodbc.connect("Driver={SQL Server};"
                                 "Server=DELLV3510-01\SQLEXPRESS;"
                                 "Database=biblioteka;"
                                 "Trusted_connection =yes;")

        # Cursor
        cursorMS = db_msql.cursor()
        # Kwerenda dodająca atrybuty użytkownika do bazy
        query = "INSERT INTO tblBook(ISBN, title, pages, cover, book_genre, thumbnail, publisher, published_year, " \
                "description, state) " \
                "VALUES (?,?,?,?,?,?,?,?,?,?) "
        # Argumenty dodawane poprzez kwerendę
        arg = (self.ISBN, self.title, self.pages, self.cover, self.book_genre, self.thumbnail, self.publisher, self.published_year,
               self.description, self.state)
        # Wywołanie kwerendy
        cursorMS.execute(query, arg)
        # Zatwierdzenie wywołania kwerendy
        db_msql.commit()

        #ładujemy wartość book_id
        wynik_zapytania = cursorMS.execute("SELECT TOP (1) [book_id] FROM [biblioteka].[dbo].[tblBook] order by [book_id] desc")
        for row in wynik_zapytania:
            self.book_id = row[0]
        print(cursorMS.fetchall())
        db_msql.commit()

        #Tworzymy powiązanie pomiędzy book_id a author_id w bazie w tabeli tblAuthor_Book
        for i_author_id in self.author_id:
            # Połączenie do SQL
            db_msql = pyodbc.connect("Driver={SQL Server};"
                                     "Server=DELLV3510-01\SQLEXPRESS;"
                                     "Database=biblioteka;"
                                     "Trusted_connection =yes;")
            # Cursor
            cursorMS = db_msql.cursor()
            # Kwerenda dodająca atrybuty użytkownika do bazy
            query = "INSERT INTO tblAuthor_Book(author_id, book_id) VALUES (?,?) "
            # Argumenty dodawane poprzez kwerendę
            arg = (i_author_id, self.book_id)
            # Wywołanie kwerendy
            cursorMS.execute(query, arg)
            # Zatwierdzenie wywołania kwerendy
            db_msql.commit()

        # Zamknięcie połączenia z bazą
        db_msql.close()

        print("Książka została dodana do bazy \n")

        print("---------------------------------")
        print("Wybierz opcję: ")
        back = input("1 - Powrót do menu głównego ")

        if back == 1:
            return 1

    def book_delete(self):
        """Wywołanie metody powoduje usunięcie książki ze wskazanym parametrem book_id z tabali tblBook,
        tblAuthor_Book, tblBooking,tblBorrowing z bazy biblioteka"""

        # Opcja powinna być dostępna tylko po wejściu w daną książkę!


        # Połączenie do SQL
        db_msql = pyodbc.connect("Driver={SQL Server};"
                                 "Server=DELLV3510-01\SQLEXPRESS;"
                                 "Database=biblioteka;"
                                 "Trusted_connection =yes;")

        # Cursor
        cursorMS = db_msql.cursor()

        # Kwerenda usuwająca wiersze ze wskazanym book_id w bazie biblioteka
        query = "DELETE FROM tblBook WHERE book_id = ?;"

        # Argumenty dodawane poprzez kwerendę
        arg = (self.book_id)

        # Wywołanie kwerendy
        cursorMS.execute(query, arg)

        # Zatwierdzenie wywołania kwerendy
        db_msql.commit()

        # Zamknięcie połączenia z bazą
        db_msql.close()
        print("Książka została usunięta z bazy \n")
        print("---------------------------------")
        print("Wybierz opcję: ")
        back = input("1 - Powrót do menu głównego ")

        if back == 1:
            return 1

    def book_update(self):
        """Wywołanie metody powoduje aktualizację danych dotyczących kasiążki o wskazanym book_id"""
        # Opcja powinna być dostępna tylko po wejściu w daną książkę!

        old_parameters = (self.ISBN,self.title,self.pages,self.cover,self.book_genre,self.thumbnail,self.publisher,
                          self.published_year,self.description,self.state)

        self.ISBN = input("Zaktualizuj kod ISBN książki lub kliknij enter: ")
        self.title = input("Zaktualizuj tytuł książki lub kliknij enter: ")
        self.pages = int(input("Zaktualizuj liczbę stron książki lub kliknij enter: "))
        self.cover = input("Zaktualizuj rodzaj okładki twarda (h) czy miękka (s) lub kliknij enter: ")
        self.book_genre = input("Zaktualizuj gatunek książki lub kliknij enter: ")
        self.thumbnail = input("Zaktualizuj adres do ikony książki lub kliknij enter: ")
        self.publisher = input("Zaktualizuj wydawcę książki lub kliknij enter: ")
        self.published_year = int(input("Zaktualizuj rok wydania książki lub kliknij enter: "))
        self.description = input("Zaktualizuj opis lub kliknij enter: ")
        self.state = int(input("Zaktualizuj status książki 1 - dostępna, 2 - zarezerwowana, 3 - wypożyczona lub kliknij enter: "))

        updated_parameters = (self.ISBN,self.title,self.pages,self.cover,self.book_genre,self.thumbnail,self.publisher,
                          self.published_year,self.description,self.state)

        new_parameters = ()

        for i in range(len(updated_parameters)):
            if updated_parameters[i] == "":
                new_parameters = new_parameters + old_parameters[i]
            else:
                new_parameters = new_parameters + updated_parameters[i]


        # Połączenie do SQL
        db_msql = pyodbc.connect("Driver={SQL Server};"
                                 "Server=DELLV3510-01\SQLEXPRESS;"
                                 "Database=biblioteka;"
                                 "Trusted_connection =yes;")

        # Cursor
        cursorMS = db_msql.cursor()

        # Kwerenda dodająca atrybuty użytkownika do bazy
        query = """UPDATE [dbo].[tblBook]
                    SET    [ISBN] = ?
                          ,[title] = ?
                          ,[pages] = ?
                          ,[cover] = ?
                          ,[book_genre] = ?
                          ,[thumbnail] = ?
                          ,[publisher] = ?
                          ,[published_year] = ?
                          ,[description] = ?
                          ,[state] = ?
                    WHERE book_id = ? """


        # Argumenty dodawane poprzez kwerendę
        arg = (self.ISBN, self.title, self.pages, self.cover, self.book_genre, self.thumbnail, self.publisher, self.published_year,
               self.description, self.state, self.book_id)

        # Wywołanie kwerendy
        cursorMS.execute(query, arg)

        # Zatwierdzenie wywołania kwerendy
        db_msql.commit()

        # Zamknięcie połączenia z bazą
        db_msql.close()
        print("Dane książki zostały zaktualizowane \n")
        print("---------------------------------")
        print("Wybierz opcję: ")
        back = input("1 - Powrót do menu głównego ")

        if back == 1:
            return 1

    def author_id_search(self,author_name):
        # Połączenie do SQL
        db_msql = pyodbc.connect("Driver={SQL Server};"
                                 "Server=DELLV3510-01\SQLEXPRESS;"
                                 "Database=biblioteka;"
                                 "Trusted_connection =yes;")
        # Cursor
        cursorMS = db_msql.cursor()

        # Sprawdzanie czy author istnieje w bazie
        wynik_zapytania = cursorMS.execute(
            f"SELECT author_id FROM [biblioteka].[dbo].[tblAuthor] WHERE name IN {author_name}")
        #zdefiniowanietypuzmiennej author_id jako tuple
        author_id =()

        #wyciągnięcie wszystkich autorów z bazy i przypisanie ich do krotki author_id
        for row in wynik_zapytania:
            author_id+=(row[0],)

        db_msql.commit()
        # sprawdzenie czy są wstawieni autorzy
        if len(author_id) == 0:
            print(f"Brak autora o nazwie {author_name} w bazie. Proszę dodaj nowego authora lub sprawdź poprawnosć nazwy")
        else:
            return (author_id)

        print("---------------------------------")
        print("Wybierz opcję: ")
        back = input("1 - Powrót do menu głównego ")

        if back == 1:
            return 1

    def book_search(self):
        """Wywołanie metody powoduje wyszukanie książki po parametrach book_id, title, book_genre, state"""
        # metoda nie jest przypisana do klasy book!

        book_id = int(input("Wprowadź id_książki lub wprowadź 0: "))
        title = input("Wprowadź fragment tytułu lub zostaw wartość pustą: ")
        book_genre = input("Wprowadź gatunek lub zostaw wartość pustą: ")
        state = int(input("Wprowadż status 1 - dostępna, 2 - zarezerwowana, 3 - wypożyczona: "))

        # Połączenie do SQL
        db_msql = pyodbc.connect("Driver={SQL Server};"
                                 "Server=DELLV3510-01\SQLEXPRESS;"
                                 "Database=biblioteka;"
                                 "Trusted_connection =yes;")

        # Cursor
        cursorMS = db_msql.cursor()
        # Kwerenda pozwalająca na wyszukiwanie książki.
        query = """SELECT * FROM [dbo].[tblBook]  
                   WHERE
                   ([book_id] = ? OR
                   CHARINDEX(?, [title], 1) <> 0 OR
                   CHARINDEX(?, [book_genre], 1) <> 0) AND
                   [state] = ? ;"""

        # Argumenty dodawane poprzez kwerendę
        arg = (book_id, title,  book_genre, state)

        # Wywołanie kwerendy
        cursorMS.execute(query,arg)
        wynik_zapytania = cursorMS.fetchall()
        os.system('cls')
        print("---------------------------------")
        print("Wyniki wyszukiwania:")
        for row in wynik_zapytania:

            print(f" book_id: {row[0]}; title: {row[2]}; genre: {row[5]} ")

        # Zatwierdzenie wywołania kwerendy
        db_msql.commit()

        # Zamknięcie połączenia z bazą
        db_msql.close()
        print("---------------------------------")
        print("Wybierz opcję: ")
        back = input("1 - Powrót do menu głównego ")

        if back == 1:
            return 1

    def book_selection(self):
        """Wywołanie metody powoduje wybranie książki o podanym parametrze book_id"""
        # metoda nie jest przypisana do klasy book!

        book_id = int(input("Wprowadź id_książki: "))

        # Połączenie do SQL
        db_msql = pyodbc.connect("Driver={SQL Server};"
                                 "Server=DELLV3510-01\SQLEXPRESS;"
                                 "Database=biblioteka;"
                                 "Trusted_connection =yes;")

        # Cursor
        cursorMS = db_msql.cursor()
        # Kwerenda pozwalająca na wyszukiwanie książki.
        query = """SELECT * FROM [dbo].[tblBook]  
                   WHERE [book_id] = ?;"""

        # Argumenty dodawane poprzez kwerendę
        arg = (book_id)

        # Wywołanie kwerendy
        cursorMS.execute(query,arg)
        wynik_zapytania = cursorMS.fetchall()
        for row in wynik_zapytania:
            if row[0]>0:
                # załadowanie wartości do instancji klasy Book
                self.book_id = book_id
                self.ISBN = row[1]
                self.title = row[2]
                self.pages = row[3]
                self.cover = row[4]
                self.book_genre = row[5]
                self.thumbnail = row[6]
                self.publisher = row[7]
                self.published_year = row[8]
                self.description = row[9]
                self.state = row[10]


                print("---------------------------------")
                print("Wyniki wyszukiwania:\n")
                print(f"book_id: {self.book_id}\n"
                      f"ISBN: {self.ISBN}\n"
                      f"title: {self.title}\n"
                      f"pages: {self.pages}\n"
                      f"cover: {self.cover} (h-hardback, s -softback)\n"
                      f"genre: {self.book_genre}\n"
                      f"thumbnail: {self.thumbnail }\n"              
                      f"publisher: {self.publisher}\n"              
                      f"year: {self.published_year}\n"
                      f"description: {self.description}\n"                           
                      f"state: {self.state} (1-dostępna,2-zarezerwowana,3-wypożyczona)\n")

                print("---------------------------------")
                print("Wybierz opcję: ")
                back = input("1 - Powrót do menu głównego ")

                if back == 1:
                    return 1
            else:
                print(f"\n Książka o podanym id: {book_id} nie występuje w bazie\n")
                time.sleep(5)
                break

        # Zatwierdzenie wywołania kwerendy
        db_msql.commit()

        # Zamknięcie połączenia z bazą
        db_msql.close()

        print("---------------------------------")
        print("Wybierz opcję: ")
        back = input("1 - Powrót do menu głównego ")

        if back == 1:
            return 1

    def book_booking(self,user_id):
        """Wywołanie metody powoduje zarezerwowanie książki, którą aktualnie oglądamy"""
        # metoda przypisana do klasy book!


        # Połączenie do SQL
        db_msql = pyodbc.connect("Driver={SQL Server};"
                                 "Server=DELLV3510-01\SQLEXPRESS;"
                                 "Database=biblioteka;"
                                 "Trusted_connection =yes;")

        # Cursor
        cursorMS = db_msql.cursor()

        # Kwerenda dodająca atrybuty użytkownika do bazy
        query = """UPDATE [dbo].[tblBook]
                    SET    [state] = ?
                    WHERE book_id = ? """


        # Argumenty dodawane poprzez kwerendę
        arg = (2, self.book_id)

        # Wywołanie kwerendy
        cursorMS.execute(query, arg)

        # Zatwierdzenie wywołania kwerendy
        db_msql.commit()

        starttime = str(datetime.date.today())
        endtime = str(datetime.date.today() + datetime.timedelta(days=31))

        # Kwerenda dodająca atrybuty użytkownika do bazy
        query = "INSERT INTO tblBooking(user_id,book_id,starttime,endtime) " \
                "VALUES (?,?,?,?) "

        # Argumenty dodawane poprzez kwerendę
        arg = (user_id, self.book_id, starttime, endtime)

        # Wywołanie kwerendy
        cursorMS.execute(query, arg)

        # Zatwierdzenie wywołania kwerendy
        db_msql.commit()

        # Zamknięcie połączenia z bazą
        db_msql.close()

        print(f"\nKsiążka o podanym id: {self.book_id} została zarezerwowana dla użytkownika o id: {user_id} \n")
        print("---------------------------------")
        print("Wybierz opcję: ")
        back = input("1 - Powrót do menu głównego ")

        if back == 1:
            return 1

    def book_borrowing(self,user_id):
        """Wywołanie metody powoduje wypożyczenie książki, którą aktualnie oglądamy"""
        # metoda przypisana do klasy book!


        # Połączenie do SQL
        db_msql = pyodbc.connect("Driver={SQL Server};"
                                 "Server=DELLV3510-01\SQLEXPRESS;"
                                 "Database=biblioteka;"
                                 "Trusted_connection =yes;")

        # Cursor
        cursorMS = db_msql.cursor()

        # Kwerenda dodająca atrybuty użytkownika do bazy
        query = """UPDATE [dbo].[tblBook]
                    SET    [state] = ?
                    WHERE book_id = ? """


        # Argumenty dodawane poprzez kwerendę
        arg = (3, self.book_id)

        # Wywołanie kwerendy
        cursorMS.execute(query, arg)

        # Zatwierdzenie wywołania kwerendy
        db_msql.commit()

        starttime = str(datetime.date.today())
        endtime = str(datetime.date.today() + datetime.timedelta(days=2))

        # Kwerenda dodająca atrybuty użytkownika do bazy
        query = "INSERT INTO tblBorrowing(user_id,book_id,starttime,endtime) " \
                "VALUES (?,?,?,?) "

        # Argumenty dodawane poprzez kwerendę
        arg = (user_id,self.book_id,starttime,endtime)

        # Wywołanie kwerendy
        cursorMS.execute(query, arg)

        # Zatwierdzenie wywołania kwerendy
        db_msql.commit()

        # Zamknięcie połączenia z bazą
        db_msql.close()
        print(f"Książka {self.book_id} została wypożyczona dla użytkownika {user_id}\n")
        print("---------------------------------")
        print("Wybierz opcję: ")
        back = input("1 - Powrót do menu głównego ")

        if back == 1:
            return 1


    def book_review_add(self,user_id):
        """Wywołanie metody powoduje dodanie recenzji i oceny książki, którą aktualnie oglądamy"""
        # metoda przypisana do klasy book!

        stars = int(input("Wprowadź liczbę gwiazdek od 1 do 5: "))
        review = input("Wprowadź recenzję książki: ")


        # Połączenie do SQL
        db_msql = pyodbc.connect("Driver={SQL Server};"
                                 "Server=DELLV3510-01\SQLEXPRESS;"
                                 "Database=biblioteka;"
                                 "Trusted_connection =yes;")

        # Cursor
        cursorMS = db_msql.cursor()

        # Kwerenda dodająca atrybuty użytkownika do bazy
        query = "INSERT INTO tblReview(book_id,user_id,stars,review) " \
                "VALUES (?,?,?,?) "


        # Argumenty dodawane poprzez kwerendę
        arg = (self.book_id,user_id, stars, review) #zamiast 1 należy wprowadzić id USera integracja z kodem Artura

        # Wywołanie kwerendy
        cursorMS.execute(query, arg)

        # Zatwierdzenie wywołania kwerendy
        db_msql.commit()

        # Zamknięcie połączenia z bazą
        db_msql.close()
        print("\nTwoja opinia została dodana \n")
        print("---------------------------------")
        print("Wybierz opcję: ")
        back = input("1 - Powrót do menu głównego ")

        if back == 1:
            return 1

    def book_review_show(self):
        """Wywołanie metody powoduje wyświetlenie recenzji i ocen książki, którą aktualnie oglądamy"""
        # metoda przypisana do klasy book!

        # Połączenie do SQL
        db_msql = pyodbc.connect("Driver={SQL Server};"
                                 "Server=DELLV3510-01\SQLEXPRESS;"
                                 "Database=biblioteka;"
                                 "Trusted_connection =yes;")

        # Cursor
        cursorMS = db_msql.cursor()
        # Kwerenda pozwalająca na wyszukiwanie książki.
        query = """SELECT * FROM [dbo].[vReview]  
                   WHERE [book_id] = ?;"""

        # Argumenty dodawane poprzez kwerendę
        arg = (self.book_id)

        # Wywołanie kwerendy
        cursorMS.execute(query,arg)
        wynik_zapytania = cursorMS.fetchall()
        i = 0
        for row in wynik_zapytania:
            if row[0]>0:
                i += 1
                # załadowanie wartości do instancji klasy Book
                review_id = row[0]
                stars = row[1]
                review = row[2]
                title = row[3]
                ISBN = row[4]
                name = row[5]
                surname = row[6]

                print(f"###{i}###\n"
                      f"review_id: {review_id}\n"
                      f"stars: {stars}\n"
                      f"review: {review}\n"
                      f"title: {title}\n"
                      f"ISBN: {ISBN}\n"
                      f"Autor opinii: {name} {surname}\n\n")
            else:
                print(f"Książka nie posiada jeszcze recenzji")
                break

        # Zatwierdzenie wywołania kwerendy
        db_msql.commit()

        # Zamknięcie połączenia z bazą
        db_msql.close()

        print("---------------------------------")
        print("Wybierz opcję: ")
        back = input("1 - Powrót do menu głównego ")

        if back == 1:
            return 1

    def book_return_booking(self,user_id):
        """Wywołanie metody powoduje zarezerwowanie książki, którą aktualnie oglądamy"""
        # metoda przypisana do klasy book!


        # Połączenie do SQL
        db_msql = pyodbc.connect("Driver={SQL Server};"
                                 "Server=DELLV3510-01\SQLEXPRESS;"
                                 "Database=biblioteka;"
                                 "Trusted_connection =yes;")

        # Cursor
        cursorMS = db_msql.cursor()

        # Kwerenda dodająca atrybuty użytkownika do bazy
        query = """UPDATE [dbo].[tblBook]
                    SET    [state] = ?
                    WHERE book_id = ? """


        # Argumenty dodawane poprzez kwerendę
        arg = (1, self.book_id)

        # Wywołanie kwerendy
        cursorMS.execute(query, arg)

        # Zatwierdzenie wywołania kwerendy
        db_msql.commit()

        # Kwerenda aktualizująca endtime książki w tabeli tblBooking
        query = """UPDATE [dbo].[tblBooking]
                    SET    endtime = ?
                    WHERE book_id = ? AND user_id = ?"""


        # Argumenty dodawane poprzez kwerendę
        arg = (str(datetime.date.today()), self.book_id, user_id)

        # Wywołanie kwerendy
        cursorMS.execute(query, arg)

        # Zatwierdzenie wywołania kwerendy
        db_msql.commit()

        # Zamknięcie połączenia z bazą
        db_msql.close()
        print("Odwołano rezerwacje książki \n")
        print("---------------------------------")
        print("Wybierz opcję: ")
        back = input("1 - Powrót do menu głównego ")

        if back == 1:
            return 1

    def book_return_borrowing(self,user_id):
        """Wywołanie metody powoduje zarezerwowanie książki, którą aktualnie oglądamy"""
        # metoda przypisana do klasy book!

        # Połączenie do SQL
        db_msql = pyodbc.connect("Driver={SQL Server};"
                                 "Server=DELLV3510-01\SQLEXPRESS;"
                                 "Database=biblioteka;"
                                 "Trusted_connection =yes;")

        # Cursor
        cursorMS = db_msql.cursor()

        # Kwerenda dodająca atrybuty użytkownika do bazy
        query = """UPDATE [dbo].[tblBook]
                       SET    [state] = ?
                       WHERE book_id = ? """

        # Argumenty dodawane poprzez kwerendę
        arg = (1, self.book_id)

        # Wywołanie kwerendy
        cursorMS.execute(query, arg)

        # Zatwierdzenie wywołania kwerendy
        db_msql.commit()

        # Kwerenda aktualizująca endtime książki w tabeli tblBooking
        query = """UPDATE [dbo].[tblBorrowing]
                       SET    endtime = ?
                       WHERE book_id = ? AND user_id = ?"""

        # Argumenty dodawane poprzez kwerendę
        arg = (str(datetime.date.today()), self.book_id, user_id)

        # Wywołanie kwerendy
        cursorMS.execute(query, arg)

        # Zatwierdzenie wywołania kwerendy
        db_msql.commit()

        # Zamknięcie połączenia z bazą
        db_msql.close()
        print("Książka została oddana \n")
        print("---------------------------------")
        print("Wybierz opcję: ")
        back = input("1 - Powrót do menu głównego ")

        if back == 1:
            return 1


    def book_search_as(self,book_id):


        """Pobranie danych z bazy dla danej książki"""


        self.book_id = book_id

        # Połączenie do SQL
        db_msql = pyodbc.connect("Driver={SQL Server};"
                                 "Server=DELLV3510-01\SQLEXPRESS;"
                                 "Database=biblioteka;"
                                 "Trusted_connection =yes;")

        # Cursor
        cursorMS = db_msql.cursor()

        # Kwerenda dodająca atrybuty użytkownika do bazy
        query = "SELECT * FROM tblBook WHERE book_id = ?;"

        # Argumenty dodawane poprzez kwerendę
        arg = (self.book_id)

        # Wywołanie kwerendy
        cursorMS.execute(query, arg)


        # Zatwierdzenie wywołania kwerendy
        #db_msql.commit()

        result = [self.book_id, self.ISBN,self.title,self.pages,self.cover,self.book_genre,self.thumbnail,self.publisher, self.published_year,self.description, self.state]

        for row in cursorMS:
            print(row)
            for index in range(1,len(result)):

                result[index] = row[index]
        book_id = result[0]
        result = result[1:]
        # Zamknięcie połączenia z bazą
        db_msql.close()


        if result[0] == "":
            print("Brak książki o danym ID")

        print(result, book_id)
        return result,book_id
# Test dodania książki do listy - działa :)
# Book1 = Book()
# print(Book1.book_add())
#
# # Test usunięcia książki z listy - działa :)
# print(Book1.book_delete())

# Test aktualizacji książki z listy - działa :)
# print(Book1.book_update())

# Test funkcji book_search - działa :)
# print(book_search())

# Test funkcji book_selection - działa :)
# Book1 = Book()
# print(Book1.book_selection())

# # Test funkcji book_booking - działa :)
# print(Book1.book_booking())

# Test funkcji book_borrowing - działa :)
# print(Book1.book_borrowing())

# Test funkcji book_review_add - działa :)
# print(Book1.book_review_add())

# Test funkcji book_review_show - działa :)
# print(Book1.book_review_show())

# Test funkcji book_return_booking - działa :)
# print(Book1.book_return_booking())

# Test funkcji book_return_borrowing - działa :)
# print(Book1.book_return_borrowing())
