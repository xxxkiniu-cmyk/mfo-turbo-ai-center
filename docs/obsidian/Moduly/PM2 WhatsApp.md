---
status: "DZIAŁA"
data_testu: "2026-10-31"
tags: [mfo, modul]
---
# PM2 WhatsApp

**Stan: DZIAŁA**, zakres: zarządca i proces, nie wiadomości.

## Weryfikacja
Metoda: odczyt istniejącego gniazda PM2, pm2 jlist i systemctl is-active jednostki PM2.
Wynik: usługa active, dwie aplikacje w PM2, antigravity-gold online. Nie uruchamiano nowego demona. Nie testowano dostarczenia wiadomości.
Czas pomiarów: 14:45 do 14:46 UTC.

## Powiązania
- [[WSL Ubuntu]]
- [[WhatsApp Antigravity]]
- [[Autostart]]
- [[Logi]]
