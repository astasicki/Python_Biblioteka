from user import User
from author import Author
from book import Book
import os
import time


running = True

while running:
    os.system('cls')
    print("--------WITAJ W SWOJEJ BIBLIOTECE!--------"
          "\n 1 - Zaloguj się,"
          "\n 2 - Zarejestruj się,"
          "\n 3 - Wyszukaj książkę"
          "\n 4 - Opuść bibliotekę")

    try:
        menu = int(input("Wybierz opcję z menu: \n"))

        if menu == 1:
            os.system('cls')
            #LOGOWANIE DO APLIKACJI
            print("--------LOGOWANIE--------")
            email = input("Podaj adres email: ")
            password = input("Podaj hasło: ")
            u = User(email = email, password = password)
            login = u.user_login()

            #Brak użytkownika w bazie"
            if login == 2:
                pass

            #Niepoprawne hasło
            elif login == 0:
                pass

            #Logowanie poprawne
            elif login[0] == 1:
                if login[1] == 1:
                    os.system('cls')
                    print(f"Witaj {login[2]}! Co nowego w świecie bibliotekarza?")
                    print("\n 1 - Wyszukaj książkę,"
                          "\n 2 - Wybierz książkę,"
                          "\n 3 - Wyszukaj użytkownika"
                          "\n 4 - Wybierz użytkownika"
                          "\n 5 - Wyszukaj autora"
                          "\n 6 - Wybierz autora"
                          "\n 7 - Opuść bibliotekę")

                    print("\n")
                    menu = int(input("Wybierz opcję z menu: \n"))

                    #Wyszukaj książkę
                    if menu == 1:
                        os.system('cls')
                        print("--------WYSZUKAJ KSIĄŻKĘ--------")
                        b = Book()
                        search = b.book_search()


                    # Wybierz książkę
                    elif menu == 2:
                        pass

                    # Wyszukaj użytkownika
                    elif menu == 3:
                        pass

                    # Wybierz użytkownika
                    elif menu == 4:
                        pass

                    # Wyszukaj autora
                    elif menu == 5:
                        pass

                    # Wybierz autora
                    elif menu == 6:
                        pass

                    # Wybierz autora
                    elif menu == 7:
                        os.system('cls')
                        print("Do zobaczenia wkrótce!")
                        break






                elif login[1] == 0:
                    print(f"Witaj {login[2]}! Co nowego w świecie czytelnika?")





                time.sleep(4)
                pass



        elif menu == 2:
            os.system('cls')
            # REJESTRACJA DO APLIKACJI
            print("--------REJESTRACJA--------")
            u = User()
            registration = u.user_add()

            #Pomyślne dodanie użytkownika do bazy
            if registration == 1:
                print("Użytkownik pomyślnie dodany do bazy danych!"
                      "\n Zaloguj się, aby kontynuować na swoim nowym koncie")
                pass

            #Wprowadzenie błędnych danych
            elif registration == 0:


                pass


        elif menu == 3:
            os.system('cls')
            print("--------WYSZUKAJ SWOJĄ ULUBIONĄ KSIĄŻKĘ--------")
            b = Book()
            search = b.book_search()
            if search == 1:
                os.system('csl')
                pass


        elif menu == 4:
            os.system('cls')
            print("Do zobaczenia wkrótce!")
            break

    except ValueError:

        pass