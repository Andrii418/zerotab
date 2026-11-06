# Przypadki testowe (TestCase)

## TC001: Dodawanie osoby

| Pole | Wartość |
|---|---|
| ID | TC001 |
| Tytuł | Dodawanie osoby |
| Warunki początkowe | Strona główna `/ui` jest otwarta, baza jest pusta |
| Kroki testowe | 1. W polu "Name" w sekcji "People" wpisz `Anna`. <br/>2. Kliknij "Add person". |
| Oczekiwany rezultat | Strona się przeładowuje, a w sekcji "People" widoczna jest pozycja "Anna" |

## TC002: Odrzucenie pustej nazwy osoby

| Pole | Wartość |
|---|---|
| ID | TC002 |
| Tytuł | Odrzucenie nazwy osoby składającej się z samych spacji |
| Warunki początkowe | Strona główna `/ui` jest otwarta |
| Kroki testowe | 1. W polu "Name" w sekcji "People" wpisz trzy spacje. <br/>2. Kliknij "Add person". |
| Oczekiwany rezultat | Wyświetla się czerwony komunikat "Name must not be blank", a osoba nie zostaje dodana |

## TC003: Tworzenie grupy z członkami

| Pole | Wartość |
|---|---|
| ID | TC003 |
| Tytuł | Tworzenie grupy z trzema członkami |
| Warunki początkowe | Dodane są osoby: Anna, Ben, Carl |
| Kroki testowe | 1. W sekcji "New group" wpisz nazwę `Trip`. <br/>2. Zaznacz Annę, Bena i Carla. <br/>3. Kliknij "Create group". |
| Oczekiwany rezultat | Aplikacja otwiera stronę grupy "Trip", a w sekcji "Members" widoczne są trzy osoby |

## TC004: Podział po równo z rozdzieleniem groszy

| Pole | Wartość |
|---|---|
| ID | TC004 |
| Tytuł | Podział 100,00 PLN po równo między trzy osoby |
| Warunki początkowe | Otwarta strona grupy "Trip" z członkami Anna, Ben, Carl |
| Kroki testowe | 1. W polu "Description" wpisz `Dinner`. <br/>2. W polu "Amount (PLN)" wpisz `100,00`. <br/>3. W polu "Paid by" wybierz Annę. <br/>4. W polu "Split type" wybierz "Equal". <br/>5. Zostaw zaznaczonych wszystkich uczestników. 6. Kliknij "Add expense". |
| Oczekiwany rezultat | W tabeli "Expenses" pojawia się wydatek "Dinner" na kwotę 100.00 PLN, a w kolumnie podziału: Anna 33.34, Ben 33.33, Carl 33.33 (suma równa dokładnie 100.00) |

## TC005: Podział procentowy z resztą groszy

| Pole | Wartość |
|---|---|
| ID | TC005 |
| Tytuł | Podział procentowy 50/30/20 kwoty 100,01 PLN |
| Warunki początkowe | Otwarta strona grupy "Trip" z członkami Anna, Ben, Carl |
| Kroki testowe | 1. Wpisz opis `Tickets` i kwotę `100,01`. <br/>2. Wybierz płatnika Annę. <br/>3. W polu "Split type" wybierz "Percentage". <br/>4. Wpisz udziały: Anna 50, Ben 30, Carl 20. <br/>5. Kliknij "Add expense". |
| Oczekiwany rezultat | Wydatek zostaje dodany z podziałem: Anna 50.01, Ben 30.00, Carl 20.00 |

## TC006: Błędna suma procentów

| Pole | Wartość |
|---|---|
| ID | TC006 |
| Tytuł | Odrzucenie procentów, których suma nie wynosi 100 |
| Warunki początkowe | Otwarta strona grupy "Trip" z członkami Anna, Ben, Carl |
| Kroki testowe | 1. Wpisz opis `Taxi` i kwotę `50`. <br/>2. W polu "Split type" wybierz "Percentage". <br/>3. Zaznacz Annę i Bena, wpisz udziały 60 i 30. <br/>4. Kliknij "Add expense". |
| Oczekiwany rezultat | Wyświetla się komunikat "Percentages must sum to 100", a wydatek nie pojawia się na liście |

## TC007: Kwoty niezgodne z sumą wydatku

| Pole | Wartość |
|---|---|
| ID | TC007 |
| Tytuł | Odrzucenie podziału kwotami, gdy suma nie zgadza się z kwotą wydatku |
| Warunki początkowe | Otwarta strona grupy "Trip" z członkami Anna, Ben, Carl |
| Kroki testowe | 1. Wpisz opis `Museum` i kwotę `100`. <br/>2. W polu "Split type" wybierz "Exact". <br/>3. Zaznacz Annę i Bena, wpisz kwoty 50 i 20. <br/>4. Kliknij "Add expense". |
| Oczekiwany rezultat | Wyświetla się komunikat "Amounts must sum to the total", a wydatek nie zostaje zapisany |

## TC008: Nieprawidłowa kwota wydatku

| Pole | Wartość |
|---|---|
| ID | TC008 |
| Tytuł | Odrzucenie kwoty, która nie jest liczbą |
| Warunki początkowe | Otwarta strona grupy "Trip" z członkami Anna, Ben, Carl |
| Kroki testowe | 1. Wpisz opis `Snacks`. <br/>2. W polu "Amount (PLN)" wpisz `abc`. <br/>3. Kliknij "Add expense". |
| Oczekiwany rezultat | Wyświetla się komunikat "Enter a valid number", a wydatek nie zostaje dodany |

## TC009: Przecinek jako separator dziesiętny

| Pole | Wartość |
|---|---|
| ID | TC009 |
| Tytuł | Akceptacja kwoty zapisanej z przecinkiem |
| Warunki początkowe | Otwarta strona grupy "Trip" z członkami Anna, Ben, Carl |
| Kroki testowe | 1. Wpisz opis `Coffee` i kwotę `12,50`. <br/>2. Wybierz płatnika Annę, podział "Equal", wszyscy uczestnicy zaznaczeni. <br/>3. Kliknij "Add expense". |
| Oczekiwany rezultat | Wydatek "Coffee" zostaje dodany z kwotą 12.50 PLN, a suma udziałów wynosi 12.50 |

## TC010: Salda i minimalne rozliczenie

| Pole | Wartość |
|---|---|
| ID | TC010 |
| Tytuł | Obliczanie sald i listy przelewów dla dwóch wydatków |
| Warunki początkowe | Otwarta strona nowej, pustej grupy z członkami Anna, Ben, Carl |
| Kroki testowe | 1. Dodaj wydatek `Hotel`, kwota `90`, płaci Anna, podział "Equal", wszyscy uczestnicy. <br/>2. Dodaj wydatek `Taxi`, kwota `30`, płaci Ben, podział "Equal", wszyscy uczestnicy. <br/>3. Przejdź do sekcji "Balances" i "Settlement". |
| Oczekiwany rezultat | Salda: Anna 50.00 PLN (zielone), Ben -10.00 PLN, Carl -40.00 PLN (czerwone). Rozliczenie ma dwa przelewy: Carl pays Anna 40.00 PLN oraz Ben pays Anna 10.00 PLN |

## TC011: Usuwanie wydatku

| Pole | Wartość |
|---|---|
| ID | TC011 |
| Tytuł | Usunięcie wydatku i przeliczenie sald |
| Warunki początkowe | W grupie jest jeden wydatek (np. `Hotel`, 90 PLN, płaci Anna) |
| Kroki testowe | 1. W wierszu wydatku kliknij "Delete". <br/>2. W oknie potwierdzenia kliknij "OK". |
| Oczekiwany rezultat | Wydatek znika z tabeli, wyświetla się "No expenses yet.", salda wszystkich osób wynoszą 0.00 PLN, a w sekcji "Settlement" widnieje "All settled up." |

## TC012: Anulowanie usuwania wydatku

| Pole | Wartość |
|---|---|
| ID | TC012 |
| Tytuł | Anulowanie usunięcia wydatku w oknie potwierdzenia |
| Warunki początkowe | W grupie jest jeden wydatek |
| Kroki testowe | 1. W wierszu wydatku kliknij "Delete". <br/>2. W oknie potwierdzenia kliknij "Cancel" (Anuluj). |
| Oczekiwany rezultat | Wydatek pozostaje na liście, a salda nie zmieniają się |

## TC013: Dodawanie członka do istniejącej grupy

| Pole | Wartość |
|---|---|
| ID | TC013 |
| Tytuł | Dodanie nowego członka do grupy |
| Warunki początkowe | Istnieje grupa "Trip" (Anna, Ben, Carl) oraz osoba Dave, która nie należy do grupy |
| Kroki testowe | 1. Otwórz stronę grupy "Trip". <br/>2. W sekcji "Members" wybierz z listy Dave'a. <br/>3. Kliknij "Add member". |
| Oczekiwany rezultat | Dave pojawia się wśród członków, a na liście "Paid by" i w uczestnikach formularza wydatku jest dostępny |

## TC014: Usuwanie grupy

| Pole | Wartość |
|---|---|
| ID | TC014 |
| Tytuł | Usunięcie grupy wraz z wydatkami |
| Warunki początkowe | Istnieje grupa "Trip" z co najmniej jednym wydatkiem |
| Kroki testowe | 1. Otwórz stronę grupy "Trip". <br/>2. Kliknij "Delete group". <br/>3. W oknie potwierdzenia kliknij "OK". |
| Oczekiwany rezultat | Aplikacja wraca na stronę główną `/ui`, a grupa "Trip" nie jest już widoczna na liście grup |

## TC015: Dostęp do nieistniejącej grupy

| Pole | Wartość |
|---|---|
| ID | TC015 |
| Tytuł | Odpowiedź API dla nieistniejącej grupy |
| Warunki początkowe | Aplikacja działa, grupa o id 999 nie istnieje |
| Kroki testowe | 1. Otwórz `http://127.0.0.1:8000/docs`. <br/>2. Rozwiń `GET /groups/{group_id}` i kliknij "Try it out". <br/>3. Wpisz `999` i kliknij "Execute". |
| Oczekiwany rezultat | Kod odpowiedzi 404, a ciało odpowiedzi to `{"detail": "Group 999 not found"}` |