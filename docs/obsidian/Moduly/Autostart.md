---
status: "NIEZWERYFIKOWANY"
data_testu: "2026-10-31"
tags: [mfo, modul]
---
# Autostart

**Stan: NIEZWERYFIKOWANY**, zakres: niezawodny zimny start.

## Weryfikacja
Metoda: odczyt Get-ScheduledTask/Get-ScheduledTaskInfo i systemctl show.
Wynik: zadanie WSL-Ubuntu-Autostart Running, LastTaskResult=267009, jednostki enabled i Restart=on-failure. To nie dowodzi udanego startu po restarcie. Etap 5 skorygował diagnozę Flask: usługa korzysta z istniejącego venv, które zawiera zależności. Sam restart pozostaje nieprzetestowany. Nie zmieniano konfiguracji ani autostartu.
Czas pomiarów: 14:45 do 14:46 UTC.

## Powiązania
- [[Windows 11]]
- [[WSL Ubuntu]]
- [[systemd]]
- [[PM2 WhatsApp]]
- [[Dysk E]]
