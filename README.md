# Lab03 — Blog: Komentarze z Moderacją

System blogowy oparty na Flasku, umożliwiający dodawanie postów i komentarzy. Kluczową funkcjonalnością jest system moderacji: komentarze domyślnie są ukryte (`approved=false`) i pojawiają się publicznie dopiero po zatwierdzeniu przez moderatora.

##  Funkcjonalności

* **Posty:** Dodawanie i wyświetlanie listy postów.
* **Komentarze:** System komentowania. Nowy komentarz trafia do "poczekalni".
* **Moderacja:** Panel dla moderatora wyświetlający oczekujące wpisy. Możliwość zatwierdzenia komentarza (zmiana statusu na widoczny).
* **API:** RESTowe endpointy filtrujące dane (publiczne API nie zwraca niezatwierdzonych treści).

##  Technologia

* **Backend:** Python 3, Flask, Flask-SQLAlchemy
* **Baza danych:** SQLite (plik `blog.db`)
* **Frontend:** HTML5, CSS3, JavaScript (Fetch API)

##  Instrukcja uruchomienia

1. Stwórz środowisko wirtualne:

    python -m venv venv

2. Aktywuj środowisko:

    Windows:
    .\venv\Scripts\activate

    macOS/Linux:
    source venv/bin/activate

3. Zainstaluj wymagane biblioteki:

    pip install -r requirements.txt

4. Uruchom serwer:

    python app.py

5. Otwórz aplikację:
   Wejdź w przeglądarce na adres: [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

##  Zrzuty ekranu

### 1. Dodawanie komentarza (Widoczny tylko dla moderatora)
![Oczekujący komentarz](img/screen1.png)

### 2. Widok po zatwierdzeniu (Widoczny publicznie)
![Zatwierdzony](img/screen2.png)