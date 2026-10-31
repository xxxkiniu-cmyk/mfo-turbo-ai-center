---
status: "DZIAŁA"
data_testu: "2026-10-31"
tags: [mfo, modul]
---
# Antigravity CLI

**Stan: DZIAŁA**, wyłącznie zakres: aktywna usługa.

## Weryfikacja
Metoda: systemctl show antigravity-cli-daemon.service oraz journalctl.
Wynik: active/running, enabled, Restart=on-failure, zero restartów i zwróconych błędów w ostatnich 30 minutach. Nie testowano poleceń zdalnego sterowania. Nie utożsamiać tej usługi z botem WhatsApp.
Czas pomiarów: 14:45 do 14:46 UTC.

## Powiązania
- [[WSL Ubuntu]]
- [[systemd]]
