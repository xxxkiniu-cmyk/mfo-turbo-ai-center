---
status: "DZIAŁA"
data_testu: "2026-10-31"
tags: [mfo, modul]
---
# systemd

**Stan: DZIAŁA**, zakres: menedżer i aktywne jednostki.

## Weryfikacja
Metoda: PID 1, systemctl is-system-running i show dla panelu, modeli, Telegrama i Antigravity CLI.
Wynik: system running, cztery jednostki active/running i enabled, Restart=on-failure, NRestarts=0. PM2 systemowo active. Nie testowano awarii ani automatycznego odtwarzania przez zatrzymanie procesów.
Czas pomiarów: 14:45 do 14:46 UTC.

## Powiązania
- [[Autostart]]
- [[Panel MFO]]
- [[llama.cpp]]
- [[Antigravity CLI]]
- [[Telegram]]
- [[PM2 WhatsApp]]
