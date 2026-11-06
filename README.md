# ZeroTab

## Nazwa kursu

Testowanie i Jakość Oprogramowania

## Autor

Andrii Toianyk, 37742

## Temat projektu

ZeroTab – system rozliczania wspólnych wydatków

## Opis projektu

ZeroTab to aplikacja webowa do rozliczania wspólnych wydatków w grupie osób (np. wyjazd, mieszkanie, wspólne zakupy). Użytkownik:

1. dodaje osoby i tworzy grupy,
2. rejestruje wydatki, wskazując płatnika i sposób podziału,
3. widzi salda każdej osoby (kto jest na plusie, a kto na minusie),
4. dostaje minimalną listę przelewów, która zeruje wszystkie długi w grupie.

Sposoby podziału wydatku:

- **equal**: po równo, z poprawnym rozdzieleniem groszy (100,00 PLN na 3 osoby = 33,34 + 33,33 + 33,33),
- **percentage**: w procentach, z rozdzieleniem reszty algorytmem największej reszty,
- **exact**: dokładnymi kwotami, z walidacją sumy.

Najważniejsze decyzje projektowe:

- Kwoty są liczone na `Decimal` i przechowywane w bazie jako grosze (`int`), więc nie ma błędów zaokrągleń typowych dla `float`.
- Sposoby podziału to wzorzec **Strategy** (`app/strategies`), wybierany przez **Factory** (`app/strategies/factory.py`). Dodanie nowego sposobu podziału nie wymaga zmian w istniejącym kodzie.
- Walidacja sumy całkowitej jest w klasie bazowej strategii (**Template Method**).
- Algorytm rozliczeń jest zachłanny: łączy największego dłużnika z największym wierzycielem i daje maksymalnie *n − 1* przelewów dla *n* osób z niezerowym saldem. Znalezienie absolutnego minimum jest problemem NP-trudnym, więc stosowane jest podejście zachłanne.
- Architektura warstwowa: `routers` → `services` → `repositories` → `models`, wstrzykiwanie zależności przez FastAPI (`app/dependencies.py`).

Struktura projektu:

```
app/
  models/         modele SQLAlchemy
  repositories/   dostęp do bazy
  services/       logika aplikacji, salda i algorytm rozliczeń
  strategies/     sposoby podziału wydatku
  routers/        API REST i widoki HTML
  schemas/        walidacja danych wejściowych i wyjściowych
  web/            parser formularzy, prezentery, szablony stron
  templates/      szablony Jinja2
  static/         CSS i JavaScript
tests/
  unit/           testy jednostkowe
  integration/    testy integracyjne
docs/
  test-cases.md   przypadki testowe dla testera manualnego
```

## Uruchomienie projektu

Wymagania: Python 3.12 lub nowszy.

```
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

(Linux/macOS: `source .venv/bin/activate`.)

Aplikacja jest dostępna pod adresem `http://127.0.0.1:8000` (interfejs użytkownika), a dokumentacja API pod `http://127.0.0.1:8000/docs`. Baza danych SQLite (`zerotab.db`) tworzy się automatycznie przy pierwszym uruchomieniu.

## Testy

Uruchomienie wszystkich testów:

```
pytest
```

Uruchomienie z raportem pokrycia kodu:

```
pytest --cov=app --cov-report=term-missing
pytest --cov=app --cov-report=html
```

Wynik: **171 testów, pokrycie kodu 99%**. Wszystkie testy są napisane w konwencji AAA (Arrange-Act-Assert).

### Testy jednostkowe (114)

Katalog: [`tests/unit`](tests/unit)

| Plik | Co testuje |
|---|---|
| [test_money.py](tests/unit/test_money.py) | zaokrąglanie do groszy, konwersje kwota ↔ grosze |
| [test_equal_split.py](tests/unit/test_equal_split.py) | podział po równo, reszta groszy, walidacja uczestników i kwoty |
| [test_percentage_split.py](tests/unit/test_percentage_split.py) | podział procentowy, suma procentów, reszta groszy |
| [test_exact_split.py](tests/unit/test_exact_split.py) | podział kwotami, zgodność sumy z kwotą wydatku |
| [test_distribution.py](tests/unit/test_distribution.py) | algorytm największej reszty |
| [test_strategy_factory.py](tests/unit/test_strategy_factory.py) | wybór strategii podziału |
| [test_balance_calculator.py](tests/unit/test_balance_calculator.py) | obliczanie sald (suma sald zawsze równa 0) |
| [test_settlement.py](tests/unit/test_settlement.py) | algorytm minimalizacji przelewów |
| [test_expense_service.py](tests/unit/test_expense_service.py) | serwis wydatków z mockami repozytoriów |
| [test_group_service.py](tests/unit/test_group_service.py) | serwis grup z mockami repozytoriów |
| [test_settlement_service.py](tests/unit/test_settlement_service.py) | serwis rozliczeń z mockiem repozytorium |
| [test_form_parser.py](tests/unit/test_form_parser.py) | parsowanie formularza wydatku |
| [test_presenters.py](tests/unit/test_presenters.py) | zamiana sald i przelewów na wiersze widoku |

### Testy integracyjne (57)

Katalog: [`tests/integration`](tests/integration). Testy używają prawdziwej bazy SQLite w pamięci (osobnej dla każdego testu) i klienta HTTP `TestClient`. Konfiguracja: [conftest.py](tests/integration/conftest.py).

| Plik | Co testuje |
|---|---|
| [test_api.py](tests/integration/test_api.py) | endpointy REST: osoby, grupy, wydatki, salda, rozliczenia, kody błędów |
| [test_repositories.py](tests/integration/test_repositories.py) | repozytoria na prawdziwej bazie, kaskadowe usuwanie |
| [test_web_ui.py](tests/integration/test_web_ui.py) | strony i formularze interfejsu użytkownika |

## Dokumentacja API

Interaktywna dokumentacja (Swagger UI) jest generowana automatycznie pod adresem `http://127.0.0.1:8000/docs`.

| Metoda | Ścieżka | Opis | Kody odpowiedzi |
|---|---|---|---|
| POST | `/people` | dodanie osoby | 201, 422 |
| GET | `/people` | lista osób | 200 |
| POST | `/groups` | utworzenie grupy | 201, 404, 422 |
| GET | `/groups` | lista grup | 200 |
| GET | `/groups/{group_id}` | szczegóły grupy | 200, 404 |
| POST | `/groups/{group_id}/members` | dodanie członka do grupy | 200, 404 |
| DELETE | `/groups/{group_id}` | usunięcie grupy | 204, 404 |
| POST | `/groups/{group_id}/expenses` | dodanie wydatku | 201, 404, 422 |
| GET | `/groups/{group_id}/expenses` | lista wydatków grupy | 200 |
| DELETE | `/expenses/{expense_id}` | usunięcie wydatku | 204, 404 |
| GET | `/groups/{group_id}/balances` | salda członków grupy | 200, 404 |
| GET | `/groups/{group_id}/settlement` | minimalna lista przelewów | 200, 404 |
| GET | `/health` | sprawdzenie działania aplikacji | 200 |

Przykład żądania dodania wydatku (`POST /groups/1/expenses`):

```json
{
  "payer_id": 1,
  "description": "Hotel",
  "category": "travel",
  "amount": "90.00",
  "split_type": "equal",
  "shares": {"1": "1", "2": "1", "3": "1"}
}
```

Znaczenie pola `shares` zależy od `split_type`: dla `equal` liczą się tylko klucze (uczestnicy), dla `percentage` wartości to procenty (suma 100), a dla `exact` kwoty (suma równa kwocie wydatku). Kwoty są przesyłane jako tekst, żeby nie tracić dokładności.

Błędy domenowe zwracają JSON w postaci `{"detail": "..."}`: 404 dla nieistniejących zasobów i 422 dla niepoprawnych danych.

## Przypadki testowe

Pełne przypadki testowe dla testera manualnego (ID, tytuł, warunki początkowe, kroki testowe, oczekiwany rezultat) znajdują się w pliku [docs/test-cases.md](docs/test-cases.md).

| ID | Tytuł |
|---|---|
| TC001 | Dodawanie osoby |
| TC002 | Odrzucenie nazwy osoby składającej się z samych spacji |
| TC003 | Tworzenie grupy z trzema członkami |
| TC004 | Podział 100,00 PLN po równo między trzy osoby |
| TC005 | Podział procentowy 50/30/20 kwoty 100,01 PLN |
| TC006 | Odrzucenie procentów, których suma nie wynosi 100 |
| TC007 | Odrzucenie podziału kwotami, gdy suma nie zgadza się z kwotą wydatku |
| TC008 | Odrzucenie kwoty, która nie jest liczbą |
| TC009 | Akceptacja kwoty zapisanej z przecinkiem |
| TC010 | Obliczanie sald i listy przelewów dla dwóch wydatków |
| TC011 | Usunięcie wydatku i przeliczenie sald |
| TC012 | Anulowanie usunięcia wydatku w oknie potwierdzenia |
| TC013 | Dodanie nowego członka do grupy |
| TC014 | Usunięcie grupy wraz z wydatkami |
| TC015 | Odpowiedź API dla nieistniejącej grupy |

## Technologie

- Python 3.13
- FastAPI (API REST i obsługa widoków)
- Jinja2 (szablony HTML interfejsu użytkownika)
- SQLAlchemy 2 i SQLite (baza danych)
- Pydantic (walidacja danych)
- Uvicorn (serwer aplikacji)
- pytest, pytest-cov, `unittest.mock` i `TestClient` (testy)
- Ruff (linter i porządek importów)
- Git i GitHub (kontrola wersji)