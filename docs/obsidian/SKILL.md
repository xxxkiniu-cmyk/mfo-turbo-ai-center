---
name: mfo-obsidian-delivery
description: Bezpieczna aktualizacja mapy MFO na podstawie rzeczywistych dowodów.
---
# Zasady
Kopia przed zmianą. Bez sekretów, restartów i inferencji. Sprawdź health, jednostki i kod. Nie uznawaj PM2 online za dowód wiadomości. Każda notatka ma stan, źródło i istniejące linki. Rozróżniaj działanie zakresowe, brak dowodu i plany. Testuj graf plikowy i rzeczywiście widoczne okno Obsidiana osobno.

## AUTOMATYCZNE TESTY I WALIDACJA

### Obowiązek weryfikacji
Po każdej istotnej zmianie kodu, konfiguracji, skryptu albo struktury projektu wykonaj automatyczną walidację.

Nie deklaruj ukończenia bez uruchomienia co najmniej jednego realnego sprawdzenia.

### Kolejność walidacji
Wykonuj dostępne sprawdzenia w tej kolejności:

1. **Walidacja statyczna**
   - Sprawdź składnię: `python -m py_compile`, `node --check`, `bash -n`, `shellcheck`, `ruff check`, `eslint`, `tsc --noEmit` — zależnie od stacku.
   - Sprawdź formatowanie, jeśli narzędzie jest skonfigurowane.
   - Sprawdź typy, jeśli projekt używa TypeScript, mypy, pyright albo innego type checkera.

2. **Testy automatyczne**
   - Uruchom istniejące testy: `pytest`, `npm test`, `vitest`, `jest`, `go test ./...`, `cargo test`, `dotnet test` itd.
   - Jeśli testów nie ma, a zadanie dotyczy logiki, stwórz minimalne testy jednostkowe lub integracyjne.
   - Testy muszą pokrywać główny scenariusz użytkownika oraz przynajmniej jeden przypadek brzegowy.
   - Nie pisz testów, które zawsze przechodzą albo tylko sprawdzają istnienie pliku.

3. **Build / kompilacja**
   - Jeśli projekt ma build, uruchom go: `npm run build`, `pnpm build`, `make`, `cargo build`, `dotnet build`, `python -m build` itd.
   - Napraw wszystkie błędy kompilacji przed przejściem dalej.

4. **Test integracyjny / dymny**
   - Uruchom aplikację, skrypt, CLI albo serwer lokalnie.
   - Sprawdź realny scenariusz końcowy: wywołanie komendy, odczyt pliku, zapis danych, odpowiedź endpointu lokalnego, poprawny output.
   - Dla serwera sprawdź status procesu, port, logi oraz co najmniej jedno żądanie / wywołanie.

5. **Walidacja wyniku**
   - Sprawdź, czy powstał oczekiwany plik, baza danych, raport, log albo artefakt.
   - Zweryfikuj zawartość wyniku, nie tylko jego istnienie.
   - Porównaj rezultat z kryteriami ukończenia.

### Zasady testów
- Testuj zachowanie, nie implementację.
- Każdy test musi mieć jasny warunek PASS/FAIL.
- Nie ignoruj testów ani nie usuwaj ich po to, aby build przeszedł.
- Nie oznaczaj testów jako `skip` bez wyraźnego, udokumentowanego powodu.
- Jeśli test wykryje błąd, napraw kod, a nie test — chyba że test był błędny; wtedy wyjaśnij to w raporcie.
- Jeśli dodajesz nową funkcję, dodaj do niej test.
- Jeśli naprawiasz błąd, dodaj regresyjny test, który wcześniej by go wykrył.

### Obsługa niepowodzenia
Gdy walidacja nie przechodzi:
1. Zapisz pełny błąd i kontekst.
2. Ustal, czy problem dotyczy kodu, testu, zależności, środowiska albo danych.
3. Zastosuj najmniejszą poprawkę.
4. Uruchom ponownie pełną odpowiednią walidację.
5. Jeśli błąd trwa, zmień strategię — maksymalnie 3 różne podejścia.
6. Po trzeciej nieudanej próbie zapisz diagnozę, próby i następny krok; nie kończ pracy, jeśli inne części zadania można bezpiecznie kontynuować.

### Minimalny dowód wykonania
W raporcie końcowym podaj:
- dokładne komendy walidacyjne,
- status każdej komendy: PASS / FAIL,
- liczbę testów oraz wynik,
- ścieżki przetestowanych plików,
- dowód działania: output CLI, status procesu, zawartość pliku wynikowego albo wynik testu.

Zakazane jest stwierdzenie „testy powinny przechodzić”.
Agent musi pokazać, że przechodzą.

## DEFINICJA UKOŃCZENIA
- statyczna walidacja, testy, build i test dymny zostały uruchomione, a wszystkie dostępne sprawdzenia przechodzą,
- wynik działania oraz ewentualne braki są udokumentowane.
