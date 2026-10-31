# Architektura MFO

[[START]] · [[MFO TURBO AI CENTER]]

Diagramy pokazują zależności potwierdzone konfiguracją lub kodem, nie wynik pełnych testów funkcjonalnych. Szczegółowe statusy i dowody są w notatkach modułów. Pełne relacje opisowe można eksplorować w widoku grafu, filtr `path:Moduly`.

## Rdzeń i dane

```mermaid
flowchart TD
    W[Windows 11] --> U[WSL Ubuntu i systemd]
    U --> F[Flask: port 8082]
    U --> L[llama.cpp: port 8080]
    WWW[Panel WWW] --> F
    F --> L
    L --> Q[Załadowany Qwen 3B]
    F --> H[Historia JSON i RAG]
    E[Dysk E: pamięć AI] --- H
    F --> T[Router zadań]
    T --> J[JCODE]
```

[[Llama]] to plik modelu obecny na dysku, nie dowód aktywnego załadowania. RAG i router mają potwierdzony kod, ale nie wykonano ich pełnego testu funkcjonalnego.

## Procesy towarzyszące

```mermaid
flowchart TD
    A[Zadanie Windows po logowaniu] --> S[WSL i systemd]
    S --> P[PM2 resurrect]
    P --> WA[WhatsApp Antigravity: proces online]
    S --> TG[Telegram: usługa aktywna]
    TG --> L[API modelu 8080]
    S --> CLI[Antigravity CLI]
    MIC[Mikrofon START STOP: niezweryfikowany] --- WF[Wispr Flow]
```

Nie potwierdzono przesyłania wiadomości, działania START/STOP ani pełnego startu po restarcie.

## Integracje bez potwierdzenia

[[GitHub]]: brak autoryzacji i potwierdzonego repozytorium docelowego. [[Linear]]: brak dowodu konfiguracji. Te notatki nie oznaczają działających integracji.

## Eksploatacja

[[Monitoring]] · [[Logi]] · [[Kopie bezpieczenstwa]] · [[Ochrona API]] · [[Autostart]]
