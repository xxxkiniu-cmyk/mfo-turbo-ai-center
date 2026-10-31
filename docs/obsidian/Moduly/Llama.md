---
status: "NIEZWERYFIKOWANY"
data_testu: "2026-10-31"
tags: [mfo, modul]
---
# Llama

**Stan: NIEZWERYFIKOWANY**.

## Weryfikacja
Metoda: is_file dla Llama-3.2-3B-Q4_K_M.gguf i GET /v1/models uruchomionego serwera.
Wynik: plik istnieje, ale aktywny model to Qwen. Nie ładowano innego modelu, nie sprawdzano sumy dużego pliku ani inferencji. Obecność pliku nie potwierdza działania Llama.
Czas pomiarów: 14:45 do 14:46 UTC.

## Powiązania
- [[llama.cpp]]
- [[Modele AI]]
