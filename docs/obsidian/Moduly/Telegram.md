---
status: "DZIAŁA"
data_testu: "2026-10-31"
tags: [mfo, modul]
---
# Telegram

**Stan: DZIAŁA**, wyłącznie zakres: aktywna usługa i logika offline.

## Weryfikacja
Metoda: systemctl show mfo-telegram.service, journalctl i istniejący test_telegram_bot.py z atrapami sieci.
Wynik: active/running, enabled, zero restartów i zwróconych błędów dziennika w oknie 30 minut. Testy offline 44/44 PASS po jednej korekcie umask diagnostyki. Pierwsze 43/44 wynikało z umask 077 zmieniającej oczekiwane 755 na 700 w syntetycznym katalogu. Nie testowano dostarczenia wiadomości i nie używano prawdziwych tokenów w testach.
Czas pomiarów: 14:45 do 14:46 UTC.

## Powiązania
- [[Modele AI]]
- [[Ochrona API]]
- [[systemd]]
