import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Funzione simulata per recuperare dati di mercato
def get_market_data(city, area, beds):
    """
    Simula il recupero di dati di mercato basati su città, zona e numero di posti letto.
    In una versione reale, qui effettueresti una chiamata API per ottenere dati aggiornati.
    """
    # Valori predefiniti basati sulla città (esempi)
    if city.lower() in ['roma', 'rome']:
        occupancy = 75  # tasso di occupazione in percentuale
        adr = 120       # prezzo medio per notte in €
    elif city.lower() in ['milano', 'milan']:
        occupancy = 70
        adr = 110
    elif city.lower() in ['firenze', 'florence']:
        occupancy = 80
        adr = 100
    else:
        occupancy = 65
        adr = 90

    # Leggera modifica in base al numero di posti letto
    occupancy += (beds - 1) * 1   # ad esempio, ogni letto extra aumenta leggermente l’attrattiva
    adr += (beds - 1) * 5         # ogni letto extra può aumentare l’ADR di qualche euro

    return {'occupancy': occupancy, 'adr': adr}

st.title("Simulatore Avanzato: Domanda e Prezzi Ottimali per Affitti Brevi")

# --- Sezione: Dati di Mercato ---
st.header("Informazioni sulla Proprietà")
city = st.text_input("Città", value="Roma")
area = st.text_input("Zona/Quartiere", value="Centro")
beds = st.number_input("Numero di posti letto", min_value=1, value=2)

# Recupera i dati di mercato simulati
market_data = get_market_data(city, area, beds)
st.write("### Dati di Mercato Simulati")
st.write(f"Tasso di occupazione medio: **{market_data['occupancy']}%**")
st.write(f"Prezzo medio per notte (ADR): **€ {market_data['adr']}**")

# --- Sezione: Parametri Base per la Simulazione ---
st.header("Parametri per la Simulazione")
# Usa i dati di mercato come default, con possibilità di modifica
prezzo_base = st.number_input("Prezzo per notte da considerare (€)", min_value=0.0, value=float(market_data['adr']), step=5.0)
notti_disponibili = st.number_input("Notti disponibili nel mese", min_value=1, value=30)
occupazione_attuale = st.slider("Tasso di occupazione (%)", min_value=0, max_value=100, value=int(market_data['occupancy']))
costi_fissi = st.number_input("Costi fissi mensili (€)", min_value=0.0, value=500.0, step=50.0)
costo_variabile = st.number_input("Costo variabile per notte (€)", min_value=0.0, value=10.0, step=1.0)

# Calcolo dei risultati attuali
notti_prenotate_attuali = int((occupazione_attuale / 100) * notti_disponibili)
fatturato_attuale = prezzo_base * notti_prenotate_attuali
costi_totali_attuali = costi_fissi + (costo_variabile * notti_prenotate_attuali)
profitto_attuale = fatturato_attuale - costi_totali_attuali

st.subheader("Risultati Attuali")
st.write(f"Notti prenotate: **{notti_prenotate_attuali}** su {notti_disponibili}")
st.write(f"Fatturato: **€ {fatturato_attuale:.2f}**")
st.write(f"Costi Totali: **€ {costi_totali_attuali:.2f}**")
st.write(f"Profitto: **€ {profitto_attuale:.2f}**")

# --- Sezione: Simulazione della Variazione del Prezzo ---
st.header("Simulazione: Variazione del Prezzo e Ottimizzazione")
elasticity = st.slider("Elasticità della domanda", min_value=0.0, max_value=1.0, value=0.2, step=0.05)

# Gamma di prezzi intorno al prezzo base
price_range = np.arange(prezzo_base * 0.8, prezzo_base * 1.2, 1.0)
profits = []
occupancies = []

for p in price_range:
    # Calcola la variazione percentuale rispetto al prezzo base
    delta_price = (p - prezzo_base) / prezzo_base
    # Simula l'impatto sul tasso di occupazione (lineare in base all'elasticità)
    occupazione_sim = max(0, occupazione_attuale - (elasticity * delta_price * 100))
    nights_sim = int((occupazione_sim / 100) * notti_disponibili)
    
    # Calcolo del fatturato e del profitto per il nuovo scenario
    revenue_sim = p * nights_sim
    cost_variable_sim = costo_variabile * nights_sim
    profit_sim = revenue_sim - (costi_fissi + cost_variable_sim)
    
    profits.append(profit_sim)
    occupancies.append(nights_sim)

# Identifica il prezzo che massimizza il profitto
max_profit = max(profits)
optimal_price = price_range[profits.index(max_profit)]
optimal_occupancy = occupancies[profits.index(max_profit)]

st.subheader("Prezzo Ottimale Stimato")
st.write(f"Prezzo ottimale per notte: **€ {optimal_price:.2f}**")
st.write(f"Occupazione stimata: **{optimal_occupancy}** notti prenotate")
st.write(f"Profitto massimo stimato: **€ {max_profit:.2f}**")

# Visualizzazione grafica
fig, ax1 = plt.subplots(figsize=(8, 4))
ax1.plot(price_range, profits, 'b-', label="Profitto (€)")
ax1.set_xlabel("Prezzo per notte (€)")
ax1.set_ylabel("Profitto (€)", color='b')
ax1.tick_params(axis='y', labelcolor='b')

ax2 = ax1.twinx()
ax2.plot(price_range, occupancies, 'r--', label="Notti Prenotate")
ax2.set_ylabel("Notti Prenotate", color='r')
ax2.tick_params(axis='y', labelcolor='r')

st.pyplot(fig)
st.write("Questa simulazione mostra come le variazioni del prezzo influenzano il profitto e il numero di notti prenotate. I dati di mercato simulati vengono usati come riferimento iniziale, ma puoi modificarli per testare scenari differenti.")
