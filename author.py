import pyodbc
import os
import time

class Author:
    def __init__(self,name = "",  birth_date ="", biography = ""):
        self.name = name
        self.birth_date = birth_date
        self.biography = biography

    def author_add(self):

        """Wywołanie metody powoduje dodanie autora do bazy."""

        # POBRANIE DANYCH OD UŻYTKOWNIKA
        self.name = input("Podaj imię i nazwisko autora: ")
        self.birth_date = input("Podaj datę urodzenia autora (RRRR-MM-DDD): ")
        self.biography = input("Wprowadź biografię autora: ")

        # Połączenie do SQL
        db_msql = pyodbc.connect("Driver={SQL Server};"
                                 "Server=DELLV3510-01\SQLEXPRESS;"
                                 "Database=biblioteka;"
                                 "Trusted_connection =yes;")

        # Cursor
        cursorMS = db_msql.cursor()

        authors = []
        for row_log in cursorMS.execute('SELECT name FROM tblAuthor'):
            authors.append("".join(row_log))

        if self.name in authors:
            print("------------------------------------------")
            print(f"Autor {self.name} widnieje w bazie autorów")
            time.sleep(4)
            os.system('cls')
            return 0

        # Kwerenda dodająca atrybuty użytkownika do bazy
        query = "INSERT INTO tblAuthor(name, birth_date,biography) " \
                "VALUES (?,CONVERT(datetime,?,120),?) "

        # Argumenty dodawane poprzez kwerendę
        arg = (self.name, self.birth_date, self.biography)

        try:

            # Wywołanie kwerendy
            cursorMS.execute(query, arg)

            # Zatwierdzenie wywołania kwerendy
            db_msql.commit()

            # Zamknięcie połączenia z bazą
            db_msql.close()

            time.sleep(4)
            os.system('cls')

            print("Autor został dodany \n")
            print("---------------------------------")
            print("Wybierz opcję: ")
            back = input("1 - Powrót do menu głównego ")

            if back == 1:
                return 1

        except:
            print("------------------------------------------")
            print("Wprowadzono błędne dane - spróbuj ponownie")
            time.sleep(4)
            os.system('cls')
            return 0

    def author_search(self,author_id):


        """Pobranie danych z bazy dla danego autora"""


        self.author_id = author_id

        # Połączenie do SQL
        db_msql = pyodbc.connect("Driver={SQL Server};"
                                 "Server=DELLV3510-01\SQLEXPRESS;"
                                 "Database=biblioteka;"
                                 "Trusted_connection =yes;")

        # Cursor
        cursorMS = db_msql.cursor()

        # Kwerenda dodająca atrybuty użytkownika do bazy
        query = "SELECT * FROM tblAuthor WHERE author_id = ?;"

        # Argumenty dodawane poprzez kwerendę
        arg = (self.author_id)

        # Wywołanie kwerendy
        cursorMS.execute(query, arg)


        # Zatwierdzenie wywołania kwerendy
        #db_msql.commit()

        result = [self.name, self.birth_date, self.biography]

        for row in cursorMS:


            for index in range(len(result)):

                result[index] = row[index+1]

        # Zamknięcie połączenia z bazą
        db_msql.close()

        if result[0] == "":
            print("Brak autora o danym ID")

        return result,author_id

    def author_find(self):
        """Wywołanie metody powoduje wyszukanie użytkownika po parametrach name, surname, email"""


        author_id = int(input("Wprowadź id_autora lub wprowadź 0: "))
        name = input("Wprowadź imię autora lub zostaw wartość pustą: ")
        birth_date = input("Wprowadź datę urodzenia autora lub zostaw wartość pustą: ")
        biography = input("Wprowadż fragment biografii użytkownika: ")

        # Połączenie do SQL
        db_msql = pyodbc.connect("Driver={SQL Server};"
                                 "Server=DELLV3510-01\SQLEXPRESS;"
                                 "Database=biblioteka;"
                                 "Trusted_connection =yes;")

        # Cursor
        cursorMS = db_msql.cursor()
        # Kwerenda pozwalająca na wyszukiwanie książki.
        query = """SELECT * FROM [dbo].[tblAuthor]  
                   WHERE
                   ([author_id] = ? OR
                   CHARINDEX(?, [name], 1) <> 0) OR
                   CHARINDEX(?, [biography], 1) <> 0 OR
                   CHARINDEX(?, [birth_date], 1) <> 0;"""

        # Argumenty dodawane poprzez kwerendę
        arg = (author_id, name,  biography, birth_date)

        # Wywołanie kwerendy
        cursorMS.execute(query,arg)
        wynik_zapytania = cursorMS.fetchall()
        os.system('cls')
        print("---------------------------------")
        print("Wyniki wyszukiwania:")
        for row in wynik_zapytania:

            print(f" author_id: {row[0]} \n"
                  f" name: {row[1]}\n"
                  f" birth_date: {row[2]} \n"
                  f" biography: {row[3]}")
            print("---------------------------------")

        # Zatwierdzenie wywołania kwerendy
        db_msql.commit()

        # Zamknięcie połączenia z bazą
        db_msql.close()

        print("Wybierz opcję: ")
        back = input("1 - Powrót do menu głównego ")

        if back == 1:
            return 1




    def author_update(*args):

        """Wywołanie metody powoduje zaktualizowanie wartości atrybutów w bazie danych.
        Domyślnie atrybuty przyjmują wartości aktualnie występujące w bazie.
        Użytkownik wprowadza zmianę i po zatwierdzeniu wartość jest wprowadzana do bazy"""

        arr = list(args)



        name,birth_date, biography = arr[1][0]
        author_id = arr[1][1]



        print("Aktualizacja danych:")
        print("Jeśli nie chcesz aktalizować danej to kliknij Enter. W przeciwnym przypadku wpisz zaktualizowaną daną")
        new_name = input("Podaj imię i nazwisko autora: ")
        new_birth_date = input("Podaj datę urodzenia autora (RRRR-MM-DDD): ")
        new_biography = input("Podaj biografię autora: ")



        old_data = [name, birth_date, biography]
        new_data = [new_name, new_birth_date, new_biography]

        for i in range(len(old_data)):

            if new_data[i] != "":
                old_data[i] = new_data[i]


        #Połączenie do SQL
        db_msql = pyodbc.connect("Driver={SQL Server};"
                                 "Server=DELLV3510-01\SQLEXPRESS;"
                                 "Database=biblioteka;"
                                 "Trusted_connection =yes;")

        #Cursor
        cursorMS = db_msql.cursor()


        query = "UPDATE tblAuthor " \
                "SET name = ?, birth_date = CONVERT(datetime,?,120),biography = ? " \
                "WHERE author_id = ?"
        #Argumenty dodawane poprzez kwerendę

        old_data.append(author_id)

        arg = old_data

        try:

            # Wywołanie kwerendy
            cursorMS.execute(query, arg)

            # Zatwierdzenie wywołania kwerendy
            db_msql.commit()

            # Zamknięcie połączenia z bazą
            db_msql.close()

            time.sleep(4)
            os.system('cls')

            print("Dane użytkownika zostały zaktualizowane \n")
            print("---------------------------------")
            print("Wybierz opcję: ")
            back = input("1 - Powrót do menu głównego ")

            if back == 1:
                return 1

        except:
            print("------------------------------------------")
            print("Wprowadzono błędne dane - spróbuj ponownie")
            time.sleep(4)
            os.system('cls')
            return 0

    def author_delete(self, author_id):

        """Wywołanie metody powoduje usunięcie utora z bazy danych (wartości wszystkich atrybutów w bazie) dla wskazanego author_id"""

        self.author_id = author_id

        # Połączenie do SQL
        db_msql = pyodbc.connect("Driver={SQL Server};"
                                 "Server=DELLV3510-01\SQLEXPRESS;"
                                 "Database=biblioteka;"
                                 "Trusted_connection =yes;")

        # Cursor
        cursorMS = db_msql.cursor()

        # Kwerenda dodająca atrybuty użytkownika do bazy
        table = ['tblAuthor_Book', 'tblAuthor']

        for tbl in table:
            query = f"DELETE FROM {tbl} WHERE author_id = ?"

            # Argumenty dodawane poprzez kwerendę
            arg = (self.author_id)

            # Wywołanie kwerendy
            cursorMS.execute(query, arg)

            # Zatwierdzenie wywołania kwerendy
            db_msql.commit()

        # Zamknięcie połączenia z bazą
        db_msql.close()
        print("Użytkownik został usunięty \n")
        print("---------------------------------")
        print("Wybierz opcję: ")
        back = input("1 - Powrót do menu głównego ")

        if back == 1:
            return 1
