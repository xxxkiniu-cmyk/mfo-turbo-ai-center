---
status: "DZIAŁA"
data_testu: "2026-10-31"
tags: [mfo, modul]
---
# Qwen

**Stan: DZIAŁA**, zakres: model dostępny w uruchomionym serwerze.

## Weryfikacja
Metoda: GET /v1/models i /health na porcie 8080 oraz /api/health panelu.
Wynik: katalog zwraca jeden model z identyfikatorem Qwen, gotowość serwera potwierdzona. Nie wykonano inferencji, więc jakość i poprawność odpowiedzi pozostają niezweryfikowane.
Czas pomiarów: 14:45 do 14:46 UTC.

## Powiązania
- [[llama.cpp]]
- [[Modele AI]]
