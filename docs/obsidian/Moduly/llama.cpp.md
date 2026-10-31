---
status: "DZIAŁA"
data_testu: "2026-10-31"
tags: [mfo, modul]
---
# llama.cpp

**Stan: DZIAŁA**, zakres: uruchomiony serwer i interfejs odczytu.

## Weryfikacja
Metoda: systemctl show mfo-llama-backend.service, ss, GET /health, /v1/models i /slots na porcie 8080.
Wynik: active/running, enabled, zero restartów, PID zgodny z nasłuchem. HTTP 200, jeden slot i gotowy model Qwen. Bez testu generowania.
Czas pomiarów: 14:45 do 14:46 UTC.

## Powiązania
- [[Qwen]]
- [[Llama]]
- [[Modele AI]]
- [[systemd]]
