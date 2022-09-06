from user import User
from author import Author
from book import Book
import os
import time


def menu_librarian_book_edition(book_id,bk_isbn, bk_title,bk_pages, bk_cover, bk_book_genre, bk_thumbnail, bk_publisher, bk_published_year, bk_description, bk_state, name):
    os.system('cls')
    running = True
    while running:
        os.system('cls')
        print(f"Twoja książka o id {book_id} to: "
              f"\n ISBN: {bk_isbn}, "
              f"\n Tytuł: {bk_title},"
              f"\n Liczba stron: {bk_pages} "
              f"\n Okładka: {bk_cover}"
              f"\n Gatunek: {bk_book_genre}"
              f"\n Thumbnail: {bk_thumbnail}"
              f"\n Wydawnictwo: {bk_publisher}"
              f"\n Rok wydania: {bk_published_year}"
              f"\n Opis: {bk_description}"
              f"\n Status: {bk_state}")
        print("\n")
        print("--------MENU EDYCJI KSIĄŻKI--------")
        print(""
              "\n 1 - Usuń książkę,"
              "\n 2 - Dodaj książkę"
              "\n 3 - Zaktualizuj książkę"
              "\n 4 - Wypożycz książkę"
              "\n 5 - Zarezerwuj książkę"
              "\n 6 - Dodaj recenzje"
              "\n 7 - Pokaż recenzję"
              "\n 8 - Oddaj książkę"
              "\n 9 - Wróć do menu głównego"

              )
        print("\n")
        menu = int(input("Wybierz opcję edycji książki: \n"))

        book = Book(book_id = book_id, ISBN = bk_isbn, title = bk_title, pages = bk_pages, cover = bk_cover, book_genre=bk_book_genre, thumbnail= bk_thumbnail,
                    publisher=bk_publisher, published_year=bk_published_year, description=bk_description, state=bk_state)

        if menu == 1:
            os.system('cls')
            print("--------USUŃ KSIĄŻKĘ--------")
            deleting = book.book_delete()
            if deleting == 1:
                os.system('cls')
                pass

        elif menu == 2:
            os.system('cls')
            print("--------DODAJ KSIĄŻKĘ--------")
            add = book.book_add()
            if add == 1:
                os.system('cls')
                pass

        elif menu == 3:
            os.system('cls')
            print("--------ZAKTUALIZUJ KSIĄŻKĘ--------")
            updating = book.book_update()
            if updating == 1:
                os.system('cls')
                pass

        elif menu == 4:
            os.system('cls')
            print("--------WYPOŻYCZ KSIĄŻKĘ--------")
            borrow = book.book_borrowing()
            if borrow == 1:
                os.system('cls')
                pass

        elif menu == 5:
            os.system('cls')
            print("--------ZAREZERWUJ KSIĄŻKĘ--------")
            booking = book.book_booking()
            if booking == 1:
                os.system('cls')
                pass

        elif menu == 6:
            os.system('cls')
            print("--------DODAJ RECENZJĘ--------")
            review = book.book_review_add()
            if review == 1:
                os.system('cls')
                pass


        elif menu == 7:
            os.system('cls')
            print("--------POKAŻ RECENZJĘ--------")
            review_show = book.book_review_show()
            if review_show == 1:
                os.system('cls')
                pass

        elif menu == 8:
            os.system('cls')
            print("--------ODDAJ KSIĄŻKĘ--------")
            book_back = book.book_return_borrowing()
            if book_back == 1:
                os.system('cls')
                pass

        elif menu == 9:
            print("--------PRZEJDŹ DO MENU GŁÓWNEGO--------")
            os.system('cls')
            menu_librarian(name)


def menu_librarian_user_edition(user_id,us_name,us_surname,us_email,name):
    os.system('cls')
    running = True
    while running:
        os.system('cls')
        print(f"Twój użytkownik o id {user_id} to: "
              f"\n Imię: {us_name}, "
              f"\n Nazwisko {us_surname},"
              f"\n Email: {us_email} ")
        print("\n")
        print("--------MENU EDYCJI UŻYTKOWNIKA--------")
        print(""
              "\n 1 - Zaktualizuj użytkownika,"
              "\n 2 - Wyświetl zarezerwowane książki"
              "\n 3 - Wyświetl wypożyczone książki"
              "\n 4 - Wyświetl kary użytkownika za przekroczenie terminu"
              "\n 5 - Wróć do menu głównego"
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
            print("--------WYŚWIETL WYPOŻYCZONE KSIĄŻKI--------")
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
            print(penalty)
            if penalty[0] == 1:
                os.system('cls')
                pass

        elif menu == 5:
            print("--------PRZEJDŹ DO MENU BIBLIOTEKARZA--------")
            os.system('cls')
            menu_librarian(name)



def menu_librarian(name):
    running = True

    while running:

        os.system('cls')
        print(f"Witaj {name}! Co nowego w świecie bibliotekarza?")
        print("\n------- KSIĄŻKI ------- "
              "\n 1 - Wyszukaj książkę,"
              "\n 2 - Edytuj książkę,"
              
              "\n"
              "\n------- UŻYTKOWNICY ------- "
              "\n 3 - Wyszukaj użytkownika,"
              "\n 4 - Edytuj użytkownika"
              "\n 5 - Dodaj użytkownika,"
              "\n 6 - Wyszukaj i usuń użytkownika,"
              "\n"
              "\n------- AUTORZY ------- "
              "\n 7 - Wyszukaj autora,"
              "\n 8 - Zaktualizuj dane autora,"
              "\n 9 - Dodaj autora,"
              "\n 10 - Wyszukaj i usuń autora,"
              "\n"
              "\n------- WYJŚCIE -------  "
              "\n 11 - Opuść bibliotekę.")

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



        # Edytuj książkę
        elif menu == 2:
            os.system('cls')
            print("--------EDYTUJ KSIĄŻKE--------")

            book_id = input("Podaj book_id książki: ")
            b1 = Book()
            search = b1.book_search_as(book_id)
            menu_librarian_book_edition(search[1], search[0][0], search[0][1], search[0][2], search[0][3], search[0][4], search[0][5], search[0][6], search[0][7], search[0][8], search[0][10], name)






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
            menu_librarian_user_edition(search[1],search[0][0],search[0][1],search[0][4],name)

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

        # Wyszykaj i usuń użytkownika
        elif menu == 6:
            os.system('cls')
            print("--------WYSZKUAJ I USUŃ UŻYTKOWNIKA--------")
            u1 = User()
            u1.user_find()
            user_id = int(input("\n Podaj id użytkownika, którego chcesz usunąć: "))
            delete = u1.user_delete((user_id))
            if delete == 1:
                os.system('cls')
                pass


        # Wyszukaj autora
        elif menu == 7:
            os.system('cls')
            print("--------WYSZKUAJ AUTORA--------")
            author = Author()
            find = author.author_find()
            if find == 1:
                os.system('cls')
                pass

        # Edytuj autora

        elif menu == 8:
            os.system('cls')
            print("--------WYSZUKAJ ID AUTORA--------")
            a = Author()
            a.author_find()
            author_id = int(input("\n Podaj id autora, którego dane chcesz zaktualizować: "))
            a1 = Author()
            print("\n--------ZAKTUALIZUJ DANE AUTORA--------\n")
            updating = a1.author_update(a1.author_search(author_id))
            if updating == 1:
                os.system('cls')
                pass

        # Dodaj autora
        elif menu == 9:
            os.system('cls')
            print("--------DODAJ AUTORA--------")
            a1 = Author()
            add = a1.author_add()
            if add == 1:
                os.system('cls')
                pass
            elif add == 0:
                os.system('cls')
                pass

        # Wyszukaj i usuń autora
        elif menu == 10:
            os.system('cls')
            print("--------WYSZUKAJ I USUŃ AUTORA--------")
            a1 = Author()
            a1.author_find()
            author_id = int(input("Podaj id autora, którego chcesz usunąć: "))
            delete = a1.author_delete((author_id))
            if delete == 1:
                os.system('cls')
                pass


        # Opuść bibliotekę
        elif menu == 11:
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
                        menu_reader(name = login[2])


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


if __name__ == "__main__":
    menu_library()



