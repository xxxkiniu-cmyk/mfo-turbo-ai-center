---
status: "DZIAŁA"
data_testu: "2026-10-31"
tags: [mfo, modul]
---
# Modele AI

**Stan: DZIAŁA**, zakres: dostępność serwera modeli.

## Weryfikacja
Metoda: GET /health, /v1/models i /slots na porcie 8080.
Wynik: trzy odpowiedzi HTTP 200, status ok, jeden model Qwen i jeden slot. Nie wykonano inferencji. Llama nie została załadowana do testu.
Czas pomiarów: 14:45 do 14:46 UTC.

## Powiązania
- [[llama.cpp]]
- [[Qwen]]
- [[Llama]]
- [[Panel MFO]]
- [[JCODE]]
