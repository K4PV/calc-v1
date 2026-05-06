import streamlit as st
import yfinance as yf

st.set_page_config(page_title="Calculadora Trading", page_icon="📈")

st.title("📈 Mi Calculadora de Trading")

# Entrada del Ticker
ticker = st.text_input("Escribe el símbolo (ej: AAPL, TSLA, BTC-USD)", "AAPL").upper()

try:
    # Obtener precio real
    data = yf.Ticker(ticker)
    precio_actual = data.fast_info['last_price']
    st.metric(label=f"Precio Actual de {ticker}", value=f"${precio_actual:.2f}")

    st.write("---")
    st.subheader("Calculadora de Promedio")
    
    col1, col2 = st.columns(2)
    with col1:
        c1 = st.number_input("Cantidad Compra 1", min_value=0.0, value=0.0)
        p1 = st.number_input("Precio Compra 1", min_value=0.0, value=0.0)
    with col2:
        c2 = st.number_input("Cantidad Compra 2", min_value=0.0, value=0.0)
        p2 = st.number_input("Precio Compra 2", min_value=0.0, value=0.0)

    total_acciones = c1 + c2
    if total_acciones > 0:
        inversion = (c1 * p1) + (c2 * p2)
        promedio = inversion / total_acciones
        st.success(f"Tu precio promedio es: ${promedio:.2f}")
        
        # Comparación con mercado
        diff = ((precio_actual - promedio) / promedio) * 100
        st.metric("Estado de la inversión", f"{diff:.2f}%", delta=f"{diff:.2f}%")

except:
    st.warning("Introduce un símbolo válido para empezar.")
