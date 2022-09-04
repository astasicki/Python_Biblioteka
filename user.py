import pyodbc
import datetime
from datetime import datetime, timedelta
import pandas as pd
import time
import os




class User:
    def __init__(self,name = "", surname = "", birth_date ="", pesel = "",
                 email= "", password= "", phone= "",
                 gender= "", city= "", street= "", house_no= "",
                 librarian= "", false_login_counter= "",
                 false_login_date= "" ):
        self.name = name
        self.surname = surname
        self.birth_date = birth_date
        self.pesel = pesel
        self.email = email
        self.password = password
        self.phone = phone
        self.gender = gender
        self.city = city
        self.street = street
        self.house_no = house_no
        self.librarian = librarian
        self.false_login_counter = false_login_counter
        self.false_login_date = false_login_date


    def user_add(self):

        """Wywołanie metody powoduje dodanie użytkownika do bazy.
        Atrybut librarian domyślnie przujmuje wartość 0. Może ona zostać zmieniona jedynie przez administratora.
        Atrybuty false_login_counter, false_login_date, actual_borrowing_number, actual_booking_number domyślnie przyjmują wartość 0. """

        #POBRANIE DANYCH OD UŻYTKOWNIKA
        self.name = input("Podaj swoje imię: ").upper()
        self.surname = input("Podaj swoje nazwisko: ").upper()
        self.birth_date = input("Podaj swoją datę urodzenia (RRRR-MM-DDD): ")
        self.pesel = input("Podaj swój PESEL: ")
        self.email = input("Podaj swój adres e-mail: ")
        self.password = input("Podaj hasło do swojego konta: ")
        self.phone = input("Podaj swój numer telefonu: ")
        self.gender = input("Podaj swoją płeć (M,F): ").lower()
        self.city = input("Podaj nazwę miejscowości, w której mieszkasz: ")
        self.street = input("Podaj ulicę, przy której mieszkasz: ")
        self.house_no = input("Podaj swój numer budynku/mieszkania: ")
        self.librarian = 0
        self.false_login_counter = 0
        self.false_login_date = "1900-01-01 00:00:00"


        #Połączenie do SQL
        db_msql = pyodbc.connect("Driver={SQL Server};"
                                 "Server=DELLV3510-01\SQLEXPRESS;"
                                 "Database=biblioteka;"
                                 "Trusted_connection =yes;")

        #Cursor
        cursorMS = db_msql.cursor()

        emails = []
        for row_log in cursorMS.execute('SELECT email FROM tblUser'):
            emails.append("".join(row_log))

        if self.email in emails:
            print("------------------------------------------")
            print(f"Użytkownik o adresie {self.email} widnieje w bazie użytkowników - zaloguj się")
            time.sleep(4)
            os.system('cls')
            return 0


        #Kwerenda dodająca atrybuty użytkownika do bazy
        query = "INSERT INTO tblUser(name, surname, birth_date,pesel, email, password, phone, gender, city, street, house_no, librarian, false_login_counter, false_login_date) " \
                "VALUES (?,?,CONVERT(datetime,?,120),?,?,?,?,?,?,?,?,?,?,CONVERT(datetime,?,120)) "

        #Argumenty dodawane poprzez kwerendę
        arg = (self.name, self.surname, self.birth_date, self.pesel, self.email, self.password, self.phone, self.gender, self.city,
               self.street, self.house_no, self.librarian, self.false_login_counter, self.false_login_date)

        try:

            #Wywołanie kwerendy
            cursorMS.execute(query, arg)

            #Zatwierdzenie wywołania kwerendy
            db_msql.commit()

            #Zamknięcie połączenia z bazą
            db_msql.close()

            time.sleep(4)
            os.system('cls')
            return 1

        except:
            print("------------------------------------------")
            print("Wprowadzono błędne dane - spróbuj ponownie")
            time.sleep(4)
            os.system('cls')
            return 0



    def user_delete(self, user_id):

        """Wywołanie metody powoduje usunięcie użytkownika z bazy danych (wartości wszystkich atrybutów w bazie) dla wskazanego user_id"""


        self.user_id = user_id

        # Połączenie do SQL
        db_msql = pyodbc.connect("Driver={SQL Server};"
                                 "Server=DELLV3510-01\SQLEXPRESS;"
                                 "Database=biblioteka;"
                                 "Trusted_connection =yes;")

        # Cursor
        cursorMS = db_msql.cursor()

        # Kwerenda dodająca atrybuty użytkownika do bazy
        table = ['tblBorrowing','tblBooking','tblReview','tblUser']

        for tbl in table:

            query = f"DELETE FROM {tbl} WHERE user_id = ?"



            # Argumenty dodawane poprzez kwerendę
            arg = (self.user_id)

            # Wywołanie kwerendy
            cursorMS.execute(query, arg)

            # Zatwierdzenie wywołania kwerendy
            db_msql.commit()

        # Zamknięcie połączenia z bazą
        db_msql.close()

    def user_search(self,user_id):


        """Pobranie danych z bazy dla danego użytkownika"""


        self.user_id = user_id

        # Połączenie do SQL
        db_msql = pyodbc.connect("Driver={SQL Server};"
                                 "Server=DELLV3510-01\SQLEXPRESS;"
                                 "Database=biblioteka;"
                                 "Trusted_connection =yes;")

        # Cursor
        cursorMS = db_msql.cursor()

        # Kwerenda dodająca atrybuty użytkownika do bazy
        query = "SELECT * FROM tblUser WHERE user_id = ?;"

        # Argumenty dodawane poprzez kwerendę
        arg = (self.user_id)

        # Wywołanie kwerendy
        cursorMS.execute(query, arg)


        # Zatwierdzenie wywołania kwerendy
        #db_msql.commit()

        result = [self.name, self.surname, self.birth_date, self.pesel, self.email, self.password, self.phone,
                  self.gender, self.city, self.street, self.house_no, self.librarian, self.false_login_counter, self.false_login_date]




        for row in cursorMS:


            for index in range(1,len(result)+1):

                result[index-1] = row[index]

        # Zamknięcie połączenia z bazą
        db_msql.close()


        if result[0] == "":
            print("Brak użytkownika o danym ID")

        return result,user_id

    def user_update(*args):

        """Wywołanie metody powoduje zaktualizowanie wartości atrybutów w bazie danych.
        Domyślnie atrybuty przyjmują wartości aktualnie występujące w bazie.
        Użytkownik wprowadza zmianę i po zatwierdzeniu wartość jest wprowadzana do bazy"""

        arr = list(args)


        #print(arr[1])
        print(arr[1][0])
        #print(arr[1][1])


        name, surame, birth_date,pesel, email, password, number, gender, city, street, house_no,librarian, false_login_counter, false_login_date = arr[1][0]
        user_id = arr[1][1]



        print("Aktualizacja danych:")
        print("Jeśli nie chcesz aktalizować danej to kliknij Enter. W przeciwnym przypadku wpisz zaktualizowaną daną")
        new_name = input("Podaj swoje imię: ").upper()
        new_surname = input("Podaj swoje nazwisko: ").upper()
        new_birth_date = input("Podaj swoją datę urodzenia (RRRR-MM-DDD): ")
        new_pesel = input("Podaj swój PESEL: ")
        new_email = input("Podaj swój adres e-mail: ")
        new_password = input("Podaj hasło do swojego konta: ")
        new_phone = input("Podaj swój numer telefonu: ")
        new_gender = input("Podaj swoją płeć (M/F): ").lower()
        new_city = input("Podaj nazwę miejscowości, w której mieszkasz: ")
        new_street = input("Podaj ulicę, przy której mieszkasz: ")
        new_house_no = input("Podaj swój numer budynku: ")
        new_librarian = librarian
        new_false_login_counter = false_login_counter
        new_false_login_date = false_login_date


        old_data = [name, surame, birth_date, pesel, email, password, number, gender, city, street, house_no,librarian, false_login_counter, false_login_date]
        new_data = [new_name, new_surname, new_birth_date, new_pesel, new_email, new_password, new_phone, new_gender, new_city, new_street, new_house_no,new_librarian, new_false_login_counter, new_false_login_date]

        for i in range(len(old_data)):

            if new_data[i] != "":
                old_data[i] = new_data[i]

        print(old_data)
        #Połączenie do SQL
        db_msql = pyodbc.connect("Driver={SQL Server};"
                                 "Server=DELLV3510-01\SQLEXPRESS;"
                                 "Database=biblioteka;"
                                 "Trusted_connection =yes;")

        #Cursor
        cursorMS = db_msql.cursor()


        #Kwerenda dodająca atrybuty użytkownika do bazy
        #query = "INSERT INTO tblUser(name, surname, birth_date, email, password, phone, gender, city, street, house_no, librarian, false_login_counter, false_login_date, actual_borrowing_number, actual_booking_number) " \
         #       "VALUES (?,?,CONVERT(datetime,?,120),?,?,?,?,?,?,?,?,?,CONVERT(datetime,?,120),?,?) "


        query = "UPDATE tblUser " \
                "SET name = ?, surname = ?, birth_date = CONVERT(datetime,?,120),PESEL = ?, email = ?, password = ?, phone = ?, gender = ?, city = ?, street = ?, house_no = ?, librarian = ?,false_login_counter = ?, false_login_date = CONVERT(datetime,?,120)" \
                "WHERE user_id = ?;"
        #Argumenty dodawane poprzez kwerendę
        old_data.append(user_id)
        for i in old_data:
            print(i)
        arg = old_data

        #Wywołanie kwerendy
        cursorMS.execute(query, arg)

        #Zatwierdzenie wywołania kwerendy
        db_msql.commit()

        #Zamknięcie połączenia z bazą
        db_msql.close()

    def user_booking(self,user_id):

        """Wywołanie metody powoduje wyświetlenie zarezerwowanych przez użytkownika książek """

        self.user_id = user_id

        # Połączenie do SQL
        db_msql = pyodbc.connect("Driver={SQL Server};"
                                 "Server=DELLV3510-01\SQLEXPRESS;"
                                 "Database=biblioteka;"
                                 "Trusted_connection =yes;")

        # Cursor
        cursorMS = db_msql.cursor()

        # Kwerenda dodająca atrybuty użytkownika do bazy
        query = "SELECT * FROM tblBooking WHERE user_id = ?"


        # Argumenty dodawane poprzez kwerendę
        arg = (self.user_id)

        # Wywołanie kwerendy
        cursorMS.execute(query, arg)

        book_ids = []
        for row in cursorMS:

            book_ids.append(row[2])

        index = 0
        print("Lista Twoich zarezerowanych książek")
        for book in book_ids:

        # Kwerenda dodająca atrybuty użytkownika do bazy
            query = "SELECT * FROM tblBook WHERE book_id = ?"

        # Argumenty dodawane poprzez kwerendę
            arg = book


        # Wywołanie kwerendy
            cursorMS.execute(query, arg)


            oprawa = {"h":"Twarda",
                      "s":"Miękka"}

            for row in cursorMS:
                index += 1
                print(f"-------- KSIĄŻKA NR {index} --------")
                print(f"ISBN: {row[1]}")
                print(f"Tytuł: {row[2]}")
                print(f"Liczba stron: {row[3]}")
                print(f"Oprawa: {oprawa[row[4]]}")
                print(f"Gatunek: {row[5]}")
                print(f"Link: {row[6]}")
                print(f"Wydawnictwo: {row[7]}")
                print(f"Rok wydania: {row[8]}")
                print(f"Opis: {row[9]}")
                print("\n")





        # Zamknięcie połączenia z bazą
        db_msql.close()

    def user_borrowing(self,user_id):

        """Wywołanie metody powoduje wyświetlenie wypożyczonych przez użytkownika książek """

        self.user_id = user_id

        # Połączenie do SQL
        db_msql = pyodbc.connect("Driver={SQL Server};"
                                 "Server=DELLV3510-01\SQLEXPRESS;"
                                 "Database=biblioteka;"
                                 "Trusted_connection =yes;")

        # Cursor
        cursorMS = db_msql.cursor()

        # Kwerenda dodająca atrybuty użytkownika do bazy
        query = "SELECT * FROM tblBorrowing WHERE user_id = ?"


        # Argumenty dodawane poprzez kwerendę
        arg = (self.user_id)

        # Wywołanie kwerendy
        cursorMS.execute(query, arg)

        book_ids = []
        for row in cursorMS:

            book_ids.append(row[2])

        index = 0
        print("Lista Twoich wypożyczonych książek")
        for book in book_ids:

        # Kwerenda dodająca atrybuty użytkownika do bazy
            query = "SELECT * FROM tblBook WHERE book_id = ?"

        # Argumenty dodawane poprzez kwerendę
            arg = book


        # Wywołanie kwerendy
            cursorMS.execute(query, arg)


            oprawa = {"h":"Twarda",
                      "s":"Miękka"}

            for row in cursorMS:
                index += 1
                print(f"-------- KSIĄŻKA NR {index} --------")
                print(f"ISBN: {row[1]}")
                print(f"Tytuł: {row[2]}")
                print(f"Liczba stron: {row[3]}")
                print(f"Oprawa: {oprawa[row[4]]}")
                print(f"Gatunek: {row[5]}")
                print(f"Link: {row[6]}")
                print(f"Wydawnictwo: {row[7]}")
                print(f"Rok wydania: {row[8]}")
                print(f"Opis: {row[9]}")
                print("\n")





        # Zamknięcie połączenia z bazą
        db_msql.close()

    def user_longer_endtime (self,user_id,book_id):

        """Wywołanie metody powoduje wydłużenie wypożyczenia książki o kolejny miesiąc, tj. zwiększenie atrybutu endtime o 31 dni.  """

        # Połączenie do SQL
        db_msql = pyodbc.connect("Driver={SQL Server};"
                                 "Server=DELLV3510-01\SQLEXPRESS;"
                                 "Database=biblioteka;"
                                 "Trusted_connection =yes;")

        # Cursor
        cursorMS = db_msql.cursor()

        # Kwerenda dodająca atrybuty użytkownika do bazy
        query = "SELECT endtime FROM tblBorrowing WHERE user_id = ? and book_id = ?"

        # Argumenty dodawane poprzez kwerendę
        arg = (user_id, book_id)

        # Wywołanie kwerendy
        cursorMS.execute(query, arg)

        for time in cursorMS:

            date_time_obj = time[0]

            new_endtime = (datetime.strptime(date_time_obj, '%Y-%m-%d') + timedelta(days = 31)).date()


        query = "UPDATE tblBorrowing " \
                "SET endtime = CONVERT(datetime,?,120) " \
                "WHERE user_id = ? AND book_id = ?;"


        #Argumenty
        arg = [str(new_endtime),user_id,book_id]

        # Wywołanie kwerendy
        cursorMS.execute(query, arg)

        # Zatwierdzenie wywołania kwerendy
        db_msql.commit()

        # Zamknięcie połączenia z bazą
        db_msql.close()

    def user_penalty(self,user_id):

        """Wywołanie metody powoduje podliczenie kary dla użytkownika.
        Kara naliczana jest jako różnica pomiędzy wartością atrybutu endtime a aktualną datą,
        pomnożona przez 2zł, tj. 2zł za każdy dzień wykroczenia dla każdej książki. """

        # Połączenie do SQL
        db_msql = pyodbc.connect("Driver={SQL Server};"
                                 "Server=DELLV3510-01\SQLEXPRESS;"
                                 "Database=biblioteka;"
                                 "Trusted_connection =yes;")

        # Cursor
        cursorMS = db_msql.cursor()

        # Kwerenda dodająca atrybuty użytkownika do bazy
        query = "SELECT book_id, endtime FROM tblBorrowing WHERE user_id = ? and endtime < GETDATE()"

        # Argumenty dodawane poprzez kwerendę
        arg = (user_id)

        # Wywołanie kwerendy
        cursorMS.execute(query, arg)
        books = []
        terms = []
        penaltys = []

        for row in cursorMS:

            book = row[0]
            endtime = datetime.strptime(row[1], "%Y-%m-%d").date()
            terms.append(endtime)
            books.append(book)



            actual_time = datetime.now().date()
            diff_time = (actual_time - endtime)
            penalty = diff_time.days * 2
            penaltys.append(penalty)



        titles = []
        for book in books:

        # Kwerenda dodająca atrybuty użytkownika do bazy
            query = "SELECT title FROM tblBook WHERE book_id = ?"


        # Argumenty dodawane poprzez kwerendę
            arg = book

        # Wywołanie kwerendy
            cursorMS.execute(query, arg)

            for book in cursorMS:
                titles.append(book)

        print("Podusmowanie kar:")
        for index,title in enumerate(titles):
            print(f"Książka: {title}, Termin wypożyczenia: {terms[index]}, Naliczona kara: {penaltys[index]} zł")





        df = pd.DataFrame(columns = ['Tytul', 'Kara, zl'])
        df['Tytul'] = titles
        df['Kara, zl'] = penaltys

        eksport = input("Czy chcesz wyeksportować raport? Nie - Enter, Tak - T").upper()
        if eksport =="T":
            df.to_csv(r"C:\Users\a.sochaj\PycharmProjects\BIBLIOTEKA\kary.csv",index = False)


        return df

    def user_login(self):

        email = self.email
        haslo = self.password

        # Połączenie do SQL
        db_msql = pyodbc.connect("Driver={SQL Server};"
                                 "Server=DELLV3510-01\SQLEXPRESS;"
                                 "Database=biblioteka;"
                                 "Trusted_connection =yes;")

        # Cursor
        cursorMS = db_msql.cursor()

        emails = []
        for row_log in cursorMS.execute('SELECT email FROM tblUser'):
            emails.append("".join(row_log))

        if email not in emails:
            print(f"Użytkownik o adresie {self.email} nie widnieje w bazie użytkowników.")
            print("Spróbuj ponownie lub zarejestruj się w naszym systemie!")
            print("------------------------------------------")
            # Odczekanie i wyczyszczenie konsoli
            time.sleep(4)
            os.system('cls')

            return 2


        # Kwerenda pobierająca atrybuty użytkownika z bazy
        query = "SELECT email, password FROM tblUser WHERE email = ?;"

        # Argumenty dodawane poprzez kwerendę
        arg = (email)

        # Wywołanie kwerendy
        cursorMS.execute(query, arg)





        for i in cursorMS:
            if i[1] == haslo:

                libs = []
                # Kwerenda pobierająca atrybuty użytkownika z bazy
                query = "SELECT name, librarian FROM tblUser WHERE email = ?;"

                # Argumenty dodawane poprzez kwerendę
                arg = (email)

                # Wywołanie kwerendy
                cursorMS.execute(query, arg)

                names = []
                libs = []
                for lib in cursorMS:

                    libs.append(lib[1])
                    names.append(lib[0].capitalize())



                print("Logowanie zakończone powodzeniem")
                return 1, libs[0], names[0]

            else:
                print("Niepoprawne hasło")
                print("Spróbuj ponownie")
                print("------------------------------------------")
                #Odczekanie i wyczyszczenie konsoli
                time.sleep(4)
                os.system('cls')
                return 0

    def user_register(self):

        email = self.email
        haslo = self.password

        # Połączenie do SQL
        db_msql = pyodbc.connect("Driver={SQL Server};"
                                 "Server=DELLV3510-01\SQLEXPRESS;"
                                 "Database=biblioteka;"
                                 "Trusted_connection =yes;")

        # Cursor
        cursorMS = db_msql.cursor()

        emails = []
        for row_log in cursorMS.execute('SELECT email FROM tblUser'):
            emails.append("".join(row_log))

        if email in emails:
            print(f"Użytkownik o adresie {self.email} widnieje w bazie użytkowników - zaloguj się")
            return 0
        else:
            return 1











