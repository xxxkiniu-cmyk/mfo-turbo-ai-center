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
   - Sprawdź składnię, formatowanie i typy odpowiednimi narzędziami dla projektu, np. `python -m py_compile`, `node --check`, `bash -n`, `shellcheck`, `ruff check`, `eslint`, `tsc --noEmit`.
2. **Testy automatyczne**
   - Uruchom istniejące testy.
   - Jeśli testów nie ma, a zadanie dotyczy logiki, dodaj minimalne testy jednostkowe lub integracyjne obejmujące główny scenariusz i przypadek brzegowy.
   - Nie pisz testów sprawdzających wyłącznie istnienie pliku ani takich, które zawsze przechodzą.
3. **Build / kompilacja**
   - Uruchom build projektu, jeśli jest skonfigurowany, i napraw błędy przed dalszą weryfikacją.
4. **Test integracyjny / dymny**
   - Uruchom aplikację, skrypt, CLI albo serwer i sprawdź rzeczywisty scenariusz końcowy.
   - Dla serwera sprawdź proces, port, logi i co najmniej jedno żądanie.
5. **Walidacja wyniku**
   - Sprawdź zawartość oczekiwanego pliku, bazy, raportu lub artefaktu i porównaj ją z kryteriami ukończenia.

### Zasady testów
- Testuj zachowanie; każdy test ma jasny warunek PASS/FAIL.
- Nie ignoruj ani nie usuwaj testów, aby build przeszedł.
- Nie oznaczaj testów jako `skip` bez udokumentowanego powodu.
- Gdy test wykryje błąd, napraw kod, chyba że test jest błędny; wtedy uzasadnij korektę.
- Nowa funkcja wymaga testu, a naprawa błędu — testu regresyjnego.

### Obsługa niepowodzenia
Gdy walidacja nie przechodzi:
1. Zapisz pełny błąd i kontekst.
2. Ustal, czy przyczyna dotyczy kodu, testu, zależności, środowiska czy danych.
3. Zastosuj najmniejszą poprawkę i ponów odpowiednią walidację.
4. Po maksymalnie trzech różnych nieudanych podejściach zapisz diagnozę i następny krok; kontynuuj bezpieczne, niezależne części zadania.

### Minimalny dowód wykonania
W raporcie końcowym podaj dokładne komendy i status PASS/FAIL, liczbę testów i wynik, sprawdzone ścieżki oraz dowód działania: output, status procesu, zawartość wyniku lub wynik testu.
Nie pisz „testy powinny przechodzić”. Pokaż wynik.

## DEFINICJA UKOŃCZENIA
- Statyczna walidacja, testy, build i test dymny zostały uruchomione, a wszystkie dostępne sprawdzenia przechodzą.
- Wynik działania oraz ewentualne braki są udokumentowane.

