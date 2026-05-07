import streamlit as st
import yfinance as yf

st.set_page_config(page_title="Trading Engine", page_icon="⚡")

# --- 1. LISTENER Y ESTADO ---
# Inicializamos la lista dinámica si no existe
if 'orders' not in st.session_state:
    st.session_state.orders = []

st.title("⚡ Trading Exposure Engine")

ticker = st.text_input("Símbolo", "BTC-USD").upper()

try:
    precio_actual = yf.Ticker(ticker).fast_info['last_price']
    st.metric(f"Mercado {ticker}", f"${precio_actual:,.2f}")

    st.divider()

    # --- 2. INPUT DE ÓRDENES ---
    col1, col2 = st.columns(2)
    with col1:
        qty = st.number_input("Cantidad (Volumen)", min_value=0.0, step=0.01)
    with col2:
        px = st.number_input("Precio de Ejecución", min_value=0.0, value=precio_actual, step=0.01)

    # El "Listener": Al hacer clic, "escucha" y guarda la orden
    if st.button("Ejecutar Orden 📥"):
        if qty > 0 and px > 0:
            st.session_state.orders.append({"qty": qty, "price": px})
            st.toast(f"Orden ejecutada: {qty} @ {px}")
        else:
            st.error("Revisa los valores")

    # --- 3. CÁLCULO DE EXPOSICIÓN ---
    if st.session_state.orders:
        st.subheader("📊 Resumen de Exposición")
        
        total_qty = sum(order['qty'] for order in st.session_state.orders)
        # Exposición = Suma de (Precio * Volumen)
        total_exposure = sum(order['price'] * order['qty'] for order in st.session_state.orders)
        avg_price = total_exposure / total_qty

        # Output de resultados
        c1, c2, c3 = st.columns(3)
        c1.metric("Volumen Total", f"{total_qty:,.4f}")
        c2.metric("Exposición Total", f"${total_exposure:,.2f}")
        c3.metric("Precio Promedio", f"${avg_price:,.2f}", 
                  delta=f"{(precio_actual - avg_price):,.2f} vs Market")

        # Tabla dinámica de órdenes
        st.write("### 📜 Historial de Órdenes (Array)")
        st.table(st.session_state.orders)

        if st.button("Limpiar Historial 🗑️"):
            st.session_state.orders = []
            st.rerun()

except Exception as e:
    st.info("Esperando ticker válido...")

    st.warning("Introduce un símbolo válido para empezar.")
