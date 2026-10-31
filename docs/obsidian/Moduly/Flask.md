---
status: "DZIAŁA"
data_testu: "2026-10-31"
tags: [mfo, modul]
---
# Flask

**Stan: DZIAŁA**, wyłącznie zakres: już działająca aplikacja HTTP.

## Weryfikacja
Metoda: GET / i /api/health, stan mfo-panel-local.service oraz import w aktualnym interpreterze.
Wynik: żywy proces obsługuje HTTP 200, lecz test_chat_limits nie zaimportował flask (ModuleNotFoundError). Osobna próba przez /proc/508/exe potwierdziła brak modułu Flask w aktualnym interpreterze. Nie ustalono przyczyny rozbieżności, nie restartowano usługi i niczego nie instalowano. Odtworzenie procesu jest NIEZWERYFIKOWANE i ryzykowne.
Czas pomiarów: 14:45 do 14:46 UTC.

## Powiązania
- [[Panel MFO]]
- [[Panel WWW]]
- [[Historia JSON]]
- [[Router zadan]]
