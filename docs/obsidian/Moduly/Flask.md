---
status: "DZIAŁA"
data_testu: "2026-10-31"
tags: [mfo, modul]
---
# Flask

**Stan: DZIAŁA**, wyłącznie zakres: już działająca aplikacja HTTP.

## Weryfikacja
Metoda: odczyt ExecStart i argv0 usługi, uruchomienie testów w istniejącym ~/.local/share/mfo-recovery/venv/bin/python. Rzeczywiste GET / oraz POST /api/chat z poprawnym CSRF i pustym komunikatem.
Wynik: 11 testów chat_limits PASS i 5 testów chat_memory PASS. GET 200, POST 400 zgodnie z walidacją. Wcześniejszy brak Flask wynikał z użycia /proc/PID/exe, które wskazuje bazowy interpreter poza venv. Nie był dowodem brakującej zależności aktywnej usługi. Niczego nie instalowano, nie zmieniano kodu ani nie restartowano. Restart oraz pełna inferencja nadal nieprzetestowane.
Czas testów: 2026-10-31, do 15:00 UTC. Szczegóły: [[Raport_naprawy_20261101]].

## Powiązania
- [[Panel MFO]]
- [[Panel WWW]]
- [[Historia JSON]]
- [[Router zadan]]
