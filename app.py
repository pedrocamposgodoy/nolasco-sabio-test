import streamlit as st
import pandas as pd
import os
from openai import OpenAI

# ==========================================
# 1. ESTILOS Y CONFIGURACIÓN
# ==========================================
try:
    from nolasco_styles import inject_styles
except ImportError:
    def inject_styles(): st.write("Cargando estilos base...")

st.set_page_config(page_title="Nolasco Sabio - CHAT TEST", layout="wide")
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
st.markdown('<div class="nc-brand-header">El Sabio Patrimonial</div>', unsafe_allow_html=True)
st.dataframe(df, use_container_width=True)

# ==========================================
# 4. EL CHATBOT (Con Autodiagnóstico)
# ==========================================
st.markdown("---")
st.subheader("💬 Consulta al Sabio sobre tus datos")

# Memoria del chat
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Ventana para escribir
if prompt := st.chat_input("Pregunta al Sabio..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # COMPROBACIÓN TÉCNICA DEL "CHORIZO"
        if "OPENAI_API_KEY" not in st.secrets:
            st.error("❌ ERROR: No encuentro la clave en 'Secrets' de Streamlit.")
            full_response = "Por favor, configura la clave en los ajustes de Streamlit Cloud (Settings > Secrets)."
        else:
            try:
                client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
                contexto_datos = df.to_string()
                
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": f"Eres el Sabio Patrimonial. Responde basándote en estos datos reales: {contexto_datos}"},
                        {"role": "user", "content": prompt}
                    ]
                )
                full_response = response.choices[0].message.content
                st.success("✅ Conexión con ChatGPT exitosa")
            except Exception as e:
                st.error(f"❌ ERROR DE API: {str(e)}")
                full_response = "Tengo la clave, pero OpenAI me da error (posiblemente falta de saldo en tu cuenta o la clave es incorrecta)."

        st.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})
