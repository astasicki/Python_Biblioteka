from user import User
from author import Author
from book import Book
import os
import time



def menu_librarian_user_edition(user_id,name,surname,email):
    os.system('cls')
    running = True
    while running:
        os.system('cls')
        print(f"Twój użytkownik o id {user_id} to: "
              f"\n Imię: {name}, "
              f"\n Nazwisko {surname},"
              f"\n Email: {email} ")
        print("\n")
        print("--------MENU EDYCJI UŻYTKOWNIKA--------")
        print(""
              "\n 1 - Zaktualizuj użytkownika,"
              "\n 2 - Wyświetl zarezerwowane książki"
              "\n 3 - Wyświetl wypożyczone książki"
              "\n 4 - Wyświetl kary użytkownika za przekroczenie terminu"
              )
        print("\n")
        menu = int(input("Wybierz opcję edycji użytkownika: \n"))

        user = User()

        if menu == 1:
            os.system('cls')
            print("--------ZAKTUALIZUJ DANE UŻYTKOWNIKA--------")
            updating = user.user_update(user.user_search(user_id))
            if updating == 1:
                os.system('cls')
                pass

        elif menu == 2:
            os.system('cls')
            print("--------WYŚWIETL ZAREZERWOWANE KSIĄŻKI--------")
            booking = user.user_booking(user_id)
            if booking == 1:
                os.system('cls')
                pass

        elif menu == 3:
            os.system('cls')
            print("--------WYŚWIETL ZAREZERWOWANE KSIĄŻKI--------")
            borrowing = user.user_borrowing(user_id)
            print(f"BORROWING PRZYJMUJE WARTOŚĆ {borrowing}")
            if borrowing == 2:
                os.system('cls')
                pass
            elif borrowing == 1:
                book_id = int(input("Podaj id książki, którą chcesz przedłużyć: "))
                time = user.user_longer_endtime(user_id, book_id)
                if time == 1:
                    os.system('cls')
                    pass


        elif menu == 4:
            os.system('cls')
            print("--------WYŚWIETL KARY UŻYTKOWNIKA ZA PRZEKROCZENIE TERMINU--------")
            penalty = user.user_penalty(user_id)
            if penalty[0] == 1:
                os.system('cls')
                pass



def menu_librarian(name):
    running = True

    while running:

        os.system('cls')
        print(f"Witaj {name}! Co nowego w świecie bibliotekarza?")
        print("\n 1 - Wyszukaj książkę,"
              "\n 2 - Wybierz książkę,"
              "\n 3 - Wyszukaj użytkownika,"
              "\n 4 - Edytuj użytkownika"
              "\n 5 - Dodaj użytkownika,"
              "\n 6 - Wyszukaj i usuń użytkownika"
              "\n 7 - Wyszukaj autora,"
              "\n 8 - Wybierz autora,"
              "\n 9 - Opuść bibliotekę.")

        print("\n")
        menu = int(input("Wybierz opcję z menu: \n"))

        # Wyszukaj książkę
        if menu == 1:
            os.system('cls')
            print("--------WYSZUKAJ KSIĄŻKĘ--------")
            b = Book()
            search = b.book_search()

            if search == 1:
                os.system('cls')
                pass



        # Wybierz książkę
        elif menu == 2:
            os.system('cls')
            print("--------WYBIERZ KSIĄŻKĘ--------")
            b = Book()
            selection = b.book_selection()

            if selection == 1:
                print("WSZYSTKO OK")





        # Wyszukaj użytkownika
        elif menu == 3:
            os.system('cls')
            print("--------WYSZUKAJ UŻYTKOWNIKA--------")
            u1= User()
            search = u1.user_find()

            if search == 1:
                os.system('cls')
                pass

        # Edytuj użytkownika
        elif menu == 4:
            os.system('cls')
            print("--------EDYTUJ UŻYTKOWNIKA--------")

            user_id = input("Podaj user_id użytkownika: ")
            u1 = User()
            search = u1.user_search(user_id)
            menu_librarian_user_edition(search[1],search[0][0],search[0][1],search[0][4])

        # Dodaj użytkownika
        elif menu == 5:
            os.system('cls')
            print("--------DODAJ UŻYTKOWNIKA--------")
            u1 = User()
            add = u1.user_add()

            if add == 1:
                os.system('cls')
                pass
            elif add == 0:
                os.system('cls')
                pass

        # Usuń użytkownika
        elif menu == 6:
            os.system('cls')
            print("--------WYSZKUAJ I USUŃ UŻYTKOWNIKA--------")
            u1 = User()
            u1.user_find()
            user_id = int(input("Podaj id użytkownika, którego chcesz usunąć: "))
            delete = u1.user_delete((user_id))
            if delete == 1:
                os.system('cls')
                pass


        # Wyszukaj autora
        elif menu == 7:
            pass

        # Wybierz autora
        elif menu == 8:
            pass

        # Opuść bibliotekę
        elif menu == 9:
            os.system('cls')
            print("Do zobaczenia wkrótce!")
            break




def menu_library():
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
                        menu_librarian(name = login[2])

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



menu_library()


