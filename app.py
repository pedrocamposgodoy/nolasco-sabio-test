import streamlit as st
import pandas as pd
import os
import anthropic

# ==========================================
# 1. ESTILOS Y CONFIGURACIÓN
# ==========================================
try:
    from nolasco_styles import inject_styles
except ImportError:
    def inject_styles(): st.write("Cargando estilos base...")

st.set_page_config(page_title="Nolasco Sabio - CLAUDE TEST", layout="wide")
inject_styles()

# ==========================================
# 2. CARGA DE DATOS (Tu CSV)
# ==========================================
def cargar_datos():
    if os.path.exists('datos_simulados.csv'):
        return pd.read_csv('datos_simulados.csv')
    return pd.DataFrame()

df = cargar_datos()

# ==========================================
# 3. INTERFAZ VISUAL
# ==========================================
st.markdown('<div class="nc-brand-header">El Sabio Patrimonial (Motor Anthropic)</div>', unsafe_allow_html=True)
st.dataframe(df, use_container_width=True)

# ==========================================
# 4. EL CHATBOT (Conexión Anthropic)
# ==========================================
st.markdown("---")
st.subheader("💬 Consulta al Sabio sobre tus datos")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Pregunta al Sabio..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        if "ANTHROPIC_API_KEY" not in st.secrets:
            st.error("❌ ERROR: No encuentro ANTHROPIC_API_KEY en 'Secrets'.")
            full_response = "Configura la clave en Streamlit Cloud."
        else:
            try:
                # Conectamos con Anthropic
                client = anthropic.Anthropic(api_key=st.secrets["ANTHROPIC_API_KEY"])
                contexto_datos = df.to_string()
                
                # Le damos las instrucciones al "cerebro"
                system_prompt = f"Eres el Sabio Patrimonial de la empresa Nolasco. Responde basándote ÚNICAMENTE en estos datos reales: {contexto_datos}"
                
                # Llamamos a Claude 3 Haiku (es rapidísimo y barato)
                response = client.messages.create(
                    model="claude-3-5-sonnet-20240620",
                    max_tokens=500,
                    system=system_prompt,
                    messages=[
                        {"role": "user", "content": prompt}
                    ]
                )
                full_response = response.content[0].text
                st.success("✅ Conexión con Anthropic (Claude) exitosa")
            except Exception as e:
                st.error(f"❌ ERROR DE API: {str(e)}")
                full_response = "Error de conexión (posiblemente necesites recargar saldo en tu cuenta de Anthropic)."

        st.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})
