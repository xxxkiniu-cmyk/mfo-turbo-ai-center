---
status: "DZIAŁA"
data_testu: "2026-10-31"
tags: [mfo, modul]
---
# Panel MFO

**Stan: DZIAŁA**, zakres: API i HTTP.

## Weryfikacja
Metoda: GET 127.0.0.1:8082/api/health, GET /, systemctl i ss.
Wynik: HTTP 200, llama_ready=true, HTML i cookie CSRF obecne. MainPID usługi zgodny z PID nasłuchu. Brak testu inferencji i zapisu historii. Aktualny interpreter nie importuje Flask, więc restart jest ryzykowny.
Czas pomiarów: 14:45 do 14:46 UTC.

## Powiązania
- [[MFO TURBO AI CENTER]]
- [[Flask]]
- [[Panel WWW]]
- [[Modele AI]]
- [[Historia JSON]]
- [[Router zadan]]
- [[systemd]]
