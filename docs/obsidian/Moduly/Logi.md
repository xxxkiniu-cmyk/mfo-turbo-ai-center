---
status: "DZIAŁA"
data_testu: "2026-10-31"
tags: [mfo, modul]
---
# Logi

**Stan: DZIAŁA**, zakres: dostęp do mechanizmów dziennika.

## Weryfikacja
Metoda: journalctl --user dla panelu, llama, Telegrama i Antigravity CLI, poziom err, ostatnie 30 minut, limit 50 wpisów na jednostkę; os.access katalogu PM2 logs.
Wynik: polecenia dziennika zakończone poprawnie, zero zwróconych błędów w tym zakresie, katalog PM2 czytelny. Nie kopiowano treści logów do publikacji, nie sprawdzano pełnej retencji ani wszystkich logów Windows.
Czas pomiarów: 14:45 do 14:46 UTC.

## Powiązania
- [[Monitoring]]
- [[PM2 WhatsApp]]
- [[systemd]]
