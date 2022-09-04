import pyodbc

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

        # Kwerenda dodająca atrybuty użytkownika do bazy
        query = "INSERT INTO tblAuthor(name, birth_date,biography) " \
                "VALUES (?,CONVERT(datetime,?,120),?) "

        # Argumenty dodawane poprzez kwerendę
        arg = (self.name, self.birth_date, self.biography)

        # Wywołanie kwerendy
        cursorMS.execute(query, arg)

        # Zatwierdzenie wywołania kwerendy
        db_msql.commit()

        # Zamknięcie połączenia z bazą
        db_msql.close()

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
        return result,author_id


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
        print(arg)
        #Wywołanie kwerendy
        cursorMS.execute(query, arg)

        #Zatwierdzenie wywołania kwerendy
        db_msql.commit()

        #Zamknięcie połączenia z bazą
        db_msql.close()

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
