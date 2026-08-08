import time
from core.event_bus import EventBus, Event

# Inicjalizujemy szynę zdarzeń
bus = EventBus()

# Definiujemy funkcję dla agenta Thermomix
def agent_thermomix(event):
    print(f"🍳 [Agent Thermomix]: Odebrałem komunikat od [{event.source}]!")
    print(f"   ➡️ Treść zadania: {event.payload}")

# Definiujemy funkcję dla loggera
def agent_logger(event):
    print(f"📊 [Agent Logger]: Zapisuję w dzienniku zdarzenie z parametrami: {event.payload}")

# Rejestrujemy subskrypcje poprawnie (przekazując funkcję jako argument)
bus.subscribe("ROZKAZ_KUCHENNY", agent_thermomix)
bus.subscribe("ROZKAZ_KUCHENNY", agent_logger)

print("--- START ROZMOWY MIĘDZY AGENTAMI ---")

# Agent Router nadaje komunikat
bus.publish(Event(
    type="ROZKAZ_KUCHENNY",
    payload={"przepis": "Zupa krem z pomidorów", "czas": "15 min", "temp": "100°C"},
    source="RouterAgent"
))

time.sleep(0.5)
print("--- KONIEC TESTU ---")
